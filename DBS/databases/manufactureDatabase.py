
class manufactureDatabase:
    def __init__(self,dbconn):
        self.dbconn=dbconn

    def manufacturesDetail(self):
        cursor=self.dbconn.cursor()
        query="SELECT * FROM manufacturedetail"
        cursor.execute(query)
        details=cursor.fetchall()
        return details
    
    def does_manufacture_exist(self, ManufactureID):
        cursor=self.dbconn.cursor()
        query ="SELECT * FROM manufacturedetail WHERE ManufactureID = %s"
        cursor.execute(query, (ManufactureID,))
        details = cursor.fetchall()
        return True if details else False
