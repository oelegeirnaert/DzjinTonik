import configparser
import logging
import time

from pymongo import MongoClient

class ProgramConfig(object):
    def __init__(self, logfileName):

        today = time.strftime("%Y-%m-%d")
        log_filename = "Logs/%s-%s.log" %(logfileName, today)
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        #print(config.sections())

        #FIRST OF ALL, GET ENVIRONMENT
        self.environment = self.config['DZJINTONIK'].get('environment', 'test')

        #MongoDB
        self.mongodb_server = self.config['MONGODB'].get('server', 'localhost')
        self.mongodb_port = self.config['MONGODB'].getint('port', 27017)
        self.mongodb_client = MongoClient(self.mongodb_server, self.mongodb_port)
        self.mongodb_database = None

        #SQL
        self.sql_server = self.config['SQL'].get('server', 'sqldwprtest')
        self.sql_database = self.config['SQL'].get('database', 'AdminApps_PLANNING_INT')

        #DzjinTonik - https://dzjintonik.eu/
        self.asp_session = self.config['DZJINTONIK'].get('asp_session', None)
        self.request_token =  self.config['DZJINTONIK'].get('request_token', 'test')
        self.chrome_path = self.config['DZJINTONIK'].get('chrome_path', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe')
        self.default_dzjintonik_user_email = self.config['DZJINTONIK'].get('default_dzjintonik_user_email', 'dzjintonik@medialaan.be')
        self.internal_company_id = self.config['DZJINTONIK'].get('internal_company_id', 'test')
        self.program_id = self.config['DZJINTONIK'].get('program_id', 'test')
        self.master_program_id  = self.config['DZJINTONIK'].get('master_program_id', 'test')
        self.domain = ''



        if self.continue_in_environment() == False:
            sys.exit()

        self.set_env_specific_values()
        self.headers = {'Accept': 'application/json','Content-Type': 'application/x-www-form-urlencoded'}
        self.cookies = {'InternalCompanyId': '1', 'ASP.NET_SessionId': self.asp_session, '__RequestVerificationToken': self.request_token, 'ProgramId':''}
        self.contact_get = self.domain + '/Contact/Get'
        self.contact_update = self.domain + '/Contact/Update'
        self.person_get = self.domain + '/Person/Get'
        self.person_update = self.domain + '/Person/Update'
        self.set_recup_hours = self.domain + '/PercentageReportPlanBalance/Create'
        
    def set_env_specific_values(self):
        the_env = self.environment.upper()
        if the_env == 'TEST':
            dt_domain = self.config['DZJINTONIK'].get('test_domain')
            my_mongodb = self.mongodb_client.dbDzjinTonikTEST
        elif the_env == 'UAT':
            dt_domain = self.config['DZJINTONIK'].get('uat_domain')
            my_mongodb = self.mongodb_client.dbDzjinTonikUAT
        elif the_env == 'PROD':
            dt_domain = self.config['DZJINTONIK'].get('prod_domain')
            my_mongodb = self.mongodb_client.dbDzjinTonikPROD
        else:
            print("No valid environment")
            sys.exit()

        print("THE DOMAIN WILL BE: %s" %dt_domain)
        self.domain = dt_domain
        self.mongodb_database = my_mongodb

    def continue_in_environment(self):

        if self.environment is None:
            print("Please set an environment...")
            system.exit()

        self.environment = self.environment.upper()

        if 'PROD' in self.environment.upper():
            print("YOU ARE WORKING IN PRODUCTION ENVIRONMENT!")
            answer = ask_yes_no_question("Are you sure you'd like to continue in PRODUCTION?")
            if not answer:
                print("Stopping actions!")
                sys.exit()
        else:
            print("YOU ARE WORKING IN %s, WHICH IS NICE!" %self.environment)
