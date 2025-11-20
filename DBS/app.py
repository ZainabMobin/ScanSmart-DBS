import streamlit as st
from databases.mysql_connector import connect_db
from services.employeeService import validate_login, validate_cashier_info
from services.billService import get_bills_from_db, scan_bill, checkout_billing, change_quantity, get_total_from_details
from services.scannerService import ScannerService #class with functions for camera control (used in both admin and cashier)
from services.productService import scan_product_barcode, add_product, update_quantity_after_scan
import time

# Global DB connection, injected in each layer as we go down the path up to the database layer.
dbconn = connect_db()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'  # initial landing page

#create scanner object
if 'scanner' not in st.session_state:
    st.session_state.scanner = ScannerService()

if 'seen_products' not in st.session_state:
    st.session_state.seen_products = set()

#set to false, true only when cashier starts billing
if 'billing_active' not in st.session_state:
    st.session_state.billing_active = False


if 'bill_detail_list' not in st.session_state:
    st.session_state.bill_detail_list = []

if 'bool_checkout' not in st.session_state:
    st.session_state.bool_checkout = True
# Function to switch pages (from login to the role-based page with exclusive functions)
def go_to(page_name):
    st.session_state.page = page_name

#responsible for logging out to the main welcome page
def logout():
    st.session_state.page = 'landing'
    st.session_state.emp_id = None
    st.session_state.role = None

# -------------------- Landing Page --------------------
if st.session_state.page == 'landing':
    st.title("Welcome to ScanSmart")
    if st.button("Login"):
        go_to('login')

# -------------------- Login Page --------------------
elif st.session_state.page == 'login':
    st.subheader("Login")
    email = st.text_input("Email", placeholder="Type here")
    password = st.text_input("Password", placeholder="Type here", type="password")

    if st.button("Enter"):
        role, st.session_state.emp_id = validate_login(dbconn, email, password) #set employee ID under st as an attribute like the session_state.page is
        if role == "Not Found":
            st.error("User not found. Did you make a typo?")
        else:
            st.success("Login Successful")
            if role == "Cashier":
                go_to('cashier')
            elif role == "Admin":
                go_to('admin')

# -------------------- Cashier Page --------------------
# cashier functions:
#   View All bills made by specific cashier
#   create bills for customers by scanning QR/Bar Codes
elif st.session_state.page == 'cashier':
    st.title("Cashier Dashboard")
    if st.button("Start Billing"): # set up a loop that runs and display added billdetails in the reciept area.
        st.session_state.bill_detail_list = []
        st.session_state.billing_active = True
        st.session_state.scanner.start_scanner() #starts scanning for product QRCodes
    
        print("Camera begins scanning products")
        st.rerun()
    
    # ---------------------- BILLING LOOP ------------------------
    if st.session_state.billing_active:

        prodID = st.session_state.scanner.get_latest_product_id()
        if prodID:
            st.session_state.bill_detail_list, prod_found = scan_bill(dbconn, st.session_state.bill_detail_list, st.session_state.scanner, st.session_state.seen_products)
            if not prod_found:
                st.error("Product not found in inventory.")
                time.sleep(2) #sleep to retain message on the screen before it is rerun()
                
        # Show bill details being collected
        st.subheader("Current Bill")
        for item in st.session_state.bill_detail_list:
            st.write(f"{item.ProductName} x {item.QuantitySold} = {item.TotalAmount}")
            print(f"{item.ProductName} - {item.UnitPrice} x {item.QuantitySold} = {item.TotalAmount}")
            #unique keys identify the button ids for each bill detail that is stored and displayed on the screen
            if st.button("+ increment", key=f"inc_{item.ProdID}"):
                increment = 1
                change_quantity(dbconn, item.ProdID, st.session_state.bill_detail_list, increment)
            if st.button("- decrement", key=f"dec_{item.ProdID}"):
                increment = -1
                change_quantity(dbconn, item.ProdID,  st.session_state.bill_detail_list, increment)
        total = get_total_from_details(st.session_state.bill_detail_list)
        if total != 0:
            st.write(f"Grand Total: PKR {total}")

        CustomerName = st.text_input("Customer's Name: ", placeholder="Type Here")
        st.session_state.bool_checkout = True
        # ---------------------- CHECKOUT ------------------------
        if st.button("Checkout"):
            if not st.session_state.bill_detail_list: #attempting to checkout with no products
                st.error("Error: Bill must have at least 1 product!")
                st.session_state.st.session_state.bool_checkout = False
                time.sleep(1)
            #check either customer name feild is empty, has spaces or has at least one digit
            if not (CustomerName.strip() and CustomerName.isalpha()):
                st.error("Invalid customer name")
                st.session_state.bool_checkout = False
                time.sleep(1)

            if st.session_state.bool_checkout: #cinditions fulfilled for checkout
                if checkout_billing(dbconn, st.session_state.bill_detail_list, CustomerName, st.session_state.emp_id):
                    st.success("Bill saved successfully!")
                    time.sleep(2)
                else:
                    st.error("Bill could not be saved")
                    time.sleep(2)

                st.session_state.scanner.stop_scanner()  # turns off camera
                st.session_state.bill_detail_list = []    # resets list
                st.session_state.seen_products.clear() #clears the set of scanned prod ids
                st.session_state.billing_active = False  # ends billing session
                st.session_state.bool_checkout = True

        st.rerun() #reruns/refreshes page for continual scanning and display of items in real time

    #Displays bills of the logged in cashier
    if st.button("Display My Bills"):
        bills = get_bills_from_db(dbconn, st.session_state.emp_id)
        if bills:
            for bill in bills:
                st.subheader(f"Bill ID: {bill.BillID}")
                st.write(f"Cashier: {bill.CashierName}")
                st.write(f"Customer Name: {bill.CustomerName}")
                st.write(f"Date: {bill.Date}")
                st.write("Products:")
                for item in bill.details:
                    st.write(f"- {item.ProductName} - {item.UnitPrice} PKR x {item.QuantitySold} = {item.TotalAmount} PKR")
                st.write(f"Grand Total: {bill.TotalAmount} PKR")
                st.markdown("---")
        else:
            st.info("No bills found. Start scanning to save bills under your name")
    
    if st.button("Logout"):
        logout()

# -------------------- Admin Page --------------------
#Admin functions:
#   update product quantity by scanning Barcode
#   add product in database
#   add cashiers by filling in info
#   View ALL Bills from ALL Employees
elif st.session_state.page == 'admin':
    st.title("Admin Dashboard")

    # Update product quantity by scanning it
    if st.button("Scan Product to Update Quantity"):
        product_id = scan_product_barcode(dbconn)
        st.session_state.scanned_product = product_id

    if "scanned_product" in st.session_state:
        product_id = st.session_state.scanned_product
        st.success(f"Scanned Product ID: {product_id}")

        new_q = st.text_input("Enter new quantity:")

        if st.button("Update Quantity"):
            if update_quantity_after_scan(dbconn, product_id, new_q):
                st.success("Quantity updated successfully!")
                del st.session_state.scanned_product   # <-- clears after update
            else:
                st.error("Invalid quantity or update failed.")
   
    # add product to db
    st.subheader("Add Product form")
    with st.form("product_form"):
        Name = st.text_input("Product Name:")
        Category = st.text_input("category:")
        Price = st.text_input("Product price:")
        QuantityAvailable = st.text_input("Quantity Available:")
        ManufactureID = st.text_input("Manufacture ID:")

        submit = st.form_submit_button("Save Product")

    if submit: #button clicked, bussiness logic checks
        price_chk, quantity_chk, manufacture_chk = add_product(dbconn, Name, Category, Price, QuantityAvailable, ManufactureID)

        if not price_chk:
            st.error("Price must be greater than 0 and a decimal number")
        if not quantity_chk:
            st.error("Quantity must be a non negative number")
        if not manufacture_chk:
            st.error("Manufacture ID is not registered")

        if price_chk and quantity_chk and manufacture_chk:
            st.success("Product info stored successfully!")


    # #add cashier info
    st.subheader("Add Cashier Info")
    st.text("Email must be unique" \
    "Contact must be unique, following the format 03xxxxxxxxx" \
    "Password must include:")
    st.text("- At least 1 number")
    st.text("- At least 1 lowercase letter")
    st.text("- have a minimum length of 7 characters")

    # ---- FORM FIX ----
    with st.form("cashier_form"):
        Name = st.text_input("Full Name:")
        ContactNumber = st.text_input("Contact Number:")
        Email = st.text_input("Email:")
        Address = st.text_input("Address:")
        Password = st.text_input("Password:", type="password")

        submit = st.form_submit_button("Save Info")

    if submit: #button clicked, business logic checks
        email_chk, contact_chk, pass_chk = validate_cashier_info(dbconn, Name, ContactNumber, Email, Address, Password)

        if not email_chk:
            st.error("Email must be unique")
        if not contact_chk:
            st.error("Contact must be unique and follow stated rules ")
        if not pass_chk:
            st.error("Password must follow the stated rules")

        if email_chk and contact_chk and pass_chk:
            st.success("Cashier info stored successfully!")


    if st.button("Display All bills"):
        try:
            bills = get_bills_from_db(dbconn) #gets all bills, function run in the the service layer
            if bills:
                for bill in bills:
                    st.subheader(f"Bill ID: {bill.BillID}")
                    st.write(f"Cashier: {bill.CashierName}")
                    st.write(f"Customer Name: {bill.CustomerName}")
                    st.write(f"Date: {bill.Date}")
                    st.write("Products:")
                    for item in bill.details:
                        st.write(f"- {item.ProductName} - {item.UnitPrice} PKR x {item.QuantitySold} = {item.TotalAmount} PKR")
                    st.write(f"Grand Total: {bill.TotalAmount} PKR")
                    st.markdown("---")  # separator between bills
            else:
                st.info("No bills saved yet")
        except Exception as e:
            st.error(f"Error fetching bills: {e}")

    # DISPLAY BILLS: returned bill has these attributes:
    # bill - (BillId, customerName, Date, TotalAmount, EmployeeID)
        # \- CashierName
        # - details - (BillDetailID, BillID, EmployeeID, QuantitySold, UnitPrice, TotalAmount, ProductName)

    if st.button("Logout"):
        logout()
