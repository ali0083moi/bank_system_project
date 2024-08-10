# bank_system_project
* This is a project to learn more about Django ORM
* The DB is on Postgres.


To run this project you have to run these commands first:
* python manage.py create_random_users 
* python manage.py create_random_accounts

The result of time of filtering 10 million accounts without index:
![The result of time of filtering 10 million accounts without index](image1.png)

The result of time of filtering 10 million accounts after indexing:
![The result of time of filtering 10 million accounts after indexing](image2.png)

As we can see the time of the query without indexing is less than the time of the query after indexing.

Created by Ali Moghadasi