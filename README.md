Fully functional web app with basic UI/UX

Updated Functions:
- Implemented billing function catering to dynamic changes and increment/decrement mechanism
- Added scannerService class with relevant functions
- Refactored code for adding products and updating quantity
- Added business checks, renamed functions for readibility and changed Fstring queries to parameteized ones (prevents SQL injection)

Functions:
- Cashier: scans bills and saves them to the database
- Cashier: views bills made by them
- Admin: Update product quantity by scanning barcode
- Add product in database
- Add cashier to database
- View all bills created by everyone
  
Convention Used:
- Functions: snake_case
- Class: camelCase
