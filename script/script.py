"""
Script to perform data transfero of titles table
from test_db to target_db

test_db repository: https://github.com/datacharmer/test_db
"""
import os
import time

import mysql.connector



target_db = mysql.connector.connect(
    host=os.environ["TARGET_DB_HOST"],
    user=os.environ["TARGET_DB_USER"],
    passwd=os.environ["TARGET_DB_PASSWORD"],
    database=os.environ["TARGET_DB_DATABASE"],
    port=os.environ["TARGET_DB_PORT"],
)

test_db = mysql.connector.connect(
    host=os.environ["TEST_DB_HOST"],
    user=os.environ["TEST_DB_USER"],
    passwd=os.environ["TEST_DB_PASSWORD"],
    database=os.environ["TEST_DB_DATABASE"],
    port=os.environ["TEST_DB_PORT"],
)

target_cursor = target_db.cursor()
test_cursor = test_db.cursor()

def check_target_db_titles_len():
    """
    check target_db titles table rows
    """
    try:
        target_cursor.execute("SELECT COUNT(*) FROM titles;")
        rows = target_cursor.fetchone()[0]
    except Exception as error:
        raise error

    return rows

def target_db_titles_empty():
    """
    check if target_db is empty
    """
    length = check_target_db_titles_len()
    if length != 0:
        raise ValueError("titles table in target_db is not empty")
    return True

def query_test_db_titles():
    """
    query titles table in test_db. Does not query data directly,
    but set pointer to right place in test_db
    """
    try:
        test_cursor.execute("SELECT * FROM titles;")
    except Exception as error:
        raise error

def insert_target_db_titles():
    """
    insert data from cursor of test_db to target_db table titles
    iterates one row at a time
    """
    for row in test_cursor:
        command = ("INSERT INTO titles(emp_no, title, from_date, to_date) \
            VALUES (%s, '%s', '%s', '%s');" % (row))
        target_cursor.execute(command)

def insert_target_db_titles_v2():
    """
    insert data from cursor of test_db to target_db table titles
    iterates FETCH_SIZE rows at a time
    """
    while True:
        rows = test_cursor.fetchmany(int(os.environ["FETCH_SIZE"]))
        target_cursor.executemany("INSERT INTO titles(emp_no, title, from_date, to_date) \
            VALUES (%s, %s, %s, %s);", rows)
        if len(rows) != int(os.environ["FETCH_SIZE"]):
            break

def commit_target_db():
    """
    save changes in target_db
    """
    target_db.commit()

def perform_data_transfer():
    """
    use query_test_db_titles() and insert_target_db_titles_V2() method
    to perform data transfer, measure its time
    """
    start = time.time()
    query_test_db_titles()
    insert_target_db_titles_v2()
    stop = time.time()
    information = f"#####\n data transfer took {stop-start} ms\n#####"
    print(information)

def test_correct_data_target_db():
    """
    perform test if data that have been transfered i correct.
    Uses check sum crc, execly how its done in readme.md of github
    repository of test_db
    """
    target_cursor.execute("DROP TABLE IF EXISTS tchecksum;")
    target_cursor.execute("CREATE TABLE tchecksum (chk char(100));")
    target_cursor.execute("SET @crc = '';")
    target_cursor.execute("INSERT INTO tchecksum \
        SELECT @crc := MD5(CONCAT_WS('#',@crc, emp_no, title, from_date,to_date)) \
        FROM titles order by emp_no,title,from_date;")
    target_cursor.execute("SELECT @crc;")

    return target_cursor.fetchone()[0]

if __name__ == "__main__":


    print("Step 1. Check if target_db titles are empty")
    result = target_db_titles_empty()
    print(result)
    print("Step 1. Finished")
    print("-------------------\n")

    print("Step 2. Query titles table data from test_db")
    perform_data_transfer()
    print("Step2. Finished")
    print("-------------------\n")

    crc = test_correct_data_target_db()
    if crc == os.environ["TITLES_CRC"]:
        print("Data transfer proved to be correct")
        commit_target_db()
    else:
        print("data transfer prooved to be incorrect")
