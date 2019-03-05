import cherrypy
import random
import string
from jinja2 import Environment, FileSystemLoader

from models import *
from config import ProgramConfig

env = Environment(loader=FileSystemLoader('templates'))

class HelloWorld(object):
    def __init__(self, config):
        self._config = config

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(salutation='Hello', target='World2')

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))

    @cherrypy.expose
    def user(self, person_id):
        p = Person(config=self._config, id=int(person_id))

        if p.get_from_dt():
            self._config.logger.debug("LOGGED:%s" %p.__dict__)
            tmpl = env.get_template('user.html')
            return tmpl.render(user = p)
        else:
            return "Cannot get this person %s" %int(person_id)


if __name__ == '__main__':
    my_config = ProgramConfig("Server")
    cherrypy.quickstart(HelloWorld(my_config))
