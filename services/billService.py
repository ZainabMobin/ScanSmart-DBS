from models.Bill import Bill
from models.BillDetail import BillDetail
from models.Product import Product
from databases.employeeDatabase import employeeDatabase
from databases.billDatabase import billDatabase
from databases.productDatabase import productDatabase
from services.scannerService import ScannerService
from collections import defaultdict #to create dict of bill details grouped by BillID
from datetime import datetime #to create data in the correct format
import cv2 #for camera scanning, additionally installed libs are qrcode, opencv
import winsound

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

def get_bills_from_db(dbconn, EmployeeID = None): #function overloading for when TOTAL bills are needed vs when a cashier views their own bills
    productDb = productDatabase(dbconn)
    billDb = billDatabase(dbconn)
    employeeDb = employeeDatabase(dbconn)

    bill_rows = billDb.get_bills(EmployeeID) #either gets total bills or bills for a single employee
    product_rows = billDb.get_bill_details()
    #groups product details by BillID for each bill
    grouped_details = defaultdict(list)
    for row in product_rows:
        product = BillDetail(BillID=row[1], ProdID=row[2], QuantitySold=row[3], UnitPrice=row[4], TotalAmount=row[5]) #create product object from the info in the tuple
        product.ProductName = productDb.get_prodname_from_id(product.ProdID) #get the product name and attach it with the product detail
        grouped_details[product.BillID].append(product) #group the row by BillID and append the product to each billDetail

    total_bills = []
    for row in bill_rows:
        bill = Bill(*row) #create a bill obj instead of working with tuple
        bill.details = grouped_details[bill.BillID] #link the billProduct Details with the Bill (already grouped by Bill ID in grouped_details)
        bill.CashierName = employeeDb.get_name_by_id(bill.EmployeeID, "Cashier")
        total_bills.append(bill)

    return total_bills


#Initiales scanner thread for continous scanning
def scan_bill(dbconn, detail_list, scanner, seen_set):
    productDb = productDatabase(dbconn)
    billId = get_latest_billid_from_db(dbconn)

    # read all new scanned product IDs
    while scanner.is_enqueued():
        prod_id = scanner.get_enqueued_id()

        # skip duplicates
        if prod_id in seen_set:
            continue
        seen_set.add(prod_id)

        # fetches product from DB
        product_tuple = productDb.get_prod_from_id(prod_id)
        if not product_tuple:
            return detail_list, False
        
        product = Product(*product_tuple)
        billDetail = BillDetail(BillID=billId, ProdID=prod_id, QuantitySold=1, UnitPrice=product.Price, TotalAmount=product.Price, ProductName=product.Name)

        detail_list.append(billDetail)
        print(f"appended billdetail: {billDetail.BillID} {billDetail.QuantitySold} {billDetail.UnitPrice} {billDetail.TotalAmount}")
        winsound.Beep(1000,500)

    return detail_list, True


#assigns billDetailID to the billDetails, adds date, customer name and cashierID to Bill
def checkout_billing(dbconn, detail_list, CustomerName, EmployeeID): 
    billDb = billDatabase(dbconn)

    #empty list
    if not isinstance(detail_list, list) or not detail_list:
        print("No products scanned to for billing!")
        return False
     
    bill = create_bill(detail_list, EmployeeID)#create bill at the end
    billDb.save_bill(CustomerName, bill.Date, bill.TotalAmount, bill.EmployeeID)
   
    for detail in detail_list: #save each billdetail in the list 
        billDb.save_bill_details(detail.BillID, detail.ProdID, detail.QuantitySold, detail.UnitPrice, detail.TotalAmount)
    return True

    
#assigns date, total amount, employeeID to Bill 
def create_bill(detail_list, EmployeeID):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    totalAmount = 0
    for detail in detail_list:
        totalAmount = totalAmount + detail.TotalAmount
    bill = Bill(Date=date, TotalAmount=totalAmount, EmployeeID=EmployeeID)
    return bill

def get_latest_billid_from_db(dbconn):
    billDb = billDatabase(dbconn)
    latest_BillID = billDb.get_latest_bill_id()
    return (latest_BillID + 1) if latest_BillID else 1


#changes quantity in billdetail object
def change_quantity(dbconn, prodID, detail_list, increment):
    productDb = productDatabase(dbconn)
    total_stock = productDb.get_quantity_from_id(prodID)
    to_remove = None
    for detail in detail_list:
        if detail.ProdID == prodID:
            if(detail.QuantitySold == 1 and increment == -1): #removes billdetail if quantity hits 0
                to_remove = detail
                break
            if(detail.QuantitySold == total_stock): #change nothing is quantity is equal to total quantity
                break
            detail.QuantitySold +=increment
            detail.TotalAmount = detail.UnitPrice*detail.QuantitySold
            break

    if to_remove:
        detail_list.remove(detail)
    return detail_list


#gives grand total for item details
def get_total_from_details(detail_list):
    total = 0
    for detail in detail_list:
        total = total + detail.TotalAmount

    return total
