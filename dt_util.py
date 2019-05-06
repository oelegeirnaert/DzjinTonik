import webbrowser
import sys
import pymssql
import datetime

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise Error('Boolean value expected.')

def ask_yes_no_question(question):
    answer = input('%s (y/n) ' %question)
    return str2bool(answer)
    
def check_if_json(str):
    if "<html>" in str:
        print(str)
        return False
    if "<title>" in str:
        print(str)
        return False
    return True

def logged_in(response, a_config):
    a_config.logger.info("Checking if you're logged into DT.")
    if "<title>DT - Login</title>" in response:
        strMessage = "You need to login into DzjinTonik first... Be sure to set the correct variables on top of this file!"
        print(strMessage)
        a_config.logger.error(strMessage)
        webbrowser.open(a_config.domain)
        sys.exit()
        return False
    elif "<title>" in response:
        print(response)
        print("An other error occured... Please read the lines above! SUGGESTION: Is your model correct? Are you sending an ID?")
        return False
    elif "<html>" in response:
        print(response)
        print("Your output is html, which is not nice!")
        return False
    return True

def get_sql_list_from_file(config, sql_file):
        conn = pymssql.connect(server = config.sql_server, database = config.sql_database)
        cursor = conn.cursor(as_dict=True)

        message = "Trying to connect to %s/%s" %(config.sql_server, config.sql_database)
        print(message)

        strQry = None

        try:
            with open(sql_file, 'r') as myfile:
                strQry = myfile.read().replace('\n', '')
        except Exception as e:
            print("Sorry, I cannot read your SQL file: %s!" %file)

        print(strQry)

        if strQry is not None:
            cursor.execute(strQry)
            return cursor.fetchall()

        return None

def get_date_from_string(datestring):
    if datestring is not None:
        return datetime.datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S')
    return datestring
