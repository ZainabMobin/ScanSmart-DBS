class Bill:
    def __init__(self, BillID=None, CustomerName=None, Date=None, TotalAmount=None, EmployeeID=None):
        self.BillID = BillID
        self.CustomerName = CustomerName
        self.Date = Date
        self.TotalAmount = TotalAmount
        self.EmployeeID = EmployeeID


    def set_total_amount(self, TotalAmount): #set total amount of bill
        self.TotalAmount = TotalAmount