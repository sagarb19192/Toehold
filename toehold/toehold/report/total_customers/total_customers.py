import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data

def get_columns():
    return [
        _("Total Customers") + ":Data:150",
        _("Count") + ":Int:100"
    ]

def get_data():
    total_customers = frappe.db.count('Customer')
    return [["Total Customers", total_customers]]
