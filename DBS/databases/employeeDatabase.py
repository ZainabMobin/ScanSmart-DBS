class employeeDatabase:
    def __init__(self, dbconn):
        self.dbconn = dbconn

    def check_email_exists(self, email):
        cursor = self.dbconn.cursor()
        query = "SELECT 1 FROM Employee WHERE Email = %s LIMIT 1"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return True if result else False 


    def get_password_from_email(self, email):
        cursor = self.dbconn.cursor()
        query = "SELECT password FROM Employee WHERE Email = %s LIMIT 1"
        cursor.execute(query, (email,))
        encrypted_password = cursor.fetchone()
        cursor.close()
        return encrypted_password[0] if encrypted_password else None

    def check_contact_exists(self, ContactNumber):
        cursor = self.dbconn.cursor()
        query = "SELECT 1 FROM Employee WHERE ContactNumber = %s LIMIT 1"
        cursor.execute(query, (ContactNumber,))
        result = cursor.fetchone()
        cursor.close()
        return True if result else False
        
    def get_id_by_email(self, email):
        cursor = self.dbconn.cursor()
        query = "SELECT EmployeeID FROM Employee WHERE Email = %s LIMIT 1"
        cursor.execute(query, (email,))
        emp_id = cursor.fetchone()
        cursor.close()
        return emp_id[0] if emp_id else None #need to return tuple back to the service layer

    def get_role_from_id(self, emp_id):
        cursor = self.dbconn.cursor()
        query = "SELECT Role FROM Employee WHERE EmployeeID = %s LIMIT 1"
        cursor.execute(query, (emp_id,))
        role = cursor.fetchone()
        cursor.close()
        return role[0] if role else None


    def get_name_by_id(self, empid, role=None):
        cursor = self.dbconn.cursor()
        if role == "Cashier":
            query = "SELECT Name FROM Employee WHERE EmployeeID = %s AND Role = 'Cashier' LIMIT 1"
        else:
            query = "SELECT Name FROM Employee WHERE EmployeeID = %s LIMIT 1"
        cursor.execute(query, (empid,)) 
        result = cursor.fetchone()
        cursor.close()
        return result [0] if result else None
    

    def insert_employee_in_db(self, Name, Role, ContactNumber, Email, Address, HireDate, encrypted_password):
        cursor = self.dbconn.cursor()
        query = "INSERT INTO Employee(Name, Role, ContactNumber, Email, Address, HireDate, Password) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (Name, Role, ContactNumber, Email, Address, HireDate, encrypted_password))
        self.dbconn.commit() #saves changes in the database
        cursor.close()
    
    #get all employeed detail from database
    def get_employee_details(self):
        cursor = self.dbconn.cursor()
        query = "SELECT EmployeeID,Name,Role,ContactNumber,Email FROM employee"
        cursor.execute(query)
        result = cursor.fetchall()  # fetch all results
        cursor.close()              # close cursor
        return result
        # return cursor.fetchall()