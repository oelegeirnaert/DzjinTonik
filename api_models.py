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
