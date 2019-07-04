from datetime import datetime
import sys
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
from admodels import *
from config import ProgramConfig



def test(config):
    format_string = '{:25} {:>6} {:19} {:19} {}'
    print(format_string.format('User', 'Logins', 'Last Login', 'Expires', 'Description'))

    filter = "(&(objectClass=person)(objectClass=user)(sn=g*))"
    server = Server(my_config.ldap_server_name, get_info=ALL)
    conn = Connection(server, user='{}\\{}'.format(config.ldap_domain_name, config.ldap_user_name), password=config.ldap_password, auto_bind=True)
    conn.search(config.ldap_dsn, search_filter = filter, search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
    print(len(conn.entries))
    for e in conn.entries:
        print(str(e.uSNChanged))
        print("Changed on: %s" %e.whenChanged)
        print("Created on: %s" %e.whenCreated)
        print("Employee id: %s" %e.employeeID)
        print("Account enabled: %s" %e.userAccountControl)
        try:
            desc = e.description
            logonCount = e.logonCount
            lastLogon = e.lastLogon
            accountExpires = e.accountExpires


        except LDAPCursorError:
            desc = "error"
            logonCount = "?"
            lastLogon = "?"
            accountExpires = "?"
        print(format_string.format(str(e.name), str(logonCount), str(lastLogon)[:19], str(accountExpires)[:19], desc))

my_config = ProgramConfig("LDAPTests")
test(my_config)
