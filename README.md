# TMXScreen Scraper Updater
## Installation Instructions

### Copy this repo
First, copy this repo locally with `git clone https://github.com/jovonho/TmxScreen_Scraper.git destination`.

### Set up PostgreSQL
Download PostgreSQL from https://www.postgresql.org/download/ and install it (https://www.postgresql.org/docs/13/tutorial-install.html).  

Once installed, open a command line and login to your postgres server with `psql -U <username>`.  

At the psql command line, create the database with `create database tmx encoding 'UTF8' template template0 lc_collate 'C' lc_ctype 'en_US.UTF8';`.  

### Set up Python Virtual Env
This project uses a python virtual environment which is a self-contained environment with everything needed for the program to function. This includes a python interpreter of a given version and all dependencies in their correct versions.  

That way, if a new version of a package was to break some functionality, the project would still work since it has the working versions in its environment.  

From the project directory, run `py -m venv .venv` to create the virtual env in the `.venv` directory.  

Then, run `.venv/Scripts/activate` to activate it. Your command prompt should change to reflect this.
  
Now, install the project dependencies using `py -m pip install -r requirements.txt`.  

### Init project and launch
Check `config/db.ini` and modify it with your info if necessary.  

Launch the scraper with `py launch.py -db`. This will create and fill the table with the latest quotes.  

You can also run `dbinit.py`, `scrape_symbols.py` and `getquote.py` independently from the command line.  


