import cv2
import threading
from pyzbar.pyzbar import decode
import queue

class ScannerService:
    def __init__(self):
        self.camera_on = False
        self.cap = None #camera attribute
        self.thread = None

        self.latest_id = None
        self.prev_id = None
        self.prod_queue = queue.Queue()

    #background thread runs and scans QRcode
    def start_scanner(self):
        if self.camera_on:
            print("Camera turned ON")
            return  # if camera already on, no need to turn it on again
        self.camera_on = True
        self.thread = threading.Thread(target=self._scanner_loop, daemon=True) #camera thread set to daemon thread
        self.thread.start()

#threading function
    def _scanner_loop(self):
        self.cap = cv2.VideoCapture(0)

        while self.camera_on:
            ret, frame = self.cap.read()
            if not ret:
                continue
            decoded_values = decode(frame)
            if decoded_values:
                product_id = decoded_values[0].data.decode()
                # Unique scan check
                if product_id != self.prev_id:
                    self.latest_id = product_id
                    self.prev_id = product_id
                    self.prod_queue.put(product_id)
                    print(f" New Scan enqueued: {self.latest_id}")
        # When stopped
        if self.cap is not None:
            self.cap.release()
 
    # Returns the latest product ID (once only)
    def get_latest_product_id(self):
        value = self.latest_id
        self.latest_id = None   # clear after returning once
        print(f"returning {value}") #check that runs every time the main page s rerun i.e., when the scan_bill() is called
        return value

    def get_enqueued_id(self):
        return self.prod_queue.get()

    def is_enqueued(self):
        return not self.prod_queue.empty()

    def stop_scanner(self):
        self.camera_on = False
