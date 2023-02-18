CREATE DATABASE energy_emission_temperature_relation;
USE energy_emission_temperature_relation;

CREATE TABLE co2_emission (
	country VARCHAR(50),
    record_year INT,
    emission_tonnes BIGINT
);
LOAD DATA LOCAL INFILE 'd:/Milestones/General Programming/Porto/Data Science/source/energy_emission_temperature_relation/clean_data/co2_emission.csv'
INTO TABLE co2_emission
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE power_plant (
	country VARCHAR(50),
    plant_name TEXT,
    capacity_megawatt FLOAT,
    energy_source VARCHAR(15)
);
LOAD DATA LOCAL INFILE 'd:/Milestones/General Programming/Porto/Data Science/source/energy_emission_temperature_relation/clean_data/power_plant.csv'
INTO TABLE power_plant
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE world_temperature (
	record_year INT,
    temperature_change_celsius FLOAT
);
LOAD DATA lOCAL INFILE 'd:/Milestones/General Programming/Porto/Data Science/source/energy_emission_temperature_relation/clean_data/world_temperature.csv'
INTO TABLE world_temperature
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
