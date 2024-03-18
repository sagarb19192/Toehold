import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Category") + ":Data:150"
    ]

def get_data(filters):
    # Construct the query to fetch the data
    query = """
        SELECT DISTINCT custom_category AS category
        FROM `tabSales Invoice`
        WHERE docstatus = 0
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Format the data into rows for the report
    formatted_data = [[d.category] for d in data]

    return formatted_data
