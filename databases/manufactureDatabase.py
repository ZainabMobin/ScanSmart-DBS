
class manufactureDatabase:
    def __init__(self,dbconn):
        self.dbconn=dbconn

    def get_manufacture_detail(self):
        cursor=self.dbconn.cursor()
        query = "SELECT * FROM ManufactureDetail"
        cursor.execute(query)
        details = cursor.fetchall()
        cursor.close()
        return details
    
    def does_manufacture_exist(self, ManufactureID):
        cursor=self.dbconn.cursor()
        query = "SELECT * FROM ManufactureDetail WHERE ManufactureID = %s"
        cursor.execute(query, (ManufactureID,))
        details = cursor.fetchall()
        return True if details else False
