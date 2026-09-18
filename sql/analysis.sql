```sql
-- ============================================================
-- WEATHER RISK PIPELINE - ANALYSE SQL
-- Base de données : weather_risk
-- ============================================================


-- ============================================================
-- 1. DISTRIBUTION GLOBALE DES RISQUES
-- ============================================================
-- Question :
-- Combien d'enregistrements appartiennent à chaque catégorie de risque ?

SELECT
    risk_category,
    COUNT(*) AS number_of_records
FROM weather_risk
GROUP BY risk_category
ORDER BY number_of_records DESC;


-- ============================================================
-- 2. VILLE / JOUR AVEC LE RISQUE LE PLUS ÉLEVÉ
-- ============================================================
-- Question :
-- Quelle ville et quelle date présentent le risque météorologique le plus élevé ?

SELECT
    c.city,
    w.date,
    w.risk_score,
    w.risk_category
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
ORDER BY w.risk_score DESC
LIMIT 10;


-- ============================================================
-- 3. RISQUE MOYEN PAR VILLE
-- ============================================================
-- Question :
-- Quelles villes ont le risque moyen le plus élevé
-- pendant la période de prévision ?

SELECT
    c.city,
    ROUND(AVG(w.risk_score)::numeric, 2) AS average_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
GROUP BY c.city
ORDER BY average_risk DESC
LIMIT 10;


-- ============================================================
-- 4. JOUR AVEC LE RISQUE LE PLUS ÉLEVÉ
-- ============================================================
-- Question :
-- Quelles dates ont le risque météorologique moyen le plus élevé ?

SELECT
    w.date,
    ROUND(AVG(w.risk_score)::numeric, 2) AS average_risk,
    MAX(w.risk_score) AS maximum_risk
FROM weather_risk w
GROUP BY w.date
ORDER BY average_risk DESC;


-- ============================================================
-- 5. RISQUE PAR VILLE ET PAR DATE
-- ============================================================
-- Question :
-- Afficher le niveau de risque pour chaque ville et chaque jour.

SELECT
    c.city,
    w.date,
    w.risk_score,
    w.risk_category
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
ORDER BY w.risk_score DESC, w.date;


-- ============================================================
-- 6. TOP 10 DES COMBINAISONS VILLE / DATE LES PLUS RISQUÉES
-- ============================================================
-- Question :
-- Quelles sont les 10 combinaisons ville/date les plus risquées ?

SELECT
    c.city,
    w.date,
    w.risk_score,
    w.risk_category,
    w.rain_risk,
    w.wind_risk,
    w.gust_risk,
    w.temperature_risk,
    w.weather_code_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
ORDER BY w.risk_score DESC
LIMIT 10;


-- ============================================================
-- 7. ANALYSE DES CAUSES DU RISQUE
-- ============================================================
-- Question :
-- Quels facteurs météorologiques contribuent le plus au risque ?

SELECT
    c.city,
    w.date,
    w.risk_score,
    w.rain_risk,
    w.wind_risk,
    w.gust_risk,
    w.temperature_risk,
    w.weather_code_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
ORDER BY w.risk_score DESC
LIMIT 10;


-- ============================================================
-- 8. MOYENNE DES COMPOSANTES DU RISQUE
-- ============================================================
-- Question :
-- Quelle est la contribution moyenne de chaque composante du risque ?

SELECT
    ROUND(AVG(rain_risk)::numeric, 2) AS average_rain_risk,
    ROUND(AVG(wind_risk)::numeric, 2) AS average_wind_risk,
    ROUND(AVG(gust_risk)::numeric, 2) AS average_gust_risk,
    ROUND(AVG(temperature_risk)::numeric, 2) AS average_temperature_risk,
    ROUND(AVG(weather_code_risk)::numeric, 2) AS average_weather_code_risk
FROM weather_risk;


-- ============================================================
-- 9. CATÉGORIE DE RISQUE PAR VILLE
-- ============================================================
-- Question :
-- Combien de jours Low, Moderate, High, etc. chaque ville possède-t-elle ?

SELECT
    c.city,
    w.risk_category,
    COUNT(*) AS number_of_days
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
GROUP BY c.city, w.risk_category
ORDER BY c.city, number_of_days DESC;


-- ============================================================
-- 10. VILLES AVEC UN RISQUE MODÉRÉ OU PLUS ÉLEVÉ
-- ============================================================
-- Question :
-- Quelles villes ont au moins un jour avec un risque supérieur à Low ?

SELECT DISTINCT
    c.city
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.risk_score > 20
ORDER BY c.city;


-- ============================================================
-- 11. NOMBRE DE JOURS À RISQUE PAR VILLE
-- ============================================================
-- Question :
-- Quelles villes ont le plus de jours à risque ?

SELECT
    c.city,
    COUNT(*) AS risky_days
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.risk_score > 20
GROUP BY c.city
ORDER BY risky_days DESC, c.city;


-- ============================================================
-- 12. ANALYSE DU RISQUE LIÉ AUX PRÉCIPITATIONS
-- ============================================================
-- Question :
-- Quelles villes et quelles dates ont le risque de précipitation le plus élevé ?

SELECT
    c.city,
    w.date,
    w.precipitation,
    w.precipitation_probability,
    w.rain_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.rain_risk > 0
ORDER BY w.rain_risk DESC, w.precipitation DESC
LIMIT 10;


-- ============================================================
-- 13. ANALYSE DU RISQUE LIÉ AU VENT
-- ============================================================
-- Question :
-- Quelles villes et quelles dates ont le risque de vent le plus élevé ?

SELECT
    c.city,
    w.date,
    w.wind_speed,
    w.wind_gusts,
    w.wind_risk,
    w.gust_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.wind_risk > 0
   OR w.gust_risk > 0
ORDER BY
    GREATEST(w.wind_risk, w.gust_risk) DESC,
    w.wind_speed DESC
LIMIT 10;


-- ============================================================
-- 14. ANALYSE DU RISQUE LIÉ À LA TEMPÉRATURE
-- ============================================================
-- Question :
-- Quelles villes et quelles dates ont le risque de température le plus élevé ?

SELECT
    c.city,
    w.date,
    w.temp_max,
    w.temp_min,
    w.temperature_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.temperature_risk > 0
ORDER BY w.temperature_risk DESC
LIMIT 10;


-- ============================================================
-- 15. ANALYSE DU RISQUE LIÉ AUX CONDITIONS MÉTÉOROLOGIQUES
-- ============================================================
-- Question :
-- Quelles villes et quelles dates ont le risque lié aux conditions météo le plus élevé ?

SELECT
    c.city,
    w.date,
    w.weather_code,
    w.weather_code_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.weather_code_risk > 0
ORDER BY w.weather_code_risk DESC
LIMIT 10;


-- ============================================================
-- 16. VILLES LES PLUS RISQUÉES ET LEUR JOUR LE PLUS RISQUÉ
-- ============================================================
-- Question :
-- Pour chaque ville, quel est son jour avec le risque maximal ?

SELECT
    c.city,
    MAX(w.risk_score) AS maximum_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
GROUP BY c.city
ORDER BY maximum_risk DESC
LIMIT 10;


-- ============================================================
-- 17. ÉVOLUTION DU RISQUE PAR JOUR
-- ============================================================
-- Question :
-- Comment le risque global évolue-t-il d'un jour à l'autre ?

SELECT
    w.date,
    ROUND(AVG(w.risk_score)::numeric, 2) AS average_risk,
    ROUND(MAX(w.risk_score)::numeric, 2) AS maximum_risk,
    ROUND(MIN(w.risk_score)::numeric, 2) AS minimum_risk
FROM weather_risk w
GROUP BY w.date
ORDER BY w.date;


-- ============================================================
-- 18. NOMBRE DE VILLES À RISQUE PAR JOUR
-- ============================================================
-- Question :
-- Combien de villes dépassent le niveau Low chaque jour ?

SELECT
    w.date,
    COUNT(*) FILTER (WHERE w.risk_score > 20) AS risky_cities,
    COUNT(*) FILTER (WHERE w.risk_score <= 20) AS low_risk_cities
FROM weather_risk w
GROUP BY w.date
ORDER BY w.date;


-- ============================================================
-- 19. VILLE AVEC LE RISQUE MOYEN LE PLUS ÉLEVÉ
-- ============================================================
-- Question :
-- Quelle ville possède le risque moyen le plus élevé ?

SELECT
    c.city,
    ROUND(AVG(w.risk_score)::numeric, 2) AS average_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
GROUP BY c.city
ORDER BY average_risk DESC
LIMIT 1;


-- ============================================================
-- 20. REQUÊTE PRINCIPALE DU PROJET
-- ============================================================
-- Question :
-- Quelles villes et quelles périodes présentent le plus grand
-- risque météorologique dans les prochains jours ?

SELECT
    c.city,
    w.date,
    w.risk_score,
    w.risk_category,
    w.rain_risk,
    w.wind_risk,
    w.gust_risk,
    w.temperature_risk,
    w.weather_code_risk
FROM weather_risk w
JOIN cities c
    ON w.city_id = c.city_id
ORDER BY w.risk_score DESC, w.date
LIMIT 20;
```
