import pandas as pd

# Ekstraksi data csv dan pembersihan data
src = pd.read_csv('exchange_interest.csv')

columns = src.columns.tolist()
for column in columns:
    if src[column].count().item() == 0:
        src.drop(column, axis = 1, inplace = True)
src.drop(['SUBJECT', 'LOCATION', 'FREQUENCY', 'Frequency', 'Time', 'PowerCode Code', 'PowerCode', 'Unit Code'],
            axis = 1, inplace = True)
src.rename(columns = {'TIME' : 'Period'}, inplace = True)
src.drop(src[src.Country == 'Euro area (19 countries)'].index, inplace = True)
src.Country.mask(src.Country == 'China (People\'s Republic of)', 'China', inplace = True)

# Membagi data untuk parameter exchange rate dan interest percent
src_dict = {}
units = src.Unit.unique().tolist()
for unit in units:
    if unit == 'Percentage':
        src_dict.update({'interest' : src[src.Unit == unit]})
    else:
        src_dict.update({'exchange' : src[src.Unit == unit]})

src_exchange = pd.DataFrame(src_dict['exchange'])
src_exchange.drop('Subject', axis = 1, inplace = True)

src_interest = pd.DataFrame(src_dict['interest'])
src_interest.Subject.mask(src_interest.Subject == 'Long-term interest rates, Per cent per annum', 'Long-Term Interest', inplace = True)
src_interest.Subject.mask(src_interest.Subject == 'Short-term interest rates, Per cent per annum', 'Short-Term Interest', inplace = True)
src_interest.Subject.mask(src_interest.Subject == 'Immediate interest rates, Call Money, Interbank Rate, Per cent per annum', 'Immediate Interest', inplace = True)

exchange = pd.DataFrame({'Country' : src_exchange.Country,
                         'Period' : pd.to_datetime(src_exchange.Period),
                         'OneUSD' : src_exchange.Value})

interest = pd.DataFrame({'Country' : src_interest.Country,
                         'Interest' : src_interest.Subject,
                         'Period' : pd.to_datetime(src_interest.Period),
                         'Percentage' : src_interest.Value})

# Menyatukan dan reformatting dataframe menjadi dataframe kolektif untuk sajian tabel
par = []
for i in range(exchange.Country.count().item()):
    par.append('Currency Exchange')

comp_exch = exchange.rename(columns = {'OneUSD' : 'Value'})
comp_exch.insert(1, 'Parameter', par)
comp_intr = interest.rename(columns = {'Interest' : 'Parameter',
                                       'Percentage' : 'Value'})
collective = pd.concat([comp_exch, comp_intr], ignore_index = True)
collective.Value = collective.Value.apply('{:,}'.format)

# List untuk nama negara yang akan dipantau
countries = src.Country.unique().tolist()
