from models import *
from config import ProgramConfig

my_config = ProgramConfig("GetPerson", environment="test")
my_contact = Contact(my_config, 26083)
my_contact.get_from_dt()
print(my_contact.__dict__)
my_person = Person(my_config, 129)
my_person.get_from_dt()
print(my_person.__dict__)

search_contact = Contact(my_config, 116)
search_contact.get_from_dt()
#search_contact.search_in_dt()
search_contact.download_picture()
print(search_contact)

# TODO: test
