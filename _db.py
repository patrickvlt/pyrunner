import mysql.connector
import re
import sys
import os

def OutputDB():
    orig_stdout = sys.stdout
    f = open('pyrunner/database.txt', 'w')
    sys.stdout = f

    tables = []
    tableColumns = []
    dbOutput = []




    # -----------------------------------------------------------
    # Retrieving data
    # -----------------------------------------------------------

    def FindString(key,content):
        regex = r""+key+"=.*"
        match = re.search(regex, content)
        match = match.group()
        match = match.replace(key+'=','')
        return match

    # Get DB credentials from .env
    f = open(('.env'), 'r')
    env = f.read()
    DB_HOST = 'mysql'
    # DB_HOST = FindString("DB_HOST",env)
    DB_PORT = FindString("DB_PORT",env)
    DB_DATABASE = FindString("DB_DATABASE",env)
    DB_USERNAME = FindString("DB_USERNAME",env)
    DB_PASSWORD = FindString("DB_PASSWORD",env)

    # Connect to server
    cnx = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD)

    # Get a cursor
    cur = cnx.cursor()

    # Get Tables
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='"+DB_DATABASE+"' ")
    results = cur.fetchall()

    print('Fetch database.')

    print(results)
    
    for result in results:
        tables.append(result[0])

    for table in tables:
        # Get Datatypes
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'"+table+"' AND TABLE_SCHEMA='"+DB_DATABASE+"'"
        cur.execute(query)
        results = cur.fetchall()
        tableColumns = []
        for result in results:
            tableColumns.append(result[0])

        print(' ')
        print('Table: '+table)
        print(' ')

        # Get Values
        query = "SELECT * FROM "+DB_DATABASE+"."+table
        cur.execute(query)
        rows = cur.fetchall()

        y = 0

        for row in rows:
            x = 0
            for value in row:
                print(str(tableColumns[x])+": "+str(value))
                x = x + 1

    # Close connection
    cnx.close()

    sys.stdout = orig_stdout
    f.close()
