import pandas as pd

df_plant = pd.read_csv('./raw_data/global_power_plants.csv')
df_plant.drop(columns = ['latitude', 'longitude', 'other_fuel2', 'other_fuel3', 'owner of plant',
                         'geolocation_source', 'secondary fuel', 'generation_gwh_2021', 'country code',
                         'estimated_generation_gwh_2021', 'start date'], axis = 1, inplace = True)
df_plant.rename(columns = {'country_long' : 'Country',
                           'name of powerplant' : 'Power_Plant_Name',
                           'capacity in MW' : 'Capacity_MW',
                           'primary_fuel' : 'Energy_Source'}, inplace = True)
df_plant.to_csv('./clean_data/power_plant.csv', index = False)

df_emission = pd.read_csv('./raw_data/annual-co2-emissions-by-region.csv')
df_emission.drop(columns = 'Code', axis = 1, inplace = True)
df_emission.drop(df_emission[(df_emission['Annual CO2 emissions (zero filled)'] == 0)].index, inplace = True)
df_emission.rename(columns = {'Annual CO2 emissions (zero filled)' : 'CO2_Emission_Tonnes',
                              'Entity' : 'Country'}, inplace = True)
df_emission.reset_index(inplace = True)
df_emission.drop(columns = 'index', inplace = True)
df_emission.to_csv('./clean_data/co2_emission.csv', index = False)

df_temperature = pd.read_csv('./raw_data/Global_annual_mean_temp.csv')
df_temperature.drop(columns = 'Lowess(5)', axis = 1, inplace = True)
df_temperature.rename(columns = {'No_Smoothing' : 'Temperature_Change_Celsius'}, inplace = True)
df_temperature.to_csv('./clean_data/world_temperature.csv', index = False)
