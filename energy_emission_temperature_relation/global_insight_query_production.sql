-- opening database
USE energy_emission_temperature_relation;

-- extracting world power plant data
SELECT * FROM power_plant
WHERE country IN (SELECT DISTINCT country FROM co2_emission
				  WHERE record_year >= 2010
				  AND record_year <= 2020);

-- extracting emission data for countries with power plant
SELECT country, record_year, ROUND((emission_tonnes / 1000000), 2) AS emission_MegaT
FROM co2_emission
WHERE record_year >= 2010
AND record_year <= 2020
AND country IN (SELECT DISTINCT country FROM power_plant)
AND country NOT LIKE 'Africa%'
AND country NOT LIKE 'Asia%'
AND country NOT LIKE 'Europe%'
AND country NOT LIKE 'High%'
AND country NOT LIKE 'Inter%'
AND country NOT LIKE 'Low%'
AND country NOT LIKE 'North Am%'
AND country NOT LIKE 'Ocean%'
AND country NOT LIKE 'Upper%'
AND country NOT LIKE 'World%';