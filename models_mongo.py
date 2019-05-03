import datetime

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

class Freelancer(object):
    def __init__(self, Id, FullName, Username, Password, AccountStatus, copy_from_person_id):
        self.Id = Id
        self.FullName = FullName
        self.Username = Username
        self.Password = Password
        self.AccountStatus = AccountStatus
        self.UpdateSuccess = False
        self.CreatedOn = datetime.datetime.now()
        self.CopiedFrom = copy_from_person_id

    def update_success(self, status):
        self.UpdateSuccess = status

class ContactApprover(object):
    def __init__(self, Id, FullName, DepartmentGroup, Department, ApproverID, ApproverFullName):
        self.Id = Id
        self.FullName = FullName
        self.Department = Department
        self.DepartmentGroup = DepartmentGroup
        self.ApproverID = ApproverID
        self.ApproverFullName = ApproverFullName
        self.UpdatedOn = datetime.datetime.now()
        self.UpdateSuccess = False

    def update_success(self, status):
        self.UpdateSuccess = status

class MongoHRGroup(object):
    def __init__(self, item):
        self.ContactId = item[0]
        self.FullName = ""
        self.Blox = item[1]
        self.Is_Journalist = item[2]
        self.Is_TV = item[3]
        self.Is_Radio = item[4]
        self.Book_Payroll = item[5]
        self.Book_Only_Holidays = item[6]
        self.Explicit_Supplements = item[7]
        self.Apply_10_Percent = item[8]
        self.CreatedOn = datetime.datetime.now()
