class LaborAction:
    def __init__(self, dateFrom=None, dateTo=None, Employer=None, LaborOrg=None, State_Name=None):
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.Employer = Employer
        self.LaborOrg = LaborOrg
        self.State_Name = State_Name
    def __str__(self):
        return "Employer: " + str(self.Employer) + "\nLabor Org: " + str(self.LaborOrg) + "\nState: " + str(self.State_Name) + "\nStart Date: " + str(self.dateFrom) + "\nEnd Date: " + str(self.dateTo)