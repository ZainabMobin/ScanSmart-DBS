from databases.productDatabase import productDatabase
from databases.manufactureDatabase import manufactureDatabase 
from decimal import Decimal
import cv2
import winsound
from pyzbar import pyzbar

def add_product(dbconn, Name, Category, Price, QuantityAvailable, ManufactureID):
    productDb = productDatabase(dbconn)
    ManufactureDb = manufactureDatabase(dbconn)
    price_chk = quantity_chk = manufacture_chk = True
    
    #either the price is not a number or it is a non-positive integer
    if not(Price.isdigit()) or int(Price)<=0:
        price_chk = False
    #either the quantity is not a number or a non-negative integer
    if not(QuantityAvailable.isdigit()) or int(QuantityAvailable) < 0:
        quantity_chk = False
    #either manufactureID is not a number, or a non-positive integer or it does not exist in the database
    if not (ManufactureID.isdigit() and int(ManufactureID) > 0 and ManufactureDb.does_manufacture_exist(ManufactureID)): 
        manufacture_chk = False

    if not (price_chk and quantity_chk and manufacture_chk):
        return price_chk, quantity_chk, manufacture_chk
    if productDb.add_new_product(Name, Category, Price, QuantityAvailable, ManufactureID):
        print("product added successfully")
        return True, True, True
   
def scan_product_barcode(dbconn):
    productDatabase_obj=productDatabase(dbconn)
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    print("Starting webcam. Press 'q' to quit.")
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
          
        # Show webcam feed
        cv2.imshow("Barcode Scanner", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def update_quantity_after_scan(dbconn, productId, new_quantity):
    productDatabase_obj=productDatabase(dbconn)
    if not new_quantity.isdigit() or int(new_quantity)<0:
        return False

    if productDatabase_obj.update_quantity_available_in_db(int(productId),new_quantity):
        print("Quantity Successfully Updated")
    else:
        print("Quantity could not be updated, try again later")
    return True