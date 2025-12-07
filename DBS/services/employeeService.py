#import stuff here
from databases.employeeDatabase import employeeDatabase
from datetime import datetime
import bcrypt


def validate_login(dbconn, email, password):
    employeeDb = employeeDatabase(dbconn)
    #email exists
    if not employeeDb.check_email_exists(email):
        return "Not Found", -1
    
    #password matches email 
    if not check_password(email, password, employeeDb):
        return "Not Found", -1
   
    #Employee is valid, send role with emp_id
    emp_id = employeeDb.get_id_by_email(email)
    role = employeeDb.get_role_from_id(emp_id)
    return role, emp_id

def validate_employee_info(dbconn, Name,Role, ContactNumber, Email, Address, Password):
    employeeDb = employeeDatabase(dbconn)
    email_chk = contact_chk = pass_chk = True
    if employeeDb.check_email_exists(Email): #email exists in the database already
        email_chk = False
    if not (len(ContactNumber)==11) or not (ContactNumber.isdigit()) or employeeDb.check_contact_exists(ContactNumber): #11 digits, only digits and unique -> True
        contact_chk = False
    if not (len(Password) >= 7 and any(c.isdigit() for c in Password) and any(c.islower() for c in Password)):
        pass_chk = False

    if not (email_chk and contact_chk and pass_chk):
        return email_chk, contact_chk, pass_chk
    
    HireDate = datetime.now().strftime('%Y-%m-%d') #converts to datetime in compatible format to be  stored in the database

    encrypted_password = encrypt_password(Password)
    employeeDb.insert_employee_in_db(Name, Role, ContactNumber, Email, Address, HireDate, encrypted_password)
    return email_chk, contact_chk, pass_chk
 

def check_password( email, password, employeeDb):
    encrypted_password = employeeDb.get_password_from_email(email)
    return bcrypt.checkpw(password.encode('utf-8'), encrypted_password.encode('utf-8')) #returns true of false

def encrypt_password(password):
    bytes_pw = password.encode('utf-8')
    return bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
