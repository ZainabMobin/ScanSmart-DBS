import pytest
from services.employeeService import validate_login
from databases.mysql_connector import connect_db


# create database connection once for all cases 
@pytest.fixture(scope="module")
def dbconn():
    conn = connect_db()
    yield conn
    conn.close()

# partition logins under: 
# cashier, manager

# parametrise inputs, expected outputs
@pytest.mark.parametrize("email, password, expected_role, expected_id", [
    ('ali@shop.com', 'Cashier1', 'Cashier', 1),
    ('zain@shop.com', 'Cashier7', 'Cashier', 7),
    ('noman@shop.com', 'Admin1', 'Admin', 9),
    ('maham@shop.com', 'Admin5', 'Admin', 13),
])


def test_check_login(dbconn, email, password, expected_role, expected_id):
    role, id = validate_login(dbconn, email, password)
    # compare returned vs expected
    print(f"\n[DEBUG] Input: {email} {password} | Got: ({role=}, {id=}) | Expected: ({expected_role=}, {expected_id=})")

    assert role == expected_role
    assert id == expected_id

# checks if employees are able to log in
# pytest -s -v login_test.py