# OptiSpend product guide

## 1. Product intent

OptiSpend is a personal-finance companion designed to make money easier to understand and act on. It brings a person’s financial picture together and helps them think through choices such as a purchase, a savings goal, a card benefit, or an upcoming expense.

The product should feel calm, clear, and trustworthy. It should make the next useful action easy to find without presenting every metric and option at once. People can explore more detail when they want it.

### Product promise

- Give people a clear view of their money, including assets minus liabilities.
- Help them make considered spending decisions while keeping their autonomy.
- Surface useful benefits and reminders at the moment they matter.
- Make financial planning feel relevant to the person’s life stage and goals.

## 2. Experience principles

1. **Start simple.** The overview gives a short, useful summary; deeper detail lives in dedicated sections.
2. **Show context with advice.** A recommendation should explain the key reason and the conditions that could change it.
3. **Keep the person in control.** Suggestions are guidance. Purchases, transfers, bookings, and account changes require the person’s decision and explicit review.
4. **Be clear about uncertainty.** Label sample values, estimates, freshness, and data sources. Never present a model or estimate as a live quote.
5. **Use a supportive tone.** Encourage planning without shaming someone for spending, saving, or choosing a goal.
6. **Personalize presentation, not truth.** Life stage can change tone and emphasis, while financial facts and limitations remain clear.
7. **Make consent visible.** A future account connection should show what data is requested, why, for how long, and how to revoke access.

## 3. Life-stage personalization

Onboarding asks which stage currently feels most relevant. It can be skipped or changed later.

| Segment | Experience direction | Emphasis |
| --- | --- | --- |
| College student | Colorful, expressive, and interactive | Spending awareness, first savings habits, attainable goals |
| Early career | A blend of lively and composed | Building buffers, automating goals, organizing benefits and liabilities |
| Established / high earning | Restrained, polished, and information-rich | Coordinating assets, liabilities, commitments, and long-term plans |

The current prototype changes theme and selected copy based on this choice. The user profile and underlying sample financial data are not independently modeled for each segment.

## 4. Information architecture

### Overview

A concise landing page for net worth, available-to-spend context, near-term alerts, and a sample money-habits signal. Net worth is calculated as assets minus liabilities. Shortcuts lead to purchase planning, goals, or a deeper portfolio view.

### Talk to your money

A conversational entry point for questions about the sample data, future plans, and navigating the prototype. The current reply logic is local and rule-based. It is not connected to an LLM or financial data service. Demo reminders ask for confirmation and only affect the local prototype state.

### Spend Gatekeeper

A purchase-planning view where someone can enter an item or service, an amount, a category, and an optional link. It presents sample cash-flow context, relevant mock card-benefit examples, and broad depreciation context for certain goods. Link results are illustrative: the prototype does not open submitted links or search other merchants for live prices.

A future comparison flow could normalize the total payable price across merchants, including delivery or booking fees, eligibility, payment offers, cancellation terms, and reward value. It should identify the source and timestamp for each live result.

The longer-term **financial gatekeeper** concept is an opt-in checkpoint before a user completes a discretionary purchase. It would compare the planned spend with that user’s chosen savings targets, known fixed obligations, and available cash-flow buffer, then explain the trade-offs and suggest relevant payment benefits. OptiSpend should inform and help the user review a choice; it should not silently block or execute a transaction. The current prototype is not connected to a payment rail or issuer authorization flow and cannot intercept, approve, or decline real transactions.

### Divers

A broad view of financial holdings and places money can be held: banking and savings, mutual funds, Indian and US stocks, bonds and G-Secs, gold and silver, real estate, government schemes, and retirement. The prototype uses sample portfolio records and simple filters; broker data is not connected.

### Asset Pulse

Tracks user-entered cars, phones, gadgets, watches, and property using purchase details, optional current quotes, and optional linked loan balances. The prototype calculates illustrative resale estimates and broad depreciation context, keeps the uncertainty visible, and includes example updates tied to sample holdings. Cars24, Spinny, CarWale, Cashify, property valuations, and company news are not live sources in this demo.

### Invest

A sample view for comparing investment options and exploring holdings. It is a presentation prototype, not a personalized recommendation engine or an execution flow.

A future wealth-optimization layer could compare eligible card rewards and surface savings, investment, or tax-planning ideas using a user’s stated goals, time horizon, liquidity needs, and risk preferences. Any tax or investment output must show assumptions, source and date, uncertainty, fees, and relevant eligibility; it should distinguish general education from regulated personalized advice and require appropriate review before action. The current prototype does not calculate tax liability, produce risk-profiled recommendations, verify live products or rates, or place investments.

### Rewards

Shows example card benefits and a sample offer lookup. The interface demonstrates how a relevant offer can be summarized first, with full terms available on demand. Offer availability, eligibility, caps, and redemption value must be verified with the issuer before a real purchase. The HDFC Millennia example links to issuer terms; offers are not fetched live.

### Protect

A place for insurance and protection coverage summaries. Current values are sample data; there is no underwriting or policy connection.

### Credit Score and Loans

Sample credit-score context and loan summaries or calculators. The credit score is separate from OptiSpend’s sample money-habits signal. No bureau or lender data is connected.

### Goals and events

Tracks sample savings goals and upcoming events so that planning can account for meaningful dates and commitments. Demo reminders remain local to the prototype.

### Connected accounts

Lists mock banks, brokerages, and data providers such as Groww, Zerodha, INDmoney, banks, and Account Aggregator flows. The controls explain a future consent step but do not establish a real connection or store account credentials.

### Profile and settings

A place to change the life-stage preference and other sample preferences. Current preference changes are local to the browser.

## 5. Contextual signals and emotional design

The product can surface a small number of timely prompts: upcoming bills and events, expiring card points, cash above a chosen buffer, relevant card benefits, and changes to holdings a person owns. Location-aware or macroeconomic opportunities are a future capability and must include source, date, relevance, and uncertainty.

Emotional language should support a person’s goals and sense of agency. For example, a travel nudge may acknowledge progress while showing the effect on the person’s plan. It should never declare that a person “deserves” or does not deserve a purchase based on a behavioral score.

## 6. What works today vs. future work

| Capability | Current prototype | Future integration needed |
| --- | --- | --- |
| Net worth | Calculates from included sample assets and liabilities | Consented, normalized accounts and verified valuations |
| Purchases | Local API evaluates against sample balances and obligations; UI keeps the choice with the person | Fresh consented balances, bills, merchant parsing, live offer rules |
| Pre-purchase gatekeeper | Informational check only; no transaction approval or blocking | Explicit opt-in, normalized obligations, fresh account data, and a consented payment or issuer workflow; no silent blocking |
| Purchase links | Validates a URL and shows an illustrative comparison | Secure page retrieval, merchant matching, price search, terms verification |
| Rewards | Sample card examples and benefit details | Issuer or offer-provider feeds, eligibility, caps, expiry and redemption data |
| Chat | Local intent handling over sample records | Authenticated model service, permission-scoped retrieval, action review |
| Wealth and tax optimization | Educational sample comparisons only | User-approved risk and goal inputs, current product and tax rules, suitability controls, and qualified review where required |
| Accounts and brokers | Mock connection catalog | Consented provider adapters and revocation handling |
| Asset valuations | Broad illustrative estimates and user-entered quotes | Licensed or permitted valuation sources, quote timestamps, condition and location inputs |
| News and signals | Example holding-specific card | Current trusted sources matched only to owned holdings, with citations and uncertainty |

## 7. Backend and analytics design work

As part of the OptiSpend project, the backend and analytics work explores transaction-aware purchase checks and wealth-optimization workflows. A small local service is implemented to make the purchase-check path concrete. The production-scale services below remain architecture and system-design work; provider access, data residency, throughput, cost, retention, and regulatory requirements would need validation before implementation.

### Project work summary

- Implemented a local purchase-check API that compares a planned amount with sample available balance, a protected event reserve, and a comfort buffer, then returns a short explanation for the person to review.
- Built a producer/consumer event flow for purchase checks. It processes broad category, amount band, and guidance outcome only; item names, links, exact purchase amounts, account data, and transaction records are not retained in analytics.
- Added an in-memory aggregate endpoint for check counts by category, amount band, and outcome. The aggregates clear when the local service stops.
- Designed recommendation workflows for matching eligible card benefits to planned purchases and, as future work, surfacing savings, investment, or tax-planning ideas using stated goals, time horizon, liquidity needs, and risk preferences.
- Proposed a production-scale path using consented Plaid / Sahamati-compatible data adapters, Kafka event intake, Flink stream processing, Redis for short-lived decision context, PostgreSQL for application records, and Delta Lake for governed historical analytics.
- Considered data freshness, consent scope, event deduplication, auditability, uncertainty, data minimization, and human review as part of the recommendation pipeline.

The local service uses Python's standard library and a single-process in-memory queue. It demonstrates the API and event-processing boundary without requiring a broker or database. Kafka, Flink, Redis, PostgreSQL, Delta Lake, Plaid, and Sahamati are not connected in this prototype; the later architecture describes how the design could scale and integrate with consented external data.

1. **Consent and provider adapters:** Plaid (where supported) and India’s Account Aggregator ecosystem through compatible Sahamati participants can provide consented financial data. Adapters normalize provider-specific accounts, balances, transactions, and consent events. Product availability and the exact API path depend on geography, provider participation, and user authorization.
2. **Event intake:** A backend publishes normalized, consent-scoped updates to Kafka. Events include provider, account reference, event time, ingestion time, consent scope, and a deduplication key; credentials and unnecessary personal data stay out of event payloads.
3. **Streaming analysis:** Flink can reconcile events, categorize transactions, update obligation and savings-target views, and evaluate user-configured gatekeeper rules. Late, duplicated, corrected, or missing events need explicit handling so recommendations do not treat incomplete data as certain.
4. **Fast decision context:** Redis can hold short-lived derived context for low-latency purchase checks, with explicit freshness markers and expiration. It should not become the source of truth for financial records.
5. **Application records:** PostgreSQL can store user preferences, goals, consent references, normalized account metadata, review history, and recommendation explanations, protected with encryption, access controls, and audit logging.
6. **Historical analytics:** Delta Lake can hold governed, access-controlled historical data for trend analysis and model evaluation, subject to minimization, retention, deletion, and applicable consent obligations.
7. **Recommendation response:** The API returns an explanation with the values and dates used, freshness, missing-data caveats, and relevant alternatives. A purchase decision remains user-controlled. Financial execution stays outside the recommendation path unless a separately authorized, compliant product flow is designed.

Plaid, Sahamati, Kafka, Flink, Redis, PostgreSQL, and Delta Lake are proposed integration and infrastructure examples only. This static prototype uses local sample data and does not connect to any of them.

## 8. Integration and data principles

A production implementation should put external access behind a backend service, not in browser-only code. Each imported record should carry its provider, consent scope, retrieval time, freshness state, and revocation status. Account Aggregator or other open-finance flows should be used only where available and with explicit user consent.

Never ask for or store a bank or brokerage password in the interface. Do not execute a payment, trade, loan application, booking, or insurance action from a conversational suggestion. Present the proposed action, amount, destination, and key terms for the person to review and confirm.

Potential adapters include:

- Indian financial-data consent flows and supported Account Aggregator participants
- Banks and payment accounts
- Brokerage and investment platforms such as Groww, Zerodha, and INDmoney
- Card issuers and reward / offer providers
- Merchant, travel, resale, and property-data sources
- Credit bureaus, lenders, and insurance providers

Provider names are examples of possible future integrations, not endorsements or claims of current access.

## 9. Running the prototype

See the [README](../README.md) for local setup. The site is static and uses sample data. Keep the local server process running while browsing; closing it makes the localhost page unavailable.
