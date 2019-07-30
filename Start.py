import datetime
import sys
import string
import random
import copy
import requests
import sys
import pymssql
import logging
import time

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
            if comp=="409000":
                c.DefaultInternalCompanyId = 2
                c.CompanyId = 40
            if comp=="409100":
                c.DefaultInternalCompanyId = 1
                c.CompanyId = 1
            if comp=="409200":
                c.DefaultInternalCompanyId = 3
                c.CompanyId = 41
            if comp=="409300":
                c.DefaultInternalCompanyId = 4
                c.CompanyId = 42
            if comp=="409400":
                c.DefaultInternalCompanyId = 5
                c.CompanyId = 43
            if comp=="409500":
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

def update_shift_with_planningdepartementgroup(config = None, sqlfile = None, visible = None, apply_update = False):
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

        if visible is not None:
            if visible == True:
                current_pi.Visibility = 1
            if visible == False:
                current_pi.Visibility = 0
        else:
            print("Don't touch the visibility")

        current_pi.PlanningDepartmentGroupId = pdgid
        print(current_pi.__dict__)
        #sys.exit()
        postback_end_point = "%s/%s" %(api_end_point, current_pi.Id)
        print(postback_end_point)
        #sys.exit()
        if apply_update:
            postback = requests.put(postback_end_point, data=current_pi.__dict__, headers= my_headers)
            if postback.status_code == 200:
                print("Updated")
            else:
                print("ERROR")
                print(postback.text)

def get_all_planningitems(config, output_file):
    endpoint = "%s%s?PageSize=0" %(config.api_domain, "planningitem")
    print(endpoint)
    print(config.headers)
    my_headers = {'Authorization': config.api_authorization}
    r = requests.get(endpoint, headers = my_headers)
    f = open(output_file, "a")
    f.write(r.text)
    f.close()
    sys.exit()

def convert_json_file_to_csv(input_file = None, output_file = None):
    import csv
    print("The input file is: %s" %input_file)
    print("The output file is: %s" %output_file)

    json_file = open(input_file)
    json_parsed = json.load(json_file)

    items = json_parsed['PageItems']
    csv_data = open(output_file, 'w')
    csvwriter = csv.writer(csv_data)

    header = True
    for item in items:
          if header == True:
                 header = item.keys()
                 csvwriter.writerow(header)
                 header = False
          csvwriter.writerow(item.values())
    csv_data.close()
    sys.exit()

def stringMaker(booking, person, asset, planningdepartment, planningdepartmentgroup):
    if not person is None:
        return "Person %s %s is booked on %s in planningboard %s-%s" %(person.FirstName, person.LastName, booking.ActualStart, planningdepartment, planningdepartmentgroup)

    if not asset is None:
        return "Asset %s is booked on %s in planningboard %s-%s" %(asset.Name, booking.ActualStart, planningdepartment, planningdepartmentgroup)


def WolfTechIntegration(config, sqlfile, loadfrom):
    if not isinstance(config, ProgramConfig):
        raise Exception("Your config must be a config class.")

    sql_planboards = dt_util.get_sql_list_from_file(config, sqlfile)
    for current_planboard in sql_planboards:
        pdid = current_planboard['PlanningDepartmentId']
        pdgid = current_planboard['PlanningDepartmentGroupId']
        pdname = current_planboard['PlanningDepartmentName']
        pdgname = current_planboard['PlanningDepartmentGroupName']
        print("%s %s" %(pdid, pdgid))

        current_endpoint = "%s/booking?PlanningDepartmentId=%s&DepartmentGroupIds=%s&changedafter=%s&pagesize=0" %(config.api_domain, pdid, pdgid, loadfrom)
        my_headers = {'Authorization': config.api_authorization}
        r = requests.get(current_endpoint, headers=my_headers)
        my_booking_list = json.loads(r.text)['PageItems']

        current_booking_item = Api_BookingItem()
        current_person = Api_Person()
        current_asset = Api_Asset()

        #Maybe it's better to load all the assets and persons in two calls instead of doing them in the for-loop.
        #Something like: "%s/person?pagesize=0" %(config.api_domain) instead of "%s/person?resourceId=%s" %(config.api_domain, current_booking_item.ResourceId)
        #Next you can query them in-memory so we save time because we don't need to query the slower API everytime.

        for current_booking in my_booking_list:
            current_booking_item.__dict__ = current_booking

            if current_booking_item.CategoryTypeId == 1:
                print("Load Person")
                current_person_endpoint = "%s/person?resourceId=%s" %(config.api_domain, current_booking_item.ResourceId)
                current_person_request = requests.get(current_person_endpoint, headers=my_headers)
                current_person_json = json.loads(current_person_request.text)['PageItems'][0]
                current_person.__dict__ = current_person_json

            if current_booking_item.CategoryTypeId == 2:
                print("Load Asset")
                current_asset_endpoint = "%s/asset?resourceId=%s" %(config.api_domain, current_booking_item.ResourceId)
                current_asset_request = requests.get(current_asset_endpoint, headers=my_headers)
                current_asset_json = json.loads(current_asset_request.text)['PageItems'][0]
                current_asset.__dict__ = current_asset_json

            #I think in this way we have all the information necessary to send it to WolfTech.
            # - We know on which planboard we are currently looping
            # - We know the booking on this planboard
            # - We know everything about the person
            # - We know everything about the asset
            print(stringMaker(current_booking_item, current_person, current_asset, pdname, pdgname))



def WolfTechIntegrationBetterPerformance(config, sqlfile, loadfrom):
    if not isinstance(config, ProgramConfig):
        raise Exception("Your config must be a config class.")

    config.logger.info("Loading all necessary planboards from SQL Server")
    sql_planboards = dt_util.get_sql_list_from_file(config, sqlfile)
    for current_planboard in sql_planboards:
        pdid = current_planboard['PlanningDepartmentId']
        pdgid = current_planboard['PlanningDepartmentGroupId']
        pdname = current_planboard['PlanningDepartmentName']
        pdgname = current_planboard['PlanningDepartmentGroupName']
        print("%s %s" %(pdid, pdgid))

        config.logger.info("Load all channged bookings after %s on planboard: %s-%s" %(loadfrom, pdname, pdgname))
        current_endpoint = "%s/booking?PlanningDepartmentId=%s&DepartmentGroupIds=%s&changedafter=%s&pagesize=0" %(config.api_domain, pdid, pdgid, loadfrom)
        my_headers = {'Authorization': config.api_authorization}
        r = requests.get(current_endpoint, headers=my_headers)
        my_booking_list = json.loads(r.text)['PageItems']
        config.logger.info("Total of bookings loaded: %s" %len(my_booking_list))

        current_booking_item = Api_BookingItem()

        #Load all person data
        config.logger.info("Load all person data")
        all_persons = []
        persons_endpoint = "%s/person?pagesize=0" %(config.api_domain)
        all_persons_request = requests.get(persons_endpoint, headers=my_headers)
        all_persons_json = json.loads(all_persons_request.text)['PageItems']
        config.logger.info("Total of persons loaded: %s" %len(all_persons_json))
        all_persons.append(all_persons_json)

        sys.exit()

        #Load all asset data
        config.logger.info("Load all asset data")
        all_assets = []
        assets_endpoint = "%s/asset?pagesize=0" %(config.api_domain)
        all_assets_request = requests.get(assets_endpoint, headers=my_headers)
        all_assets_json = json.loads(current_asset_request.text)['PageItems']
        all_assets.__dict__ = all_assets_json



        #Maybe it's better to load all the assets and persons in two calls instead of doing them in the for-loop.
        #Something like: "%s/person?pagesize=0" %(config.api_domain) instead of "%s/person?resourceId=%s" %(config.api_domain, current_booking_item.ResourceId)
        #Next you can query them in-memory so we save time because we don't need to query the slower API everytime.

        for current_booking in my_booking_list:
            current_booking_item.__dict__ = current_booking

            if current_booking_item.CategoryTypeId == 1:
                print("Load Person")
                current_person.__dict__ = current_person_json

            if current_booking_item.CategoryTypeId == 2:
                print("Load Asset")

                current_asset.__dict__ = current_asset_json

            #I think in this way we have all the information necessary to send it to WolfTech.
            # - We know on which planboard we are currently looping
            # - We know the booking on this planboard
            # - We know everything about the person
            # - We know everything about the asset
            print(stringMaker(current_booking_item, current_person, current_asset, pdname, pdgname))

def Change_Shift_Times_MCR(config, shift_ids, shift_from):
    db = config.mongodb_database
    from_date_obj = datetime.datetime.strptime(shift_from, '%d-%m-%Y')
    headers = {
        'Accept': "application/json",
        'Authorization': config.api_authorization
        }


    shift_endpoint = "%sshift" %config.api_domain
    planning_endpoint = "%splanningitem" %config.api_domain
    booking_endpoint = "%sbooking" %config.api_domain

    api_pi = Api_PlanningItem()
    api_bi = Api_BookingItem()
    api_shift = Api_Shift()

    for shift_id in shift_ids:
        shift_params = {'shiftid': shift_id,
            'pagesize': 0,
        }

        shift_request = requests.get(shift_endpoint, headers = headers, params={'id': shift_id})
        print(shift_request.text)
        api_shift.__dict__ = json.loads(shift_request.text)

        shift_start_datetime = datetime.datetime.strptime(api_shift.StartTime, '%Y-%m-%dT%H:%M:%S')
        shift_end_datetime = datetime.datetime.strptime(api_shift.EndTime, '%Y-%m-%dT%H:%M:%S')

        answer = dt_util.ask_yes_no_question("Would you like to update the bookings with shiftname %s with the following starttime: %s and endtime: %s" %(api_shift.Name, shift_start_datetime.time(), shift_end_datetime.time()))
        if answer == False:
            continue



        planning_item_request = requests.request("GET", planning_endpoint, headers = headers, params=shift_params)
        json_planningitems = json.loads(planning_item_request.text)['PageItems']

        for json_pi in json_planningitems:
            api_pi.__dict__ = json_pi
            print("Update PlanningItemId: %s" %api_pi.Id)
            #2019-04-29T15:00:00
            pi_start = datetime.datetime.strptime(api_pi.StartTime, '%Y-%m-%dT%H:%M:%S')

            if pi_start < from_date_obj:
                print("Start of shift %s is before %s, do not edit!" %(pi_start, from_date_obj))
                continue

            db.mcr_planningitem_update.update_one({'Id':api_pi.Id}, {'$set':api_pi.__dict__}, upsert=True)
            api_pi = change_start_end(api_pi, shift_start_datetime.time(), shift_end_datetime.time())
            update_pi_request = requests.put(planning_endpoint, data=api_pi.__dict__, headers=headers, params={'id': api_pi.Id})
            if update_pi_request.status_code != 200:
                print(update_pi_request.text)
                my_answer = dt_util.ask_yes_no_question("Error, continue?")
                if my_answer == False:
                    sys.exit()

            booking_params = {'planningitemid': api_pi.Id,
                'pagesize': 0,
            }
            r_booking = requests.get(booking_endpoint, headers=headers, params=booking_params)
            json_bookings = json.loads(r_booking.text)['PageItems']
            for json_booking in json_bookings:
                api_bi.__dict__ = json_booking
                db.mcr_booking_update.update_one({'Id':api_bi.Id}, {'$set':api_bi.__dict__}, upsert=True)
                api_bi = change_start_end(api_bi, shift_start_datetime.time(), shift_end_datetime.time())
                update_bi_request = requests.put(booking_endpoint, data=api_bi.__dict__, headers=headers, params={'id':api_bi.Id})
                if update_bi_request.status_code != 200:
                    print(update_bi_request.text)
                    my_answer = dt_util.ask_yes_no_question("Error, continue?")
                    if my_answer == False:
                        sys.exit()


def change_start_end(item, new_start_time, new_end_time):
    item.StartTime = datetime.datetime.strptime(item.StartTime, '%Y-%m-%dT%H:%M:%S')
    item.EndTime = datetime.datetime.strptime(item.EndTime, '%Y-%m-%dT%H:%M:%S')
    item.ActualStart = datetime.datetime.strptime(item.ActualStart, '%Y-%m-%dT%H:%M:%S')
    item.ActualEnd = datetime.datetime.strptime(item.ActualEnd, '%Y-%m-%dT%H:%M:%S')

    if isinstance(item, Api_PlanningItem):
        item.DateFrom = datetime.datetime.strptime(item.DateFrom, '%Y-%m-%dT%H:%M:%S')
        item.DateTo = datetime.datetime.strptime(item.DateTo, '%Y-%m-%dT%H:%M:%S')

    current_start_time = item.StartTime.time()
    current_end_time = item.EndTime.time()

    current_actual_start_time = item.ActualStart.time()
    current_actual_end_time = item.ActualEnd.time()

    print_new_times(item, "old")
    item.StartTime = item.StartTime.replace(hour=new_start_time.hour, minute=new_start_time.minute)
    item.EndTime = item.EndTime.replace(hour=new_end_time.hour, minute=new_end_time.minute)
    item.ActualStart = item.ActualStart.replace(hour=new_start_time.hour, minute=new_start_time.minute)
    item.ActualEnd = item.ActualEnd.replace(hour=new_end_time.hour, minute=new_end_time.minute)


    if current_end_time < current_start_time:
        print("add one day to planned end time")
        item.EndTime = item.EndTime.replace(day=item.StartTime.day)
        if isinstance(item, Api_PlanningItem):
            #item.DateTo = item.DateTo.replace(day=item.DateFrom.day+1)
            #As discussed with the business on 20190626.
            #If we do a day+1 we see double items on the plan board. So we keep the same from day.
            item.DateTo = item.DateTo.replace(day=item.DateFrom.day)

    if current_actual_end_time < current_actual_start_time:
        print("Add one day to actual end time")
        item.ActualEnd = item.ActualEnd.replace(day=item.ActualStart.day)


    print_new_times(item, "new")

    return item

def print_new_times(item, conv_str):
    print("The %s start datetime is: %s" %(conv_str, item.StartTime))
    print("The %s end datetime is: %s" %(conv_str, item.EndTime))
    print("The %s actual start datetime is: %s" %(conv_str, item.ActualStart))
    print("The %s actual end datetime is: %s" %(conv_str, item.ActualEnd))

def change_planningitems_for_production(config, from_production_id, to_production_id, year_to_change):
    '''
    The business asked to change the planned items to a new production for reporting reasons (Cost Calculation & Budgetting)
    Currently they are all booked under the same production, but as it's a new episode, it should be another production.
    '''

    db = config.mongodb_database

    from_production = Api_Production().get_by_id(config = config, id = from_production_id)
    to_production = Api_Production().get_by_id(config = config, id = to_production_id)

    answer = dt_util.ask_yes_no_question("Are you sure you'd like to change all the planningitems from production '%s' to '%s' planned in year %s?" %(from_production.Name, to_production.Name, year_to_change))
    if answer == False:
        sys.exit()

    my_list = Api_PlanningItem.get_all(config,0)
    list_to_change = []
    list_of_failures = []

    for item in my_list:
        item.DateFrom = datetime.datetime.strptime(item.DateFrom, '%Y-%m-%dT%H:%M:%S')
        item_year = item.DateFrom.year

        #For readability and easy understanding, different IF
        if item.ProductionId is None:
            continue

        if item.ProductionId != from_production.Id :
            continue

        if  item_year != year_to_change:
            continue

        print(item)
        list_to_change.append(item)

        db.bestekijkers.update_one({'Id':item.Id}, {'$set':item.__dict__}, upsert=True)


        item.ProductionId = to_production.Id

        if not item.push_to_dt(config):
            config.logger.error("Update failed for: %s" %item.__dict__)
            list_of_failures.append(item)

    print("%s items were changed..." %len(list_to_change))

def ChangeHolidays(config, input_file):
    a_holiday = Api_Holiday()
    a_holiday.Id = 25341
    a_holiday.get_by_id(config)

def Change_Bookings_Without_Break(config, sql_file, update_all, update_in_dt):
    '''
    Following HR and Belgian Social Inspection rules, every person should take at
    least 30min of break for shifts longer than x minutes/hours.
    '''
    bookings_to_change = dt_util.get_sql_list_from_file(config, sql_file)
    for booking in bookings_to_change:
        current_booking_id = booking['BOOKING_ID']
        try:
            current_booking = Api_BookingItem().get_by_id(config, current_booking_id)

            current_planningitem_id = current_booking.PlanningItemId
            try:
                current_planningitem = Api_PlanningItem().get_by_id(config, current_planningitem_id)
            except Exception as e:
                print("Cannot get planningitem with id: %s" %pid)
                print(e)

            current_shift_id = current_planningitem.ShiftId
            try:
                current_shift = Api_Shift().get_by_id(config, current_shift_id)
                print(current_shift.Name)
            except Exception as e:
                print("Cannot get shift with id: %s" %current_shift_id)
                print(e)
        except Exception as e:
            print("Cannot get booking with id: %s" %current_booking_id)
            print(e)

        print_full_info(current_shift, current_planningitem, current_booking)

        if current_shift.Break is not None:
            if not isinstance(current_planningitem, ItemDoesNotExist):
                if current_planningitem.BreakTime is None or current_planningitem.BreakTime != current_shift.Break:
                    current_planningitem.BreakTime = current_shift.Break

                if current_planningitem.ActualBreak is None or current_planningitem.ActualBreak >= 0:
                    current_planningitem.ActualBreak = current_shift.Break

            if not isinstance(current_booking, ItemDoesNotExist):
                if current_booking.BreakTime is None or current_booking.BreakTime != current_shift.Break:
                    current_booking.BreakTime = current_shift.Break

                if current_booking.ActualBreak is None or current_booking.ActualBreak >= 0:
                    current_booking.ActualBreak = current_shift.Break

        print_full_info(current_shift, current_planningitem, current_booking)

        if update_in_dt:
            if not isinstance(current_booking, ItemDoesNotExist):
                current_booking.update_by_id(config)
            if not isinstance(current_planningitem, ItemDoesNotExist):
                current_planningitem.update_by_id(config)

        if not update_all:
            answer = dt_util.ask_yes_no_question("Update next?")
            if not answer:
                print("OK, BYE BYE, thanks for using me!")
                sys.exit()
            else:
                print("OK, let's update the next item")
                time.sleep(2)



def print_full_info(shift, planningitem, booking):
    if not isinstance(shift, Api_Shift):
        print("This is not a shift...")

    if not isinstance(planningitem, Api_PlanningItem):
        print("This is not a planningsitem...")

    if not isinstance(booking, Api_BookingItem):
        print("This is not a booking...")

    print("%s" % '-' * 80)
    if shift.Break is not None:
        print("Shift %s with break: %s" %(shift.Name, shift.Break))
    else:
        print("This shift has no breaktime set!")

    if not isinstance(planningitem, ItemDoesNotExist):
        print("  Planningitem planned break: %s" %planningitem.BreakTime)
        print("  Planningitem actual break: %s" %planningitem.ActualBreak)
    else:
        print("This planningitem is None!")

    if not isinstance(booking, ItemDoesNotExist):
        print("  Booking planned break: %s" %booking.BreakTime)
        print("  Booking actual break: %s" %booking.ActualBreak)
    else:
        print("The booking is none!")
    print("%s" % '-' * 80)

def Restore_Holidays(config, sqlfile, update_in_dt, update_all):
    '''
        NOT COMPLETED YET!
        Take the right holiday nominal value.
        FI: if the booking happend in march, and the nominal has been changed in april.
        Take the holiday nominal of march instead of the one of today!

        FIX: Instead of doing this task by scriptiong.
        Just change the status of the booking in the GUI, and all the logic will be applied by DT.
        Only 45 cases, not that much to do it manually taken into account the development costs/time.
    '''
    nominal = Api_Nominal().get_by_resourceid(config, 2)
    sys.exit()
    list = dt_util.get_sql_list_from_file(config, sqlfile)
    print(list)
    for item in list:
        current_booking_id = item['BookingId']
        current_booking = Api_BookingItem().get_by_id(config, current_booking_id)
        current_holiday = Api_Holiday().get_by_bookingid(config, current_booking_id)

        if isinstance(current_booking, ItemDoesNotExist):
            print("The current booking with this ID doesn't exist... So do nothing...")
            continue

        if isinstance(current_holiday, Api_Holiday):
            print("The holiday for this booking already exists.")
            continue
        else:
            current_holiday = Api_Holiday()
            current_holiday.ResourceId = item['ResourceId']
            current_holiday.DateFrom = item['StartTime']
            current_holiday.DateTo = item['EndTime']
            current_holiday.RoleId = 398
            current_holiday.Type = 1
            current_holiday.TransactionType = 1
            current_holiday.Status = 2
            current_holiday.BookingId = current_booking.Id
            print(current_holiday)
            print(update_in_dt)
            if update_in_dt:
                try:
                    print("Trying to create current holiday for %s %s..." %(item['FirstName'], item['LastName']))
                    current_holiday.create(config)
                    print("Check holidays via:")
                    print("%s/Contact?ContactId=%s#holidayTab" %(config.domain, item['ContactId']))
                    print("Creation success!")
                except Exception as e:
                    print(e)

        if not update_all:
            answer = dt_util.ask_yes_no_question("Update next one?")
            if not answer:
                sys.exit()

def Get_All_Productions(config):
    my_list, count = Api_Production.get_all(config)
    print("We've found %s productions" %count)
    for item in my_list:
        print(item.Name)

def Get_All_Nominals(config):
    my_list, count = Api_Nominal.get_all(config)
    print("We've found %s nominals." %count)
    for item in my_list:
        print(item)

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

my_config = ProgramConfig("CorrectHolidays", "test", logging.DEBUG, True)
#SetHRGroupsForContactsFromFile(my_config, "INPUT_FILES/set_hr_groups_20190329.csv" )
#SetCompanyFromFile(my_config, "QUERIES/set_company.sql")
#Delete_Old_BloxNumbers(my_config, "QUERIES/remove_old_blox.sql")
#SetExecutivesFromFile(my_config, "INPUT_FILES/is_executive.csv")
#UpdateShifts(my_config, "INPUT_FILES/update_shifts_with_6min.txt", 6)
#SetExecutivesFromFileViaAPI(my_config, "INPUT_FILES/is_executive20190430.csv")
#update_user_password_from_departement_group_via_api(my_config, "QUERIES/reset_password_nieuwsdienst.sql", "TXT_FILES/password_person_id_to_update.txt")
#update_shift_with_planningdepartementgroup(my_config, "QUERIES/update_nieuws_shifts_starting_june.sql", apply_update=True)
#get_all_planningitems(my_config, "OUTPUT_FILES/planningitems.json")
#convert_json_file_to_csv(input_file = "OUTPUT_FILES/planningitems.json", output_file = "OUTPUT_FILES/planningitems.csv")
#print(random_password_generator())
#WolfTechIntegrationBetterPerformance(my_config, "QUERIES/wolftechplanboards.sql", 20190501)
#Change_Shift_Times_MCR(my_config, [172, 173], '01-07-2019')

'''
if my_config.environment.upper() == 'PROD':
    change_planningitems_for_production(my_config, 20, 77, 2019)
else:
    change_planningitems_for_production(my_config, 20, 21, 2018) #in test we don't have 77
'''

#ChangeHolidays(my_config, 'INPUT_FILES/holiday_ids_to_change.txt')

#config, sql_file, update_all, update_in_dt
#Change_Bookings_Without_Break(my_config, "QUERIES/shifts_without_break.sql", True, True)
#Restore_Holidays(my_config, "QUERIES/Restore_Holidays.sql", True, False)
#Get_All_Productions(my_config)
Get_All_Nominals(my_config)
