import datetime
import sys
import string
import random
import copy

from models import *
from config import ProgramConfig

class Mailing(object):
    def __init__(self, Id, FullName, Username, Password, AccountStatus):
        self.Id = Id
        self.FullName = FullName
        self.Username = Username
        self.Password = Password
        self.PasswordSetOn = datetime.datetime.now()
        self.UpdateSuccess = False
        self.IsActive = AccountStatus

    def update_success(self, status):
        self.UpdateSuccess = status

def update_user(config, dzjintonik_id):
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

def random_password_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

my_config = ProgramConfig("SetUserPasswords")
update_user(my_config, 5)
