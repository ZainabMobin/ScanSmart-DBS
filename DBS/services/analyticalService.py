import mysql.connector
import matplotlib.pyplot as plt
import streamlit as st

def plot_sales_by_category(dbconn):
    """Graph 1: Sales by Category"""
    query = """
    SELECT p.Category, SUM(bd.TotalAmount) as TotalSales
    FROM BillDetail bd
    JOIN Product p ON bd.ProdID = p.ProdID
    GROUP BY p.Category
    ORDER BY TotalSales DESC;
    """

    try:
        cursor = dbconn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            st.error("✗ No data found for sales by category!")
            return None

        categories = [row[0] for row in data]
        sales = [float(row[1]) for row in data]

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(categories, sales, color='#0066FF')
        ax.set_xlabel('Product Category', fontsize=12)
        ax.set_ylabel('Total Sales (PKR)', fontsize=12)
        ax.set_title('Total Sales by Category', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig  # Return figure instead of showing
        
    except mysql.connector.Error as err:
        st.error(f"✗ Database error: {err}")
        return None


def plot_top_products(dbconn, top_n=10):
    """Graph 2: Top Selling Products"""
    query = """
    SELECT p.Name, SUM(bd.QuantitySold) as TotalQuantity
    FROM BillDetail bd
    JOIN Product p ON bd.ProdID = p.ProdID
    GROUP BY p.ProdID, p.Name
    ORDER BY TotalQuantity DESC
    LIMIT %s;
    """

    try:
        cursor = dbconn.cursor()
        cursor.execute(query, (top_n,))
        data = cursor.fetchall()

        if not data:
            st.error("✗ No data found for top products!")
            return None

        products = [row[0] for row in data]
        quantities = [row[1] for row in data]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(products, quantities, color='#00CC66')
        ax.set_xlabel('Quantity Sold', fontsize=12)
        ax.set_ylabel('Product Name', fontsize=12)
        ax.set_title(f'Top {top_n} Selling Products', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        
        return fig  # Return figure instead of showing
        
    except mysql.connector.Error as err:
        st.error(f"✗ Database error: {err}")
        return None


def plot_daily_sales_trend(dbconn):
    """Graph 3: Daily Sales Trend"""
    query = """
    SELECT DATE(Date) as SaleDate, SUM(TotalAmount) as DailySales
    FROM Bill
    GROUP BY DATE(Date)
    ORDER BY SaleDate;
    """

    try:
        cursor = dbconn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            st.error("✗ No data found for daily sales!")
            return None

        dates = [row[0] for row in data]
        sales = [float(row[1]) for row in data]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, sales, marker='o', linewidth=2, markersize=6, color='#0066FF')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Total Sales (PKR)', fontsize=12)
        ax.set_title('Daily Sales Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig  # Return figure instead of showing
        
    except mysql.connector.Error as err:
        st.error(f"✗ Database error: {err}")
        return None


def plot_employee_performance(dbconn):
    """Graph 4: Employee Performance"""
    query = """
    SELECT e.Name, COUNT(b.BillID) as TotalBills, SUM(b.TotalAmount) as TotalSales
    FROM Bill b
    JOIN Employee e ON b.EmployeeID = e.EmployeeID
    GROUP BY e.EmployeeID, e.Name
    ORDER BY TotalSales DESC;
    """

    try:
        cursor = dbconn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            st.error("✗ No data found for employee performance!")
            return None

        employees = [row[0] for row in data]
        total_sales = [float(row[2]) for row in data]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(employees, total_sales, color='#FF6B6B')
        ax.set_xlabel('Employee Name', fontsize=12)
        ax.set_ylabel('Total Sales (PKR)', fontsize=12)
        ax.set_title('Employee Sales Performance', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig  # Return figure instead of showing
        
    except mysql.connector.Error as err:
        st.error(f"✗ Database error: {err}")
        return None


def plot_inventory_status(dbconn, threshold=50):
    """Graph 5: Inventory Status (Low Stock)"""
    query = """
    SELECT Name, QuantityAvailable
    FROM Product
    ORDER BY QuantityAvailable ASC
    LIMIT 15;
    """

    try:
        cursor = dbconn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            st.error("✗ No data found for inventory status!")
            return None

        products = [row[0] for row in data]
        quantities = [row[1] for row in data]

        colors = ['red' if q < threshold else 'orange' if q < 100 else 'green' 
                  for q in quantities]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(products, quantities, color=colors)
        ax.axvline(threshold, color='red', linestyle='--', linewidth=2, 
                   label=f'Low Stock Threshold ({threshold})')
        ax.set_xlabel('Quantity Available', fontsize=12)
        ax.set_ylabel('Product Name', fontsize=12)
        ax.set_title('Inventory Status', fontsize=14, fontweight='bold')
        ax.legend()
        plt.tight_layout()
        
        return fig  # Return figure instead of showing
        
    except mysql.connector.Error as err:
        st.error(f"✗ Database error: {err}")
        return None