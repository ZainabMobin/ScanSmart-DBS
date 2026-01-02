# About
ScanSmart is a desktop-based inventory management and billing system developed as part of the CS:220 – Database Systems course. The system is designed to support day-to-day retail operations by enabling product scanning, dynamic billing, inventory management, and role-based access for administrators and cashiers. 

Built using Streamlit and Python, with a MySQL relational database, ScanSmart emphasizes secure database interactions, modular backend design, and real-time operational insights through analytical reporting.

# Implementation Details

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

**Conventions Used:**

- Functions: snake_case
- Class: camelCase
