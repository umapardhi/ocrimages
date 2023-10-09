import pandas as pd
import hdbcli
from hdbcli import dbapi

conn = dbapi.connect(
    address='03b7ba32-1aca-46d2-b2ab-7e832d9d8881.hana.trial-us10.hanacloud.ondemand.com',
    port=443,
    user='DBADMIN',
    password='Acceron@123'
)

print('jj')
cursor = conn.cursor()

# Define the SQL INSERT statement
insert_query = "INSERT INTO your_table_name (column1, column2, ...) VALUES (?, ?, ...)"

# Prepare the data for insertion as a list of tuples
# data_to_insert = [tuple(row) for row in df.values]

# Execute the INSERT statement for all rows in the DataFrame
# cursor.executemany(insert_query, data_to_insert)

# Commit the changes to the database
conn.commit()

conn.close()