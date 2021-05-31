import os
import time

import mysql.connector

target_db = mysql.connector.connect(
    host=os.environ["TEST_DB_HOST"],
    user=os.environ["TEST_DB_USER"],
    passwd=os.environ["TEST_DB_PASSWORD"],
    database=os.environ["TEST_DB_DATABASE"],
    port=os.environ["TEST_DB_PORT"],
)

target_cursor = target_db.cursor()

set_variable_crc = "SET @crc = '';"
calculate_crc = "SELECT @crc := MD5(CONCAT_WS('#',@crc, emp_no, title, from_date,to_date)) FROM titles order by emp_no,title,from_date;"
query_crc = "SELECT @crc;"

target_cursor.excecute(set_variable_crc)
target_cursor.excecute(calculate_crc)
target_cursor.excecute(query_crc)

crc = target_cursor.fetchone()
print(crc)
print(crc == os.environ[])