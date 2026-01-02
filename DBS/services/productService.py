from databases.productDatabase import productDatabase
from databases.manufactureDatabase import manufactureDatabase 
from models.Product import Product
import cv2
import winsound
from pyzbar import pyzbar


#checks price validity 
def is_valid_price(value):
    try:
        price = float(value)
        return price > 0  # Only positive prices allowed
    except ValueError:
        return False

# Usage:


def add_product(dbconn, Name, Category, Price, QuantityAvailable, ManufactureID):
    productDb = productDatabase(dbconn)
    ManufactureDb = manufactureDatabase(dbconn)
    price_chk = quantity_chk = manufacture_chk = True
    
    #either the price is not a number or it is a non-positive integer
    if not is_valid_price(Price):
        price_chk = False
    #either the quantity is not a number or a non-negative integer
    try:
        quantity=int(QuantityAvailable)
        if quantity <0:
            quantity_chk=False
        else:
            quantity_chk=True
    except:
        quantity_chk=False 
        
    #either manufactureID is not a number, or a non-positive integer or it does not exist in the database
    if not (ManufactureID.isdigit() and int(ManufactureID) > 0 and ManufactureDb.does_manufacture_exist(ManufactureID)): 
        manufacture_chk = False

    if not (price_chk and quantity_chk and manufacture_chk):
        return price_chk, quantity_chk, manufacture_chk
    if productDb.add_new_product(Name, Category, Price, QuantityAvailable, ManufactureID):
        print("product added successfully")
        return True, True, True
   

#scans product code once
def scan_product_barcode(dbconn):
    productDatabase_obj=productDatabase(dbconn)
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect barcodes
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            print(f"Scanned Product ID: {barcode_data}")
            winsound.Beep(1000,500)
            if (productDatabase_obj.finding_prod(int(barcode_data))):
                cap.release()
                cv2.destroyAllWindows()
                return barcode_data
        


def update_quantity_after_scan(dbconn, productId, new_quantity):
    productDatabase_obj=productDatabase(dbconn)
    if not new_quantity.isdigit() or int(new_quantity)<0:
        return False

    if productDatabase_obj.update_quantity_available_in_db(int(productId),new_quantity):
        print("Quantity Successfully Updated")
    else:
        print("Quantity could not be updated, try again later")
    return True

#helper function to delete a product
def delete_product_after_scan (dbconn,productid):
    productDatabase_obj=productDatabase(dbconn)
    if productDatabase_obj.delete_product(productid):
        return True


def scan_product(dbconn, detail_list, scanner):
    productDb = productDatabase(dbconn)

    # read all new scanned product IDs
    while scanner.is_enqueued():
        prod_id = scanner.get_enqueued_id()

        # fetches product from DB
        product_tuple = productDb.get_prod_from_id(prod_id)
        if not product_tuple:
            return detail_list, False
        
        product = Product(*product_tuple)
        detail_list.append(product)
        winsound.Beep(1000,500)

    return detail_list, True