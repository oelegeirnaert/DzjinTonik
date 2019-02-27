import requests
import webbrowser
import json
import calendar
import datetime
import sys

class DzjinTonikObject(object):
    def __init__(self, config):
        self.config = config

    def reset_config(self, config):
        self.config = config

    def remove_config(self):
        self.config = None

    def logged_in(self, response, a_config):
        a_config.logger.info("Checking if you're logged into DT.")
        if "<title>DT - Login</title>" in response:
            strMessage = "You need to login into DzjinTonik first... Be sure to set the correct variables on top of this file!"
            print(strMessage)
            a_config.logger.error(strMessage)
            webbrowser.open(a_config.domain)
            sys.exit()
            return False
        elif "<title>" in response:
            print(response)
            print("An other error occured... Please read the lines above! SUGGESTION: Is your model correct? Are you sending an ID?")
            return False
        return True

    def post_json_obj(self, url):
        self.config.logger.info('Update data to url: %s' %(url))
        self.config.logger.info("Data we'll send in post: %s" %self.__dict__)

        my_config = self.config
        cookies = self.config.cookies
        headers = self.config.headers
        self.config = None

        r = requests.post(url, cookies=cookies, headers=headers, data=self.__dict__)
        if self.logged_in(r.text, my_config) and r.status_code == 200:
            my_config.logger.debug('Data we got returned: \n %s' %r.text)
            if r.status_code == 200:
                myjson = json.loads(r.text)
                self.__dict__ = myjson['Data'][0]
                self.config = my_config
                return True
            else:
                self.config.logger.error('Cannot post to url %s with data %s ... ERROR: %s' %(url, data, r.text))
                return False

    def get_json_obj(self, url):
        self.config.logger.debug('Get data from: %s' %(url))

        my_config = self.config #before we get the data, we'll store the config.
        cookies = self.config.cookies
        headers = self.config.headers
        self.config = None

        r = requests.post(url, cookies = cookies, headers=headers, data=self.__dict__)
        my_config.logger.debug('Data we got returned: \n %s' %r.text)
        if self.logged_in(r.text, my_config) and r.status_code == 200:
            self.__dict__ = json.loads(r.text)
            self.config = my_config
            return True
        return False

class Person(DzjinTonikObject):
    def __init__(self, config, id=None):
        super().__init__(config)
        self.Username = ''
        self.Password = ''
        self.FirstName = ''
        self.LastName = ''
        self.FullName = ''
        self.LanguageId = ''
        self.IsActive = ''
        self.IsNewVersionUploaded = ''
        self.LanguageName = ''
        self.InternalCompanyId = ''
        self.DefaultInternalCompanyId = ''
        self.DefaultInternalCompanyName = ''
        self.ContactId = ''
        self.ContactPhoto = ''
        self.IsHolidayApprover = ''
        self.AllowedOutlookIntegration = ''
        self.ApplicationRoles = ''
        self.ApplicationRoleNames = ''
        self.CreateUser = ''
        self.CreateTimestamp = ''
        self.UpdateUser = ''
        self.UpdateTimestamp = ''
        self.Id = id
        self.MainApplicationRoles = ''
        self.CreateUpdateUserInfo = ''

    def get_full_name(self):
        return "%s %s (%s)" %(self.FirstName, self.LastName, self.Id)

    def set_password(self, password):
        self.Password = password

    def get_from_dt(self):
        if self.get_json_obj(self.config.person_get):
            return True
        return False

    def send_to_dt(self):
        if self.post_json_obj(self.config.person_update):
            return True
        return False

class Contact(DzjinTonikObject):
    def __init__(self, config, Id=None):
        super().__init__(config)
        self.Province = ''
        self.LinkToCrewList = ''
        self.NotActive = ''
        self.EyeColor = ''
        self.HairLength = ''
        self.HairColor = ''
        self.BodyType = ''
        self.Weight = ''
        self.Height = ''
        self.Gender = ''
        self.Biography = ''
        self.HolidayApproverId = ''
        self.HolidayRequestInfo = ''
        self.ContactType = ''
        self.FirstName = ''
        self.LastName = ''
        self.ShortName = ''
        self.ArtistName = ''
        self.FullName = ''
        self.ResourceId = ''
        self.ResourceName = ''
        self.Function = ''
        self.AllowDoubleBooking = ''
        self.Phone = ''
        self.Mobile = ''
        self.InternalPhone = ''
        self.Email = ''
        self.SecondEmail = ''
        self.Website = ''
        self.OfficeLocation = ''
        self.GeneralRemark = ''
        self.Importance = ''
        self.Roles = ''
        self.RoomNumber = ''
        self.CountryCode = ''
        self.Street = ''
        self.Zip = ''
        self.City = ''
        self.ResourceDefaultTariff = ''
        self.ResourceCostPerDay = ''
        self.ResourceCostPerHour = ''
        self.InternalCostProductionId = ''
        self.InternalCost = ''
        self.InactiveFrom = ''
        self.IncludeInActuals = ''
        self.KeepPrivate = ''
        self.HasToConfirmPlanning = ''
        self.ExpenseNoteAllowed = ''
        self.Photo = ''
        self.UseInEmployeePlan = ''
        self.PlanningGroups = ''
        self.AuditionGroups = ''
        self.SideSkills = ''
        self.DriversLicenseFlags = ''
        self.RolesText = ''
        self.LanguageId = ''
        self.CompanyId = ''
        self.CompanyName = ''
        self.CompanyAddress = ''
        self.CompanyZip = ''
        self.CompanyCity = ''
        self.CompanyCountryCode = ''
        self.CompanyCountryId = ''
        self.CompanyRegistrationNumber = ''
        self.CompanyVat = ''
        self.CompanyEmail = ''
        self.CompanyPhone = ''
        self.CompanyWebsite = ''
        self.AgentId = ''
        self.DefaultInternalCompanyId = ''
        self.CostCenterId = ''
        self.BusinessUnitId = ''
        self.ContactHRId = ''
        self.HRRemarks = ''
        self.ICEinfo = ''
        self.DateOfBirth = ''
        self.PlaceOfBirth = ''
        self.DimonaNumber = ''
        self.SSN = ''
        self.Nationality = ''
        self.MaritalStatus = ''
        self.MaritalStatusDate = ''
        self.NamePartner = ''
        self.DateOfBirthPartner = ''
        self.OccupationPartner = ''
        self.RevenuePartner = ''
        self.Dependents = ''
        self.Education = ''
        self.TypeOfContract = ''
        self.DateCurrentContract = ''
        self.DateContractEnd = ''
        self.CareerSeniority = ''
        self.IdentityCardNumber = ''
        self.Iban = ''
        self.Age = ''
        self.PayrollTaxId = ''
        self.PayrollTaxFreeText = ''
        self.SalaryScale = ''
        self.GrossMonthlyWage = ''
        self.LumpExpenses = ''
        self.EmploymentStreet = ''
        self.EmploymentZip = ''
        self.EmploymentCity = ''
        self.JointCommittee = ''
        self.SocialSubscriptionType = ''
        self.SocialSubscriptionKm = ''
        self.MealTickets = ''
        self.MealTicketsEmployeeContribution = ''
        self.BudgetDailyRate = ''
        self.HourlyRate = ''
        self.DailyCost = ''
        self.TotalYearlyCost = ''
        self.TotalHourlyCost = ''
        self.DocumentIds = ''
        self.DocumentHRIds = ''
        self.IsEmployee = ''
        self.CountryId = ''
        self.CountryName = ''
        self.InternalCompanyNumber = ''
        self.IbanValid = ''
        self.IsProfileApplicationLocked = ''
        self.ProfileApplicaitonSequence = ''
        self.CreateUser = ''
        self.CreateTimestamp = ''
        self.UpdateUser = ''
        self.UpdateTimestamp = ''
        self.Id = Id

    def get_from_dt(self):
        print(self.config.contact_get)
        if self.get_json_obj(self.config.contact_get):
            return True
        return False

    def send_to_dt(self):
        if self.post_json_obj(self.config.contact_update):
            return True
        return False

    def get_full_name(self):
        return "%s %s" %(self.FirstName, self.LastName)

    def get_link(self):
        return "%s/Contact?ContactId=%s" %(self.config.domain, self.Id)


class PlanBalanceGrid(DzjinTonikObject):

    def __init__(self, config , row, fixed):
        super().__init__(config)
        self.config.logger.info("Currently handling the recup hours of %s" %row["Name"])
        self.ContactId = int(row["ContactId"])
        self.Date = self.toISOtime(int(row["Year"]), int(row["Month"]))
        self.Balance = float(row["Balance"])
        self.Fixed = fixed

    def toISOtime(self, year, month):
        self.config.logger.debug("Create last day of the month from year %s and month %s" %(year, month))
        c = calendar.monthrange(year,month)
        self.config.logger.debug(c)
        dt = datetime.datetime(year=year, month=month, day=c[1])
        return dt.isoformat()

    def send_to_dt(self):
        if self.post_json_obj(self.config.set_recup_hours):
            return True
        return False
