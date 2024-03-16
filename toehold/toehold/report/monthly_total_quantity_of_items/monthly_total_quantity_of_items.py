import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Item") + ":Data:250",
        _("Total Quantity") + ":Int:150"
    ]

def get_data(filters):
    # Construct the query to fetch the data
    query = """
        SELECT 
            sii.item_code AS item,
            COUNT(si.name) AS total_quantity
        FROM `tabSales Invoice` si
        LEFT JOIN `tabSales Invoice Item` sii ON si.name = sii.parent
        WHERE si.docstatus = 0
    """

    if filters and filters.get('month') and filters.get('year'):
        # Extract month and year from filters
        month = int(filters['month'])
        year = int(filters['year'])
        # Set date range for the specified month and year
        start_date = datetime(year, month, 1).strftime('%Y-%m-%d')
        end_date = datetime(year, month+1, 1).strftime('%Y-%m-%d')
        query += f" AND si.posting_date >= '{start_date}' AND si.posting_date < '{end_date}'"

    query += """
        GROUP BY item
        ORDER BY item
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Format the data into rows for the report
    formatted_data = [[d.item, d.total_quantity] for d in data]

    return formatted_data
