import requests
import json
from config import ProgramConfig

class Api_Nominal():
    def __init__(self):
        self.ExternalId = ""
        self.ContactId = ""
        self.Nominal = ""
        self.NominalHoliday = ""
        self.WorkSchedule = ""
        self.FTE = ""
        self.IsExecutive = ""
        self.Suspension = ""
        self.SuspensionTypeId = ""
        self.SuspensionHours = ""
        self.DateFrom = ""
        self.DateTo = ""
        self.Id = ""

class Api_Person():
    def __init__(self):
        self.ExternalI= ''
        self.InternalCompanyId= ''
        self.CostCenterId= ''
        self.BusinessUnitId= ''
        self.FirstName= ''
        self.LastName= ''
        self.ShortName= ''
        self.InternalCompanyNumber= ''
        self.Phone= ''
        self.Mobile= ''
        self.CompanyId= ''
        self.CompanyName= ''
        self.CompanyRegistrationNumber= ''
        self.Email= ''
        self.NominalIds= []
        self.SuspensionIds= []
        self.Planned= ''
        self.ResourceId= ''
        self.ContactType= ''
        self.PlanningDepartmentGroupIds= []
        self.PlanningGroupIds= []
        self.ContactOccupation= ''
        self.Remarks= ''
        self.Function= ''
        self.Merge= ''
        self.Id= ''

class Api_PlanningItem():
    def __init__(self):
        self.ExternalId = ''
        self.PlanningDepartmentId = ''
        self.PlanningDepartmentGroupId = ''
        self.ProductionId = ''
        self.ProductionPhaseId = ''
        self.PlanningColumnId = ''
        self.DateFrom = ''
        self.DateTo = ''
        self.StartTime = ''
        self.EndTime = ''
        self.BreakTime = ''
        self.ActualStart = ''
        self.ActualEnd = ''
        self.ActualBreak = ''
        self.Locked = ''
        self.Visibility = ''
        self.Remarks = ''
        self.Color = ''
        self.ShiftId = ''
        self.PlanningTypeId = ''
        self.Type = ''
        self.RequestedContactId = ''
        self.CreateUser = ''
        self.CreateTimestamp = ''
        self.UpdateUser = ''
        self.UpdateTimestamp = ''
        self.Id = ''

    def push_to_dt(self, config):
        endpoint = "%splanningitem" %config.api_domain
        params = {
            'id': self.Id
        }
        planning_item_update_request = requests.put(endpoint, params=params, headers=config.api_headers, data=self.__dict__)
        print(planning_item_update_request.status_code)
        if planning_item_update_request.status_code != 200:
            config.logger.error("An error occured: %s" %planning_item_update_request.text)
            return False

        print("Update success")
        return True

    @staticmethod
    def get_all(config, paged_items = 0):
        list = []
        endpoint = "%splanningitem" %config.api_domain
        params = { 'PageSize': paged_items}
        planningitems_request = requests.get(endpoint, params = params, headers = config.api_headers)
        results = json.loads(planningitems_request.text)['PageItems']
        for result in results:
            pi = Api_PlanningItem()
            pi.__dict__ = result
            list.append(pi)

        return list

    def __str__(self):
        return "PIid: %s for production %s on %s created by %s" %(str(self.Id), self.ProductionId, self.DateFrom, self.CreateUser)

class Api_BookingItem():
    def __init__(self):
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

class Api_Asset():
    def __init__(self):
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

class Api_Shift():
    def __init__(self):
        self.ExternalId=''
        self.Name=''
        self.StartTime=''
        self.EndTime=''
        self.Break=''
        self.Id=''

class Api_Production():
    def __init__(self):
        self.ExternalId=''
        self.MasterId=''
        self.IsMaster=''
        self.UseMultiSourceBudget=''
        self.UseBudgetPhases=''
        self.UseWorkBudgetDetail=''
        self.UseOpenBudget=''
        self.LengthRemarks=''
        self.DefaultBudgetViewId=''
        self.AnalyticalCode=''
        self.CostCenterId=''
        self.BusinessUnitId=''
        self.FunctionalTypeId=''
        self.FunctionalTypeName=''
        self.Color=''
        self.ShortName=''
        self.EndDate=''
        self.StartDate=''
        self.NumberOfEpisodes=''
        self.EpisodeDuration=''
        self.Season=''
        self.ProductionTypeId=''
        self.ProductionTypeName=''
        self.InternalCompanyId=''
        self.InternalCompanyName=''
        self.InternalCompanyIsInternal=''
        self.InternalCompanyCompanyId=''
        self.InternalCompanyCompanyName=''
        self.CompanyId=''
        self.CompanyName=''
        self.CompanyAddress=''
        self.CompanyZip=''
        self.CompanyCity=''
        self.CompanyCountryCode=''
        self.IsInternal=''
        self.ShowInShortFilter=''
        self.Name=''
        self.SalesBudgetId=''
        self.ProductionBudgetId=''
        self.WorkBudgetId=''
        self.ChannelId=''
        self.ChannelName=''
        self.ChannelLogo=''
        self.CostPrefix=''
        self.Prefix=''
        self.Iban=''
        self.Bic=''
        self.CustomerInvoiceLogo=''
        self.FinancialYearId=''
        self.ResponsibleId=''
        self.Status=''
        self.ProgramMarker=''
        self.UseTaxShelter=''
        self.Phone=''
        self.CompanyContactId=''
        self.ChannelIdNumber=''
        self.CompanyContactFirstName=''
        self.CompanyContactLastName=''
        self.GeneralLedgerCostId=''
        self.GeneralLedgerRevenueId=''
        self.IbanValid=''
        self.FinancialYearFrom=''
        self.FinancialYearTo=''
        self.Categories=''
        self.DocumentIds=''
        self.CombinedName=''
        self.ResponsibleName=''
        self.ProductionStatusId=''
        self.ProductionStatusName=''
        self.Id=''

    def get_by_id(self, config = None, id = None):
        endpoint = "%sproduction" %config.api_domain
        params = { 'Id': id}
        production_request = requests.get(endpoint, params = params, headers = config.api_headers)
        self.__dict__ = json.loads(production_request.text)

        return self
