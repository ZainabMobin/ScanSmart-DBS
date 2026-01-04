import streamlit as st

from databases.mysql_connector import connect_db
from databases.billDatabase import billDatabase
from databases.employeeDatabase import employeeDatabase
from databases.manufactureDatabase import manufactureDatabase

from services.scannerService import ScannerService
from services.productService import scan_product,add_product, scan_product_barcode,update_quantity_after_scan,delete_product_after_scan
from services.employeeService import validate_employee_info
from services.analyticalService import plot_daily_sales_trend,plot_employee_performance,plot_inventory_status,plot_sales_by_category,plot_top_products

import time
import matplotlib.pyplot as plt
K_RESULTS = 10

dbconn=connect_db()
billDatabase_obj = billDatabase(dbconn)
employeeDatabase_obj=employeeDatabase(dbconn)
manufactureDatabase_obj=manufactureDatabase(dbconn)


def admin_page():
    # CRITICAL: Clear all login page styles first
    st.markdown("""
        <style>
        /* Force remove login page elements */
        .left-half {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
        }
        
        .icon-heading, .icon-row, .icon-box, .feature-item {
            display: none !important;
        }
        
        /* Reset any two-column layout from login */
        .stApp > div > div > div {
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Apply admin page CSS
    if st.session_state.page == "Admin":
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            /* Reset any login page styles */
            .left-half {
                display: none !important;
            }
 
            * {
                font-family: 'Inter', sans-serif;
            }
            
            /* White background for entire app */
            .stApp {
                background-color: #ffffff !important;
            }
            
            /* Main content area */
            .main .block-container {
                background-color: #ffffff !important;
                padding: 2rem 3rem !important;
            }
            
            /* Input fields */
            .stTextInput {
                position: relative;
                z-index: 999 !important;
            }

            .stTextInput > div > div {
                border: none !important;
            }
            
            .stTextInput > div > div > input {
                width: 100%;
                padding: 10px 12px;
                border-radius: 5px;
                border: 2px solid #0066FF !important;
                background-color: white !important;
                color: black !important;
                font-size: 16px;
                cursor: text;
                position: relative;
                z-index: 1000 !important;
                caret-color: black !important;
            }

            .stTextInput > div > div > input::placeholder {
                color: #999999;
                opacity: 1;
            }

            .stTextInput > div > div > input:focus {
                outline: none;
                border: 2px solid #0047b3;
                box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
            }

            /* Fix the black border on the right side of input */
            .stTextInput > div {
                border: none !important;
                background: transparent !important;
            }

            .stTextInput > div > div {
                border: none !important;
                background: transparent !important;
            }

            /* input container is blue bordered */
            .stTextInput > div > div {
                border: 2px solid #0066FF !important;
                border-radius: 5px !important;
                overflow: hidden !important;
            }
            
            /* Main buttons */
            div.stButton > button {
                padding: 12px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                border: 2px solid #e0e0e0;
                width: 100%;
                height: 50px;
                background-color: #0066FF;
                color: white;
                transition: all 0.3s ease;
            }

            div.stButton > button:hover {
                background-color: #0052cc;
                color: white;
                border-color: #0066FF;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
            }
            
            /* Start scanning button */
            .start-scanning-btn button {
                background-color: #0066FF !important;
                color: white !important;
                padding: 20px !important;
                border-radius: 12px !important;
                font-size: 20px !important;
                font-weight: 700 !important;
                width: 100% !important;
                height: 80px !important;
                border: none !important;
            }
            
            .start-scanning-btn button:hover {
                background-color: #0052cc !important;
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 102, 255, 0.3);
            }
            
            /* Stop scanning button */
            .stop-scanning-btn button {
                background-color: #ff4444 !important;
                color: white !important;
                padding: 12px 30px !important;
                border-radius: 10px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                width: 100% !important;
                height: 50px !important;
                border: none !important;
            }
            
            .stop-scanning-btn button:hover {
                background-color: #cc0000 !important;
            }
            
            /* Card styling */
            .admin-card {
                background-color: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                margin: 20px 0;
                border: 1px solid #f0f0f0;
            }
            
            /* Dataframe styling */
            .stDataFrame {
                background-color: white !important;
            }
            
            /* Tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: white;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: white;
                border-radius: 8px;
                color: #666;
                font-weight: 600;
                border: 2px solid #e0e0e0;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #0066FF !important;
                color: white !important;
                border-color: #0066FF !important;
            }
                     /* White background for modal */
                    /* DIALOG/MODAL STYLING */

            [data-testid="stModal"] {
                background-color: rgba(255, 255, 255, 0.95) !important;
            }

            [data-testid="stModal"] > div {
                background-color: white !important;
            }

            /* Modal content container */
            [data-testid="stModal"] [data-testid="stVerticalBlock"] {
                background-color: white !important;
            }

            /* Modal header/title area */
            [data-testid="stModal"] h2 {
                color: #0066FF !important;
                background-color: white !important;
            }

            /* Text color in modal */
            [data-testid="stModal"] p {
                color: #333 !important;
            }

            /* Input fields in modal */
            [data-testid="stModal"] .stTextInput > div > div > input {
                background-color: white !important;
                color: black !important;
                border: 2px solid #0066FF !important;
            }

            /* Buttons in modal (NOT the close button) */
            [data-testid="stModal"] button[kind="primary"],
            [data-testid="stModal"] button[kind="secondary"] {
                background-color: #0066FF !important;
                color: white !important;
            }

            [data-testid="stModal"] button[kind="primary"]:hover,
            [data-testid="stModal"] button[kind="secondary"]:hover {
                background-color: #0052cc !important;
            }
                    
            
            /* Sidebar styling */
        section[data-testid="stSidebar"] {
        visibility: visible !important;
        transform: none !important;
        display: block !important;
        }
        
        /* Make sure main content area adjusts for sidebar */
        .stApp > div:first-child {
            display: flex !important;
        }
        
        /* Remove any potential hiding */
        [data-testid="stSidebar"] {
            min-width: 340px !important;
        }
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important;
                padding-top: 2rem !important;
            }

            [data-testid="stSidebar"] > div:first-child {
                background-color: #f8f9fa !important;
            }

            /* Sidebar buttons */
            [data-testid="stSidebar"] button {
                background-color:#0066FF !important;
                color:white !important;
                border: 2px solid #00008B !important;
                border-radius: 8px !important;
                padding: 12px 20px !important;
                font-size: 15px !important;
                font-weight: 600 !important;
                width: 100% !important;
                margin-bottom: 10px !important;
                transition: all 0.3s ease !important;
            }

            [data-testid="stSidebar"] button:hover {
                background-color: #0052cc !important;
                color: white !important;
                transform: translateX(5px) !important;
            }


            /* Remove page names and navigation */
            [data-testid="stSidebarNavItems"] {
                display: none !important;
            }

            /* Remove the "app" text and page list */
            .css-1544g2n {
                display: none !important;
            }

            ul[role="listbox"] {
                display: none !important;
            }

            /* Active button state */
            [data-testid="stSidebar"] button:focus {
                background-color: #0066FF !important;
                color: white !important;
            }
                    [data-testid="stModal"] {
    background-color: rgba(255, 255, 255, 0.95) !important;
}

             
            /* Buttons in modal */
            [data-testid="stModal"] button {
                background-color: #0066FF !important;
                color: white !important;
            }

            [data-testid="stModal"] button:hover {
                background-color: #0052cc !important;
            }
            
            /* HIDE THE CLOSE (X) BUTTON  of dialog box*/
            [data-testid="stModal"] button[aria-label="Close"] {
                display: none !important;
                visibility: hidden !important;
            }
                        
         
                
            /* Hide streamlit branding */
            header {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Remove any gray backgrounds */
            [data-testid="stHeader"] {
                background-color: white !important;
            }
            
            [data-testid="stToolbar"] {
                background-color: white !important;
            }
            
            </style>
        """, unsafe_allow_html=True)

    if "active_admin_tab" not in st.session_state:
        st.session_state.active_admin_tab = "admin_start_page"
    
    # Initialize expanded bills state for admin
    if 'expanded_admin_bills' not in st.session_state:
        st.session_state.expanded_admin_bills = set()
    
    # Create scanner object
    if 'scanner' not in st.session_state:
        st.session_state.scanner = ScannerService()
    
    if 'scan_active' not in st.session_state:
        st.session_state.scan_active = False

    if 'scan_product_list' not in st.session_state:
        st.session_state.scan_product_list = []
    
    if 'admin_bill_list' not in st.session_state:
        st.session_state.admin_bill_list = []
    
    # SIDEBAR NAVIGATION - MOVED TO TOP
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; border-bottom: 2px solid #0066FF; margin-bottom: 10px;'>
                <h1 style='color: #0066FF; margin: 0;margin-top:-100px;'> Menu</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Scan Products", key="admin_scan_product", use_container_width=True):
            st.session_state.expanded_admin_bills = set()
            st.session_state.admin_bill_list = []
            st.session_state.active_admin_tab = "scan_product"  
            st.rerun()
        
        if st.button("Bills", key="admin_bills", use_container_width=True):
            tab_initial_setting()
            st.session_state.active_admin_tab = "admin_bill_detail"
            st.rerun()
        
        if st.button("Manage Products", key="admin_manage_prod", use_container_width=True):
            tab_initial_setting()
            st.session_state.active_admin_tab = "admin_manage_products"
            st.rerun()
        
                
        if st.button("Employee Details", key="admin_employee_details", use_container_width=True):
            tab_initial_setting()
            st.session_state.active_admin_tab = "admin_employee_details"
            st.rerun()
        
                
        if st.button("Manufacturer Details", key="admin_manufacturer_details", use_container_width=True):
            tab_initial_setting()
            st.session_state.active_admin_tab = "admin_manufacturer_details"
            st.rerun()
        
        if st.button("Analytics", key="admin_analytics", use_container_width=True):
            tab_initial_setting()
            st.session_state.active_admin_tab = "admin_analytics"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Logout", key="admin_logout", use_container_width=True):
            st.session_state.page = "login"
            st.session_state.scanner.stop_scanner()
            st.session_state.scan_product_list = []
            st.session_state.scan_active = False
            st.session_state.active_admin_tab = "admin_start_page"
            st.session_state.expanded_admin_bills = set()
            st.session_state.admin_bill_list = []
            st.rerun()
    
    # MAIN CONTENT - COMES AFTER SIDEBAR
    # Header
    st.markdown("""
        <h1 style="color: #0066FF;margin-top: -80px;">Smart Scan</h1>
        <h2 style="color:black; font-size: 28px;margin-top:-30px;">Admin Dashboard</h2>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    # col1, col2, col3, col4 = st.columns([2.7, 1.6, 1.9, 1.9])
    
    # Render the appropriate tab content
    if st.session_state.active_admin_tab == "admin_start_page":
        admin_start_page()
    elif st.session_state.active_admin_tab == "scan_product":
        if not st.session_state.scan_active:
            show_scan_start_page()  # New function for start page
        else:
            admin_scan_product()  # Active scanning page
    elif st.session_state.active_admin_tab == "admin_bill_detail":
        show_admin_bills_view() 
    elif st.session_state.active_admin_tab=="admin_manage_products":
        admin_manage_products()
    elif st.session_state.active_admin_tab=="admin_employee_details":
        admin_employee_details()
    elif st.session_state.active_admin_tab=="admin_manufacturer_details":
        admin_manufacturer_details()
    elif st.session_state.active_admin_tab=="admin_analytics":
        admin_analytics()

def tab_initial_setting():
    st.session_state.scanner.stop_scanner()
    st.session_state.scan_product_list = []
    st.session_state.scan_active = False
    st.session_state.expanded_admin_bills = set()


#--------------start page of admin dashboard----
def admin_start_page(): 
    st.markdown("""
        <div class="admin-card">
            <h3 style="color: #0066FF; margin-bottom: 20px;">Welcome to Admin Panel</h3>
            <p style="color: #666; font-size: 16px; line-height: 1.6;">
                Manage your inventory, view product detail, and update database from here.
            </p>
        </div>
    """, unsafe_allow_html=True)

#-------------scan product start page-----------
def show_scan_start_page():
    """Initial page with Start Scanning button"""
    st.markdown("""
        <div style="text-align: center; padding: 100px 20px; background-color: white; border-radius: 15px; margin-top: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color: #0066FF; margin-bottom: 20px;">Ready to Scan Products</h2>
            <p style="color: #666; margin-bottom: 40px; font-size: 18px; line-height: 1.6;">
                Click the button below to start scanning products and view their details.<br>
                The scanner will automatically detect QR codes.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="start-scanning-btn">', unsafe_allow_html=True)
        if st.button("Start Scanning", use_container_width=True, key="start_scanning"):
            st.session_state.scan_active = True
            st.session_state.scan_product_list = []
            st.session_state.scanner.start_scanner()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

#-------------scan product active page-----------
def admin_scan_product():
    """Active scanning page - only shown when scanning is active"""
    
    # Ensure scan product list is properly initialized
    if 'scan_product_list' not in st.session_state:
        st.session_state.scan_product_list = []
    
    # Clear any bill data that might be lingering
    if 'admin_bill_list' in st.session_state:
        st.session_state.admin_bill_list = []
    
    st.session_state.scan_product_list, prod_found = scan_product(
        dbconn, 
        st.session_state.scan_product_list, 
        st.session_state.scanner
    )
    
    if not prod_found:
        st.error("Product Not Found")

    billing_container = st.container()
    with billing_container:
        # Header row
        header_cols = st.columns([1, 3, 1.5, 1.5, 1.5, 2])
        with header_cols[0]:
            st.markdown("<b style='color:black;'>ProdID</b>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown("<b style='color:black;'>Name</b>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown("<b style='color:black;'>Category</b>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown("<b style='color:black;'>Price</b>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown("<b style='color:black;'>Quantity</b>", unsafe_allow_html=True)
        with header_cols[5]:
            st.markdown("<b style='color:black;'>ManufactureID</b>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
        
        if st.session_state.scan_product_list:
            for detail in st.session_state.scan_product_list:
                cols = st.columns([1, 3, 1.5, 1.5, 1.5, 2])
                with cols[0]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.ProdID}</p>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.Name}</p>', unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.Category}</p>', unsafe_allow_html=True)
                with cols[3]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.Price:.2f}</p>', unsafe_allow_html=True)
                with cols[4]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.QuantityAvailable}</p>', unsafe_allow_html=True)
                with cols[5]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.ManufactureID}</p>', unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 5px 0; border: 0.5px solid #f0f0f0;'>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: white; padding: 40px; text-align:center; border-radius: 10px;">
                    <p style="color:#0066FF; margin:0; font-size: 18px;">📷 Scan QR code to view product details</p>
                </div>
            """, unsafe_allow_html=True)
    # Stop Scanning button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="stop-scanning-btn">', unsafe_allow_html=True)
        if st.button("Stop Scanning", use_container_width=True, key="stop_scanning"):
            st.session_state.scanner.stop_scanner()
            st.session_state.scan_active = False
            st.session_state.scan_product_list = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # Auto-refresh for continuous scanning - only if scanning is active
    if st.session_state.scan_active:
        time.sleep(0.5)
        st.rerun()


#----------admin_bill_detail-----------
def show_admin_bills_view():

    """Display all bills with expandable details for admin"""
    st.session_state.scanner.stop_scanner()
    st.session_state.scan_product_list = []
    st.session_state.scan_active = False
    st.markdown('<h3 style="color:#333;margin-bottom:20px;">Bill Records</h3>', unsafe_allow_html=True)
    
    # Get ALL bills (no employee filter for admin)
    all_bills= billDatabase_obj.get_bills()  # No employee ID = get all bills
    
    if not all_bills:
        st.markdown("""
            <div style="background-color: white; padding: 40px; text-align:center; border-radius: 10px; margin-top: 20px;">
                <p style="color:#666; margin:0; font-size: 18px;">No bills found in the system</p>
            </div>
        """, unsafe_allow_html=True)
        return
     # 🆕 🔽 Initialize pagination state
    if "admin_bill_page" not in st.session_state:
        st.session_state.admin_bill_page = 1

    total_bills = len(all_bills)
    total_pages = (total_bills + K_RESULTS - 1) // K_RESULTS

    # Clamp page safely
    st.session_state.admin_bill_page = max(
        1, min(st.session_state.admin_bill_page, total_pages)
    )

    # Slice bills for current page
    start = (st.session_state.admin_bill_page - 1) * K_RESULTS
    end = start + K_RESULTS
    paged_bills = all_bills[start:end]

    bills_container = st.container()
    with bills_container:
        # Header row with column names
        header_cols = st.columns([1, 1.5, 3, 1.4, 1.5, 0.1])
        with header_cols[0]:
            st.markdown("<b style='color:black;'>Bill ID</b>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown("<b style='color:black;'>Customer Name</b>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown("<b style='color:black;'>Date</b>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown("<b style='color:black;'>Total Amount</b>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown("<b style='color:black;'>Cashier ID</b>", unsafe_allow_html=True)

        st.markdown(
            "<hr style='margin: 10px 0; border: 1px solid #e0e0e0;'>",
            unsafe_allow_html=True
        )

        # loop over and Display ONLY paged bills
        for bill in paged_bills:
            bill_id = bill[0]
            is_expanded = bill_id in st.session_state.expanded_admin_bills
            
            cols = st.columns([1, 1.5, 3, 1.4, 1.5, 0.1])
            
            with cols[0]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[0]}</p>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[1]}</p>', unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[2]}</p>', unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[3]:.2f}</p>', unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[4]}</p>', unsafe_allow_html=True)
            with cols[5]:
                button_label = "🔽" if not is_expanded else "🔼"
                if st.button(
                    button_label,
                    key=f"toggle_admin_bill_{bill_id}",
                    use_container_width=True
                ):
                    if bill_id in st.session_state.expanded_admin_bills:
                        st.session_state.expanded_admin_bills.remove(bill_id)
                    else:
                        st.session_state.expanded_admin_bills.add(bill_id)
                    st.rerun()
            
            # Show details if expanded (UNCHANGED)
            if is_expanded:
                bill_details = billDatabase_obj.get_bill_detail_admin(bill_id)
                
                if bill_details:
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                                    padding: 5px; border-radius: 10px; margin: 10px 0 20px 0; 
                                    border-left: 4px solid #0066FF; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(
                        f"<h4 style='color:#0066FF; margin-bottom: 15px;'>Bill Details -{bill_id:03d}</h4>",
                        unsafe_allow_html=True
                    )
                    
                    detail_header_cols = st.columns([1.5, 3, 1.5, 1.5, 1.5])
                    with detail_header_cols[0]:
                        st.markdown("<b style='color:#495057;'>Product ID</b>", unsafe_allow_html=True)
                    with detail_header_cols[1]:
                        st.markdown("<b style='color:#495057;'>Product Name</b>", unsafe_allow_html=True)
                    with detail_header_cols[2]:
                        st.markdown("<b style='color:#495057;'>Quantity</b>", unsafe_allow_html=True)
                    with detail_header_cols[3]:
                        st.markdown("<b style='color:#495057;'>Unit Price</b>", unsafe_allow_html=True)
                    with detail_header_cols[4]:
                        st.markdown("<b style='color:#495057;'>Total</b>", unsafe_allow_html=True)
                    
                    st.markdown(
                        "<hr style='margin: 8px 0; border: 1px solid #dee2e6;'>",
                        unsafe_allow_html=True
                    )
                    
                    for detail in bill_details:
                        detail_cols = st.columns([1.5, 3, 1.5, 1.5, 1.5])
                        with detail_cols[0]:
                            st.markdown(f"<p style='margin:5px 0;'>{detail[0]}</p>", unsafe_allow_html=True)
                        with detail_cols[1]:
                            st.markdown(f"<p style='margin:5px 0;'>{detail[1]}</p>", unsafe_allow_html=True)
                        with detail_cols[2]:
                            st.markdown(f"<p style='margin:5px 0; text-align:center;'>{detail[2]}</p>", unsafe_allow_html=True)
                        with detail_cols[3]:
                            st.markdown(f"<p style='margin:5px 0;'>PKR {detail[3]:.2f}</p>", unsafe_allow_html=True)
                        with detail_cols[4]:
                            st.markdown(f"<p style='color:#0066FF; font-weight:600; margin:5px 0;'>PKR {detail[4]:.2f}</p>", unsafe_allow_html=True)
                        st.markdown(
                            "<hr style='margin: 5px 0; border: 0.5px solid #dee2e6;'>",
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<p style='color:#999; font-style:italic;'>No details available for this bill</p>",
                        unsafe_allow_html=True
                    )
            
            st.markdown(
                "<hr style='margin: 8px 0; border: 0.5px solid #f0f0f0;'>",
                unsafe_allow_html=True
            )

        # Pagination controls (bottom)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        
        with col1:
            if st.session_state.admin_bill_page > 1:
                if st.button("⬅ Previous"):
                    st.session_state.admin_bill_page -= 1
                    st.rerun()

        with col2:
            st.markdown(
                f"<p style='text-align:center; color:#333;'>"
                f"Page {st.session_state.admin_bill_page} of {total_pages}"
                f"</p>",
                unsafe_allow_html=True
            )

        with col3:
            if st.session_state.admin_bill_page < total_pages:
                if st.button("Next ➡"):
                    st.session_state.admin_bill_page += 1
                    st.rerun()


def admin_manage_products():
    st.markdown('<h3 style="color:#0066FF; margin-bottom: 20px;">Product Management</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add Product", key="admin_add_product", use_container_width=True):
            admin_add_products()
    
    with col2:
        if st.button("Update Product", key="admin_update_product", use_container_width=True):
            admin_update_product()
        
    
    with col3:
        if st.button("Delete Product", key="admin_delete_product", use_container_width=True):
            admin_delete_product()
            


@st.dialog("Add New Product")
def admin_add_products():
    st.markdown('<p style="color:#0066FF; margin-bottom: 20px;">Enter the product details below</p>', unsafe_allow_html=True)
    
    with st.container():
        Name = st.text_input("",placeholder="Product Name",key="new_product_name")
        Category = st.text_input("",placeholder="Category",key="new_product_category")
        Price = st.text_input("",placeholder="Price",key="new_product_price")
        Quantity = st.text_input("",placeholder="Quantity",key="new_product_quantity")
        ManufactureID = st.text_input("",placeholder="Manufacture ID:",key="new_product_manufactureID")

        col1, col2 = st.columns(2)
        with col1:
            cancel = st.button("Cancel",key="cancel_add_product")
        with col2:
            submit = st.button("Save Product",key="product_add_button")

    if cancel:
        st.rerun()
    
    if submit:
        price_chk, quantity_chk, manufacture_chk = add_product(dbconn, Name, Category, Price, Quantity, ManufactureID)

        if not price_chk:
            st.error("Price must be greater than 0 and a decimal number")
        if not quantity_chk:
            st.error("Quantity must be a non-negative number")
        if not manufacture_chk:
            st.error("Manufacture ID is not registered")

        if price_chk and quantity_chk and manufacture_chk:
            st.success("Product info stored successfully!")
            time.sleep(1)
            st.rerun()
@st.dialog("Update Product")
def admin_update_product():
    if 'scanned_product_id' not in st.session_state:
        st.session_state.scanned_product_id = None
    
    st.markdown('<p style="color:#0066FF;">Scan product barcode</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Scanning", key="start_scan_update", use_container_width=True):
            product_id = scan_product_barcode(dbconn)
            if product_id:
                st.session_state.scanned_product_id = product_id
    
    if st.session_state.scanned_product_id:
        st.success(f"Product: {st.session_state.scanned_product_id}")
        
        new_quantity = st.text_input("", placeholder="New quantity", key="new_qty")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancel", key="cancel_update", use_container_width=True):
                st.session_state.scanned_product_id = None
                st.rerun()
        
        with col2:
            if st.button("Update", key="update_btn", use_container_width=True):
                if new_quantity:
                    if update_quantity_after_scan(dbconn, st.session_state.scanned_product_id, new_quantity):
                        st.success("Quantity updated!")
                        st.session_state.scanned_product_id = None
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid quantity")
                else:
                    st.error("Please enter quantity")

                    

@st.dialog("Delete Product")
def admin_delete_product():
    if 'scanned_product_id' not in st.session_state:
        st.session_state.scanned_product_id = None
    
    st.markdown('<p style="color:#0066FF;">Scan product barcode</p>', unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("Start Scanning", key="start_scan_update", use_container_width=True):
            product_id = scan_product_barcode(dbconn)
            if product_id:
                st.session_state.scanned_product_id = product_id
            else:
                st.error("Product ID not found!")
    
    if st.session_state.scanned_product_id:
        st.success(f"Product: {st.session_state.scanned_product_id}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancel", key="cancel_update", use_container_width=True):
                st.session_state.scanned_product_id = None
                st.rerun()
        
        with col2:
            if st.button("Delete", key="update_btn", use_container_width=True):
                if delete_product_after_scan(dbconn, st.session_state.scanned_product_id):
                    st.success("Successfully Deleted!")
                    st.session_state.scanned_product_id = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Error!")
    
def admin_employee_details():
    col1,col2,col3=st.columns([2,1,2])
    with col1:
        st.markdown('<h3 style="color:#333;margin-bottom:20px;">Employee Details</h3>', unsafe_allow_html=True)
    with col3:
        if st.button("Add Employee",key="admin_add_employee"):
            add_employee()
    all_employee_details=employeeDatabase_obj.get_employee_details()

    if not all_employee_details:
        st.markdown("""
            <div style="background-color: white; padding: 40px; text-align:center; border-radius: 10px; margin-top: 20px;">
                <p style="color:#666; margin:0; font-size: 18px;">No employee detail found</p>
            </div>
        """, unsafe_allow_html=True)
        return    

    # PAGINATION: initialize page state
    if "employee_page" not in st.session_state:
        st.session_state.employee_page = 0

    total_employees = len(all_employee_details)
    total_pages = (total_employees + K_RESULTS - 1) // K_RESULTS

    # Clamp page safely
    st.session_state.employee_page = max(
        1, min(st.session_state.employee_page, total_pages)
    )

    start = (st.session_state.employee_page -1 ) * K_RESULTS
    end = start + K_RESULTS
    paginated_employees = all_employee_details[start:end]

    employee_container = st.container()
    with employee_container:
        # Header row with column names
        header_cols = st.columns([1, 1, 1, 1.2, 1.7])
        with header_cols[0]:
            st.markdown("<b style='color:black;'>Employee ID</b>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown("<b style='color:black;'>Name</b>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown("<b style='color:black;'>Role</b>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown("<b style='color:black;'>Contact Number</b>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown("<b style='color:black;'>Email</b>", unsafe_allow_html=True)
       
        st.markdown("<hr style='margin: 10px 0; border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
            
        #loop and display only rendered rows
        for employee_detail in paginated_employees:
            
            cols = st.columns([1, 1, 1, 1.2, 1.7])
            
            with cols[0]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{employee_detail[0]}</p>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{employee_detail[1]}</p>', unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{employee_detail[2]}</p>', unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{employee_detail[3]}</p>', unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{employee_detail[4]}</p>', unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 8px 0; border: 0.5px solid #f0f0f0;'>", unsafe_allow_html=True)
        
        # Pagination controls (bottom)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        
        with col1:
            if st.session_state.employee_page > 1:
                if st.button("⬅ Previous"):
                    st.session_state.employee_page -= 1
                    st.rerun()
        with col2:
            st.markdown(
                f"<p style='text-align:center; color:#333;'>"
                f"Page {st.session_state.employee_page} of {total_pages}"
                f"</p>",
                unsafe_allow_html=True
            )
        with col3:
            if st.session_state.employee_page < total_pages:
                if st.button("Next ➡"):
                    st.session_state.employee_page += 1
                    st.rerun()


@st.dialog("Add employee in database")
def add_employee():


    st.markdown('<p style="color:#0066FF; margin-bottom: 20px;">Enter the employee details below</p>', unsafe_allow_html=True)
    
    with st.container():
        Name = st.text_input("",placeholder="Full Name",key="new_employee_name")
        Role = st.selectbox("Role", ["Cashier", "Admin"], key="new_employee_role")
        ContactNumber = st.text_input("",placeholder="Contact Number",key="new_employee_contact_number")
        Email = st.text_input("",placeholder="Email",key="new_employee_email")
        Address = st.text_input("",placeholder="Address",key="new_employee_address")
        Password = st.text_input("",placeholder="Password", key="new_employee_password",type="password")

        col1, col2 = st.columns(2)
        with col1:
            cancel = st.button("Cancel",key="cancel_add_employee")
        with col2:
            submit = st.button("Add Employee",key="successfully_add_employee")

    if cancel:
        st.rerun()
    
    if submit:
        email_chk, contact_chk, pass_chk = validate_employee_info(dbconn, Name,Role, ContactNumber, Email, Address, Password)

        if not email_chk:
            st.error("Email must be unique")
        if not contact_chk:
            st.error("Contact must be unique and follow stated rules ")
        if not pass_chk:
            st.error("Password must follow the stated rules")

        if email_chk and contact_chk and pass_chk:
            st.success("Cashier info stored successfully!")
            time.sleep(1)
            st.rerun()


def admin_manufacturer_details():

    st.markdown('<h3 style="color:#333;margin-bottom:20px;">Maufacturer Details</h3>', unsafe_allow_html=True)
    all_manufacturer_details = manufactureDatabase_obj.manufacturesDetail()

    if not all_manufacturer_details:
        st.markdown("""
            <div style="background-color: white; padding: 40px; text-align:center; border-radius: 10px; margin-top: 20px;">
                <p style="color:#666; margin:0; font-size: 18px;">No manufacturer detail found</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # PAGINATION STATE
    if "manufacturer_page" not in st.session_state:
        st.session_state.manufacturer_page = 0

    total_manufacturers = len(all_manufacturer_details)
    total_pages = (total_manufacturers + K_RESULTS - 1) // K_RESULTS

    # Clamp page safely
    st.session_state.manufacturer_page = max(
        1, min(st.session_state.manufacturer_page, total_pages)
    )

    start = (st.session_state.manufacturer_page - 1)* K_RESULTS
    end = start + K_RESULTS
    paginated_manufacturers = all_manufacturer_details[start:end]

    manufacturer_container = st.container()
    with manufacturer_container:
        # Header row
        header_cols = st.columns([1, 1, 1.4, 1.5])
        header_cols[0].markdown("<b style='color:black;'>Manufacturer ID</b>", unsafe_allow_html=True)
        header_cols[1].markdown("<b style='color:black;'>Manufacturer Name</b>", unsafe_allow_html=True)
        header_cols[2].markdown("<b style='color:black;'>Contact Number</b>", unsafe_allow_html=True)
        header_cols[3].markdown("<b style='color:black;'>Email</b>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

        # DISPLAY ONLY CURRENT PAGE ROWS IN LOOP
        for manufacturer_detail in paginated_manufacturers:
            cols = st.columns([1, 1, 1.4, 1.5])

            cols[0].markdown(f'<p style="color:black; margin:0; padding-top:8px;">{manufacturer_detail[0]}</p>', unsafe_allow_html=True)
            cols[1].markdown(f'<p style="color:black; margin:0; padding-top:8px;">{manufacturer_detail[1]}</p>', unsafe_allow_html=True)
            cols[2].markdown(f'<p style="color:black; margin:0; padding-top:8px;">{manufacturer_detail[2]}</p>', unsafe_allow_html=True)
            cols[3].markdown(f'<p style="color:black; margin:0; padding-top:8px;">{manufacturer_detail[3]}</p>', unsafe_allow_html=True)

            st.markdown("<hr style='margin: 8px 0; border: 0.5px solid #f0f0f0;'>", unsafe_allow_html=True)

        
        # Pagination controls (bottom)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        
        with col1:
            if st.session_state.manufacturer_page > 1:
                if st.button("⬅ Previous"):
                    st.session_state.manufacturer_page -= 1
                    st.rerun()

        with col2:
            st.markdown(
                f"<p style='text-align:center; color:#333;'>"
                f"Page {st.session_state.manufacturer_page} of {total_pages}"
                f"</p>",
                unsafe_allow_html=True
            )

        with col3:
            if st.session_state.manufacturer_page < total_pages:
                if st.button("Next ➡"):
                    st.session_state.manufacturer_page += 1
                    st.rerun()


def admin_analytics(): 
    st.markdown('<h3 style="color:#333;margin-bottom:20px;">Admin Analytics</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
            if st.button("Sales by Category", key="analytics_sales_category", use_container_width=True):
                fig = plot_sales_by_category(dbconn)
                if fig:
                    st.pyplot(fig)
                    plt.close(fig)
        
    with col2:
            if st.button("Top Products", key="analytics_top_products", use_container_width=True):
                fig = plot_top_products(dbconn)
                if fig:
                    st.pyplot(fig)
        
        
        # Row 2
    col3, col4 = st.columns(2)
    with col3:
            if st.button("Daily Trend", key="analytics_daily_trend", use_container_width=True):
                fig = plot_daily_sales_trend(dbconn)
                if fig:
                    st.pyplot(fig)
            
        
    with col4:
            if st.button("Employee Performance", key="analytics_employee", use_container_width=True):
                fig = plot_employee_performance(dbconn)
                if fig:
                    st.pyplot(fig)

        
        # Row 3
    col5, col6 = st.columns([1, 1])
    with col5:
            if st.button("Inventory Status", key="analytics_inventory", use_container_width=True):
                fig = plot_inventory_status(dbconn)
                if fig:
                    st.pyplot(fig)
                 