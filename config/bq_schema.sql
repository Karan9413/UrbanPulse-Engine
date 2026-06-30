CREATE TABLE IF NOT EXISTS zone_risk_index (
    zone_id VARCHAR,
    avg_pulse_index DOUBLE,
    total_anomalies BIGINT,
    last_updated TIMESTAMP
);