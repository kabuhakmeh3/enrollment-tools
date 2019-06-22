import os
import pandas as pd

path_to_leads = '/home/ubuntu/path/to/xlsx/'

files = [f for f in os.listdir(path_to_leads) if f.casefold().endswith('.xlsx')]

def loadSheets(excelFile):
    f = pd.ExcelFile(excelFile)
    df = pd.concat([f.parse(sheet) for sheet in f.sheet_names])
    return df.drop_duplicates()

for f in files:
    loadSheets(os.path.join(path_to_leads, f)).to_csv(f[:-5]+'.csv', sep=',', index=False)
