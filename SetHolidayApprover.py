import sys

from models import *
from config import ProgramConfig
import dt_util



def start_update(config, person_to_update, new_holiday_approver_id):

    contact_to_update = Contact(config, person_to_update)
    if not contact_to_update.get_from_dt():
        print("We cannot get the contact to update!")
        return None

    if contact_to_update is None:
        print("No person found with this ID to update.")

    current_holidayapprover_id = contact_to_update.HolidayApproverId
    contact_to_update_full_name = contact_to_update.get_full_name()
    print(contact_to_update.get_link())

    if current_holidayapprover_id is None:
        print("Currently there is no holiday approver set for %s!" %contact_to_update_full_name)

    current_holidayapprover = None
    if current_holidayapprover_id is not None:
        current_holidayapprover = Contact(config, Id=current_holidayapprover_id)
        if not current_holidayapprover.get_from_dt():
            print("We cannot get the contactinformation of the approver!")
            pass

    if current_holidayapprover is not None:
        if not dt_util.ask_yes_no_question('Currently %s is the holiday approver for %s... Would you like to change this?' %(current_holidayapprover.get_full_name(),contact_to_update.get_full_name())):
            print("Cancelled")
            return None

    new_approver = Contact(config, Id=new_holiday_approver_id)
    new_approver.get_from_dt()
    new_approver_full_name = new_approver.get_full_name()

    if not dt_util.ask_yes_no_question('Are you sure you want %s as holiday approver for %s?' %(new_approver_full_name, contact_to_update_full_name)):
        print("Cancelled")
        return None

    current_email_person_to_update = contact_to_update.Email
    config.logger.info("Current email: %s" %current_email_person_to_update)

    new_email_person_to_update = None
    if current_email_person_to_update is None:
        new_email_person_to_update = input("%s has no email set, thus the flow will not work correctly. Please provide his email:")
    else:
        if config.default_dzjintonik_user_email in current_email_person_to_update:
            new_email_person_to_update = input("This is the default email set... Please change it to: ")

    contact_to_update.Email = new_email_person_to_update
    contact_to_update.HolidayApproverId = new_holiday_approver_id

    if(contact_to_update.send_to_dt()):
        print("Everything done!")
    else:
        print("Something went wrong sending the new contact to DT.")

my_config = ProgramConfig("SetHollidayApprover")
start_update(my_config, 26053,154)
