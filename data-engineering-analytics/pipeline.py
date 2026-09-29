"""Demo ETL: synthetic application database -> local lake -> semantic marts.

This standalone data-engineering prototype uses only Python's standard library.
It does not read the running OptiSpend app database or any real user data.
"""

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
from collections import defaultdict


BASE = Path(__file__).resolve().parent
RUNTIME = BASE / "runtime"
SOURCE_DB = RUNTIME / "source" / "application.db"
LAKE = RUNTIME / "lake"
CHECKPOINT = RUNTIME / "checkpoint.json"

DEMO_ROWS = [
    ("Shopping", 2499, "within_plan", "2026-09-20T10:15:00+05:30"),
    ("Travel", 18500, "review_buffer", "2026-09-20T11:20:00+05:30"),
    ("Food & dining", 1250, "within_plan", "2026-09-21T12:30:00+05:30"),
    ("Electronics", 54999, "review_commitments", "2026-09-21T14:05:00+05:30"),
    ("Shopping", 7200, "within_plan", "2026-09-22T09:45:00+05:30"),
    ("Travel", 42000, "review_buffer", "2026-09-22T17:10:00+05:30"),
    ("Other", 899, "within_plan", "2026-09-23T18:25:00+05:30"),
    ("Electronics", 15999, "within_plan", "2026-09-24T13:40:00+05:30"),
    ("Food & dining", 3100, "within_plan", "2026-09-25T20:05:00+05:30"),
    ("Shopping", 68000, "review_commitments", "2026-09-26T16:15:00+05:30"),
    ("Travel", 9800, "within_plan", "2026-09-27T11:55:00+05:30"),
    ("Other", 23500, "review_buffer", "2026-09-28T08:35:00+05:30"),
]


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_json_atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def ensure_demo_application_db():
    SOURCE_DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(SOURCE_DB) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS purchase_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            planned_amount_inr INTEGER NOT NULL,
            guidance_outcome TEXT NOT NULL,
            occurred_at TEXT NOT NULL
        )""")
        count = db.execute("SELECT COUNT(*) FROM purchase_checks").fetchone()[0]
        if count == 0:
            db.executemany(
                "INSERT INTO purchase_checks (category, planned_amount_inr, guidance_outcome, occurred_at) VALUES (?, ?, ?, ?)",
                DEMO_ROWS,
            )
    return SOURCE_DB


def read_checkpoint():
    if not CHECKPOINT.exists():
        return 0
    try:
        return max(0, int(json.loads(CHECKPOINT.read_text(encoding="utf-8")).get("last_id", 0)))
    except (ValueError, TypeError, json.JSONDecodeError):
        return 0


def extract(last_id):
    # Open the synthetic application DB read-only, as a separate ETL consumer.
    connection = sqlite3.connect(f"file:{SOURCE_DB}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute(
            "SELECT id, category, planned_amount_inr, guidance_outcome, occurred_at "
            "FROM purchase_checks WHERE id > ? ORDER BY id", (last_id,)
        )]
    finally:
        connection.close()


def amount_band(amount):
    if amount <= 5_000:
        return "0-5000"
    if amount <= 16_000:
        return "5001-16000"
    if amount <= 50_000:
        return "16001-50000"
    return "50001-plus"


def transform(rows, ingested_at):
    bronze, silver = [], []
    for row in rows:
        amount = max(0, int(row["planned_amount_inr"]))
        occurred = datetime.fromisoformat(row["occurred_at"])
        category = str(row["category"])[:40]
        outcome = str(row["guidance_outcome"])
        if outcome not in {"within_plan", "review_buffer", "review_commitments"}:
            outcome = "review_buffer"
        bronze.append({**row, "ingested_at": ingested_at})
        # Silver keeps a stable event key for deduplication but drops the exact
        # amount before analytics and dashboard use.
        silver.append({
            "check_id": int(row["id"]),
            "event_date": occurred.date().isoformat(),
            "category": category,
            "amount_band": amount_band(amount),
            "guidance_outcome": outcome,
        })
    return bronze, silver


def append_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_gold_marts():
    silver_root = LAKE / "silver" / "purchase_checks"
    daily, by_category, by_outcome = defaultdict(list), defaultdict(list), defaultdict(list)
    seen_ids = set()
    for path in sorted(silver_root.glob("event_date=*/part-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row["check_id"] in seen_ids:
                continue
            seen_ids.add(row["check_id"])
            band = row["amount_band"]
            # Use range midpoints for a clearly labeled estimate in summary
            # marts; source exact amounts are intentionally absent from Silver.
            amount_proxy = {
                "0-5000": 2500,
                "5001-16000": 10500,
                "16001-50000": 33000,
                "50001-plus": 65000,
            }.get(band, 0)
            for target, key in ((daily, (row["event_date"],)),
                                (by_category, (row["category"],)),
                                (by_outcome, (row["guidance_outcome"],))):
                target[key].append((row, amount_proxy))

    write_mart(
        LAKE / "gold" / "purchase_checks_daily.csv",
        ["event_date", "check_count", "within_plan_count", "review_count", "estimated_amount_midpoint_inr"],
        [(
            key[0], len(values),
            sum(row["guidance_outcome"] == "within_plan" for row, _ in values),
            sum(row["guidance_outcome"] != "within_plan" for row, _ in values),
            sum(proxy for _, proxy in values),
        ) for key, values in sorted(daily.items())],
    )
    write_mart(
        LAKE / "gold" / "purchase_checks_by_category.csv",
        ["category", "check_count", "within_plan_count", "review_count", "estimated_amount_midpoint_inr"],
        [(
            key[0], len(values),
            sum(row["guidance_outcome"] == "within_plan" for row, _ in values),
            sum(row["guidance_outcome"] != "within_plan" for row, _ in values),
            sum(proxy for _, proxy in values),
        ) for key, values in sorted(by_category.items())],
    )
    write_mart(
        LAKE / "gold" / "purchase_checks_by_outcome.csv",
        ["guidance_outcome", "check_count", "estimated_amount_midpoint_inr"],
        [(key[0], len(values), sum(proxy for _, proxy in values))
         for key, values in sorted(by_outcome.items())],
    )
    return len(seen_ids)


def write_mart(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
    os.replace(temp, path)


def run_pipeline():
    ensure_demo_application_db()
    last_id = read_checkpoint()
    rows = extract(last_id)
    ingested_at = now_utc()
    bronze, silver = transform(rows, ingested_at)

    if rows:
        run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{rows[0]['id']}-{rows[-1]['id']}"
        append_jsonl(LAKE / "bronze" / "purchase_checks" / f"batch-{run_id}.jsonl", bronze)
        by_date = defaultdict(list)
        for row in silver:
            by_date[row["event_date"]].append(row)
        for event_date, records in by_date.items():
            append_jsonl(
                LAKE / "silver" / "purchase_checks" / f"event_date={event_date}" / f"part-{run_id}.jsonl",
                records,
            )
        write_json_atomic(CHECKPOINT, {"last_id": rows[-1]["id"], "updated_at": ingested_at})

    total = load_gold_marts()
    print(f"Source: synthetic application DB ({SOURCE_DB.relative_to(BASE)})")
    print(f"Extracted this run: {len(rows)} rows | Loaded to local lake: {total} sample checks")
    print(f"Dashboard-ready marts: {(LAKE / 'gold').relative_to(BASE)}")
    print("No real application, financial-account, S3, or dashboard connection was used.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    run_pipeline()
