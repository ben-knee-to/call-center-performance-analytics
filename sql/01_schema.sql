CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS staging.call_center (
 id text PRIMARY KEY, call_timestamp date NOT NULL, call_centres_city text,
 channel text, city text, customer_name text, reason text, response_time text,
 sentiment text, state text, call_duration_in_minutes numeric,
 csat_score numeric, within_sla integer, negative_sentiment integer,
 has_csat integer, day_of_week text, day integer, week_start date
);
CREATE OR REPLACE VIEW analytics.call_center AS
SELECT id, call_timestamp, call_centres_city, channel, city, customer_name,
 reason, response_time, sentiment, state, call_duration_in_minutes, csat_score,
 (response_time = 'Within SLA') AS is_within_sla,
 (sentiment IN ('Negative','Very Negative')) AS is_negative_sentiment,
 (csat_score IS NOT NULL) AS has_csat,
 EXTRACT(ISODOW FROM call_timestamp)::int AS weekday_number,
 date_trunc('week', call_timestamp)::date AS week_start
FROM staging.call_center;
