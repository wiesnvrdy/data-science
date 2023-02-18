-- opening database
USE energy_emission_temperature_relation;

-- selecting and joining related table columns, then rounding data values into two decimal places
SELECT plant.country AS country,
	   plant.total_plant_capacity_gigawatt AS total_plant_capacity_GW,
	   emission.average_emission_2010_2020_megatonnes AS average_emission_MegaT

FROM (SELECT country, (IF (	ROUND(SUM(capacity_megawatt / 1000), 2) <> 0,
							ROUND(SUM(capacity_megawatt / 1000), 2),
                            ROUND(SUM(capacity_megawatt / 1000), 3)))
                            AS total_plant_capacity_gigawatt
	  FROM power_plant
	  GROUP BY country) AS plant
      
INNER JOIN (SELECT country, ROUND(AVG(emission_tonnes / 1000000), 2) AS average_emission_2010_2020_megatonnes
			FROM co2_emission
			WHERE record_year >= 2010
			AND record_year <= 2020
			GROUP BY country) AS emission
            
ON plant.country = emission.country;
