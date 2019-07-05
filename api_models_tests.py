import logging
from config import ProgramConfig
from api_models import *
from random import randint

'''
HOLIDAY TESTS
'''

def init_holiday_config():
    my_config = ProgramConfig("Test_Holiday_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    return my_config

def test_get_holiday_by_id_fail():
    my_config = init_holiday_config()
    test = Api_Holiday().get_by_id(my_config, None)
    print(test)
    assert isinstance(test, IdRequired)

def test_get_holiday_by_nonexisting_id():
    my_config = init_holiday_config()
    test = Api_Holiday().get_by_id(my_config, -1)
    print(test)
    assert isinstance(test, ItemDoesNotExist)

def test_get_holiday_by_id():
    my_config = ProgramConfig("Test_Holiday_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    test = Api_Holiday().get_by_id(my_config, 25341)
    assert test.Amount is not None
    assert test.Amount != ''

def test_update_holiday_by_id():
    my_config = init_holiday_config()
    new_amount = randint(1,40)
    holiday  = Api_Holiday.get_by_id(my_config, 25341)
    holiday.Amount = new_amount
    holiday_update = holiday.update_by_id(my_config)
    print("NEW HOLIDAY AMOUNT: %s" %new_amount)
    print("AMOUNT FROM API: %s " %holiday_update.Amount)
    assert holiday_update.Amount == new_amount

def test_create_holiday_with_id():
    my_config = init_holiday_config()
    assert isinstance(holiday.create(my_config), IdMustBeNull)

def test_create_holiday_without_id():
    my_config = init_holiday_config()
    holiday.Id = None
    holiday = holiday.create(my_config)
    print(holiday)

def test_create_holiday_success():
    my_config = init_holiday_config()
    holiday.Id = None
    holiday.ResourceId = 545
    holiday.DateFrom = '2019-04-16T00:00:00'
    holiday.Type = 1
    holiday.TransactionType = 1
    holiday.Status = 2
    holiday.RoleId = 398
    holiday.Amount = 7.6
    holiday = holiday.create(my_config)
    assert holiday.Id is not None

test_get_holiday_by_id_fail()
test_get_holiday_by_id()
test_update_holiday_by_id()
#test_create_holiday_with_id()
#test_create_holiday_without_id()
#test_create_holiday_success()
test_get_holiday_by_nonexisting_id()


'''
TV PRODUCTION TESTS
'''


def init_production_config():
    my_config = ProgramConfig("Test_Production_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    return my_config

def test_get_production_by_id():
    config = init_production_config()
    production = Api_Production().get_by_id(config, 2)
    assert production.Name is not None
    assert production.Name != ''

#test_get_production_by_id()


'''
NOMINAL TESTS
'''

def init_nominal_config():
    my_config = ProgramConfig("Test_Nominal_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    return my_config

def test_get_nominal_by_id():
    my_config = init_nominal_config()
    nominal  = Api_Nominal.get_by_id(my_config, 3)
    assert nominal.Nominal is not None
    assert nominal.Nominal != ''

#test_get_nominal_by_id()


'''
PERSON TESTS
'''
def init_person_config():
    my_config = ProgramConfig("Test_Person_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    return my_config

def test_get_person_by_id():
    my_config = init_person_config()
    person = Api_Person.get_by_id(my_config, 1)
    assert person.FirstName is not None
    assert person.FirstName != ''

def test_get_all_persons():
    my_config = ProgramConfig("Test_Person_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    person_list = Api_Person.get_all(my_config)

#test_get_person_by_id()
#test_get_all_persons()
