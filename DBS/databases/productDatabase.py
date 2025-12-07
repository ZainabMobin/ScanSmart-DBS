class productDatabase:
    def __init__(self, dbconn):
        self.dbconn = dbconn
        
    # gets all Product info from the database, run when billing products
    def get_prod_from_id(self, prod_id):
        cursor = self.dbconn.cursor()
        query = f"SELECT * FROM Product WHERE ProdID = %s"
        cursor.execute(query, (prod_id,))
        return cursor.fetchone()


    #gets product name from id, run when the product to be displayed in bills
    def get_prodname_from_id(self, prod_id):
        cursor = self.dbconn.cursor()
        query = "SELECT Name FROM Product WHERE ProdID = %s"
        cursor.execute(query, (prod_id,))
        row = cursor.fetchone()
        cursor.close()
        return row[0] 
    
    def get_quantity_from_id(self, prod_id):
        cursor = self.dbconn.cursor()
        query = "SELECT QuantityAvailable FROM Product WHERE ProdID = %s"
        cursor.execute(query, (prod_id,))
        row = cursor.fetchone()
        cursor.close()
        return row[0] 


    def add_new_product(self,name,category,price,quantityAvailable,manufactureID):
        cursor=self.dbconn.cursor()
        query="INSERT INTO product VALUES (DEFAULT,%s,%s,%s,%s,%s)"
        val=(name,category,price,quantityAvailable,manufactureID)
        cursor.execute(query,val)
        self.dbconn.commit()
        toReturn = False
        if (cursor.rowcount): #confirm if rows are updated or not
            toReturn = True
        cursor.close()
        return toReturn
    
    def delete_product(self,prod_id):
        toReturn=False
        cursor=self.dbconn.cursor()
        query = "DELETE FROM product WHERE ProdID=%s"
        cursor.execute(query, (prod_id,))
        self.dbconn.commit()
        if (cursor.rowcount):
            toReturn=True
        cursor.close()
        return toReturn

    def update_quantity_available_in_db (self, prod_id, quantityAvailable):
        toReturn = False
        cursor=self.dbconn.cursor()
        query="UPDATE product SET QuantityAvailable=%s WHERE ProdID=%s"
        val=(quantityAvailable,prod_id)
        cursor.execute(query,val)
        self.dbconn.commit()
        if (cursor.rowcount): #confirm if rows are updated or not
            toReturn = True
        cursor.close()
        return toReturn
        # return (f"Product {prod_id} available quantity is updated")
    
    def finding_prod(self,prod_id):
        cursor=self.dbconn.cursor()
        query = "SELECT * FROM product WHERE ProdID=%s"
        cursor.execute(query, (prod_id,))
        product=cursor.fetchone()
        if product :
            return True
        else:
            return False