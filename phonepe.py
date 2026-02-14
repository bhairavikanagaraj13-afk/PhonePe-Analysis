import psycopg2
import pandas as pd
conn=psycopg2.connect(
dbname="postgres",
user="postgres",
password="B130899",
host="localhost"
)
conn.autocommit=True
cursor=conn.cursor()
try:
    cursor.execute("CREATE DATABASE phonepe_db")
except psycopg2.errors.DuplicateDatabase:
    pass
cursor.close()
conn.close()

conn = psycopg2.connect(
    dbname="phonepe_db",
    user="postgres",
    password="B130899",
    host="localhost"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Agg_Transaction(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               Transaction_type TEXT,
               Transaction_count BIGINT,
               Transaction_amount DOUBLE PRECISION
               )"""

)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Agg_User(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               User_Brand TEXT,
               User_count BIGINT,
               Device_perc DOUBLE PRECISION)
"""
)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Agg_Insurance(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               Ins_Name TEXT,
               Ins_count BIGINT,
               Ins_amount DOUBLE PRECISION)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Map_Transaction(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               District_name_T TEXT,
               DIS_T_count BIGINT,
               DIS_T_amount DOUBLE PRECISION)
"""
)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Map_User(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               User_district TEXT,
               registered_users BIGINT,
               Appopens_U BIGINT)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Map_Insurance(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               Ins_Dis_name_M TEXT,
               Ins_count_M BIGINT,
               Ins_amount_M DOUBLE PRECISION)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Top_Transaction(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               Level_top_T TEXT,
               Entity_name_top_T TEXT,
               top_count_T BIGINT,
               top_amount_T DOUBLE PRECISION
            )
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Top_User(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               Level_top_U TEXT,
               Entity_name_top_U TEXT,
               registered_Users BIGINT
               )
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Top_Insurance(
               ID SERIAL PRIMARY KEY,
               STATE VARCHAR(50),
               YEAR INT,
               QUARTER INT,
               Level_top_I TEXT,
               Entity_name_top_I TEXT,
               top_count_I BIGINT,
               top_amount_I DOUBLE PRECISION)
""")

conn.commit()

from io import StringIO
try:
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Agg_Transaction.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Agg_Transaction
     (state, year, quarter, transaction_type,
     transaction_count, transaction_amount)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Aggregated_User.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Agg_User
     (state, year, quarter, User_Brand,
     User_count, Device_perc)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Aggregated_Insurance.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Agg_Insurance
     (state, year, quarter, Ins_Name,
     Ins_count, Ins_amount)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Map_transaction.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Map_Transaction
     (state, year, quarter, District_name_T,
     DIS_T_count, DIS_T_amount)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Map_user.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Map_User
     (state, year, quarter, User_district,
     registered_users, Appopens_U)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Map_Insurance.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Map_Insurance
     (state, year, quarter, Ins_Dis_name_M,
     Ins_count_M, Ins_amount_M)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Top_Transaction.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Top_Transaction
     (state, year, quarter, Level_top_T,
     Entity_name_top_T, top_count_T,top_amount_T)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Top_user.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Top_User
     (state, year, quarter, Level_top_U,
     Entity_name_top_U, registered_Users)
     FROM STDIN WITH CSV
     """,
     buf
     )
     df = pd.read_csv(r"C:\Users\Bhairavi\OneDrive\DataScience\Top_insurance.csv")
     buf = StringIO()
     df.to_csv(buf, index=False, header=False)
     buf.seek(0)
     cursor.copy_expert(
       """
     COPY Top_Insurance
     (state, year, quarter, Level_top_I,
     Entity_name_top_I, top_count_I,top_amount_I)
     FROM STDIN WITH CSV
     """,
     buf
     )
         
     conn.commit()
except Exception as e:
     conn.rollback()
     print("Rollback error",e)
    

