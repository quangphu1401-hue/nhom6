-- Crop Performance Query
-- Dataset cho Superset: Phân tích hiệu suất mùa vụ

SELECT 
    sh.id,
    sh.season_name,
    c.name AS crop_name,
    c.crop_type,
    sh.start_date,
    sh.end_date,
    sh.yield_tonnes,
    sh.yield_per_hectare,
    sh.total_cost,
    sh.total_revenue,
    sh.profit,
    sh.avg_shi_score,
    CASE 
        WHEN sh.total_revenue > 0 AND sh.total_cost > 0 
        THEN ((sh.profit / sh.total_revenue) * 100)
        ELSE 0
    END AS profit_margin,
    sh.weather_issues,
    sh.pest_issues,
    sh.other_issues
FROM season_history sh
JOIN crops c ON sh.crop_id = c.id
ORDER BY sh.start_date DESC;

