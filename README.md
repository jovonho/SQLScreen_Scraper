# TMXScreen Scraper Updater
## Installation Instructions

### Copy this repo
First, copy this repository on your local machine with `git clone https://github.com/jovonho/TmxScreen_Scraper.git destination`.

### Set up PostgreSQL
Download PostgreSQL from https://www.postgresql.org/download/ and install it (help: https://www.postgresql.org/docs/13/tutorial-install.html).\
I used username `postgres`, password `postgresql12345$$` and the default port of `5432`.\
Once installed, open a command line and login to your postgres server with `psql -U <username>`.\
At the psql command line, create the database with `create database tmx encoding 'UTF8' template template0 lc_collate 'C' lc_ctype 'en_US.UTF8';`.\

### Set up Python Virtual Env
This project uses a python virtual environment.\
From the project directory, run `py -m venv .venv`. This will create a virtual environment in the `.venv` directory.\
Then, run `.venv/Scripts/activate` to activate the virtual env.\
\
The virtual env is a self-contained environment with everything needed for the program to function. This includes a python interpreter of a given version and all dependencies in their correct versions. That way, if a later version of a package were to break some old functionality, the project could still run since it specifies an older version.\

Install the requirement dependencies using `py -m pip install -r requirements.txt`.\

### Init project and launch
Check `config/db.ini` and modify it with your postgres info if necessary.\

Launch the scraper with `py launch.py -db`. This will create and fill the table with the latest quotes.\

You can also run `dbinit.py`, `scrape_symbols.py` and `getquote.py` independently from the command line.\


