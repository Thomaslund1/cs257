#!/usr/bin/env python3
'''
    config.py
    Configuration file for database connection parameters
    This file is imported by the Flask application to connect to the PostgreSQL database
'''

# Database connection parameters
database = 'boardgames'  
user = 'poley'           # your username
password = ''            # Empty string for local development (no password)
host = 'localhost'       # Default host for local PostgreSQL server
port = 5432              # Default PostgreSQL port

# If you are using a different database, user, or password, change them here
