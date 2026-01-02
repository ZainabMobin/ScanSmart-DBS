import streamlit as st
from databases.mysql_connector import connect_db
from pages.cash import cashier_page
from pages.login import loginPage
from pages.admin import admin_page
 
# Database connection
dbconn = connect_db()
 

# Initializing session states
if "page" not in st.session_state:
    st.session_state.page="login"
if "empID" not in st.session_state:
    st.session_state.empID = None
if "role" not in st.session_state:
    st.session_state.role = None

# ------------loginPage--------------
if st.session_state.page == "login":
    loginPage()
     
# ----------Cashier page-------------
elif st.session_state.page == "Cashier":
    cashier_page()

#-----------admin page---------------
elif st.session_state.page== "Admin":
    admin_page()