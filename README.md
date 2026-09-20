# About
ScanSmart is a desktop-based inventory management and billing system developed as part of the CS:220 Database Systems course. The system is designed to support day-to-day retail operations by enabling product scanning, dynamic billing, inventory management, and role-based access for administrators and cashiers. A QR scanning feature that works via desktop webcam makes it accessable and .

Built using Streamlit and Python, with a MySQL relational database, ScanSmart emphasizes secure database interactions, modular backend design and real-time operational insight through analytical reporting.

**Functions fully implemented:**

- Central Login with business Checks
- Manager: can update Product quantity by scanning Barcode
- Manager: can add a Product
- Manager: can add a Cashier
- Manager: can view Total bills
- Cashier: can bill customers (each product scanned once, beep sounded, functional quantity increment/decrement buttons)
- Cashier: can view bills made by them only
- Password management with hashing (bcrypt)

# Features and Tech Stack

**Frontend / UI Layer**

- Streamlit (Python): Used for page layout, UI components, session state, navigation, and event handling.
- HTML (embedded via st.markdown): Custom structure for headers, panels, branding sections, and layout control.
- CSS (inline & injected): Styling for layout, spacing, colors, typography, icons, and overriding Streamlit defaults.
- Lucide Icons (lucide_icon): SVG-based icon library for visual elements and feature highlights.
- Google Fonts (Inter): External font import for consistent typography.
- Matplotlib for data visualization and analytical graphs

**Backend / Application Logic**

- Python (Core Backend Logic): Handles authentication flow, session management, role-based routing, and business logic.
- MultiLayered Architecture (MVC with Database layer for CRUD operations)
- Backend logic coupled with the Streamlit app, not exposed as APIs.
- Modular Architecture but No Web Framework (Not a REST API)
- Barcode & QR Code Scanning: Implemented using pyzbar with multithreading support for continuous scanning.

**Database**

- MySQL R-DBMS
- MySQL Connector (Python)

**State & Control**

- Streamlit Session State (st.session_state)
- Logged-in user
- Role-based navigation
- Page switching
- Authentication persistence

**Security**

- Credential validation via backend service
- Password hashing using bcrypt
- Business Rule Validation for invalid operations (e.g., negative stock, invalid scans).
- Use of Parameterized queries to prevent SQL injection.

**Development Context**

- Desktop / Local Deployment
- Educational Project
- Course: CS:220 – Database Systems

# Implementation Details

```python
pip install qr cv2 opencv streamlit pyzbar winsound bcrypt matplotlib pandas lucide dotenv mysqlconnector   # install dependencies
streamlit run app.py    # run the webapp
``` 

**Naming Convention**

- Functions: snake_case
- Classes: camelCase
- File Name: PascalCase

## Module info:

**Models**

Objects are created at runtime that store current info. Used for insertion of data in the Database based on the role

**Databases**

CRUD operations performed in this layer/module. These methods are deliberately not made static, if they were then they couldn't have the shared database connection `dbconn`, each function would therefore have `dbconn` passed as a parameter individually. 

The service layer makes an instance of the database object and then uses the function with the dbconn passed as a constructor parameter 

i.e., The database connection is injected further into the layers until it reaches the databases module.

**Pages:**

Forms streamlit based interface for multiple pages 

**Services:**

All Data formatting, encryption/decryption and business logic is applied in the service layer











List package names without versions in requirements.txt:
```Plaintext
streamlit
mysql-connector-python
pandas
python-dotenv
```

Build and test your Docker container.

Once the app works smoothly inside the container, run pip freeze inside the running container to output the exact versions that succeeded:
```Bash
docker exec -it streamlit_app pip freeze
```

Copy that output back into your requirements.txt to lock those versions permanently.


Note on DB_HOST: Inside Docker Compose, containers communicate using service names as hostname aliases. Set DB_HOST=db so your Python app routes traffic to the MySQL container service named db.


Step 1: Initial Build and Launch

To build the images, create the network, initialize the database schema, and launch everything in the background:
```Bash

docker compose up --build -d
```
    --build forces Docker to build the Python image using your Dockerfile and requirements.txt.

    -d (detached mode) runs the containers in the background so your terminal remains free.

Step 2: Verify and View Logs

To check if both containers (mysql_db and streamlit_app) are healthy and running:
Bash

docker compose ps

To watch live logs from the Streamlit web application (useful for debugging code errors):
Bash

docker compose logs -f web

To watch live logs from the MySQL database:
Bash

docker compose logs -f db

At this point, open your browser and go to http://localhost:8501 (or whatever STREAMLIT_PORT_HOST is set to in your .env).
Everyday Workflow: How to Manage Day-to-Day Running

Once the initial setup is complete, here is how you interact with it daily:
1. Stopping the Application

When you finish working, stop the containers. Your database data remains safely stored in the mysql_data volume:
Bash

docker compose stop

2. Starting the Application Back Up

To start the app again without rebuilding:
Bash

docker compose start

3. Completely Shutting Down (Preserving Data)

To stop and remove the active containers while retaining all database records and tables:
Bash

docker compose down

When Do You Need to Rebuild?

You only need to run docker compose up --build when you modify structural configuration:

    You added a new package to requirements.txt.

    You changed your Dockerfile or docker compose.yml.

    You altered environment variables in .env.

If you only modified your Python application code (e.g., editing app.py), Streamlit auto-reloads changes inside the running container instantly—no rebuild required!
