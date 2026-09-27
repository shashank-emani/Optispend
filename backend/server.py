"""OptiSpend's local, privacy-minimal purchase analytics service.

This small standard-library service is a runnable project slice, not a bank
integration. It serves the prototype, evaluates purchase plans against sample
figures, and processes anonymous aggregate events in a local in-memory queue.
"""

from collections import Counter
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from queue import Queue
import re
import threading
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PORT = 8000
MAX_BODY_BYTES = 4096

# Illustrative values only. A production service would use fresh, consented data.
SAMPLE_AVAILABLE_AFTER_BILLS_AND_SAVINGS = 84_620
SAMPLE_EVENT_RESERVE = 12_000
SAMPLE_COMFORT_BUFFER = 16_000
SAMPLE_MILLENNIA_CASHBACK_CAP_LEFT = 620

EVENTS = Queue()
ANALYTICS_LOCK = threading.Lock()
ANALYTICS = {
    "checks": 0,
    "categories": Counter(),
    "outcomes": Counter(),
    "amountBands": Counter(),
}


def amount_band(amount):
    if amount <= 5_000:
        return "0-5000"
    if amount <= 16_000:
        return "5001-16000"
    if amount <= 50_000:
        return "16001-50000"
    return "50001-plus"


def process_events():
    """Consume minimal events, keeping no item name, URL, or exact amount."""
    while True:
        event = EVENTS.get()
        try:
            with ANALYTICS_LOCK:
                ANALYTICS["checks"] += 1
                ANALYTICS["categories"][event["category"]] += 1
                ANALYTICS["outcomes"][event["outcome"]] += 1
                ANALYTICS["amountBands"][event["amountBand"]] += 1
        finally:
            EVENTS.task_done()


threading.Thread(target=process_events, name="opti-analytics-worker", daemon=True).start()


def evaluate(payload):
    name = str(payload.get("name", "Purchase"))[:100].strip() or "Purchase"
    category = str(payload.get("category", "Other"))[:40].strip()
    if category not in {"Shopping", "Food & dining", "Travel", "Electronics", "Other"}:
        category = "Other"

    try:
        amount = round(float(payload.get("amount", 0)))
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Enter a valid purchase amount.") from None
    if amount <= 0 or amount > 10_000_000:
        raise ValueError("Enter an amount between ₹1 and ₹1 crore.")

    available = SAMPLE_AVAILABLE_AFTER_BILLS_AND_SAVINGS
    reserved = SAMPLE_EVENT_RESERVE
    after_purchase = available - amount
    after_reserve = available - reserved - amount
    if after_reserve >= SAMPLE_COMFORT_BUFFER:
        outcome = "within_plan"
        headline = "Looks comfortable within this sample plan"
        guidance = "The sample bills, savings target, and event reserve remain covered with room in the comfort buffer."
    elif after_reserve >= 0:
        outcome = "review_buffer"
        headline = "Worth checking the remaining buffer"
        guidance = "The sample event reserve remains covered, though the remaining comfort buffer would be smaller."
    else:
        outcome = "review_commitments"
        headline = "Review timing and commitments"
        guidance = "This amount would use part of the sample event reserve. You are still in control; consider the timing and other options."

    normalized = name.lower()
    excluded = any(word in normalized for word in ("fuel", "rent", "tax", "emi", "wallet"))
    partners = (
        "amazon", "flipkart", "myntra", "swiggy", "zomato", "uber",
        "bookmyshow", "tata cliq", "cult.fit", "sony liv",
    )
    is_partner = any(partner in normalized for partner in partners)
    cashback_rate = 0.05 if is_partner else 0.01
    cashback_cap = SAMPLE_MILLENNIA_CASHBACK_CAP_LEFT if is_partner else 1_000
    estimated_cashback = 0 if excluded else min(int(amount * cashback_rate), cashback_cap)
    offer_label = "Not included in this sample offer" if excluded else (
        "HDFC Millennia · sample 5% partner rate" if is_partner
        else "HDFC Millennia · sample 1% eligible-spend rate"
    )

    # Deliberately omit the item name and exact amount from this event.
    EVENTS.put({
        "category": category,
        "outcome": outcome,
        "amountBand": amount_band(amount),
    })
    EVENTS.join()

    with ANALYTICS_LOCK:
        summary = analytics_snapshot()

    return {
        "name": name,
        "amount": amount,
        "category": category,
        "outcome": outcome,
        "headline": headline,
        "guidance": guidance,
        "availableAfter": after_purchase,
        "remainingAfterReserve": after_reserve,
        "offer": {
            "label": offer_label,
            "estimatedCashback": estimated_cashback,
            "note": "Illustrative card terms and cap; confirm current issuer conditions before paying.",
        },
        "analytics": summary,
        "sampleData": True,
    }


def analytics_snapshot():
    return {
        "checks": ANALYTICS["checks"],
        "categories": dict(ANALYTICS["categories"]),
        "outcomes": dict(ANALYTICS["outcomes"]),
        "amountBands": dict(ANALYTICS["amountBands"]),
        "storage": "memory-only; resets when the local service stops",
        "retainedFields": ["category", "amount band", "guidance outcome"],
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        # Avoid writing request paths or user-submitted data to a log file.
        return

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self.send_json(200, {
                "ok": True,
                "service": "OptiSpend local sample analytics",
                "mode": "local sample data; no financial accounts connected",
            })
        if path == "/api/analytics/summary":
            with ANALYTICS_LOCK:
                snapshot = analytics_snapshot()
            return self.send_json(200, snapshot)
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/purchase-check":
            return self.send_json(404, {"error": "Endpoint not found."})

        raw_length = self.headers.get("Content-Length", "0")
        if not re.fullmatch(r"\d{1,6}", raw_length):
            return self.send_json(400, {"error": "Invalid request size."})
        length = int(raw_length)
        if length <= 0 or length > MAX_BODY_BYTES:
            return self.send_json(413, {"error": "Request is too large."})
        try:
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Send a purchase object.")
            result = evaluate(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self.send_json(400, {"error": "Send valid JSON."})
        except ValueError as error:
            return self.send_json(400, {"error": str(error)})
        return self.send_json(200, result)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"OptiSpend local backend running at http://127.0.0.1:{PORT}")
    print("Sample data only. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
