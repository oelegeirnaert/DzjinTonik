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
