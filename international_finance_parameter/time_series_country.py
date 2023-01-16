from data_prepared import exchange, interest, collective, countries
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import seaborn as sns
import os

# Preparasi plot
name_folder = True
foldername = 'timewise_country'
idx_folder = 0
while name_folder:
    try:
        os.mkdir(foldername)
    except FileExistsError:
        idx_folder += 1
        foldername = f'timewise_country_{idx_folder}'
        name_folder = True
    else:
        name_folder = False

scan_countries = [countries[7], countries[14], countries[25]]

# Plot berdasarkan negara
for country in scan_countries:

    os.mkdir(f'{foldername}\{country}')

    plt.figure(figsize = (15,2), dpi = 150)
    plt.axis('off')

    # Collective parameters table
    periods_tab = collective[collective.Country == country].Period.dt.strftime('%Y-%m-%d').unique().tolist()
    periods_tab_display = collective[collective.Country == country].Period.dt.strftime('%Y-%m').unique().tolist()
    parameters_tab = collective[collective.Country == country].Parameter.unique().tolist()
    values_tab = []
    for par_tab in parameters_tab:
        value_tab = []
        for prd_tab in periods_tab:
            try:
                sub_member = collective[collective.Country == country][collective.Parameter == par_tab][collective.Period == prd_tab].Value.item()
            except ValueError:
                value_tab.append('no data')
            else:
                value_tab.append(sub_member)
        values_tab.append(value_tab)
    
    plt.table(cellText = values_tab, rowLabels = parameters_tab,
              colLabels = periods_tab_display, loc = 'center left').scale(1,2)
    plt.savefig(f'.\{foldername}\{country}\Parameter Data Table.png')
    plt.clf()

    # Plot untuk parameter exchange rate
    if exchange[exchange.Country == country].Country.count() != 0:
        
        sns.set()
        plt.figure(figsize = (15,10))
        plt.title(f'{country} Exchange Rate over Periods', fontsize = 28)

        sns.lineplot(data = exchange[exchange.Country == country],
                     x = 'Period', y ='OneUSD', color = 'gray', marker = 'o', markersize = 9)
        
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        plt.xticks(fontsize = 14, rotation = -20)
        plt.yticks(fontsize = 18)
        plt.xlabel('Period (Year-Month)', fontsize = 22)
        plt.ylabel('National Currency per USD', fontsize = 20)

        plt.grid(color = 'silver', linestyle = '--')
        plt.legend(fontsize = 18)
        plt.savefig(f'.\{foldername}\{country}\Exchange Rate.png')
        plt.clf()
    
    # Plot untuk parameter interest rate
    if interest[interest.Country == country].Country.count() != 0:
        
        sns.set()
        plt.figure(figsize = (15,10))
        plt.title(f'{country} Interest Rate over Periods', fontsize = 28)

        sns.lineplot(data = interest[interest.Country == country],
                     x = 'Period', y = 'Percentage', hue = 'Interest', style = 'Interest',
                     markers = "o", markersize = 9, dashes = False)
    
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        plt.xticks(fontsize = 14, rotation = -20)
        plt.yticks(fontsize = 18)
        plt.xlabel('Period (Year-Month)', fontsize = 22)
        plt.ylabel('Percentage', fontsize = 20)

        plt.grid(color = 'silver', linestyle = '--')
        plt.legend(fontsize = 18)

        plt.savefig(f'.\{foldername}\{country}\Interest Rate.png')
        plt.clf()