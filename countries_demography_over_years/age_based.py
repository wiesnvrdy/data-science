from main_df import src
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pgo
import os

# Preliminary plot parent directory creation
name_folder = True
foldername = 'plot_age'
idx_folder = 0
while name_folder:
    try:
        os.mkdir(foldername)
    except FileExistsError:
        idx_folder += 1
        foldername = f'plot_age_{idx_folder}'
        name_folder = True
    else:
        name_folder = False

# Select input(s) listing
country_source = []
for country_opt in src.Country.unique():
    country_source.append(country_opt)

countries_scan = [country_source[14], country_source[20], country_source[3]]

# Select age category(s) listing
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

for age_scan_category in age_scan_categories:
    
    # Country-based filtering
    country_sub_dfs = []
    for country_scan in countries_scan:
        country_sub_dfs.append(src[src.Country == country_scan])
    age_category_df = pd.concat(country_sub_dfs)
    
    # Age-based filtering
    age_sub_dfs = []
    for age_scan_source in age_scan_sources[age_scan_categories.index(age_scan_category)]:
        age_sub_dfs.append(age_category_df[age_category_df.Age == age_scan_source])
    age_category_df = pd.concat(age_sub_dfs)
    
    # Making age category-based data frame
    age_category_df = age_category_df.groupby(['Time', 'Country'],
                                                as_index = False).agg({'Value' : pd.Series.sum})

    # Making subdata frame (country-based)
    per_country_df = []
    for country_scan in countries_scan:
        per_country_df.append(age_category_df[age_category_df.Country == country_scan].drop('Country',
                                axis = 1).rename(columns = {'Time' : 'Year',
                                                            'Value' : country_scan}))                                     
    # Merging all subdata frame (country-based)
    age_category_df = per_country_df[0]
    for i_agedf in range (1, len(per_country_df)):
        age_category_df = pd.merge(age_category_df, per_country_df[i_agedf], on = 'Year')
    
    # Plotting preparation
    col = []
    for i_col in range (1, len(age_category_df.columns.tolist())):
        col.append(age_category_df.columns.tolist()[i_col])
    os.mkdir(f'{foldername}\{age_scan_category}')
    
    # Plotting derived data source table
    subcol_df = []
    for col_name in age_category_df.columns:
        subcol_df.append(age_category_df[f'{col_name}'])
    
    pgo.Figure(data = [pgo.Table(header = dict(values = list(age_category_df.columns),
                                               fill_color = 'paleturquoise',
                                               align = 'center'),
                                 cells = dict(values = subcol_df,
                                              fill_color = 'lavender',
                                              align = 'center',
                                              format = [None] + [','] * (len(age_category_df.columns)-1)))]).write_image(f'.\{foldername}\{age_scan_category}\{age_scan_category} Data Table.png',
                                                                                                                      scale = 3)
    # Plotting (populations over years - collective)
    px.bar(age_category_df,
           x = 'Year',
           y = col,
           width = 1200,
           barmode = 'group',
           title = f'{age_scan_category} Populations Fluctuation Over Years',
           labels = {'variable' : 'Country',
                     'value' : 'Populations'}).update_layout(xaxis_title = 'Year',
                                                             yaxis_title = 'Populations',
                                                             xaxis = dict(dtick = 1),
                                                             font = dict(size = 19),
                                                             legend = dict(font = dict(size = 14))).write_image(f'.\{foldername}\{age_scan_category}\All Age Group.png',
                                                                                                                 scale = 2)
    # Plotting (populations over years - grouped)
    os.mkdir(f'{foldername}\{age_scan_category}\Per Country Plot')
    for country_group in col:
        px.line(age_category_df,
                x = 'Year',
                y = country_group,
                title = f"{age_scan_category[age_scan_category.find('(')+1:age_scan_category.find(')')]} Populations in {country_group} Over Years",
                width = 1100,
                markers = True).update_layout(xaxis_title = 'Year',
                                              yaxis_title = 'Populations',
                                              xaxis = dict(dtick = 1,
                                                           showgrid = True,
                                                           linecolor = 'black',
                                                           gridcolor =  'silver'),
                                              yaxis = dict(showgrid = True,
                                                           linecolor = 'black',
                                                           gridcolor = 'silver'),
                                              font = dict(size = 19),
                                              legend = dict(font = dict(size = 14))).write_image(f'.\{foldername}\{age_scan_category}\Per Country Plot\{country_group}.png',
                                                                                                 scale = 2)
