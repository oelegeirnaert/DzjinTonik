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

    def str_to_class(str):
        return getattr(sys.modules[__name__], str)

    def reset_config(self, config):
        self.config = config

    def remove_config(self):
        self.config = None

    def post_json_obj(self, url, data=None):
        self.config.logger.info('Update data to url: %s' %(url))


        my_config = self.config
        cookies = self.config.cookies
        headers = self.config.headers


        if data is None:
            data=self.__dict__

        print("Data we'll send in post: %s" %data)
        self.config.logger.info("Data we'll send in post: %s" %data)

        self.config = None
        r = requests.post(url, cookies=cookies, headers=headers, data=data)
        print(r.text)
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

    def get_json_obj(self, url, data=None):
        self.config.logger.debug('Get data from: %s' %(url))

        my_config = self.config #before we get the data, we'll store the config.
        cookies = self.config.cookies
        headers = self.config.headers
        self.config = None

        if data is None:
            data=self.__dict__

        r = requests.post(url, cookies = cookies, headers=headers, data=data)
        my_config.logger.debug('Data we got returned: \n %s' %r.text)
        if dt_util.logged_in(r.text, my_config) and r.status_code == 200:
            print(r.text)
            #self.__dict__ = json.loads(r.text)['Data'][0]
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
        return "%s %s" %(self.FirstName, self.LastName)

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

    def __str__(self):
        return self.FullName


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

class HRGroup(DzjinTonikObject):

    def __init__(self, config , id=None):
        super().__init__(config)
        self.config.logger.info("Currently handling the groups for hrgroupid: %s" %id)
        self.ContactId = ''
        self.ContactFirstName = ''
        self.ContactLastName = ''
        self.GroupId = ''
        self.GroupName = ''
        self.GroupType = ''
        self.From = ''
        self.To = ''
        self.ContactFullName = ''
        self.CreateUser = ''
        self.CreateTimestamp = datetime.datetime.now()
        self.UpdateUser = ''
        self.UpdateTimestamp = datetime.datetime.now()
        self.Id = id

    def delete_from_dt(self):
        if self.post_json_obj(self.config.domain + '/ContactPlanningGroup/Delete', {'Id':self.Id}):
            return True
        return False

    def send_to_dt(self):
        if self.post_json_obj(self.config.domain + '/ContactPlanningGroup/Create'):
            return True
        return False

    def get_from_dt(self):
        data = {'GroupType':4, 'Id':self.Id}
        if self.get_json_obj(self.config.domain + '/ContactPlanningGroup/Read', data=data):
            return True
        return False

    def __str__(self):
        return "- %s is in HR Group %s" %(self.ContactFullName, self.GroupName)

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

class Nominal(DzjinTonikObject):
    def __init__(self, config, contactid = None, nominalid=None, **kwargs):
        super().__init__(config)
        if contactid is None:
            self.ContactId =  ''
        else:
            self.ContactId = contactid

        self.NominalSchemeType =  ''
        self.FullTimeRatio =  ''
        self.IsExecutive =  ''
        self.ContractHours =  ''
        self.DateFrom =  ''
        self.DateTo =  ''
        self.Remarks =  ''
        self.Suspension =  ''
        self.SuspensionTypeId =  ''
        self.SuspensionTypeName =  ''
        self.SuspensionHours =  ''
        self.DaysPerWeek =  ''
        self.DailyNominal =  ''
        self.HolidayNominal =  ''
        self.MondayNominal =  ''
        self.TuesdayNominal =  ''
        self.WednesdayNominal =  ''
        self.ThursdayNominal =  ''
        self.FridayNominal =  ''
        self.SaturdayNominal =  ''
        self.SundayNominal =  ''
        self.ContactType =  ''
        self.DefaultInternalCompanyId =  ''
        self.DefaultRoleId =  ''
        self.CreateUser =  ''
        self.CreateTimestamp =  ''
        self.UpdateUser =  ''
        self.UpdateTimestamp =  ''
        if nominalid is not None:
            self.Id = nominalid
        else:
            self.Id =  ''

    def get_from_dt(self):
        data = {'id':self.Id}
        if self.get_json_obj(self.config.domain + '/Nominal/Read', data=data):
            return True
        return False

    def send_to_dt(self):
        if self.post_json_obj(self.config.domain + '/Nominal/Update'):
            return True
        return False

class CategoryValue(DzjinTonikObject):
    def __init__(self, config, id = None, **kwargs):
        super().__init__(config)
        self.Sequence = ''
        self.ParentId = ''
        self.CostPerDay = ''
        self.CostType = ''
        self.Pieces = ''
        self.PlanningItemId = ''
        self.LinkedPlanningItemId = ''
        self.PlanningItemType = ''
        self.PlanningItemVisibility = ''
        self.Title = ''
        self.CategoryId = ''
        self.CategoryName = ''
        self.ResourceId = ''
        self.ResourceName = ''
        self.ResourceHasToConfirmPlanning = ''
        self.CategoryTypeName = ''
        self.CategoryTypeId = ''
        self.CategorySystemImpact = ''
        self.CategoryLockPastAbsences = ''
        self.Val = ''
        self.Confirmed = ''
        self.IsEmployee = ''
        self.ProgramId = ''
        self.ProgramName = ''
        self.Date = ''
        self.ToDate = ''
        self.ShiftId = ''
        self.DepartmentId = ''
        self.DepartmentName = ''
        self.DepartmentGroupId = ''
        self.DepartmentGroupName = ''
        self.CompanyId = ''
        self.CompanyName = ''
        self.Kilometers = ''
        self.StartTime = ''
        self.EndTime = ''
        self.BreakTime = ''
        self.ActualStart = ''
        self.ActualEnd = ''
        self.ActualBreak = ''
        self.Overtime = ''
        self.ActualWorkingTime = ''
        self.PlannedWorkingTime = ''
        self.Log = ''
        self.NeedsEmailConfirmation = ''
        self.IncludeInActuals = ''
        self.Revenue = ''
        self.CostCenterId = ''
        self.BusinessUnitId = ''
        self.InternalCompanyId = ''
        self.TotalCost = ''
        self.ExternalCode = ''
        self.ResourceContactId = ''
        self.ResourceAssetId = ''
        self.ResourceImage = ''
        self.CategoryTypeText = ''
        self.DetailText = ''
        self.HasRights = ''
        self.IsActive = ''
        self.EBookingContractId = ''
        self.EBookingContractStatus = ''
        self.CreateUser = ''
        self.CreateTimestamp = ''
        self.UpdateUser = ''
        self.UpdateTimestamp = ''
        self.Id = id
        self.ResourceImageUrl = ''
        self.EBookingContractStatusIconClass = ''
        self.EBookingContractUrl = ''
        self.EbookingStatusTitle = ''

    def get_from_dt(self):
        data = {'id':self.Id}
        if self.get_json_obj(self.config.domain + '/CategoryValue/Get', data=data):
            return True
        return False

    def send_to_dt(self):
            if self.post_json_obj(self.config.domain + '/CategoryValue/Update'):
                return True
            return False

class BookingItem(DzjinTonikObject):
    def __init__(self, config):
        super().__init__(config)
        self.ExternalId=''
        self.PlanningItemId=''
        self.CategoryTypeId=''
        self.RoleId=''
        self.ResourceId=''
        self.CostPerDay=''
        self.BookingStatus=''
        self.Sequence=''
        self.Pieces=''
        self.Description=''
        self.StartTime=''
        self.EndTime=''
        self.BreakTime=''
        self.ActualStart=''
        self.ActualEnd=''
        self.ActualBreak=''
        self.CompanyId=''
        self.Kilometers=''
        self.InitialPlannedFrom=''
        self.InitialPlannedTo=''
        self.InitialBreakTime=''
        self.Revenue=''
        self.IncludeInActuals=''
        self.CostCenterId=''
        self.BusinessUnitId=''
        self.InternalCompanyId=''
        self.Overtime=''
        self.Duration=''
        self.CreateUser=''
        self.CreateTimestamp=''
        self.UpdateUser=''
        self.UpdateTimestamp=''
        self.Id=''

class Asset(DzjinTonikObject):
    def __init__(self, config):
        super().__init__(config)
        self.ExternalI=''
        self.CostCenterId=''
        self.BusinessUnitId=''
        self.Name=''
        self.Planned=''
        self.InternalCompanyId=''
        self.IsInactive=''
        self.Cost=''
        self.ResourceId=''
        self.RoleId=''
        self.PlanningDepartmentGroupIds=''
        self.PlanningGroupIds=''
        self.Id=''

    
