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
- Class and File name: camelCase

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

# Docker guide

## Requirements

Package names and versions without versions in requirements.txt
```PlainText
bcrypt==5.0.0
matplotlib==3.11.2
mysql-connector-python==26.7.0
opencv-python-headless==5.0.0.93
pandas==3.0.6
python-dotenv==1.2.3
python-lucide==0.5.6
pyzbar==0.1.9
qrcode==8.2
sounddevice
streamlit==1.64.0
```

## `.env` file fields

```env
DB_HOST=127.0.0.1
DB_USER=*******
DB_PASSWORD=*******
DB_NAME=inventory_management
DB_PORT=3306
MYSQL_ROOT_PASSWORD=********
STREAMLIT_PORT_HOST=8501
STREAMLIT_PORT_CONTAINER=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

Note on DB_HOST: Inside Docker Compose, containers communicate using service names as hostname aliases. Set DB_HOST=db so your Python app routes traffic to the MySQL container service named db.

## Configuration Steps

### Step 1: Initial Build and Launch

To build the images, create the network, initialize the database schema, and launch everything in the background:
```Bash
docker compose up --build -d |& tee debug.log
```
- --build forces Docker to build the Python image using the Dockerfile and requirements.txt.

- -d runs the container in the background/detached mode.

### Step 2: Verify and View Logs

```Bash
docker compose ps # helthcheck for both containers
docker compose logs -f web # view live logs from web
docker compose logs -f db # live logs from MySQL db
```

At this point, open your browser and go to http://localhost:8501 (or whatever STREAMLIT_PORT_HOST is set to in your .env).

### Step 3: Container management

```Bash
# stop application
docker compose stop

# To start the app again without rebuilding:
docker compose start

# stop and remove active containers while retaining database in volumes
docker compose down
```

![TIP] Run `docker compose up --build` modified structural configuration, like adding a new package to requirements.txt, changing  Dockerfile or docker compose.yml, or environment variables in .env.

Streamlit auto-reloads changes inside the running container instantly if the python application code is changed

## Docker Compose:

### Run containers

```bash
# -f flag: file flag, specifically execute <filename.yml> instead of default docker-compose.yml 
docker compose -f docker-compose.vols.yml up -d 

docker compose -f docker-compose.vols.yml down

docker compose -f docker-compose.vols.yml logs # view logs

docker compose -f docker-compose.vols.yml exec db bash # open container db in exec mode
```

### Docker Compose Network

<pre>

<b>     Host                        Connection                      Container (services) </b>
<hr/>
[Host Browser] ────────────── http://localhost:7002 ──────────────> [web:8501]
<b><i>STREAMLIT_PORT_HOST</i></b>                                              <b><i>STREAMLIT_PORT_CONTAINER</i></b>
                                                                         │
                                                                Internal Docker Bridge
                                                                (DNS "db" ➔ 172.18.0.2:3306)
                                                                         │
                                                                         ▼
[Host DB Tools] ──────────── localhost:7001 (iptables) ───────────> [db:3306]
<b><i>DB_PORT_HOST</i></b>                                                    <b><i>DB_PORT_CONTAINER</i></b>

</pre>
