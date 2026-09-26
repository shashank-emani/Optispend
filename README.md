# OptiSpend prototype

A responsive, browser-openable personal finance dashboard prototype. All balances, providers, scores, offers and integrations are mocked; no real accounts are contacted.

## Run locally

1. Open this folder in a terminal.
2. Start a local web server:

   ```sh
   python3 -m http.server 8000
   ```

3. Open [http://localhost:8000](http://localhost:8000) in your browser.

The project has no build step or package installation. You can also open `index.html` directly, though a local server gives the most reliable browser behavior.

## Files

- `index.html` — app shell and semantic page structure
- `styles.css` — responsive visual system
- `app.js` — view switching, sample data, and prototype interactions

## Future integrations

The connection catalog in `app.js` is presentation-only. Replace its mocked provider list and sample records with consented provider adapters (for example, an Account Aggregator flow for supported Indian financial data), and keep consent scope, freshness, source, and revocation state alongside every imported record. Never collect a bank or brokerage password in this interface.

Life-stage styling changes with the onboarding choice: vibrant for college, blended for early career, and restrained/premium for established users. Purchase-link checks, issuer offers and sample scores remain demo-only; they do not browse product pages or connect to accounts. HDFC Millennia detail view links to the issuer's current published terms.

The **Talk to your money** view demonstrates an agent-style conversation using local sample-data intent handling. It can answer common prototype questions, route the user to a relevant view, and ask for confirmation before adding a local demo reminder. It is not connected to an LLM service or financial APIs. For a production agent, replace `agentReply()` with a backend service that reads only consented financial snapshots, labels data freshness, and stages consequential actions for explicit review instead of executing them directly.

**Asset Pulse** is available from the sidebar. First-run onboarding offers an optional asset entry with a skip path; the page supports cars, phones, gadgets, watches and property, optional current quotes, and optional linked-loan balances. Entered personal-asset values and debts flow into the sample net-worth calculation. Provider-style valuations and depreciation curves are illustrative only; Cars24, Spinny, CarWale, Cashify, property data and owned-holding news are not live-connected.
