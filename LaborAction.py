class LaborAction:
    def __init__(self, dateFrom=None, dateTo=None, Employer=None, LaborOrg=None, State=None):
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.Employer = Employer
        self.LaborOrg = LaborOrg
        self.State = State
    def __str__(self):
        return "Employer: " + str(self.Employer) + "\nLabor Org: " + str(self.LaborOrg) + "\nState: " + str(self.State) + "\nStart Date: " + str(self.dateFrom) + "\nEnd Date: " + str(self.dateTo)