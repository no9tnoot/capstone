TestSQL
=======

Creators: Peter Berens, Molly Ryan, Sian Wood
Date: 16 August 2023

Evolutionary prototype of a program that generates English questions and accompanying
mySQL queries, and checks that user-entered queries produce the expected output for a
given query.


## Prerequisites

To run this prototype, the user must meet the following requirements: 

 * Have installed the latest version of Python.
 * Have flask installed (pip install flask)
 * Have Jinja 2 installed (pip install jinja2)
 * Have mysql-connector-python installed.
 * Have the chosen database running on a SQL server.
 * Have root access to the SQL server.


## Installation

Ensure all code files are downloaded and stored in the same folder on your machine.

Create a new user in your SQL server with:
    CREATE USER 'student'@'localhost' IDENTIFIED BY 'password';
    UPDATE `mysql`.`user` SET `Select_priv` = 'Y', `Show_view_priv` = 'Y' WHERE (`Host` = 'localhost') and (`User` = 'student');
    FLUSH PRIVILEGES;

The database_details.txt file can be updated to hold the relevant details for your SQL server connection in the format:
e.g.:
'localhost'
'student'
'password'
'classicmodels2022'


## Running

Run testsql as a module from the root directory and open the web interface via the link in the terminal.
- `py -m testsql` on Windows
- `python3 -m testsql` on Unix
