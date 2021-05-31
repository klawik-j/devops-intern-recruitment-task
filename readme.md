## Requirements
Docker, docker-compose, internet connection\
Database naming:
1. test_db - compleate database, includes data in titles table
2. target_db - incompleate database, titles table is empty at the beginning

## How to launch
It is possible to launch script with necessary databases or connect to external database servers

### Launch only script (external databases)
1. Copy `.env.template` to `.env` and customize it to your liking. In this scenario it is necessary to provide environment configuration to two external databases. 
2. `docker-compose run script` 
3. The script will wait with execution till databases are connected. Than, it will carry on itself.

### Launch script and necassary databases
1. Copy `.env.template` to `.env`. No change is needed. Default configuration will do just fine.
2. `docker-compose up`
3. The script will wait with execution till databases are up and running. This can tak a moment, and depends on internet connection (downloading databases from github). Than, it will carry on itself.

When the job is done:

```schell
^C
docker-compose down
```

# Part 2
## 1. Measure program efficiency (execution time).
Measure program efficiency is about measure execution time of part where data query and data transfer happen. Because the rest is mostly about databases connection time, checking their structure. The time it takes is not constant and may be different every time or depend from things that can not be fully predicted like internet connection.\
The exectution time of data transfer in first verion of program (using `Script.insert_target_db_titles()`) took on average 89s.

## 2. Profile the program and point out the main problems related to efficiency.
At this point the main issue was that the `INSERT` statement was executed for ever row in titles table separately.\
Data query from test_db seems fine, because it is single query statement.

## 3. Make sure that the database table size doesn’t affect memory consumption.
Query data is handle by cursor. This way program does not store pure data, but a pointer. Table size does not affect memory consumption.

## 4. Point out efficiency issues that have been solved by you on the particular steps of code improvements and new problems appeared after improvements, if any.
The way I improved efficiency was change in data transfer part -> `Script.insert_target_db_titles_V2()`. From now on, there is less `INSERT`. I used `cursor.executemany()`, that makes `INSERT INTO table VALUES [table of values]` rather than `INSERT INTO table VALUES (single value)`. In this case "The data values given by the parameter sequences are batched using multiple-row syntax" (~ source: [mysql docs](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html)). Table size does not affect memory consumption, because there can only be fetch no more than FETCH_SIZE data.

## 5. Compare the efficiency of the implemented optimizations (for this purpose you may use execution time) and explain which improvements solved specific problems.
After improvment execution time took on average 11s for FETCH_SIZE=1000. 
When using sql database it is important to make sql commands like `FROM`, `INSERT` as little as possible. This is the main issue when it comes to execution time efficiency. But it is also crutial to manage memory consumption. The smaller FETCH_SIZE is, the less memory is used by script. 

# TESTing
The way i choosed to test the correctness of data that ended up in target_db in titles table is check sum- crc comparision. I assume that it is enought because it is exacly how they test it in readme.md in git repository of test_db.