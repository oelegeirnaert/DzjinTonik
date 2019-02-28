import datetime
import sys
import string
import random
import copy
import requests
import sys

from models import *
from mongo_models import Freelancer, Mailing
from config import ProgramConfig
import dt_util


def get_all_persons_and_store_in_file(config, file):
    url = "%s/Person/Read" %config.domain
    print(url)
    r = requests.post(url , headers = config.headers, cookies = config.cookies, data={'pagesize':0})
    if not dt_util.logged_in(r.text, config):
        sys.exit()
    json_result = json.loads(r.text)
    f= open(file,"w+")
    f.write("ContactID;PersonID;FullName;Login\n")
    for current_json in json_result['Data']:
        current_person_id = current_json['Id']
        current_person = Person(config, current_person_id)
        if current_person.get_from_dt() == True:
            f.write("%s;%s;%s;%s\n" %(current_person.ContactId, current_person_id, current_person.FullName, current_person.Username))
    f.close()

def update_user_with_random_password(config, dzjintonik_id):
    db = config.mongodb_database
    my_config = config
    person = Person(config, dzjintonik_id)
    person.get_from_dt()
    print(person.get_full_name())
    person.set_password(random_password_generator())
    print(person.Password)

    mailing = Mailing(person.Id, person.FullName, person.Username, person.Password, person.IsActive)

    if person.send_to_dt():
        config.logger.error("Update success for user %s" %(mailing.FullName))
        mailing.update_success(True)
        db.mailing.update_one({'Id':mailing.Id}, {'$set':mailing.__dict__}, upsert=True)
    else:
        config.logger.debug("Update failed for user %s" %(person.get_full_name()))

def get_one_user(config, the_user_id):
    db = config.mongodb_database
    my_config = config
    person = Person(config=my_config, id=the_user_id)
    person.get_from_dt()
    print(person.get_full_name())

def random_password_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_freelancers_from_file(config, from_person_id, a_file):
    db = config.mongodb_database
    my_config = config
    copy_from_person = Person(config=config, id=from_person_id)
    copy_from_person.get_from_dt()

    with open(a_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for current_line in content:
        unique_password = random_password_generator()
        split = current_line.split(";")
        print(split[4])
        current_person = copy.copy(copy_from_person)
        current_person.Username = split[0]
        current_person.FirstName = split[1]
        current_person.LastName =  split[2]
        current_person.FullName = split[3]
        current_person.ContactId = split[4]
        current_person.Password = unique_password
        current_person.Id = None

        if current_person.send_to_dt():
            freelancer = Freelancer(current_person.Id, current_person.FullName, current_person.Username, unique_password, current_person.IsActive, from_person_id)
            freelancer.update_success(True)
            db.freelancer.update_one({'Id':freelancer.Id}, {'$set':freelancer.__dict__}, upsert=True)

def update_user_passwords_from_file(config, file):
    with open("TXT_FILES/password_person_id_to_update.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    for current_read_person_id_from_file in content:
        #print(current_read_person_id_from_file)
        #get_one_user(my_config, current_read_person_id_from_file)
        update_user_with_random_password(my_config, current_read_person_id_from_file)

def get_all_contacts_and_store_in_file(config, file):
    #url = "https://medialaan.dzjintonik.eu/Contact/ReadLight"
    url = "%s/Contact/ReadLight" %config.domain
    print(url)
    sys.exit()
    r = requests.post(url, headers = config.headers, cookies = config.cookies, data={'pagesize':0})
    with open(file, 'w+') as f:
        f.write(r.text)
    f.close()

my_config = ProgramConfig("CreateFreelancers")
get_all_persons_and_store_in_file(my_config, "OUTPUT_FILES/ids.txt")
#update_user_passwords_from_file(my_config, "TXT_FILES/password_person_id_to_update.txt")
#update_user(my_config, 5)
#get_one_user(my_config, 115)
#create_freelancers_from_file(my_config, 116, "TXT_FILES/freelancers_to_create.txt")
#get_all_contacts_and_store_in_file(my_config,"OUTPUT_FILES/dt_contacts.txt")
