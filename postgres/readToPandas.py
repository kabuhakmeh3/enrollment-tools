from connect import auth_db
import pandas as pd
from sqlalchemy import create_engine


# create db engine and get auth credentials
db = create_engine(auth_db())

# query contents
sql = "SELECT * FROM enrollments WHERE ENTER_DATE='2019-05-11'"

# read sql to dataframe
df = pd.read_sql(sql, db, index_col=None)

# verify result
print(df.groupby('club_name')['email'].count().sort_values(ascending=False))
