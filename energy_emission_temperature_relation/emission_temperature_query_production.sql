-- opening database
USE energy_emission_temperature_relation;

-- table data cleaning, then selecting and joining related table related table columns
SELECT emission.record_year AS record_year,
	   emission.annual_emission_gigatonnes AS annual_emission_GigaT,
       temperature.temperature_change_celsius AS temperature_change_C

FROM (SELECT record_year, ROUND(SUM(emission_tonnes / 1000000000), 2) AS annual_emission_gigatonnes
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
	  AND country NOT LIKE 'World%'
	  GROUP BY record_year) AS emission
	
INNER JOIN (SELECT *
			FROM world_temperature
			WHERE record_year >= 2010
			AND record_year <= 2020) AS temperature

ON emission.record_year = temperature.record_year;
