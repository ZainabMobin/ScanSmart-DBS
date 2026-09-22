import pytest
from services.employeeService import validate_login
from databases.mysql_connector import connect_db


# create database connection once for all cases 
@pytest.fixture(scope="module")
def dbconn():
    conn = connect_db()
    yield conn
    conn.close()


# parametrise inputs, expected outputs
@pytest.mark.parametrize("email, password, expected_role, expected_id", [
    ('ali@shop.com', 'Cashier1', 'Cashier', 1),
    ('ahmed@shop.com', 'Cashier2', 'Cashier', 2),
    ('sara@shop.com', 'Cashier3', 'Cashier', 3),
    ('hassan@shop.com', 'Cashier4', 'Cashier', 4),
    ('fatima@shop.com', 'Cashier5', 'Cashier', 5),
    ('bilal@shop.com', 'Cashier6', 'Cashier', 6),
    ('zain@shop.com', 'Cashier7', 'Cashier', 7),
    ('hadiqa@shop.com', 'Cashier8', 'Cashier', 8),
    ('noman@shop.com', 'Admin1', 'Admin', 9),
    ('maryam@shop.com', 'Admin2', 'Admin', 10),
    ('usman@shop.com', 'Admin3', 'Admin', 11),
    ('saad@shop.com', 'Admin4', 'Admin', 12),
    ('maham@shop.com', 'Admin5', 'Admin', 13),
    ('imran@shop.com', 'Admin6', 'Admin', 14),
    ('ayesha@shop.com', 'Admin7', 'Admin', 15),
])


def test_check_login(dbconn, email, password, expected_role, expected_id):
    role, id = validate_login(dbconn, email, password)
    # compare returned vs expected
    print(f"\n[DEBUG] Input: {email} {password} | Got: ({role=}, {id=}) | Expected: ({expected_role=}, {expected_id=})")

    assert role == expected_role
    assert id == expected_id

# checks if employees are able to log in
# pytest -s -v login_test.py