import datetime
import sys
import string
import random
import copy
import requests
import sys
import pymssql

from models import *
from api_models import *
from models_mongo import Freelancer, Mailing, ContactApprover, MongoHRGroup
from config import ProgramConfig
import dt_util
from datetime import timedelta

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
    return person

def random_password_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_freelancers_from_file(config, from_person_id, a_file):
    db = config.mongodb_database
    my_config = config
    copy_from_person = Person(config=config, id=from_person_id)
    copy_from_person.get_from_dt()

    content = get_list_from_file(a_file, separator = ";")

    for current_line in content:
        unique_password = random_password_generator()
        print(current_line[3])
        current_person = copy.copy(copy_from_person)
        current_person.Username = current_line[0]
        current_person.FirstName = current_line[1]
        current_person.LastName =  current_line[2]
        current_person.FullName = current_line[3]
        current_person.ContactId = current_line[4]
        current_person.Password = unique_password
        current_person.Id = None

        if current_person.send_to_dt():
            freelancer = Freelancer(current_person.Id, current_person.FullName, current_person.Username, unique_password, current_person.IsActive, from_person_id)
            freelancer.update_success(True)
            db.freelancer.update_one({'Id':freelancer.Id}, {'$set':freelancer.__dict__}, upsert=True)

def update_user_passwords_from_file(config, file):
    with open(file) as f:
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

def get_all_holiday_approvers(config, file):
    url = "%s/Contact/ReadLight" %config.domain
    r = requests.post(url, headers = config.headers, cookies = config.cookies, data={'pagesize':0})
    if not dt_util.logged_in(r.text, config):
        print("You're not loggedin")
        sys.exit()
    json_list = json.loads(r.text)
    print(r.text)
    with open(file, 'w+') as f:
        for item in json_list['Data']:
            current_contact = Contact(config, Id=item['Id'])
            current_contact.get_from_dt()
            current_contact_name = current_contact.get_full_name()

            current_approver_name = "has no approver"
            current_approver_id = None
            if current_contact.HolidayApproverId is not None:
                current_approver = Contact(config, Id=current_contact.HolidayApproverId)
                current_approver.get_from_dt()
                current_approver_name = current_approver.get_full_name()
                current_approver_id = current_contact.HolidayApproverId

            f.write("%s;%s;%s;%s;%s;\n" %(current_contact.Id, current_contact_name, current_contact.ContactType, current_approver_id, current_approver_name ))
            #sys.exit()
    f.close()

def update_contacts_with_approver_from_file(config, file):
    db = config.mongodb_database
    content = get_list_from_file(file, separator=";")

    for current_item in content:
        current_contact = Contact(config, Id=current_item[0])
        current_contact.get_from_dt()
        current_contact.HolidayApproverId = current_item[1]
        print(current_contact.HolidayApproverId)
        if current_contact.send_to_dt():
            #Id, FullName, DepartmentGroup, Department, ApproverID, ApproverFullName
            ca = ContactApprover(current_contact.Id, current_contact.get_full_name(), current_item[2], current_item[3], current_contact.HolidayApproverId, current_item[4])
            ca.update_success(True)
            db.contactapprover.update_one({'Id':ca.Id}, {'$set':ca.__dict__}, upsert=True)
        #sys.exit()

def get_list_from_file(file, separator = None):
    my_list_to_return = []

    with open(file) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    if separator is not None:
        print("Your lines will be separated with a: '%s'" %separator)
        for current_line in content:
            my_new_list = current_line.split(separator)
            my_list_to_return.append(my_new_list)
    else:
        my_list_to_return = content[:]

    return my_list_to_return


def SetHRGroupsForContactsFromFile(config, file):
    url = config.domain + '/ContactPlanningGroup/Read'
    db = config.mongodb_database
    print("Set HR Groups")


    content = get_list_from_file(file, separator=";")

    for current_item in content:
        current_mongo_hr_group = MongoHRGroup(current_item)
        current_hr_group = HRGroup(config)
        current_hr_group.From = "01/01/2017 00:00:00"
        current_hr_group.ContactId = current_mongo_hr_group.ContactId
        #current_hr_group.ContactId = current_item[0]

        r = requests.post(url , headers = config.headers, cookies = config.cookies, data={'ContactId':current_mongo_hr_group.ContactId, 'GroupType':4})
        #r = requests.post(url , headers = config.headers, cookies = config.cookies, data={'ContactId':current_item[0], 'GroupType':4})
        if not dt_util.logged_in(r.text, config):
            sys.exit()

        items = json.loads(r.text)['Data']
        if len(items) > 0:
            db.hr_groups_back_up.insert_many(items)

        for item in items:
            hrg=HRGroup(config, id=None)
            hrg.__dict__ = item
            hrg.config=config
            hrg.delete_from_dt()
            print(hrg)
            current_mongo_hr_group.FullName = hrg.ContactFullName

        if current_mongo_hr_group.Is_Journalist == "1":
            current_hr_group.Id = None
            current_hr_group.GroupId=2
            current_hr_group.send_to_dt()

        if current_mongo_hr_group.Is_TV == "1":
            current_hr_group.Id = None
            current_hr_group.GroupId=5
            current_hr_group.send_to_dt()

        if current_mongo_hr_group.Is_Radio == "1":
            current_hr_group.Id = None
            current_hr_group.GroupId = 3
            current_hr_group.send_to_dt()

        if current_mongo_hr_group.Book_Payroll == "1":
            current_hr_group.Id = None
            current_hr_group.GroupId = 7
            current_hr_group.send_to_dt()

        if current_mongo_hr_group.Book_Only_Holidays == "1":
            current_hr_group.Id = None
            current_hr_group.GroupId = 9
            current_hr_group.send_to_dt()

        if current_mongo_hr_group.Explicit_Supplements == "1":
            current_hr_group.Id = None
            current_hr_group.GroupId = 11
            current_hr_group.send_to_dt()

        if current_mongo_hr_group.Apply_10_Percent == "0":
            current_hr_group.Id = None
            current_hr_group.GroupId = 8
            current_hr_group.send_to_dt()


        # if current_mongo_hr_group.ContactId == "100":
        #     sys.exit()

        print(current_mongo_hr_group.ContactId)
        current_mongo_hr_group.config=None
        db.hr_groups.update_one({'ContactId':current_mongo_hr_group.ContactId}, {'$set':current_mongo_hr_group.__dict__}, upsert=True)

        #sys.exit()

def SetCompanyFromFile(config, sql_file):
    db = config.mongodb_database
    result = None

    cursor = dt_util.get_sql_list_from_file(config, sql_file)

    if cursor is not None:
        for row in cursor:
            print(row)
            c = Contact(config, Id=row['Id'])
            c.get_from_dt();

            comp = row['FRM']
            if comp=="409000": #De Persgroep Publishing
                c.DefaultInternalCompanyId = 2
                c.CompanyId = 40
            if comp=="409100": #Medialaan NV
                c.DefaultInternalCompanyId = 1
                c.CompanyId = 1
            if comp=="409200": #Unleashed
                c.DefaultInternalCompanyId = 3
                c.CompanyId = 41
            if comp=="409300": #JOE FM
                c.DefaultInternalCompanyId = 4
                c.CompanyId = 42
            if comp=="409400": #De Persgroep
                c.DefaultInternalCompanyId = 5
                c.CompanyId = 43
            if comp=="409500": #Morfeus
                c.DefaultInternalCompanyId = 6
                c.CompanyId = 44

            c.InternalCompanyNumber = row['WKNNEW']

            c.send_to_dt()

def Delete_Old_BloxNumbers(config, sql_file):
    answer = dt_util.ask_yes_no_question("Before doing this action, have you updated all the old blox numbers to the new dots numbers?")
    if not answer:
        print("Action cancelled!")
        sys.exit()

    cursor = dt_util.get_sql_list_from_file(config, sql_file)
    print(cursor)
    if cursor is not None:
        for row in cursor:
            print(row)
            c = Contact(config, Id=row['Id'])
            c.get_from_dt()
            c.InternalCompanyNumber = ''
            c.send_to_dt()

def SetExecutivesFromFile(config, input_file):
    my_list = get_list_from_file(input_file, separator = ";")
    url = config.domain + '/Nominal/Read'
    for current_item in my_list:

        r = requests.post(url , headers = config.headers, cookies = config.cookies, data={'ContactId':current_item[0]})
        current_item_is_executive = False
        if current_item[1] == "1":
            current_item_is_executive = True

        if not dt_util.logged_in(r, config):
            sys.exit()

        print(r.text)
        items = json.loads(r.text)['Data']

        for item in items:
            print(item)
            nominal = Nominal(config)
            nominal.__dict__ = item
            nominal.config = config

            print("Is executive in Dt %s" %nominal.IsExecutive)
            print("Is executive in file: %s" %current_item_is_executive)

            nominal_is_active = False

            frm = None
            if nominal.DateFrom is not None:
                frm = datetime.datetime.strptime(nominal.DateFrom, '%Y-%m-%dT%H:%M:%S')

            to = None
            if nominal.DateTo is not None:
                to = datetime.datetime.strptime(nominal.DateTo, '%Y-%m-%dT%H:%M:%S')

            if to is not None:
                if frm < datetime.datetime.now() < to:
                    nominal_is_active = True
            else:
                if frm < datetime.datetime.now():
                    nominal_is_active = True

            if not nominal_is_active:
                print("Nominal is not longer valid... From: %s to %s" %(frm, to))
            else:
                need_to_change = (nominal.IsExecutive != current_item_is_executive)
                if need_to_change is True:
                    print("Needs to be updated.")
                    nominal.IsExecutive = current_item_is_executive
                    nominal.send_to_dt()
                else:
                    print("No need to update.")
                    continue

def update_user_password_from_departement_group_via_sql(config, sqlfile, file):
    db = config.mongodb_database
    already_reset = get_list_from_file(file, separator = None)
    contacts_to_reset = dt_util.get_sql_list_from_file(config, sqlfile)
    contactids_to_reset = []
    for row in contacts_to_reset:
        contactids_to_reset.append(row['CONTACTID'])
    print(contactids_to_reset)

    my_get_person_list_endpoint = "%s/%s" %(config.domain, "Person/Read")
    r = requests.post(my_get_person_list_endpoint, headers=config.headers, cookies=config.cookies)
    json_result = json.loads(r.text)

    for current_person_item in json_result['Data']:
        current_person = Person(config=config, id=None)
        current_person.__dict__ = current_person_item
        current_person.config = config

        if not current_person.ContactId in contactids_to_reset:
            config.logger.info("No need to update %s because no nieuwsdienst." %current_person)
            continue

        if str(current_person.ContactId) in already_reset:
            config.logger.info("We already did a password reset for %s." %current_person)
            continue

        config.logger.info("Reset password for %s" %current_person)
        current_person.Password = random_password_generator(size=6)

        mailing = Mailing(current_person.Id, current_person.FullName, current_person.Username, current_person.Password, current_person.IsActive)
        if current_person.send_to_dt():
            config.logger.error("Update success for user %s" %(mailing.FullName))
            mailing.update_success(True)
            db.mailing2.update_one({'Id':mailing.Id}, {'$set':mailing.__dict__}, upsert=True)

def SetExecutivesFromFileViaAPI(config, file):
    my_list = get_list_from_file(file, separator=None)

    print(my_list)
    my_nominal_endpoint = ("%s%s" %(config.api_domain, "nominal"))
    my_get_nominal_list_endpoint = "%s%s" %(my_nominal_endpoint, "?pagesize=1")
    print(my_nominal_endpoint)

    print(config.api_authorization)

    headers = {
        'Accept': "application/json",
        'Authorization': config.api_authorization
        }

    response = requests.get(my_get_nominal_list_endpoint, headers=headers)
    #print(response.text)
    json_result = json.loads(response.text)
    executive_counter = 0
    non_executive_counter = 0
    current_api_model = Api_Nominal()
    contact_ids_updated = []
    contact_ids_failed_update = []
    answer = dt_util.ask_yes_no_question("We have found %s nominals.... Wanna see an overview (If Yes, changes wouldn't be send to dt)?" %len(json_result['PageItems']))

    for item in json_result['PageItems']:
        #print(item)
        set_as_executive = False
        nominal_is_active = False
        current_api_model.__dict__ = item
        current_api_model.DateTo = dt_util.get_date_from_string(current_api_model.DateTo)
        current_api_model.DateFrom = dt_util.get_date_from_string(current_api_model.DateFrom)

        if str(current_api_model.ContactId) in my_list:
            set_as_executive = True

        if current_api_model.DateTo is None:
            print("No end date-thus active")
            nominal_is_active = True
        else:
            print("Has end-date - check if still valid")
            if current_api_model.DateTo > datetime.datetime.now():
                print("Yes, nominal is still valid till %s" %current_api_model.DateTo)
                nominal_is_active = True
            else:
                print("No, nominal is not valid  anymore, it was till %s" %current_api_model.DateTo)
                nominal_is_active = False

        if nominal_is_active:

            if current_api_model.IsExecutive:
                executive_counter +=1
            else:
                non_executive_counter +=1

        if answer:
            continue


            if set_as_executive != current_api_model.IsExecutive:
                print("Values are different, so update it...")
                current_api_model.IsExecutive = set_as_executive
                print("Send update to contactid: %s with executive flag as %s" %(current_api_model.ContactId, set_as_executive))
                update_end_point = "%s/%s" %(my_nominal_endpoint, current_api_model.Id)
                r = requests.put(update_end_point, headers=headers, data=current_api_model.__dict__)
                if r.status_code == 200:
                    contact_ids_updated.append(current_api_model.ContactId)
                    config.logger.info("%s update success" %current_api_model.ContactId)
                else:
                    contact_ids_failed_update.append(current_api_model.ContactId)
                    config.logger.error("%s update fail" %current_api_model.ContactId)
            else:
                config.logger.info("Values are the same for contact id %s: %s - %s" %(current_api_model.ContactId, set_as_executive, current_api_model.IsExecutive))

    config.logger.info("We have found %s difference and have updated them..." %len(contact_ids_updated))
    config.logger.info(contact_ids_updated)
    print(contact_ids_updated)
    config.logger.info("Number of executives set in dt: %s" %executive_counter)
    config.logger.info("Number of non-executives set in dt: %s" %non_executive_counter)
    sys.exit()



        #sys.exit()

def UpdateShifts(config = None, file = None, minutes_to_add=None):
    my_list = get_list_from_file(file, separator = ";")
    for item in my_list:
        current_booking_id = item[0]
        cv = CategoryValue(config, current_booking_id)
        cv.get_from_dt()
        print(type(cv.ActualWorkingTime))
        if(cv.ActualWorkingTime == 7.5):
            print("OK, 7.5 working time - update_shift!")
            print(cv.ActualEnd)
            new_end_datetime = datetime.datetime.strptime(cv.ActualEnd, "%Y-%m-%dT%H:%M:%S")
            new_end_datetime = new_end_datetime+ timedelta(minutes=minutes_to_add)
            cv.ActualEnd = new_end_datetime
            print(new_end_datetime)
            cv.send_to_dt()
        else:
            print("NOK, no 7.5 working time - Do nothing")

        #sys.exit()

def update_shift_with_planningdepartementgroup(config = None, sqlfile = None):
    my_list = dt_util.get_sql_list_from_file(config, sqlfile)
    api_end_point = "%s%s" %(config.api_domain, "planningitem")
    my_headers = {'Authorization': config.api_authorization}
    current_pi = Api_PlanningItem()
    for id in my_list:

        my_params = {'id': id['id']}
        pdgid = id['pdgid']
        r = requests.get(api_end_point, headers = my_headers, params=my_params)
        current_pi.__dict__ = json.loads(r.text)
        print(current_pi.__dict__)
        current_pi.Visibility = 1
        current_pi.PlanningDepartmentGroupId = pdgid
        print(current_pi.__dict__)
        #sys.exit()
        postback_end_point = "%s/%s" %(api_end_point, current_pi.Id)
        print(postback_end_point)
        #sys.exit()
        postback = requests.put(postback_end_point, data=current_pi.__dict__, headers= my_headers)
        if postback.status_code == 200:
            print("Updated")
        else:
            print("ERROR")
            print(postback.text)

        #sys.exit()
        #r = requests.post(api_end_point, data=current_pi.__dict__, params = my_params)






#my_config = ProgramConfig("SetHrGroup_WithTV")
#x = get_list_from_file("INPUT_FILES/contacts_with_approver.txt", separator=";")
#for i in x:
    #print(i[1])
#get_all_persons_and_store_in_file(my_config, "OUTPUT_FILES/ids.txt")
#update_user_passwords_from_file(my_config, "TXT_FILES/password_person_id_to_update.txt")
#update_user(my_config, 5)
#get_one_user(my_config, 115)
#create_freelancers_from_file(my_config, 116, "TXT_FILES/freelancers_to_create.txt")
#get_all_contacts_and_store_in_file(my_config,"OUTPUT_FILES/dt_contacts.txt")
#get_all_holiday_approvers(my_config, "OUTPUT_FILES/holiday_approvers.txt")
#update_contacts_with_approver_from_file(my_config, "INPUT_FILES/contacts_with_approver.txt")
my_config = ProgramConfig("UpdateShift20190506", "prod")
#SetHRGroupsForContactsFromFile(my_config, "INPUT_FILES/set_hr_groups_20190329.csv" )
#SetCompanyFromFile(my_config, "QUERIES/set_company.sql")
#Delete_Old_BloxNumbers(my_config, "QUERIES/remove_old_blox.sql")
#SetExecutivesFromFile(my_config, "INPUT_FILES/is_executive.csv")
#UpdateShifts(my_config, "INPUT_FILES/update_shifts_with_6min.txt", 6)
#SetExecutivesFromFileViaAPI(my_config, "INPUT_FILES/is_executive20190430.csv")
#update_user_password_from_departement_group_via_api(my_config, "QUERIES/reset_password_nieuwsdienst.sql", "TXT_FILES/password_person_id_to_update.txt")
#update_shift_with_planningdepartementgroup(my_config, "QUERIES/update_nieuws_shifts.sql")
