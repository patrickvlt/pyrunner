import mysql.connector
import re
import sys
import os

customArgs = []
customArgs.append('--table=')

tableName = None

for customArg in customArgs:
    for sysArg in sys.argv:
        sysArg = sysArg.split('=')
        cmd = sysArg[0]
        try:
            val = sysArg[1]
        except:
            continue
        if cmd in customArg:
            if cmd == '--table':
                tableName = val

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
DB_HOST = FindString("DB_HOST",env)
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
