import os, re, enroll_utils
import numpy as np
import pandas as pd
from connect import auth_db, load_credentials
from sqlalchemy import create_engine

credentials = load_credentials('full-access')
db = create_engine(auth_db(credentials))

def process_enrollments(file_to_read, kind='excel'):
    
    # load the file
    if kind=='excel':
        df = pd.read_excel(file_to_read)
    elif kind=='csv':
        df = pd.read_csv(file_to_read,index_col=False)
    else:
        print('Unrecognized file type. Unable to load.')

    df = df.drop_duplicates()
    df = df.dropna(thresh=8)
    
    col_names = {col:col.casefold().replace(' ','_') for col in df.columns}
    
    df = df.rename(columns=col_names)
    df = df.rename(columns={'enterdate':'enter_date'})
    
    df['enter_date'] = pd.to_datetime(df.enter_date).dt.date
    df['first_name'] = df.first_name.apply(enroll_utils.fix_name)
    df['last_name'] = df.last_name.apply(enroll_utils.fix_name)
    df['club_name'] = df.club_name.apply(enroll_utils.fix_name)
    df['email'] = df.email.apply(enroll_utils.fix_email)
    df['email'] = df.email.replace(np.NaN, 'No Email', regex=False)
    df['home_phone'] = df.home_phone.apply(enroll_utils.fix_phone)
    df['home_phone'] = df.home_phone.replace(r'', 'No Home', regex=True)
    df['cell_phone'] = df.cell_phone.apply(enroll_utils.fix_phone)
    df['cell_phone'] = df.cell_phone.replace(r'', 'No Cell', regex=True)
    df['emp_name'] = df.emp_name.str.upper()
    return df

def main():
    
    data_path = '/home/ubuntu/path/to/enrollments'
    file_name = 'processed-daily-enrollments.xlsx'

    print('Processing:', file_name)
    df_path = os.path.join(data_path, file_name)
    data = process_enrollments(df_path, kind='excel')
    print(data.shape)
    # write to database
    try:
        data.to_sql('enrollments', con=db, if_exists='append', index=False)
        print(file_name, 'successfully written to db')
    except:
        print('error writing to database...see logs')

if __name__ == '__main__':
    main()
