-- Example semantic views after loading the Gold CSV marts into a SQL engine.
-- These are aggregate product analytics, not person-level financial advice.

CREATE VIEW semantic_purchase_checks_daily AS
SELECT
    event_date,
    SUM(check_count) AS purchase_check_count,
    SUM(within_plan_count) AS within_plan_count,
    SUM(review_count) AS checks_to_review,
    100.0 * SUM(within_plan_count) / NULLIF(SUM(check_count), 0)
        AS within_plan_rate_pct,
    SUM(estimated_amount_midpoint_inr)
        AS estimated_planned_amount_midpoint_inr
FROM purchase_checks_daily
GROUP BY event_date;

CREATE VIEW semantic_purchase_checks_by_category AS
SELECT
    category,
    SUM(check_count) AS purchase_check_count,
    SUM(within_plan_count) AS within_plan_count,
    SUM(review_count) AS checks_to_review,
    100.0 * SUM(within_plan_count) / NULLIF(SUM(check_count), 0)
        AS within_plan_rate_pct,
    SUM(estimated_amount_midpoint_inr)
        AS estimated_planned_amount_midpoint_inr
FROM purchase_checks_by_category
GROUP BY category;

CREATE VIEW semantic_purchase_checks_by_outcome AS
SELECT
    guidance_outcome,
    SUM(check_count) AS purchase_check_count,
    SUM(estimated_amount_midpoint_inr)
        AS estimated_planned_amount_midpoint_inr
FROM purchase_checks_by_outcome
GROUP BY guidance_outcome;
