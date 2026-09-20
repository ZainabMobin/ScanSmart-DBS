#created when the generate bill button is clicked, reciept saved in the backlog
class BillDetail:
    def __init__(self, BillID, ProdID, QuantitySold, UnitPrice, TotalAmount, ProductName=None, BillDetailID=None):
        self.BillDetailID = BillDetailID
        self.BillID = BillID
        self.ProdID = ProdID
        self.QuantitySold = QuantitySold
        self.UnitPrice = UnitPrice
        self.TotalAmount = TotalAmount
        self.ProductName = ProductName

#used in billing
    def change_bill_detail_quantity(self, newQuantity):
        self.QuantitySold = newQuantity
        self.TotalAmount = self.UnitPrice*newQuantity


    def get_bill_detail(self):
        return self.ProdID, self.QuantitySold, self.UnitPrice, self.TotalAmount