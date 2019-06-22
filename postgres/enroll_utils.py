# a module for various cleaning functions for enrollments

import re
import numpy as np

### Proposed changes ###
# 
# 1) import market/location dict
# 2) map location to parent market
# 3) compare against leadsheets & label sales
#
### Main module

def fix_email(email):

    blacklist = ['none@none.com', 'noemail@gmail.com',
             'noemail@yahoo.com','none@yahoo.com',
             'na@yahoo.com','na@gmail.com'] 
    try:
        email_tmp = email.casefold()
        if email_tmp in blacklist:
            result = np.NaN
        else:
            result = email_tmp
    except:
        result = np.NaN
    return result

def fix_phone(phone):
    result = re.sub("[^0-9]", "", str(phone))
    return result[-10:]

def fix_name(name):
    try:
        return name.strip()
    except:
        return name
