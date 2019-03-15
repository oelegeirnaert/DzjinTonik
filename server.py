import os
import cherrypy
import random
import string
import urllib.parse
import json
from bson import json_util

from cherrypy.lib import auth_digest

from jinja2 import Environment, FileSystemLoader

from models import *
from models_sql import *
from config import ProgramConfig

env = Environment(loader=FileSystemLoader('templates'))

class DTSecuredServer(object):
    def __init__(self, config):
        self._config = config
        self.my_env = config.environment

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('secure_index.html')
        return tmpl.render(salutation='Hello', target='World2')

    @cherrypy.expose
    def list_contacts(self):

        url = "%s/Contact/ReadLight" %self._config.domain
        r = requests.post(url, headers = self._config.headers, cookies = self._config.cookies, data={'pagesize':0})
        if not dt_util.logged_in(r.text, self._config):
            print("You're not loggedin")

        domain = self._config.domain

        tmpl = env.get_template('hr/list_contacts.html')
        return tmpl.render(salutation='Hello', results = json.loads(r.text)['Data'], domain = domain)

    @cherrypy.expose
    def my_profile(self):
        tmpl = env.get_template('me.html')
        return tmpl.render(salutation='Hello', target='World2')

    @cherrypy.expose
    def users_from_ad(self):
        tmpl = env.get_template('flows/users_from_ad.html')
        return tmpl.render(message="The function 'users_from_ad' isn't implemented yet...")

    @cherrypy.expose
    def modified_shifts_after_payroll(self):
        tmpl = env.get_template('hr/modified_shifts_after_payroll.html')
        shifts = PayrollModifiedShifts.get_modified_shifts_after_payroll(self._config)
        my_source = "%s/%s" %(self._config.sql_server, self._config.sql_database)
        return tmpl.render(shifts = shifts , source = my_source )

    @cherrypy.expose
    def approval_flow(self):
        tmpl = env.get_template('flows/index.html')
        return tmpl.render(message="The approval function isn't implemented yet...")

    @cherrypy.expose
    def search(self, **kwargs):
        text = kwargs['search']
        text = urllib.parse.unquote(text)

        search_for = text[0:2].upper()
        search_value = text[2:]

        if len(search_value) == 0:
            tmpl = env.get_template('no_results.html')
            return tmpl.render(result_object="Please provide a string to search on!")

        valid_search_prefix = False
        if search_for == "P:":
            valid_search_prefix = True
            person = Person(self._config)
            url = "%s/Person/ReadLight" %self._config.domain
            data = {'SearchTextOverview': search_value,
                'PageSize': 0
                }
            if person.search_in_dt(url, data):
                tmpl = env.get_template('person/person_item.html')
                return tmpl.render(person=person)

        if search_for == 'A:':
            valid_search_prefix = True
            print("Search for asset")
            tmpl = env.get_template('no_results.html')
            return tmpl.render(result_object="This function isn't implemented yet!")

        if search_for == 'C:':
            valid_search_prefix = True
            contact = Contact(self._config, Id=None)

            url = "%s/Contact/ReadLight" %self._config.domain
            data = {'SearchTextOverview': search_value,
                'PageSize': 0
                }

            if contact.search_in_dt(url, data):
                contact.get_from_dt()
                if contact.Photo:
                    contact.download_picture()
                tmpl = env.get_template('contact/contact_item.html')
                return tmpl.render(contact=contact, env = self.my_env, domain = self._config.domain)


        if not valid_search_prefix:
            #return "Please prefix correctly"
            print("please prefix correctly")
            tmpl = env.get_template('no_results.html')
            return tmpl.render(result_object="Please prefix correctly!", temp = 'prefix_info.html')



        tmpl = env.get_template('no_results.html')
        return tmpl.render(result_object="Sorry, your search didn't returned any results!")

class APIServer(object):
    def __init__(self, config):
        self._config = config
        self.my_env = config.environment

    @cherrypy.expose
    def remove_modified_shift(self, id):
        my_shift = PayrollModifiedShifts.get_one_modified_shift(id)[0]
        my_shift.modified_in_hr_system()
        return json.dumps("OK")


class RootServer(object):
    def __init__(self, config):
        self._config = config
        self.my_env = config.environment

    @cherrypy.expose
    def index(self):
        aut = cherrypy.request.headers.get('AUTHORIZATION')
        print(aut)
        tmpl = env.get_template('index.html')
        return tmpl.render(salutation='Hello', target='World2', env =self.my_env)

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))

    @cherrypy.expose
    def dt_login(self):
        tmpl = env.get_template('dt_login.html')
        return tmpl.render()

    @cherrypy.expose
    def do_dt_login(self, button, request_token, asp_session):
        self._config.request_token = request_token
        self._config.asp_session = asp_session
        tmpl = env.get_template('login.html')
        return tmpl.render()


    @cherrypy.expose
    def user(self, person_id):
        p = Person(config=self._config, id=int(person_id))
        if p.get_from_dt():
            self._config.logger.debug("LOGGED:%s" %p.__dict__)
            tmpl = env.get_template('user.html')
            return tmpl.render(user = p)
        else:
            raise cherrypy.HTTPRedirect("/dt_login")



USERS = {'jon': 'secret'}



if __name__ == '__main__':
    my_config = ProgramConfig("Server")
    cherrypy.config.update("server.conf")
    static_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    cherrypy.config.update({'tools.staticdir.dir': static_path, 'tools.staticdir.on': True})
    cherrypy.tree.mount(RootServer(my_config), '/')
    cherrypy.tree.mount(DTSecuredServer(my_config), '/secured', {'/': {'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost','tools.auth_digest.key': 'a565c27146791cfb',
        'tools.auth_digest.accept_charset': 'UTF-8', 'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS)}})
    cherrypy.tree.mount(APIServer(my_config), '/api', {'/': {'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost','tools.auth_digest.key': 'a565c27146791cfb',
        'tools.auth_digest.accept_charset': 'UTF-8', 'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS)}})
    # root = RootServer(my_config)
    # root.secure = SecuredServer(my_config)
    # cherrypy.quickstart(root, '/')
    cherrypy.engine.start()
    cherrypy.engine.block()
