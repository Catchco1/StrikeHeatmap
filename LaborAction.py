class LaborAction:
    def __init__(self, dateFrom, dateTo, Employer, LaborOrg, State):
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.Employer = Employer
        self.LaborOrg = LaborOrg
        self.State = State
    def __str__(self):
        return "Employer: " + self.Employer + "\nLabor Org: " + self.LaborOrg + "\nState: " + self.State + "\nStart Date: " + self.dateFrom + "\nEnd Date: " + self.dateTo