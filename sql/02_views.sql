CREATE OR REPLACE VIEW analytics.overall_kpis AS
SELECT COUNT(*) AS contacts, ROUND(AVG(call_duration_in_minutes),2) AS avg_duration_minutes,
 ROUND(AVG(csat_score),2) AS avg_csat,
 COUNT(csat_score) AS csat_responses,
 ROUND(100.0*COUNT(csat_score)/NULLIF(COUNT(*),0),2) AS csat_response_pct,
 ROUND(100.0*AVG(is_within_sla::int),2) AS within_sla_pct,
 ROUND(100.0*AVG(is_negative_sentiment::int),2) AS negative_sentiment_pct
FROM analytics.call_center;
CREATE OR REPLACE VIEW analytics.by_channel AS
SELECT channel, COUNT(*) AS contacts, ROUND(AVG(call_duration_in_minutes),2) AS avg_duration_minutes,
 ROUND(AVG(csat_score),2) AS avg_csat, COUNT(csat_score) AS csat_responses,
 ROUND(100.0*AVG(has_csat::int),2) AS csat_response_pct,
 ROUND(100.0*AVG(is_within_sla::int),2) AS within_sla_pct,
 ROUND(100.0*AVG(is_negative_sentiment::int),2) AS negative_sentiment_pct
FROM analytics.call_center GROUP BY channel;
CREATE OR REPLACE VIEW analytics.by_centre AS
SELECT call_centres_city, COUNT(*) AS contacts, ROUND(AVG(call_duration_in_minutes),2) AS avg_duration_minutes,
 ROUND(AVG(csat_score),2) AS avg_csat, COUNT(csat_score) AS csat_responses,
 ROUND(100.0*AVG(has_csat::int),2) AS csat_response_pct,
 ROUND(100.0*AVG(is_within_sla::int),2) AS within_sla_pct,
 ROUND(100.0*AVG(is_negative_sentiment::int),2) AS negative_sentiment_pct
FROM analytics.call_center GROUP BY call_centres_city;
CREATE OR REPLACE VIEW analytics.by_reason AS
SELECT reason, COUNT(*) AS contacts, ROUND(AVG(call_duration_in_minutes),2) AS avg_duration_minutes,
 ROUND(AVG(csat_score),2) AS avg_csat,
 ROUND(100.0*AVG(is_within_sla::int),2) AS within_sla_pct,
 ROUND(100.0*AVG(is_negative_sentiment::int),2) AS negative_sentiment_pct
FROM analytics.call_center GROUP BY reason;
CREATE OR REPLACE VIEW analytics.daily_trends AS
SELECT call_timestamp, COUNT(*) AS contacts, ROUND(AVG(csat_score),2) AS avg_csat,
 ROUND(100.0*AVG(is_within_sla::int),2) AS within_sla_pct
FROM analytics.call_center GROUP BY call_timestamp;
CREATE OR REPLACE VIEW analytics.sentiment_summary AS
SELECT sentiment, COUNT(*) AS contacts, ROUND(AVG(csat_score),2) AS avg_csat,
 COUNT(csat_score) AS csat_responses
FROM analytics.call_center GROUP BY sentiment;
CREATE OR REPLACE VIEW analytics.centre_channel AS
SELECT call_centres_city, channel, COUNT(*) AS contacts, ROUND(AVG(csat_score),2) AS avg_csat,
 ROUND(100.0*AVG(is_within_sla::int),2) AS within_sla_pct,
 ROUND(100.0*AVG(is_negative_sentiment::int),2) AS negative_sentiment_pct
FROM analytics.call_center GROUP BY call_centres_city, channel;
