import streamlit as st
import pandas as pd
from services.scannerService import ScannerService
from services.billService import scan_bill
from databases.mysql_connector import connect_db
from services.billService import get_latest_billid_from_db, change_quantity, get_total_from_details, checkout_billing
from databases.employeeDatabase import employeeDatabase
from databases.billDatabase import billDatabase
from pages.login import loginPage
import time

dbconn = connect_db()
employee_obj=employeeDatabase(dbconn)
billDatabase_obj=billDatabase(dbconn)

def cashier_page():
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
    
    # Clear any previous page styles and apply cashier page CSS
    if st.session_state.page=="Cashier":
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
            
            .stApp {
                background-color: #f8f9fa !important;
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
                outline: none;border: 2px solid #0047b3;box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
                
            }

            .stTextInput > div > div > button {
                background-color: #0066FF !important;border: none !important;border-radius: 4px !important;padding: 6px 8px !important;margin: 0 !important;
            }

            .stTextInput > div > div > button:hover {
                background-color: #0047b3 !important;
            }

            .stTextInput > div > div > button svg {
                fill: #FFFFFF !important;stroke: #FFFFFF !important;color: #FFFFFF !important;
            }

            .stTextInput > div > div > button svg path {
                fill: #FFFFFF !important;stroke: #FFFFFF !important;
            }

            /* Fix the black border on the right side of input */
            .stTextInput > div {
                border: none !important;background: transparent !important;
            }

            .stTextInput > div > div {
                border: none !important;background: transparent !important;
            }

            /* Make sure input container is blue bordered */
            .stTextInput > div > div {
                border: 2px solid #0066FF !important;border-radius: 5px !important;overflow: hidden !important;
            }
            
            /* Quantity +/- buttons - MUST come BEFORE general button styles */
            .stButton[data-testid*="dec_"] button,
            .stButton[data-testid*="inc_"] button {
                background-color: #f0f0f0 !important;
                color: #333 !important;
                border: 1px solid #ddd !important;
                border-radius: 6px !important;
                height: 30px !important;
                width: 30px !important;
                min-height: 30px !important;
                min-width: 30px !important;
                max-height: 30px !important;
                max-width: 30px !important;
                padding: 0 !important;
                margin: 0 !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                line-height: 1 !important;
            }

            .stButton[data-testid*="dec_"] button:hover,
            .stButton[data-testid*="inc_"] button:hover {
                background-color: #d0d0d0 !important;
                border-color: #bbb !important;
            }
                    
            /* Quantity buttons - more specific targeting */
            .stButton > button[kind="secondary"] {
                background-color: #0066FF !important;
                color: white !important;
                border: 1px solid #ddd !important;
                border-radius: 6px !important;
                height: 35px !important;
                min-height: 35px !important;
                padding: 0 !important;
                margin: 0 2px !important;
                font-size: 16px !important;
                font-weight: bold !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }

            .stButton > button[kind="secondary"]:hover {
                background-color: #d0d0d0 !important;
                border-color: #bbb !important;
            }

            /* Ensure buttons are visible */
            button[kind="secondary"] {
                opacity: 1 !important;
                visibility: visible !important;
            }
            
           /* Main buttons (Billing, Display Bills) */
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
            }

            div.stButton > button:hover {
                background-color: #0052cc;
                color: white;
                border-color: #0066FF;
            }
 
   
            /* Action buttons */
            .cancel-btn button {
                background-color: #ff4444 !important;
                color: white !important;
                border: none !important;
            }
            
            .cancel-btn button:hover {
                background-color: #cc0000 !important;
            }
            
            .checkout-btn button {
                background-color: #0066FF !important;
                color: white !important;
                padding: 15px !important;
                border-radius: 10px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                width: 100% !important;
                height: 55px !important;
                border: none !important;
            }
            
            .checkout-btn button:hover {
                background-color: #0052cc !important;
            }
            
            /* Start billing button */
            .start-billing-btn button {
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
            
            .start-billing-btn button:hover {
                background-color: #0052cc !important;
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 102, 255, 0.3);
            }
    
            /* Hide streamlit branding */
            header {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
        """, unsafe_allow_html=True)
    
    # Initialize session state for active tab
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "billing"
    
    # Create scanner object
    if 'scanner' not in st.session_state:
        st.session_state.scanner = ScannerService()

    if 'seen_products' not in st.session_state:
        st.session_state.seen_products = set()

    # Set to false, true only when cashier starts billing
    if 'billing_active' not in st.session_state:
        st.session_state.billing_active = False

    if 'bill_detail_list' not in st.session_state:
        st.session_state.bill_detail_list = []

    if 'bool_checkout' not in st.session_state:
        st.session_state.bool_checkout = True
    
    # Header
    st.markdown("""
        <h1 style="color: #0066FF;margin-top: -130px; margin-left:-350px;">Smart Scan</h1>
        <h2 style="color:black; font-size: 28px;margin-top:-30px;margin-left:-350px;">Cashier Dashboard</h2>
    """, unsafe_allow_html=True)
 
    col1, col2,col3,col4= st.columns([1,1.5,1,4])
    
    with col1:
        if st.button("Billing", key="cashier_billing_btn"):
            st.session_state.active_tab = "billing"
            st.rerun()
    
    with col2:
        if st.button("Display Bills", key="cashier_display_bills",):
            st.session_state.active_tab = "display"
            st.rerun()
    with col3:
        if st.button("Logout",key="cahier_logout"):
            st.session_state.page="login"
            st.session_state.scanner.stop_scanner()
            st.session_state.active_tab="billing"
            st.session_state.billing_active=False
            st.session_state.bill_detail_list=[]
            st.session_state.seen_products=set()
            st.rerun()
        
            
        
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show content based on active tab AND billing state
    if st.session_state.active_tab == "billing":
        if not st.session_state.billing_active:
            show_billing_start_page()  # Clean empty page
        else:
            show_billing_active_page()  # Full billing interface
    elif st.session_state.active_tab=="display":
        show_display_bills_view()


def show_billing_start_page():
    
    st.markdown("""
        <div style="text-align: center; padding: 100px 20px; background-color: white; border-radius: 15px; margin-top: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color: #0066FF; margin-bottom: 20px;">Ready to Start Billing</h2>
            <p style="color: #666; margin-bottom: 40px; font-size: 18px; line-height: 1.6;">
                Click the button below to start scanning products and create a new bill.<br>
                The scanner will automatically detect QR codes.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="start-billing-btn">', unsafe_allow_html=True)
        if st.button("Start New Bill", use_container_width=True, key="start_billing"):
            st.session_state.billing_active = True
            st.session_state.bill_detail_list = []
            st.session_state.seen_products.clear()
            st.session_state.scanner.start_scanner()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def show_billing_active_page():
    """Only show this when billing is active"""
    # Get latest product ID
    prodID = st.session_state.scanner.get_latest_product_id()
    if prodID:
        st.session_state.bill_detail_list, prod_found = scan_bill(
            dbconn, st.session_state.bill_detail_list,
            st.session_state.scanner, st.session_state.seen_products
        )
        if not prod_found:
            st.error("Product Not Found")
    
    bill_id = get_latest_billid_from_db(dbconn)

    # Create a stable container for the entire billing view
    billing_container = st.container()
    
    with billing_container:
        # Header row with column names
        header_cols = st.columns([0.8,1, 3, 1.5,2, 1.5])
        with header_cols[0]:
            st.markdown("<b style='color:black;'>Bill ID</b>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown("<b style='color:black;'>ProdID</b>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown("<b style='color:black;'>Product Name</b>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown("<b style='color:black;'>Unit Price</b>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown("<b style='color:black;'>Quantity</b>", unsafe_allow_html=True)
        with header_cols[5]:
            st.markdown("<b style='color:black;'>Amount</b>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
        
        if st.session_state.bill_detail_list:
            for idx, detail in enumerate(st.session_state.bill_detail_list):
                cols = st.columns([0.8,1, 3, 1.5,2, 1.5])
                with cols[0]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill_id}</p>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.ProdID}</p>', unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.ProductName}</p>', unsafe_allow_html=True)
                with cols[3]:
                    st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{detail.UnitPrice:.2f}</p>', unsafe_allow_html=True)
                with cols[4]:
                    # Quantity controls with improved styling
                    qty_cols = st.columns([1, 2, 1])
                    with qty_cols[0]:
                        if st.button("➖", key=f"dec_{detail.ProdID}_{idx}", use_container_width=True):
                            change_quantity(dbconn, detail.ProdID, st.session_state.bill_detail_list, -1)
                            st.rerun()
                    
                    with qty_cols[1]:
                        st.markdown(
                            f'<div style="text-align:center; padding:8px 0; color:black; font-weight:600; font-size:16px; background-color:white; border-radius:6px; margin:0 5px;">{detail.QuantitySold}</div>', 
                            unsafe_allow_html=True
                        )
                    
                    with qty_cols[2]:
                        if st.button("➕", key=f"inc_{detail.ProdID}_{idx}", use_container_width=True):
                            change_quantity(dbconn, detail.ProdID, st.session_state.bill_detail_list, 1)
                            st.rerun()
                    
                with cols[5]:
                    st.markdown(f'<p style="font-weight:600; color:#0066FF; margin:0; padding-top:8px;">{detail.TotalAmount:.2f}</p>', unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 5px 0; border: 0.5px solid #f0f0f0;'>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: white; padding: 40px; text-align:center; border-radius: 10px;">
                    <p style="color:#0066FF; margin:0; font-size: 18px;">Scan QR code to add products</p>
                </div>
            """, unsafe_allow_html=True)

        # Customer Name and Checkout section (only show if items exist)
        if st.session_state.bill_detail_list:
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Customer Name Input
            st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 10px; color:#0066FF;">Customer Name</p>', 
                        unsafe_allow_html=True)
            customer_name = st.text_input("", placeholder="Enter customer name", 
                                            label_visibility="collapsed", key="customer_name")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Calculate and display total
            total = get_total_from_details(st.session_state.bill_detail_list)
            
            # Total amount
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            margin-bottom: 20px; padding: 20px; background-color: white; 
                            border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <span style="font-size: 18px; font-weight: 600; color:#333;">Total Amount</span>
                    <span style="font-size: 28px; font-weight: 700; color: #0066FF;">PKR {total:.2f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Checkout buttons
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
                if st.button("Cancel Bill", use_container_width=True, key="cancel_bill"):
                    # Stop scanner and reset state
                    st.session_state.scanner.stop_scanner()
                    st.session_state.billing_active = False  # This triggers empty state
                    st.session_state.bill_detail_list = []
                    st.session_state.seen_products.clear()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="checkout-btn">', unsafe_allow_html=True)
                if st.button("Checkout & Print", use_container_width=True, key="checkout_bill"):
                    if not st.session_state.bill_detail_list:
                        st.error("Error: Bill must have at least 1 product!")
                    elif not (customer_name.strip() and customer_name.replace(" ", "").isalpha()):
                        st.error("Invalid customer name")
                    else:
                        if checkout_billing(dbconn, st.session_state.bill_detail_list, customer_name, st.session_state.empID):
                            st.success("Bill saved successfully!")
                            st.session_state.scanner.stop_scanner()
                            st.session_state.billing_active = False  # This triggers empty state
                            st.session_state.bill_detail_list = []
                            st.session_state.seen_products.clear()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Bill could not be saved")
                st.markdown('</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="start-billing-btn">', unsafe_allow_html=True)
        if st.button("Stop Billing", use_container_width=True, key="stop_billing"):
            st.session_state.billing_active = False
            st.session_state.bill_detail_list = []
            st.session_state.seen_products.clear()
            st.session_state.scanner.stop_scanner()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Auto-refresh for continuous scanning - but only if billing is active
    if st.session_state.billing_active:
        time.sleep(0.5)
        st.rerun()


def show_display_bills_view():
    st.session_state.scanner.stop_scanner()
    st.session_state.billing_active=False
    st.session_state.bill_detail_list=[]
    st.session_state.seen_products=set()
    employee_name=employee_obj.get_name_by_id(st.session_state.empID)
    st.markdown(f'<h3 style="color:#333;margin-bottom:20px;">Bills completed by {employee_name}</h3>', unsafe_allow_html=True)
    employee_bills = billDatabase_obj.get_bills(st.session_state.empID)
    
    if not employee_bills:
        st.markdown("""
            <div style="background-color: white; padding: 40px; text-align:center; border-radius: 10px; margin-top: 20px;">
                <p style="color:#666; margin:0; font-size: 18px;">No bills found for this employee</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    bills_container = st.container()
    with bills_container:
        # Header row with column names
        header_cols = st.columns([1,1.5,3, 1.5, 1])
        with header_cols[0]:
            st.markdown("<b style='color:black;'>Bill ID</b>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown("<b style='color:black;'>Customer Name</b>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown("<b style='color:black;'>Date</b>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown("<b style='color:black;'>Total Amount</b>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown("<b style='color:black;'>EmpID</b>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

        # Display each bill
        for bill in employee_bills:
            cols = st.columns([1,1.5,3, 1.5, 1])
            with cols[0]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[0]}</p>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[1]}</p>', unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[2]}</p>', unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">PKR {bill[3]:.2f}</p>', unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f'<p style="color:black; margin:0; padding-top:8px;">{bill[4]}</p>', unsafe_allow_html=True)
            st.markdown("<hr style='margin: 5px 0; border: 0.5px solid #f0f0f0;'>", unsafe_allow_html=True)



     