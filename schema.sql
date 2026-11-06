CREATE TABLE meter_readings (
    reading_pk BIGINT AUTO_INCREMENT PRIMARY KEY,
    reading_time DATETIME,
    global_active_power DECIMAL(10,3),
    rolling_avg_30 DECIMAL(10,3),
    is_anomaly TINYINT DEFAULT 0
);
