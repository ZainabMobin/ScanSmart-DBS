import streamlit as st
from databases.mysql_connector import connect_db
from services.styleLoader import inject_global_css
from pages.cash import cashier_page
from pages.login import loginPage
from pages.admin import admin_page
import logging, sys
from pathlib import Path

# Force attach standard stdout handler to root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove existing stale handlers to prevent duplicate lines
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# Test external css loaded
logging.info("--> LOGGER INITIALIZED SUCCESSFULLY <--")
print("--> PRINT STATEMENT FLUSHED <--", flush=True)


# Database connection
dbconn = connect_db()
 
# load css
inject_global_css("assets/style.css")

# Initializing session states
if "page" not in st.session_state:
    st.session_state.page="login"
if "empID" not in st.session_state:
    st.session_state.empID = None
if "role" not in st.session_state:
    st.session_state.role = None

# ------------loginPage--------------
if st.session_state.page == "login":
    loginPage(dbconn)
     
# ----------Cashier page-------------
elif st.session_state.page == "Cashier":
    cashier_page()

#-----------admin page---------------
elif st.session_state.page== "Admin":
    admin_page()