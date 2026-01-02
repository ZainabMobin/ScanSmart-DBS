#fetches info from the database
class billDatabase:
    def __init__(self,dbconn): 
        self.dbconn = dbconn

    def save_bill(self, CustomerName, Date, TotalAmount, EmployeeID): #saves bill in database
        cursor = self.dbconn.cursor()
        query = "INSERT INTO Bill (CustomerName, Date, TotalAmount, EmployeeID) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (CustomerName, Date, TotalAmount, EmployeeID,))
        self.dbconn.commit() #saves changes in the database
        cursor.close()
        
    def save_bill_details(self, BillID, ProdID, QuantitySold, UnitPrice, TotalAmount): #saves bill details in database
        cursor = self.dbconn.cursor()
        query = "INSERT INTO BillDetail (BillID, ProdID, QuantitySold, UnitPrice, TotalAmount) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (BillID, ProdID, QuantitySold, UnitPrice, TotalAmount,))
        self.dbconn.commit() #saves changes in the database
        cursor.close()

    #gets ALL stored bills from the database if no parameter is passed, else gets the bills of a specific employee
    def get_bills(self, emp_id = None):
        cursor = self.dbconn.cursor()
        if emp_id == None:
            query = "SELECT * FROM Bill"
            cursor.execute(query)
        else:
            query = "SELECT * FROM Bill WHERE EmployeeID = %s"
            cursor.execute(query, (emp_id,))
        return cursor.fetchall()

 
     #gets ALL stored bill Details from the database
    def get_bill_details(self):
        cursor = self.dbconn.cursor()
        query = "SELECT * FROM BillDetail"
        cursor.execute(query)
        return cursor.fetchall()
    

    def get_latest_bill_id(self):
        cursor = self.dbconn.cursor()
        query = "SELECT BillID FROM Bill ORDER BY BillID DESC LIMIT 1"
        cursor.execute(query)
        billId = cursor.fetchone()
        return billId[0] if billId else None
    
    def get_bill_detail_admin(self,billid):  #using join
        cursor=self.dbconn.cursor()
        query="""
            SELECT bd.ProdID, p.Name, bd.QuantitySold, bd.UnitPrice, bd.TotalAmount
            FROM BillDetail bd
            JOIN Product p ON bd.ProdID = p.ProdID
            WHERE bd.BillID = %s"""
        cursor.execute(query,(billid,))
        return cursor.fetchall()
    