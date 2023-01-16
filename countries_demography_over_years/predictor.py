from main_df import src
import plotly.graph_objects as pgo
import pandas as pd
import os

name_folder = True
foldername = 'predictor_table'
idx_folder = 0
while name_folder:
    try:
        os.mkdir(foldername)
    except FileExistsError:
        idx_folder += 1
        foldername = f'predictor_table_{idx_folder}'
        name_folder = True
    else:
        name_folder = False

country_source = []
for country_opt in src.Country.unique():
    country_source.append(country_opt)
country_scan = [country_source[14], country_source[20], country_source[3], country_source[29],
                country_source[26], country_source[43], country_source[31], country_source[45],
                country_source[18], country_source[7], country_source[48], country_source[23]]

age_source = [['0 to 4', '5 to 9', '10 to 14', '15 to 19'],
              ['20 to 24', '25 to 29', '30 to 34'],
              ['35 to 39', '40 to 44', '45 to 49'],
              ['50 to 54', '55 to 59', '60 to 64'],
              ['65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 and over']]
age_categories = ['0 to 19 (Youngster Age)',
                  '20 to 34 (Early Productive Age)',
                  '35 to 49 (Mid Productive Age)',
                  '50 to 64 (End Productive Age)',
                  '65 and over (Older Age)']
age_scan_categories = [age_categories[0], age_categories[4]]
age_scan_sources = []
for age_category in age_scan_categories:
    age_scan_sources.append(age_source[age_categories.index(age_category)])

analysis_results = []
for country in country_scan:
    analyze_df = pd.DataFrame(src[src.Country == country].drop('Country', axis = 1))
    analyze_dfs = []
    for age_group in age_scan_sources:
        age_subdfs = []
        for age in age_group:
            age_subdfs.append(analyze_df[analyze_df.Age == age])
        analyze_dfs.append(pd.concat(age_subdfs).groupby('Time',
                           as_index = False).agg({'Value' : pd.Series.sum}).rename(columns = {'Time' : 'X(Year)',
                                                                                    'Value' : 'Y(Population)'}))
    sub_result = []
    for df in analyze_dfs:
        df['XY'] = df['X(Year)'] * df['Y(Population)']
        df['X^2'] = df['X(Year)'] ** 2
        df['Y^2'] = df['Y(Population)'] ** 2
        n = df['XY'].count().item()
        sigma_x = df['X(Year)'].sum().item()
        sigma_y = df['Y(Population)'].sum().item()
        sigma_xy = df['XY'].sum().item()
        sigma_x2 = df['X^2'].sum().item()
        sigma_y2 = df['Y^2'].sum().item()
        slope = round(((n * sigma_xy) - (sigma_x * sigma_y)) / ((n * sigma_x2) - (sigma_x ** 2)))
        r2 = round((((n * sigma_xy) - (sigma_x * sigma_y)) / ((((n * sigma_x2) - (sigma_x ** 2)) * ((n * sigma_y2) - (sigma_y ** 2))) ** 0.5)) ** 2, 5)
        sub_result.append([slope, r2])
    
    analysis_results.append(sub_result)

plot_data = []
for i_age in range(len(age_scan_categories)):
    slope_list = []
    r2_list = []
    for i_country in range(len(country_scan)):
        slope_list.append(analysis_results[i_country][i_age][0])
        r2_list.append(analysis_results[i_country][i_age][1])
    plot_data.append([country_scan, slope_list, r2_list])

for i_plot in range(len(plot_data)):
    pgo.Figure(data = [pgo.Table(header = dict(values = ['Country', 'Population Growth Projection', 'R-Square'],
                                               fill_color = 'paleturquoise',
                                               align = 'center'),
                                cells = dict(values = plot_data[i_plot],
                                             fill_color = 'lavender',
                                             align = 'center',
                                             format = [None] + [','] + [None]))]).write_image(f'.\{foldername}\Predictor Table for {age_scan_categories[i_plot]}.png',
                                                                                                scale = 5)
