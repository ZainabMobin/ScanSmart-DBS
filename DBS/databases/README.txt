CRUD operations performed in this layer
Didn't make these methods static, if they were then they couldn't have the shared database connection dbconn, each function would therefore have dbconn passed as a parameter individually
Instead the service layer makes an instance of the database object and then uses the function with the dbconn passed as a constructor parameter 
