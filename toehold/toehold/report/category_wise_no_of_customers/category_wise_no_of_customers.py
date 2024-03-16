import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Category") + ":Data:150",
        _("No. of Customers") + ":Int:150"
    ]

def get_data(filters):
    # Construct the query to fetch the data
    query = """
        SELECT si.custom_category AS category, COUNT(DISTINCT si.customer) AS customer_count
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 0 
    """

    if filters and filters.get('from_date'):
        query += f" AND si.posting_date >= '{filters['from_date']}'"
    if filters and filters.get('to_date'):
        query += f" AND si.posting_date <= '{filters['to_date']}'"

    query += """
        GROUP BY si.custom_category
        ORDER BY si.custom_category
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Format the data into rows for the report
    formatted_data = [[d.category, d.customer_count] for d in data]

    return formatted_data
