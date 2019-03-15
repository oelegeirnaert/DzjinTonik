import shutil
import requests
import json
import calendar
import datetime
import sys

import dt_util

class DzjinTonikObject(object):
    def __init__(self, config):
        self.config = config

    def reset_config(self, config):
        self.config = config

    def remove_config(self):
        self.config = None

    def post_json_obj(self, url, data=None):
        self.config.logger.info('Update data to url: %s' %(url))
        self.config.logger.info("Data we'll send in post: %s" %self.__dict__)

        my_config = self.config
        cookies = self.config.cookies
        headers = self.config.headers
        self.config = None

        if data is None:
            data=self.__dict__

        r = requests.post(url, cookies=cookies, headers=headers, data=data)
        if dt_util.logged_in(r.text, my_config) and r.status_code == 200:
            my_config.logger.debug('Data we got returned: \n %s' %r.text)
            if r.status_code == 200:
                myjson = json.loads(r.text)
                if len(myjson['Data']) == 0:
                    print("No Results...")
                    return False
                else:
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
        if dt_util.logged_in(r.text, my_config) and r.status_code == 200:
            self.__dict__ = json.loads(r.text)
            self.config = my_config
            return True
        return False

    def search_in_dt(self, url, data):
        #self.config.logger("Search for %s" %name)
        if self.post_json_obj(url, data):
            print(self.__dict__)
            return True
        return False

class Person(DzjinTonikObject):
    def __init__(self, config=None, id=None):
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
        self.ExternalId = ''

    def __str__(self):
        return self.FirstName

    def get_contactId(self):
        return self.ContactId

    def get_full_name(self):
        return "%s %s (%s)" %(self.FirstName, self.LastName, self.Id)

    def set_password(self, password):
        self.Password = password

    def get_from_dt(self):
        if self.get_json_obj(self.config.domain + "/Person/Get"):
            return True
        return False

    def send_to_dt(self):
        if self.post_json_obj(self.config.domain + "/Person/Update"):
            return True
        return False

    def from_json(self, json):
        self.config = None
        self.__dict__ = json

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

    def download_picture(self):
        picture_url = "%s/Upload/Download?FileName=%s" %(self.config.domain, self.Photo)
        store_picture ="%s%s" %(self.config.store_contact_pictures_in, self.Photo)
        print("STORE PICTURE IN: %s" %store_picture)
        r = requests.get(picture_url, headers = self.config.headers, cookies = self.config.cookies, stream=True)
        with open(store_picture, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
        del r
        print(picture_url)

    def get_link_from_dt(self):
        return "%s/Contact?contactId=%s" %(self.config.domain, self.Id)

    def get_from_dt(self):
        if self.get_json_obj(self.config.domain + '/Contact/Get'):
            return True
        return False

    def send_to_dt(self):
        if self.post_json_obj(self.config.domain + "/Contact/Update"):
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
        if self.post_json_obj(self.config.domain + '/PercentageReportPlanBalance/Create'):
            return True
        return False

class TimeSheetDataResource(DzjinTonikObject):
    def __init__(self, config):
        super().__init__(config)
        self.sort=""
        self.group=""
        self.filter=""
        self.FromDate=""
        self.ToDate=""
        self.PlanningDepartmentId=""
        self.PlanningDepartmentGroupIds= []
        self.ProgramId=""
        self.ProgramMasterId=""
        self.PlanMode=""
        self.BookingMode=""
        self.ResourceIsNull=""
        self.ResourceId=""
        self.SchedulerGroupSearch=""
        self.PageNumber=""
        self.PageSize=""
        self.BookingColorScheme=""
        self.ResourceTypes = []
        self.ResourceTypes= []
        self.SpecificPersonId=""
        self.PostProductionAssets=""
        self.SpecificAssetId=""
        self.PlanningItemTitle=""
        self.PlanningItemVisibility=""
        self.RequestedById=""
        self.BookingStatuses = []
        self.HasOvertime=""
        self.ActualDiffers=""
        self.BookingCompanyId=""
        self.ShowHRInformation=""
        self.DatesTop=""
        self.HasBookingFilterApplied=""
        self.NavigateView=""
        self.TypeNotEqual=""
        self.EnableEBookingForActiveIndividuals=""
        self.EBookingContractStatus=""
        self.Page=""
        self.SearchTextOverview=""
