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
path_to_enrollments = '/home/ubuntu/path/to/cancel/'
enrollmentFile = 'weekly-cancellations.xlsx'

enrollments = pd.read_excel(os.path.join(path_to_enrollments,enrollmentFile))
enrollments.drop_duplicates(inplace=True)

enrollments['Email'] = enrollments.Email.apply(fix_emails)

blacklist = ['none@none.com', 'noemail@gmail.com']
enrollments = enrollments[~enrollments.Email.isin(blacklist)]

enrollments = enrollments.dropna(subset=['Email'])

# drop duplicate emails, keeping the last instance of a specific address
cols_email = ['First Name', 'Last Name', 'Email']
email_list = enrollments[cols_email].drop_duplicates(subset=['Email'], keep='last')

# write output
path_to_master = '/home/ubuntu/path/to/mailing-lists/master'
path_to_daily = '/home/ubuntu/path/to/mailing-lists/updates'

cancelFile = 'Cancelled_Memberships.csv' 

f_master = os.path.join(path_to_master, cancelFile)
f_daily = os.path.join(path_to_daily, cancelFile)

email_list[cols_email].to_csv(f_master, mode='a', header=False, index=False)
email_list[cols_email].to_csv(f_daily, mode='w', header=False, index=False)
