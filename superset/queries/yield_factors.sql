-- Yield Factors Analysis Query
-- Dataset cho Superset: Phân tích yếu tố ảnh hưởng năng suất

SELECT 
    sh.crop_id,
    c.name AS crop_name,
    COUNT(*) AS total_seasons,
    AVG(sh.yield_per_hectare) AS avg_yield,
    AVG(sh.avg_shi_score) AS avg_shi,
    AVG(sh.total_cost) AS avg_cost,
    AVG(sh.profit) AS avg_profit,
    SUM(CASE WHEN sh.weather_issues IS NOT NULL THEN 1 ELSE 0 END) AS seasons_with_weather_issues,
    SUM(CASE WHEN sh.pest_issues IS NOT NULL THEN 1 ELSE 0 END) AS seasons_with_pest_issues,
    MAX(sh.yield_per_hectare) AS max_yield,
    MIN(sh.yield_per_hectare) AS min_yield,
    MAX(sh.yield_per_hectare) - MIN(sh.yield_per_hectare) AS yield_range
FROM season_history sh
JOIN crops c ON sh.crop_id = c.id
GROUP BY sh.crop_id, c.name
HAVING COUNT(*) >= 2
ORDER BY avg_yield DESC;

