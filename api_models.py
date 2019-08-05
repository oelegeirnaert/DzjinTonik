import requests
import json

from config import ProgramConfig

class IdRequired(Exception):
    pass

class EndpointRequired(Exception):
    pass

class MethodException(Exception):
    pass

class RequestException(Exception):
    pass

class IdMustBeNull(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Api_Abstract_Model():
    def do_request(self, action, config, params=None):

        if self.endpoint is None:
            raise EndpointRequired("Please provide an endpoint")

        request_endpoint = "%s%s" %(config.api_domain, self.endpoint)

        if ("GET" in action.upper() or "PUT" in action.upper()) and self.Id is None:
            raise IdRequired("Please provide an ID for your %s-object..." %type(self).__name__)

        if params is None:
            params = {
                'id': self.Id
                }

        config.logger.debug("%s action to: %s" %(action, request_endpoint))

        if action.upper() == 'GET':
            r = requests.get(request_endpoint, params=params, headers=config.api_headers)
        elif action.upper() == 'PUT':
            config.logger.debug(self.__dict__)
            r = requests.put(request_endpoint, params=params, headers=config.api_headers, data=self.__dict__)
        elif action.upper() == 'POST':
            config.logger.debug(self.__dict__)
            r = requests.post(request_endpoint, headers=config.api_headers, data=self.__dict__)
        else:
            raise MethodException("Please choose a right method...")

        config.logger.debug("STATUSCODE: %s" %r.status_code)

        if r.status_code == 200 or r.status_code == 201 :
            self.__dict__ = json.loads(r.text)
            config.logger.debug(self.__dict__)
            return self

        if r.status_code == 404:
            raise ItemDoesNotExist("A %s with this paramaters %s does not exist." %(type(self).__name__, params))

        config.logger.info(r.text)
        raise RequestException("Your request was not successful...")

    @classmethod
    def get_by_id(cls, config, id):

        if id is None:
            return IdRequired("We need an id in order to get a %s-item." %cls.__name__)
        params = {
            'id': id
            }
        return cls().do_request("get", config, params)

    def update(self, config):
        return self.do_request("put", config)

    def create(self, config):
        config.logger.debug("Trying to create...")
        if self.Id is not None:
            config.logger.debug("ID must be null!")
            return IdMustBeNull("When creating a new object, the ID of your %s-object must be NULL instead of %s" %(type(self).__name__, self.Id))

        return self.do_request("post", config)

    @classmethod
    def get_all(cls, config, paged_items = 0):
        print(cls.endpoint)
        params = {
            'pagesize' : paged_items
        }
        request_endpoint = "%s%s" %(config.api_domain, cls.endpoint)

        r = requests.get(request_endpoint, params=params, headers=config.api_headers)
        if r.status_code != 200:
            return RequestException("Your request to get all the % items failed." %type(self).__name__)

        items = json.loads(r.text)['PageItems']
        total_items = json.loads(r.text)['TotalCount']
        list = []
        for item in items:
            item_cls = cls()
            item_cls.__dict__ = item
            list.append(item_cls)
        return list, total_items


class Api_Nominal(Api_Abstract_Model):
    endpoint = 'nominal'
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

    def __str__(self):
        return "Nominal %s with Id %s for contact: %s" %(self.Nominal, self.Id, self.ContactId)

    def get_by_resourceid(self, config, resourceId):
        nominals = super().do_request("GET", config, params={'resourceid': resourceId})
        nominal_list = []
        for nominal in nominals.PageItems:
            current_nominal = Api_Nominal()
            current_nominal.__dict__ = nominal
            nominal_list.append(current_nominal)

        print("%s nominal(s) found for resourceid: %s" %(len(nominal_list),resourceId))
        return nominal_list

    @staticmethod
    def get_active_nominal_for_date(self, search_date):
        for i in self:
            print(i)


class Api_Person(Api_Abstract_Model):
    endpoint = 'person'
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


class Api_PlanningItem(Api_Abstract_Model):
    endpoint = 'planningitem'
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

    '''
    made it available in the abstract class
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
    '''

    def __str__(self):
        return "PIid: %s for production %s on %s created by %s" %(str(self.Id), self.ProductionId, self.DateFrom, self.CreateUser)


class Api_BookingItem(Api_Abstract_Model):
    endpoint = 'booking'
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


class Api_Asset(Api_Abstract_Model):
    endpoint = 'asset'
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


class Api_Shift(Api_Abstract_Model):
    endpoint = 'shift'
    def __init__(self):
        self.ExternalId=''
        self.Name=''
        self.StartTime=''
        self.EndTime=''
        self.Break=''
        self.Id=''


class Api_Production(Api_Abstract_Model):
    endpoint = 'production'
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

    def __str__(self):
        return "%s (id: %s)" %(self.Name, self.Id)


class Api_Holiday(Api_Abstract_Model):
    endpoint = 'holiday'
    def __init__(self):
        self.ExternalId=''
        self.ResourceId=''
        self.DateFrom=''
        self.DateTo=''
        self.Type=''
        self.TransactionType=''
        self.Status=''
        self.RoleId=''
        self.Amount=''
        self.BookingId=''
        self.Remarks=''
        self.ExternalCode=''
        self.Id=''

    def __str__(self):
        return "ResourceID: %s - From %s to %s for BookingId: %s - Transaction: %s"%(self.ResourceId, self.DateFrom, self.DateTo, self.BookingId, self._get_transaction_type_name())

    def _get_transaction_type_name(self):
        types = ['Add', 'Substract']
        return types[int(self.TransactionType)]

    def get_by_bookingid(self, config, bookingid):
        config.logger.debug("Try to get holiday from booking with id %s " %bookingid)
        my_response = super().do_request("GET", config, params={'bookingid':bookingid})
        print(my_response.__dict__)
        if my_response.TotalCount==1:
            config.logger.debug("OK, one item found!")
            self.__dict__ = my_response.PageItems[0]
            config.logger.debug("MY DICT")
            print(self.__dict__)
            return self
        else:
            raise Exception("Multiple items found!")

        return None

    def create(self, config):
        print("Trying to create a holiday item.")
        if self.ResourceId is None or self.ResourceId == '':
            raise Exception("A ResourceId is required.")

        if self.DateFrom is None or self.DateFrom == '':
            raise Exception("A DateFrom is required.")

        if self.Type is None or self.Type == '':
            raise Exception("A Type is required.")

        if self.TransactionType is None or self.TransactionType == '':
            raise Exception("A TransactionType is required.")

        if self.Status is None or self.Status == '':
            raise  Exception("A Status is required.")

        if self.RoleId is None or self.RoleId == '':
            raise Exception("A RoleId is required.")

        if self.Amount is None or self.Amount == '':
            raise Exception("An Amount is required.")

        print("Tests passed!")
        config.logger.debug("Tests passed, create it.")
        return super().create(config)


class Api_PlanningDepartmentGroup(Api_Abstract_Model):
    endpoint = 'planningdepartmentgroup'
    def __init__(self):
        self.ExternalId = ''
        self.PlanningDepartmentId = ''
        self.Name = ''
        self.Sequence = ''
        self.PlanningDepartmentGroupResourceIds = []
        self.Id = ''

    def __str__(self):
        return "Planning Department Group: %s (Id: %s)" %(self.Name, self.Id)


class Api_ContactPlanningGroup(Api_Abstract_Model):
    endpoint = 'contactplanninggroup'
    def __init__(self):
        self.ContactId = ''
        self.ContactFirstName = ''
        self.ContactLastName = ''
        self.GroupId = ''
        self.GroupName = ''
        self.GroupType = ''
        self.From = ''
        self.To = ''
        self.ContactFullName = ''
        self.Id = ''

    def __str__(self):
        return "Contact Planning Group: %s (Id: %s - %s)" %(self.GroupName, self.Id, self._get_type_name())

    def _get_type_name(self):
        types = ['Contact','Asset','Company','Location', 'HR']
        return types[int(self.GroupType)]
