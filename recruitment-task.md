## Part 1
1. Import dump from https://github.com/datacharmer/test_db to the MySQL database.
2. Create a second database with the same data structure, but without data in the “titles” table (other tables may contain data, at least those which are required due to foreign keys constraints in the “titles” table).
3. Write a simple program in Python or Golang, which can connect to two different databases (keeping in mind that they may be placed on different servers) and which copies all the data from the “titles” table to the other database
4. Write a unit test to see if the script performs as it should.
5. Create documentation in a readme.txt file. The file should contain instructions for setting up an environment and running the program (this is important from the perspective of a person who will be verifying the solution).

## Part 2
1. Measure program efficiency (execution time).
2. Profile the program and point out the main problems related to efficiency.
3. Make sure that the database table size doesn’t affect memory consumption
4. Point out efficiency issues that have been solved by you on the particular steps of code improvements and new problems appeared after improvements, if any.
5. Compare the efficiency of the implemented optimizations (for this purpose you may use execution time) and explain which improvements solved specific problems.

You have 7 days to complete the task.
The final product should be the archive file with source code and unit tests, readme.txt and description of the implemented improvements.
Comments and description should be written in English.
Please send the completed task to ---------
Please use the following module when handling communication between databases:
- python - https://pypi.org/project/mysql-connector-python/
- golang - https://github.com/go-sql-driver/mysql/

## Evaulation
- Code legibility and compatibility with standards.
- Script execution time and resource usage.
- Legibility of the final solution and a description of how you got to it (part 2, point 4 and 5).
