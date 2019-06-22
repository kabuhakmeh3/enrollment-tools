import os, re, datetime
import numpy as np
import pandas as pd

# define helper functions
def fix_emails(email):
    try:
        result = email.casefold()
    except:
        result = np.NaN
    return result

def fix_clubname(name):
    try:
        return name.strip().replace(' ','_').replace('/','_')
    except:
        return name

# new enrollments
path_to_enrollments = '/home/ubuntu/path/to/enrollments/'
enrollmentFile = 'daily-enrollments.xlsx'

enrollments = pd.read_excel(os.path.join(path_to_enrollments,enrollmentFile))
enrollments.drop_duplicates(inplace=True)

enrollments['CLUB_NAME']=enrollments.CLUB_NAME.apply(fix_clubname)
enrollments['EMAIL'] = enrollments.EMAIL.apply(fix_emails)

blacklist = ['none@none.com', 'noemail@gmail.com',
             'noemail@yahoo.com','none@yahoo.com',
             'na@yahoo.com','na@gmail.com']

enrollments = enrollments[~enrollments.EMAIL.isin(blacklist)]

enrollments = enrollments.dropna(subset=['EMAIL'])

# drop duplicate emails, keeping the last instance of a specific address
cols_email = ['CLUB_NAME', 'FIRST_NAME', 'LAST_NAME', 'EMAIL']
email_list = enrollments[cols_email].drop_duplicates(subset=['EMAIL'], keep='last')

# write output
path_to_master = '/home/ubuntu/path/to/mailing-lists/master'
path_to_daily = '/home/ubuntu/path/to/mailing-lists/updates'

cols_to_write = ['FIRST_NAME','LAST_NAME','EMAIL']
locations = enrollments.CLUB_NAME.unique()

for location in locations:
    f_master = os.path.join(path_to_master, location+'.csv')
    f_daily = os.path.join(path_to_daily, location+'.csv')
    
    emails_to_write = email_list[email_list.CLUB_NAME==location][cols_to_write]
    
    emails_to_write.to_csv(f_master, mode='a', header=False, index=False)
    emails_to_write.to_csv(f_daily, mode='w', header=False, index=False)
