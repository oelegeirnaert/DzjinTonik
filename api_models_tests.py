import logging
from config import ProgramConfig
from api_models import *

'''
HOLIDAY TESTS
'''

def init_holiday():
    my_config = ProgramConfig("Test_Holiday_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    holiday = Api_Holiday()
    holiday.Id = 25341
    return holiday, my_config

def test_get_holiday_by_id_fail():
    holiday, my_config = init_holiday()
    holiday.Id = None
    assert isinstance(holiday.get_by_id(my_config), IdRequired)

def test_get_holiday_by_nonexisting_id():
    holiday, my_config = init_holiday()
    holiday.Id = -1
    assert isinstance(holiday.get_by_id(my_config), ItemDoesNotExist)

def test_get_holiday_by_id():
    holiday, my_config = init_holiday()
    holiday.get_by_id(my_config)
    assert holiday.Amount is not None
    assert holiday.Amount != ''

def test_update_holiday_by_id():
    holiday, my_config = init_holiday()
    holiday.get_by_id(my_config)
    holiday.Amount = 7.6
    holiday = holiday.update_by_id(my_config)
    assert holiday.Amount == 7.6

def test_create_holiday_with_id():
    holiday, my_config = init_holiday()
    assert isinstance(holiday.create(my_config), IdMustBeNull)

def test_create_holiday_without_id():
    holiday, my_config = init_holiday()
    holiday.Id = None
    holiday = holiday.create(my_config)
    print(holiday)

def test_create_holiday_success():
    holiday, my_config = init_holiday()
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

#test_get_holiday_by_id_fail()
test_get_holiday_by_id()
#test_update_holiday_by_id()
#test_create_holiday_with_id()
#test_create_holiday_without_id()
#test_create_holiday_success()
#test_get_holiday_by_nonexisting_id()



'''
TV PRODUCTION TESTS
'''


def init_production():
    my_config = ProgramConfig("Test_Production_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    production = Api_Production()
    production.Id = 2
    return production, my_config

def test_get_production_by_id():
    production, config = init_production()
    production.get_by_id(config)
    assert production.Name is not None
    assert production.Name != ''


#test_get_production_by_id()


'''
NOMINAL TESTS
'''

def init_nominal():
    my_config = ProgramConfig("Test_Nominal_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    nominal = Api_Nominal()
    nominal.Id = 3
    return nominal, my_config

def test_get_nominal_by_id():
    nominal, my_config = init_nominal()
    nominal.get_by_id(my_config)
    assert nominal.Nominal is not None
    assert nominal.Nominal != ''

#test_get_nominal_by_id()


'''
PERSON TESTS
'''
def init_person():
    my_config = ProgramConfig("Test_Person_API", environment="test", loglevel = logging.DEBUG, show_log = True)
    person = Api_Person()
    person.Id = 1
    return person, my_config

def test_get_person_by_id():
    person, my_config = init_person()
    person.get_by_id(my_config)
    print(person.FirstName)
    assert person.FirstName is not None
    assert person.FirstName != ''

test_get_person_by_id()
