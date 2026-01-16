-- SHI Daily Trends Query
-- Dataset cho Superset: Hiển thị SHI theo thời gian

SELECT 
    sd.date,
    c.name AS crop_name,
    c.crop_type,
    sd.shi_score,
    sd.weather_score,
    sd.care_score,
    sd.growth_score,
    sd.warning_level,
    sd.warning_message,
    CASE 
        WHEN sd.shi_score >= 80 THEN 'Xuất sắc'
        WHEN sd.shi_score >= 60 THEN 'Tốt'
        WHEN sd.shi_score >= 40 THEN 'Trung bình'
        ELSE 'Kém'
    END AS status_vn
FROM shi_daily sd
JOIN crops c ON sd.season_id = c.id
WHERE sd.date >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY sd.date DESC, c.name;

