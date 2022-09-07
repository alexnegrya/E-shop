# About
Python e-shop with **CLI**, works on **Linux** only at the moment.

# Used concepts, patterns, ideas and technologies
Project develops particulary using basics ideas of **DDD** concept.
To keep project data using **PostgreSQL** database.
Also usings defferents **API\`s**.

# Installation
1. Install Python latest version (app is being developed at 3.10.4 version).
2. Install latest [Postgre SQL](https://www.postgresql.org/download/) version and create user and DB:
   1. Enter to psql console - `sudo -u postgres psql`
   2. Create user - `CREATE USER eshop_admin WITH PASSWORD '<your password here>';`
   3. Create DB - `CREATE DATABASE eshop OWNER eshop_admin;`
4. [Set](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/#persistent-environment-variables) created DB user password to **ESHOP_DB_PASSWORD** persistent variable.
5. Download source and unpack it to a folder convient to you.
6. From this folder execute following commands to set up app:
   1. Create virtual environment - `python3 -m venv venv`
   2. Activate environment - `source venv/bin/activate`
   3. Install requirements - `python3 -m pip install -r req.txt`
7. Done! Run `python3 app_cli.py` to start the app.

## Current version
Not ready at the moment.

## Future releases
### 1.0
1. CLI cart release
2. All code refactoring and documentation
3. Cross-platform update (add Windows and Mac OS support)
