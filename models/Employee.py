class Employee: 
    def __init__(self, empID, name):
        self.empID = empID
        self.name = name

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.empID
