from main_df import src
from interface import ui
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pgo
import os

# Preliminary plot parent directory creation
name_folder = True
foldername = 'plot_country'
idx_folder = 0
while name_folder:
    try:
        os.mkdir(foldername)
    except FileExistsError:
        idx_folder += 1
        foldername = f'plot_country_{idx_folder}'
        name_folder = True
    else:
        name_folder = False

# Country input(s) listing
country_source = []
for country_opt in src.Country.unique():
    country_source.append(country_opt)

country_scan = ui(country_source)['countries']
for country in country_scan:

    # Country-based-filtering
    country_df_raw = src[src.Country == country]
    country_df_raw = pd.DataFrame({'Year' : country_df_raw.Time,
                                   'Age' : country_df_raw.Age,
                                   'Population' : country_df_raw.Value})

    # Making subdata frame (age-based)
    per_age_df = []
    for age_cat in country_df_raw.Age.unique():
        sub_df_extract = country_df_raw[country_df_raw.Age == age_cat]
        sub_df_clean = sub_df_extract.drop('Age', axis = 1).rename(columns = {'Population' : f'{age_cat}'})
        per_age_df.append(sub_df_clean)
    
    # Merging all subdata frame (age-based)
    country_df = per_age_df[0]
    for i_agedf in range (1, len(per_age_df)):
        country_df = pd.merge(country_df, per_age_df[i_agedf], on = 'Year')

    # Calculating population for few categories from previous multiple categories
    country_df['0 to 19 (Youngster Age)'] = country_df['0 to 4'] + country_df['5 to 9'] + country_df['10 to 14'] + country_df['15 to 19']
    country_df['20 to 34 (Early Productive Age)'] = country_df['20 to 24'] + country_df['25 to 29'] + country_df['30 to 34']
    country_df['35 to 49 (Mid Productive Age)'] = country_df['35 to 39'] + country_df['40 to 44'] + country_df['45 to 49']
    country_df['50 to 64 (End Productive Age)'] = country_df['50 to 54'] + country_df['55 to 59'] + country_df['60 to 64']
    country_df['65 and over (Older Age)'] = country_df['65 to 69'] + country_df['70 to 74'] + country_df['75 to 79'] + country_df['80 to 84'] + country_df['85 and over']
    dropped_col = country_df_raw.Age.unique().tolist()
    country_df.drop(dropped_col, axis = 1, inplace = True)
    
    # Plotting preparation
    col = []
    for i_col in range (1, len(country_df.columns.tolist())):
        col.append(country_df.columns.tolist()[i_col])
    os.mkdir(f'{foldername}\{country}')
    
    # Plotting derived data source table
    subcol_df = []
    for col_name in country_df.columns:
        subcol_df.append(country_df[f'{col_name}'])

    pgo.Figure(data = [pgo.Table(header = dict(values = list(country_df.columns),
                                               fill_color = 'paleturquoise',
                                               align = 'center'),
                                 cells = dict(values = subcol_df,
                                              fill_color = 'lavender',
                                              align = 'center',
                                              format = [None] + [','] * (len(country_df.columns)-1)))]).write_image(f'.\{foldername}\{country}\{country} Data Table.png',
                                                                                                                      scale = 3)

    # Plotting (populations over years - collective)
    px.bar(country_df,
           x = 'Year',
           y = col,
           width = 1200,
           barmode = 'group',
           title = f'{country} Populations Fluctuation Over Years',
           labels = {'variable' : 'Age (Group)',
                     'value' : 'Populations'}).update_layout(xaxis_title = 'Year',
                                                             yaxis_title = 'Populations',
                                                             xaxis = dict(dtick = 1),
                                                             font = dict(size = 19),
                                                             legend = dict(font = dict(size = 14))).write_image(f'.\{foldername}\{country}\All Age Group.png',
                                                                                                                 scale = 2)

    # Plotting (populations over years - grouped)
    os.mkdir(f'{foldername}\{country}\Per Group Plot')
    for age_group in col:
        px.line(country_df,
                x = 'Year',
                y = age_group,
                title = f'{country} Populations in Age {age_group} Over Years',
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
                                              legend = dict(font = dict(size = 14))).write_image(f'.\{foldername}\{country}\Per Group Plot\{age_group}.png',
                                                                                                 scale = 2)
