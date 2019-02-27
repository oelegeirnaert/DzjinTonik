import pymssql
import json
import sys

from models import *
from config import ProgramConfig

def load_recup_data_from_sql(config):
    result = None

    message = "Trying to connect to %s/%s" %(config.sql_server, config.sql_database)
    print(message)
    config.logger.debug(message)
    conn = pymssql.connect(server = config.sql_server, database = config.sql_database)
    cursor = conn.cursor(as_dict=True)

    sql_file = "QUERIES/recup_hours.sql"
    strQry = None
    try:
        with open(sql_file, 'r') as myfile:
            strQry=myfile.read().replace('\n', '')
    except Exception as e:
        print("Sorry, I cannot read your SQL file: %s!" %sql_file)
        return None


    if strQry is not None:
        cursor.execute(strQry)
        row = cursor.fetchone()
        while row:
            print(row)
            if row is not None:
                pbg = PlanBalanceGrid(config, row, True)
                result = pbg.send_to_dt()
                if result is not None:
                    print(result)
            row = cursor.fetchone()
    else:
        print("Sorry, i cannot read your sql file!")
    conn.close()

my_config = ProgramConfig("SetRecupHours")
load_recup_data_from_sql(my_config)
