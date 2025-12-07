import streamlit as st
from lucide import lucide_icon
from databases.mysql_connector import connect_db
from services.employeeService import validate_login

dbconn=connect_db()

def loginPage():
    # Hide Streamlit header
    st.markdown("""<style>header {display: none !important;}</style>""", unsafe_allow_html=True)

    # Lucide icons
    packageIcon = lucide_icon("package", width="50", height="50", stroke="white")
    shoppingIcon = lucide_icon("shopping-cart", width="35", height="35", stroke="white")
    chartIcon = lucide_icon("chart-column-increasing", width="35", height="35", stroke="white")
    if st.session_state.page=="login":
         
        # Css styling - ONLY for login page
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: white;
        }

        /* Left Panel */
        .left-half {
            position: fixed;left: 0;top: 0;width: 50vw;height: 100vh;background-color: #0066FF;color: white;padding: 5px;z-index: 0;
        }
        /* Icon styling */
        .icon-heading {margin-top: 30px;display: flex;align-items: center;gap: 20px;
        }

        .icon-row {
            margin-top: 60px;margin-left: 60px;display: flex;flex-direction: column;gap: 35px;
        }

        .icon-box {
            width: 65px;height: 65px;background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.05) 100%);
            border-radius: 16px;display: flex;align-items: center;justify-content: center;box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);border: 1px solid rgba(255,255,255,0.2);
        }

        .feature-item {
            display: flex;align-items: center;gap: 20px;
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
        /* Login button */
        div.stButton {
            position: relative;z-index: 999 !important;
        }

        div.stButton > button {
            background-color: #0066FF;color: white;padding: 10px 20px;border-radius: 8px;font-size: 16px;font-weight: bold;cursor: pointer;width: 100%;
        }

        div.stButton > button:hover {
            background-color: #0047b3;
        }
        </style>
        """, unsafe_allow_html=True)

    # Layout
    left_col, right_col = st.columns([1, 0.75])

    # Left panel with branding
    with left_col:
        st.markdown(f"""
        <div class="left-half"> 
            <div class="icon-heading"> 
                <div class="icon-box">{packageIcon}</div> 
                <div>
                    <h1 style="margin:0; margin-top:-25px; line-height:1; font-weight:700; font-size:42px;">ScanSmart</h1>
                    <p style="margin:0; margin-top:-22px; font-size:16px; opacity:0.85; font-weight:400;">Inventory Management</p>
                </div>
            </div>
            <div class="icon-row">
                <div class="feature-item">
                    <div class="icon-box">{chartIcon}</div>
                    <h3 style="margin:0;">Real Time Analytics</h3>
                </div>
                <div class="feature-item">
                    <div class="icon-box">{shoppingIcon}</div>
                    <h3 style="margin:0;">Smart Billing</h3>
                </div>
                <div class="feature-item">
                    <div class="icon-box">{packageIcon}</div>
                    <h3 style="margin:0;">Control, Track, Optimize</h3>
                </div>
            </div>
            <p style="margin-top:150px; margin-left:65px;">CS:220 Database Systems Project.</p>
            <p style="margin-left:65px;">© 2025 ScanSmart. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)

    # Right panel with login form
    with right_col:
        st.markdown("""
            <h1 style="text-align:left; color:#0066FF; margin-top:-80px;">Welcome Back</h1>
            <h4 style="text-align:left; color:black; margin-top:20px;">Enter your credentials</h4>
        """, unsafe_allow_html=True)
    
        email = st.text_input("Employee email", placeholder="Enter email",key="login_email")
        password = st.text_input("Employee password", placeholder="Enter password",key="login_password", type="password")
        
        if st.button("Login"):
            if email and password:
                role, st.session_state.empID = validate_login(dbconn, email, password)
                if role == "Not Found":
                    st.error("Not Found!")
                else:
                    st.success("Login Successfully")
                    # Set session state
                    st.session_state.role = role
                    
                    if role == "Cashier":
                        st.session_state.page = "Cashier"
                    elif role == "Admin":
                        st.session_state.page = "Admin"
                    st.rerun()
            else:
                st.error("Please enter both email and password")