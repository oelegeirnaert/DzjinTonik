import pymssql
import json
import sys



from models import *
from config import ProgramConfig

#Open Chrome - Login into DT - Check the console log for those two cookie variables:

def get_full_name(json_obj):
    return '%s %s' %(json_obj['FirstName'], json_obj['LastName'])

'''
def get_json_obj(config, url, data ):
    logger.debug('Get data from: %s with data: \n %s' %(url, data))
    r = requests.post(url, cookies = config.cookies, headers=config.headers, data=data)
    logger.debug('Data we got returnefd: \n %s' %r.text)
    if logged_in(r.text, config) and r.status_code == 200:
        return json.loads(r.text)
    return None

def post_json_obj(config, url, data):
    logger.info('Update data to url: %s with data: \n %s' %(url,data))
    r = requests.post(url, cookies=config.cookies, headers=config.headers, data=data)
    if logged_in(r.text, config) and r.status_code == 200:
        logger.debug('Data we got returned: \n %s' %r.text)
        if r.status_code == 200:
            logging.info('Updated')
            return True
        else:
            logging.error('Cannot post to url %s with data %s ... ERROR: %s' %(url, data, r.text))
            return False
'''

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise Error('Boolean value expected.')

def ask_yes_no_question(question):
    answer = input('%s (y/n) ' %question)
    if str2bool(answer):
        return True
    return False

def start_update(person_to_update, holiday_approver_id):
    json_person_to_update = get_json_obj(get_url, "id=" + str(person_to_update))
    current_holidayapprover_id = json_person_to_update['HolidayApproverId']

    if json_person_to_update is None:
        logging.error("No person found to update.")

    if json_person_to_update['HolidayApproverId'] is not None:
        json_current_holidayapprover = get_json_obj(get_url, "id=" + str(current_holidayapprover_id))

        current_holidayapprover_full_name = get_full_name(json_current_holidayapprover)
        current_person_to_update_full_name = get_full_name(json_person_to_update)

        if not ask_yes_no_question('Currently %s is the holiday approver for %s... Would you like to continue?' %(current_holidayapprover_full_name,current_person_to_update_full_name)):
            print("Cancelled")
            return None

    json_new_approver = get_json_obj(get_url, "id=" + str(holiday_approver_id))
    new_approver_full_name = get_full_name(json_new_approver)

    if not ask_yes_no_question('Are you sure you want %s as holiday approver for %s?' %(new_approver_full_name, get_full_name(json_person_to_update))):
        print("Cancelled")
        return None

    current_email_person_to_update = json_person_to_update['Email']
    logger.info("Current email: %s" %current_email_person_to_update)
    new_email_person_to_update = None
    if current_email_person_to_update is None:
        new_email_person_to_update = input("%s has no email set, thus the flow will not work correctly. Please provide his email:")
    else:
        if default_dzjintonik_user_email in current_email_person_to_update:
            new_email_person_to_update = input("This is the default email set... Please change it to: ")

    json_person_to_update['Email'] = new_email_person_to_update
    json_person_to_update['HolidayApproverId'] = holiday_approver_id

    if(post_json_obj(update_url, json_person_to_update)):
        print("Everything done!")

def load_recup_data_from_sql(config):
    result = None

    #conn = pymssql.connect(server, user, password, "tempdb")
    message = "Trying to connect to %s/%s" %(config.sql_server, config.sql_database)
    print(message)
    config.logger.debug(message)
    conn = pymssql.connect(server = config.sql_server, database = config.sql_database)
    cursor = conn.cursor(as_dict=True)

    #fields = ["DTContact.id", "recup.[JAAR]", "recup.[MAAND]", "recup.[RESID]", "recup.[NAAM]","recup.[M1_RDEF_UREN]"]

    strQry = """
    SELECT
    	distinct DTContact.id as ContactId,
    	recup.[JAAR] as Year
          ,recup.[MAAND] as Month
          ,recup.[RESID] as ResID
          ,recup.[NAAM] as Name
          ,recup.[M1_RDEF_UREN] as Balance

      FROM vmsql05.schedwin_vmma.dbo.[RECUP_6_MAAND] as Recup
       join vmsql05.schedwin_vmma.dbo.prestaties as Person on Recup.RESID = Person.resid
       join AdminApps_PLANNING_INT.lz.CONTACT as DTContact on person.bloxnummer COLLATE DATABASE_DEFAULT = DTContact.InternalCompanyNumber COLLATE DATABASE_DEFAULT
      where recup.jaar = 2019 and recup.maand = 01 and recup.naam in
      (
    'Daniel Simonya'
    )
    """

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
    conn.close()

my_config = ProgramConfig("SetRecupHours")
load_recup_data_from_sql(my_config) #working
#update_user(my_config, 5) #working
#database_test(my_config)
#print(id_generator())
#sys.exit()

#start_update(26053,155) #155 sonja de beck, 154 hayad
