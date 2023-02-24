from data_prepared import exchange, interest, collective, countries
from matplotlib import pyplot as plt
from interface import ui
import pandas as pd
import seaborn as sns
import os

# Preparasi plot
name_folder = True
foldername = 'timewise_parameter'
idx_folder = 0
while name_folder:
    try:
        os.mkdir(foldername)
    except FileExistsError:
        idx_folder += 1
        foldername = f'timewise_parameter_{idx_folder}'
        name_folder = True
    else:
        name_folder = False

scan_countries = ui(countries)['countries']

# Collective parameters table
par_list = collective.Parameter.unique().tolist()
for param in par_list:
    plt.figure(figsize = (15,2), dpi = 150)
    plt.axis('off')

    param_df = collective[collective.Parameter == param]
    tab_df = param_df[param_df.Country == scan_countries[0]]
    for i_country in range(1, len(scan_countries)):
        sub_df = param_df[param_df.Country == scan_countries[i_country]]
        tab_df = pd.concat([tab_df, sub_df], ignore_index = True)

    periods_tab = tab_df.Period.dt.strftime('%Y-%m-%d').unique().tolist()
    periods_tab_display = tab_df.Period.dt.strftime('%Y-%m').unique().tolist()
    values_tab = []
    for coun_tab in scan_countries:
        value_tab = []
        for prd_tab in periods_tab:
            try:
                sub_member = tab_df[tab_df.Country == coun_tab][tab_df.Period == prd_tab].Value.item()
            except ValueError:
                value_tab.append('no data')
            else:
                value_tab.append(sub_member)
        values_tab.append(value_tab)
    
    countries_display = []
    for coun_member in scan_countries:
        countries_display.append(coun_member)

    no_data_entries = values_tab.count(['no data'] * len(periods_tab_display))
    while no_data_entries > 0:
        countries_display.remove(countries_display[values_tab.index(['no data'] * len(periods_tab_display))])
        values_tab.remove(['no data'] * len(periods_tab_display))
        no_data_entries -= 1

    if len(value_tab) != 0:
        os.mkdir(f'{foldername}\{param}')
        plt.table(cellText = values_tab, rowLabels = countries_display,
                  colLabels = periods_tab_display, loc = 'center left').scale(1,2)
        plt.savefig(f'.\{foldername}\{param}\Parameter Data Table.png')
        plt.clf()

# Filter dataframe untuk negara yang akan diplot
exchange_total = exchange[exchange.Country == scan_countries[0]]
interest_total = interest[interest.Country == scan_countries[0]]

for idx in range(1, len(scan_countries)):
    exchange_total = exchange_total.append(exchange[exchange.Country == scan_countries[idx]])
    interest_total = interest_total.append(interest[interest.Country == scan_countries[idx]])

# Plot untuk parameter exchange rate
if len(exchange_total) != 0:

    plt.figure(figsize = (20,10))
    plt.xticks(fontsize = 16, rotation = -15)
    plt.yticks(fontsize = 22)
    plt.grid(color = 'silver', linestyle = '--')

    plt.title('Exchange Rate over Periods', fontsize = 30)

    sns.barplot(x = exchange_total.Period.dt.strftime('%Y-%m'),
                y = exchange_total.OneUSD, hue = exchange_total.Country)

    plt.xlabel('Period (Year-Month)', fontsize = 22)
    plt.ylabel('National Currency per USD', fontsize = 23)

    plt.grid(color = 'silver', linestyle = '--')
    plt.legend(fontsize = 18)
    plt.savefig(f'.\{foldername}\{par_list[0]}\Collective Chart.png')
    plt.clf()

# Plot untuk parameter interest rate
interest_types = interest_total.Interest.unique().tolist()

for i_type in interest_types:
    if len(interest_total[interest_total.Interest == i_type]) != 0:

        plt.figure(figsize = (20,10))
        plt.xticks(fontsize = 16, rotation = -15)
        plt.yticks(fontsize = 22)
        plt.grid(color = 'silver', linestyle = '--')

        plt.title(f'{i_type} Rate over Periods', fontsize = 30)

        sns.barplot(x = interest_total[interest_total.Interest == i_type].Period.dt.strftime('%Y-%m'),
                    y = interest_total[interest_total.Interest == i_type].Percentage,
                    hue = interest_total[interest_total.Interest == i_type].Country)

        plt.ylim(bottom = 0)
        if interest_total[interest_total.Interest == i_type].Percentage.min() < 0:
            plt.ylim(bottom = interest_total[interest_total.Interest == i_type].Percentage.min())
        plt.xlabel('Period (Year-Month)', fontsize = 22)
        plt.ylabel('Percentage', fontsize = 23)

        plt.grid(color = 'silver', linestyle = '--')
        plt.legend(fontsize = 18)
        plt.savefig(f'.\{foldername}\{i_type}\Collective Chart.png')
        plt.clf()
