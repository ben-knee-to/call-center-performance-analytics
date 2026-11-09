SELECT * FROM analytics.overall_kpis;
SELECT COUNT(*) AS staging_rows, COUNT(DISTINCT id) AS distinct_ids FROM staging.call_center;
SELECT * FROM analytics.by_centre ORDER BY avg_csat DESC NULLS LAST;
SELECT * FROM analytics.by_channel ORDER BY avg_csat DESC NULLS LAST;
SELECT * FROM analytics.by_reason ORDER BY contacts DESC;
SELECT * FROM analytics.sentiment_summary ORDER BY contacts DESC;
SELECT * FROM analytics.daily_trends ORDER BY call_timestamp;
