import os, datetime
import pandas as pd

path_to_data = '/home/ubuntu/path/to/sales'
data_file = 'daily-sales.csv'

month_dict = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
              7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

today = datetime.datetime.now()-datetime.timedelta(1)

try:
    data = pd.read_csv(os.path.join(path_to_data, data_file))
except:
    print('An error has occured with todays report. Please contact Admin.')

original_cols = data.columns
membership_cols = original_cols[-3:]
data['Month'] = data.Date.apply(lambda x: int(x.split('/')[0]))
data['Year'] = data.Date.apply(lambda x: int(x.split('/')[2]))
data['Day'] = data.Date.apply(lambda x: int(x.split('/')[1]))

# get data for promos
promos = ['name_of_promotion','promo','promo_3']

try: 
    enrollments = pd.read_excel(os.path.join('/home/ubuntu/path/to/enrollments/daily-enrollments.xlsx'))
except:
    print('An error has occured with todays report. Please contact Admin.')

enrollments.drop_duplicates(inplace=True)

path_to_promos = '/home/ubuntu/path/to/promos'
promo_dict = {}
for promo in promos:
    promo_df = pd.read_csv(os.path.join(path_to_promos,promo))
    promo_df['Month'] = promo_df['date'].apply(lambda x: int(x.split('/')[0]))
    promo_df['Year'] = promo_df['date'].apply(lambda x: int(x.split('/')[2]))
    promo_df['Day'] = promo_df['date'].apply(lambda x: int(x.split('/')[1]))
    promos_sold = promo_df[(promo_df.Month==today.month) & (promo_df.Year==today.year)]['sales'].sum()
    promo_dict[promo]=promos_sold

# Output (generate report)
print('Sales for {0} {1}, {2}'.format(month_dict[today.month],today.day,today.year))
print(data[(data.Month==today.month) & 
           (data.Day==today.day) &
           (data.Year==today.year)].groupby('Market')[membership_cols].sum().to_string()) 
print('\nSales for {0} {1}'.format(month_dict[today.month],today.year))
print(data[(data.Month==today.month) & (data.Year==today.year)].groupby('Market')[membership_cols].sum().to_string())
print('\nMembership Sales Totals')
print(data[(data.Month==today.month) & (data.Year==today.year)].groupby('Market')[membership_cols].sum().sum().to_string())
# promo codes
print('\nPromo Code Use Daily Totals for {0}/{1}/{2}'.format(today.month, today.day, today.year))
print(enrollments[enrollments['Promo Code'].isin(promos)]['Promo Code'].value_counts().to_string())
print('\nPromo Code Sales for {0} {1}'.format(month_dict[today.month],today.year))
print(pd.DataFrame.from_dict(promo_dict, orient='index', columns=['']).to_string())
