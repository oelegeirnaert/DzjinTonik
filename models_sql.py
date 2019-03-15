import pymssql
import json
import sys
import datetime

from models import *
from config import ProgramConfig
from models_sql import *


class PayrollModifiedShifts(object):
    modified_shifts = []
    shifts_to_check = []

    def __init__(self, config, row):
        self._config = config
        self.Actual_Start_DateTime = row['Actual_Start_DateTime']
        self.Update_DateTime = row['Update_DateTime']
        self.Planning_Department_Name = row['Planning_Department_Name']
        self.Planning_Department_Group_Name = row['Planning_Department_Group_Name']
        self.Contact_Full_Name = row['Contact_Full_Name']
        self.Booking_ID = row['Booking_Id']
        self.Modified_On = datetime.datetime.now()

    def __str__(self):
        return "Shift for %s" %self.Contact_Full_Name

    def get_one_modified_shift(id):
        print("Try to get: %s" %id)
        for x in PayrollModifiedShifts.shifts_to_check:
            print(x.Booking_ID)

        new_list = [x for x in PayrollModifiedShifts.shifts_to_check if x.Booking_ID == int(id)]
        print(new_list)
        #my_item = list(filter(lambda x: x.Booking_Id == id, ))
        #print ("TESTSDMLFKJSDKLMF: %s" %my_item)
        return new_list


    def modified_in_hr_system(self):
        self.Modified_On = datetime.datetime.now()
        self.Is_Modified = True
        db = self._config.mongodb_database
        self._config=None
        db.modified_shifts_after_payroll.update_one({'Id':self.Booking_ID}, {'$set':self.__dict__}, upsert=True)

    def get_modified_shifts_after_payroll(config, id=None):
        result = None
        shifts = []

        db = config.mongodb_database

        modified_shifts = db.modified_shifts_after_payroll.distinct('Booking_ID')
        print("5555TESTDFSDFSDFSDF: %s " %modified_shifts)

        message = "Trying to connect to %s/%s" %(config.sql_server, config.sql_database)
        print(message)
        config.logger.debug(message)
        conn = pymssql.connect(server = config.sql_server, database = config.sql_database)
        cursor = conn.cursor(as_dict=True)

        sql_file = "QUERIES/shift_edited_after_payroll.sql"
        strQry = None
        try:
            with open(sql_file, 'r') as myfile:
                strQry=myfile.read()
        except Exception as e:
            print("Sorry, I cannot read your SQL file: %s!" %sql_file)
            return None

        cursor.execute(strQry)
        if strQry is not None:

            row = cursor.fetchone()
            while row:
                if row is not None:
                    pms = PayrollModifiedShifts(config, row)
                    if pms.Booking_ID not in modified_shifts:
                        shifts.append(pms)
                    print("TEST %s " %pms)
                row = cursor.fetchone()

                #sys.exit()
        else:
            print("Sorry, i cannot read your sql file!")
        conn.close()
        print("MY SHIFTS: %s" %shifts)
        PayrollModifiedShifts.shifts_to_check = shifts
        return shifts

my_config = ProgramConfig("ShiftsAfterPayroll")
PayrollModifiedShifts.get_modified_shifts_after_payroll(my_config)
