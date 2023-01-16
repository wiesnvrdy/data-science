from data_prepared import collective
from matplotlib import pyplot as plt
import pandas as pd
import os

# Preparasi plot
name_folder = True
foldername = 'interparameter'
idx_folder = 0
while name_folder:
    try:
        os.mkdir(foldername)
    except FileExistsError:
        idx_folder += 1
        foldername = f'interparameter_{idx_folder}'
        name_folder = True
    else:
        name_folder = False

countries = collective[collective.Parameter == 'Currency Exchange'].Country.unique().tolist()
scan_countries = [countries[7], countries[13], countries[25]]

# Filter negara terpilih
for country in scan_countries:
    os.mkdir(f'{foldername}\{country}')
    country_df = collective[collective.Country == country].drop(columns = 'Country', axis = 1)

    # Ekstraksi data exchange rate untuk data universal sumbu absis
    exchange_val = pd.DataFrame(country_df[country_df.Parameter == 'Currency Exchange'])
    exchange_val.Value = exchange_val.Value.str.replace(',', '')
    exchange_val = exchange_val.Value.astype(float).tolist()

    # Ekstraksi data exchange rate dan short-term interest
    short_int_val = pd.DataFrame(country_df[country_df.Parameter == 'Short-Term Interest'])
    short_int_val.Value = short_int_val.Value.str.replace(',', '')
    short_int_val = short_int_val.Value.astype(float).tolist()
    short_int_ref = []
    for xch in exchange_val:
        short_int_ref.append(xch)
    del xch
    if len(short_int_ref) != len(short_int_val):
        delta = abs(len(short_int_ref) - len(short_int_val))
        if len(short_int_ref) > len(short_int_val):
            for i in range(delta):
                short_int_ref.pop()
        else:
            for i in range(delta):
                short_int_val.pop()
        del i
        del delta

    # Pembuatan plot exchange rate vs short-term interest
    short_int_df = pd.DataFrame({'Exchange' : short_int_ref,
                                 'Interest' : short_int_val}).sort_values('Exchange', ignore_index = True)
    if not short_int_df.empty:
        plt.figure(figsize = (15,10))
        plt.title(f"{country}'s Behavior on Short-Term Interest\nAffected by Currency Exchange Rate",
                    fontsize = 28, fontweight = 'bold')

        plt.scatter(short_int_df.Exchange, short_int_df.Interest, c = 'black', linewidths = 6)

        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 26)
        plt.xlabel('Exchange Rate', fontsize = 28)
        plt.ylabel('Percentage', fontsize = 26)

        plt.grid(color = 'gray', linestyle = '--')
        plt.savefig(f'.\{foldername}\{country}\Exchange Rate vs Short-Term Interest.png')
        plt.clf()
    
    # Analisis trendline dan R-square untuk variabel dependen => short-term interest

    # Ekstraksi data exchange rate dan immediate interest
    imm_int_val = pd.DataFrame(country_df[country_df.Parameter == 'Immediate Interest'])
    imm_int_val.Value = imm_int_val.Value.str.replace(',', '')
    imm_int_val = imm_int_val.Value.astype(float).tolist()
    imm_int_ref = []
    for xch in exchange_val:
        imm_int_ref.append(xch)
    del xch
    if len(imm_int_ref) != len(imm_int_val):
        delta = abs(len(imm_int_ref) - len(imm_int_val))
        if len(imm_int_ref) > len(imm_int_val):
            for i in range(delta):
                imm_int_ref.pop()
        else:
            for i in range(delta):
                imm_int_val.pop()
        del i
        del delta
    
    # Pembuatan plot exchange rate vs immediate interest
    imm_int_df = pd.DataFrame({'Exchange' : imm_int_ref,
                               'Interest' : imm_int_val}).sort_values('Exchange', ignore_index = True)
    if not imm_int_df.empty:
        plt.figure(figsize = (15,10))
        plt.title(f"{country}'s Behavior on Immediate Interest\nAffected by Currency Exchange Rate",
                    fontsize = 28, fontweight = 'bold')
        
        plt.scatter(imm_int_df.Exchange, imm_int_df.Interest, c = 'black', linewidths = 6)

        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 26)
        plt.xlabel('Exchange Rate', fontsize = 28)
        plt.ylabel('Percentage', fontsize = 26)

        plt.grid(color = 'gray', linestyle = '--')
        plt.savefig(f'.\{foldername}\{country}\Exchange Rate vs Immediate Interest.png')
        plt.clf()
    
    # Analisis trendline dan R-square untuk variabel dependen => immediate interest

    # Ekstraksi data exchange rate dan long-term interest
    long_int_val = pd.DataFrame(country_df[country_df.Parameter == 'Long-Term Interest'])
    long_int_val.Value = long_int_val.Value.str.replace(',', '')
    long_int_val = long_int_val.Value.astype(float).tolist()
    long_int_ref = []
    for xch in exchange_val:
        long_int_ref.append(xch)
    del xch
    if len(long_int_ref) != len(long_int_val):
        delta = abs(len(long_int_ref) - len(long_int_val))
        if len(long_int_ref) > len(long_int_val):
            for i in range(delta):
                long_int_ref.pop()
        else:
            for i in range(delta):
                long_int_val.pop()
        del i
        del delta
    
    # Pembuatan plot exchange rate vs long-term interest
    long_int_df = pd.DataFrame({'Exchange' : long_int_ref,
                                'Interest' : long_int_val}).sort_values('Exchange', ignore_index = True)
    if not long_int_df.empty:
        plt.figure(figsize = (15,10))
        plt.title(f"{country}'s Behavior on Long-Term Interest\nAffected by Currency Exchange Rate",
                    fontsize = 28, fontweight = 'bold')
        
        plt.scatter(long_int_df.Exchange, long_int_df.Interest, c = 'black', linewidths = 6)

        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 26)
        plt.xlabel('Exchange Rate', fontsize = 28)
        plt.ylabel('Percentage', fontsize = 26)

        plt.grid(color = 'gray', linestyle = '--')
        plt.savefig(f'.\{foldername}\{country}\Exchange Rate vs Long-Term Interest.png')
        plt.clf()

    # Analisis trendline dan R-square untuk variabel dependen => long-term interest