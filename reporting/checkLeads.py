import os, re, pickle, datetime
import numpy as np
import pandas as pd


cols_to_show = ['FIRST_NAME', 'LAST_NAME', 
                  'Home Phone', 'Cell Phone','Email',
                  'Down Payment', 'Invoice Value',
                  'Gender','Promo Code']

def load_pickle(pickle_file):
    with open(pickle_file, 'rb') as handle:
        return pickle.load(handle)

key_path = '/home/ubuntu/path/to/keys'
location_file = 'locations.pckl'
location_dict = load_pickle(os.path.join(key_path,location_file))

promo_file = 'promos.pckl'
promos = load_pickle(os.path.join(key_path,promo_file))

def fix_emails(email):
    try:
        result = email.casefold()
    except:
        result = np.NaN
    return result

def fix_phone(phone):
    result = re.sub("[^0-9]", "", str(phone))
    return result[-10:]

def fix_clubname(name):
    try:
        return name.strip()
    except:
        return name

def parse_leads(leads):
    leads.Email = leads.Email.apply(fix_emails)
    leads.Email = leads.Email.replace(np.NaN, 'Blank', regex=False) # dev
    leads['Phone'] = leads['Phone'].apply(fix_phone)
    leads['Phone'] = leads['Phone'].replace(r'', 'No Phone', regex=True)
    return leads

def get_true_enrollments(leads, enrollments, market):
    true_enrollments = enrollments[
        (enrollments['Cell Phone'].isin(leads.Phone.values)) |
        (enrollments['Home Phone'].isin(leads.Phone.values)) |
        (enrollments['Email'].isin(leads.Email.values)) |
        (enrollments[enrollments['CLUB_NAME'].isin(location_dict[market])]['Promo Code'].isin(promos))
        ][cols_to_show]
    return true_enrollments

# option to take path as input
path_to_leads = '/home/ubuntu/path/to/data/csv/'

files = [f for f in os.listdir(path_to_leads) if f.casefold().endswith('.csv')]

lead_dict = {f[:-4] : pd.read_csv(os.path.join(path_to_leads, f)) for f in files}

# new enrollments
path_to_enrollments = '/home/ubuntu/path/to/enrollments/'
enrollmentFile = 'daily-enrollments.xlsx'
enrollments = pd.read_excel(os.path.join(path_to_enrollments,enrollmentFile))
enrollments.drop_duplicates(inplace=True)
enrollments['CLUB_NAME']=enrollments.CLUB_NAME.apply(fix_clubname)

# check data consistency (specific columns, drop unnecessary ones)
enrollments.rename(columns={'EMAIL':'Email',
                            'PAYMENT':'Down Payment',
                            'DOWN_PAYMENT':'Down Payment',
                            'CASH_PRICE':'Invoice Value'}, inplace=True)

enrollments['Email'] = enrollments.Email.apply(fix_emails)
enrollments.Email = enrollments.Email.replace(np.NaN, 'No Email', regex=False) #dev
enrollments['Cell Phone'] = enrollments['Cell Phone'].apply(fix_phone)
enrollments['Home Phone'] = enrollments['Home Phone'].apply(fix_phone)
enrollments['Cell Phone'] = enrollments['Cell Phone'].replace(r'', 'No Cell', regex=True)
enrollments['Home Phone'] = enrollments['Home Phone'].replace(r'', 'No Home', regex=True)


## append data file
today = datetime.datetime.now() - datetime.timedelta(1)
year=str(today.year)
month=str(today.month)
day=str(today.day)
date_to_write = month+'/'+day+'/'+year

## WRITE PROMO TOTALS ##
path_to_promos = '/home/ubuntu/path/to/promos'

for promo in promos:
    with open(os.path.join(path_to_promos,promo), 'a') as myfile:
        promos_sold = str(enrollments[enrollments['Promo Code']==promo].shape[0])
        newline = date_to_write + ',' + promos_sold+'\n'
        myfile.write(newline)

# File format
# Month, Date, Year, Market, Memberships, Payment, Invoice

######
path_to_result = '/home/ubuntu/path/to/sales'
with open(os.path.join(path_to_result,'daily-sales.csv'), 'a') as myfile:
    for k in lead_dict:
        tmp_df = get_true_enrollments(parse_leads(lead_dict[k]), enrollments, k)
        sold = str(tmp_df.shape[0])
        payed = str(tmp_df['Down Payment'].sum().round(2))
        invoice = str(tmp_df['Invoice Value'].sum().round(2))
        new_line=k+','+date_to_write+','+sold+','+payed+','+invoice+'\n'
        myfile.write(new_line)
