# OptiSpend

OptiSpend is a responsive prototype for a calmer, more personal way to understand and manage money. It brings a sample net-worth picture, spending decisions, savings plans, rewards and financial goals into one approachable experience. Its central idea is simple: help people make their next money decision with more context and less clutter.

The interface adapts to a person’s life stage, keeps the home view focused, and reveals detail when someone chooses to explore. A purchase check can consider a planned amount, upcoming commitments, payment-card offers and an optional product or booking link. A conversational view provides another way to ask about the sample financial picture.

> **Prototype notice:** Accounts, balances, valuations, scores, and offers are illustrative. The local application backend evaluates purchase checks against sample figures. It does not connect to financial institutions, fetch live prices, browse submitted purchase links, provide a live AI assistant, move money, or approve or block transactions.

## Explore the product

The [OptiSpend product guide](docs/PRODUCT_GUIDE.md) describes the product intent, experience areas, personalization, current prototype behavior, and the boundaries for future integrations.

The repository has two separate engineering tracks: the user-facing application and a data engineering and analytics prototype. The latter uses a synthetic application database and local files to demonstrate ETL; it does not connect to the app service or external infrastructure.

## Run locally

The prototype uses Python’s standard library; no package installation is needed. From this folder, start the app and its local backend:

```sh
python3 backend/server.py
```

Then open [http://localhost:8000](http://localhost:8000). Keep the terminal running while you use the site; stopping it also stops the local purchase-check API.

## What’s in the prototype

- Personalized overview with sample net worth, assets and liabilities, alerts, and a money-habits signal
- Spend Gatekeeper with purchase planning, card-offer examples, and an illustrative product or travel link comparison
- Talk to your money chat, investment and savings views, rewards, protection, credit score, loans, goals, and upcoming events
- Asset Pulse for sample resale values, depreciation context, linked liabilities, and updates tied to sample holdings
- Mock connected-account and broker flows, plus profile and settings
- Local purchase-check API that returns sample guidance while keeping the final decision with the user
- Separate ETL and analytics prototype; see [Data Engineering & Analytics](data-engineering-analytics/README.md)

See the product guide for what is interactive today versus what remains a future integration.

## Project files

- `index.html` — app shell and page structure
- `styles.css` — responsive styles and life-stage themes
- `app.js` — sample data, view switching, and prototype interactions
- `backend/server.py` — local sample purchase-check API
- `backend-ui.js` — connects the Spend Gatekeeper to the local API when it is running
- `data-engineering-analytics/` — standalone synthetic-source ETL, local lake layers, and semantic metrics

## Run the separate ETL prototype

From this folder, run:

```sh
python3 data-engineering-analytics/pipeline.py
```

The pipeline generates its own synthetic SQLite source and writes local Bronze, Silver, and Gold outputs under `data-engineering-analytics/runtime/`. It does not read real user data or connect to S3, Kafka, a warehouse, Superset, or Tableau.
