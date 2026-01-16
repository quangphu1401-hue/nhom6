-- Weather Impact Analysis Query
-- Dataset cho Superset: Phân tích tác động thời tiết

SELECT 
    wd.recorded_at::date AS date,
    c.name AS crop_name,
    wd.temperature,
    wd.humidity,
    wd.precipitation,
    wd.wind_speed,
    sd.shi_score,
    sd.weather_score,
    CASE 
        WHEN wd.temperature > 35 THEN 'Stress nhiệt'
        WHEN wd.temperature < 15 THEN 'Lạnh'
        WHEN wd.precipitation > 80 THEN 'Mưa nhiều'
        WHEN wd.precipitation = 0 AND wd.humidity < 50 THEN 'Khô hạn'
        ELSE 'Bình thường'
    END AS weather_condition
FROM weather_data wd
JOIN crops c ON wd.crop_id = c.id
LEFT JOIN shi_daily sd ON sd.season_id = c.id AND sd.date = wd.recorded_at::date
WHERE wd.is_forecast = 0
  AND wd.recorded_at >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY wd.recorded_at DESC;

