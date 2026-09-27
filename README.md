# OptiSpend

OptiSpend is a responsive prototype for a calmer, more personal way to understand and manage money. It brings a sample net-worth picture, spending decisions, savings plans, rewards and financial goals into one approachable experience. Its central idea is simple: help people make their next money decision with more context and less clutter.

The interface adapts to a person’s life stage, keeps the home view focused, and reveals detail when someone chooses to explore. A purchase check can consider a planned amount, upcoming commitments, payment-card offers and an optional product or booking link. A conversational view provides another way to ask about the sample financial picture.

> **Prototype notice:** All accounts, balances, valuations, scores, offers and integrations are illustrative. The app does not connect to financial institutions, fetch live prices, browse submitted purchase links, or provide a live AI assistant. It does not move money or make financial decisions.

## Explore the product

The [OptiSpend product guide](docs/PRODUCT_GUIDE.md) describes the product intent, experience areas, personalization, current prototype behavior, and the boundaries for future integrations.

The proposed product direction also includes an opt-in real-time financial gatekeeper and a wealth-optimization layer. These are documented as future capabilities; they are not live in this prototype.

## Run locally

This is a static site with no build step or package installation. From this folder, start a local server:

```sh
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000). Keep the terminal running while you use the site; stopping the server makes the local address unavailable. You can also open `index.html` directly, though a local server is more reliable.

## What’s in the prototype

- Personalized overview with sample net worth, assets and liabilities, alerts, and a money-habits signal
- Spend Gatekeeper with purchase planning, card-offer examples, and an illustrative product or travel link comparison
- Talk to your money chat, investment and savings views, rewards, protection, credit score, loans, goals, and upcoming events
- Asset Pulse for sample resale values, depreciation context, linked liabilities, and updates tied to sample holdings
- Mock connected-account and broker flows, plus profile and settings

See the product guide for what is interactive today versus what remains a future integration.

## Project files

- `index.html` — app shell and page structure
- `styles.css` — responsive styles and life-stage themes
- `app.js` — sample data, view switching, and prototype interactions
