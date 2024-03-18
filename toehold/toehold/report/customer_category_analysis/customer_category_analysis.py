import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data, chart = get_data_and_chart(filters)
    return columns, data, None, chart

def get_columns():
    return [
        _("Customer") + ":Link/Customer:200",
        _("Category") + ":Data:200"
    ]

def get_data_and_chart(filters):
    # Construct the query to fetch the data
    query = """
        SELECT 
            si.customer AS customer,
            si.custom_category AS category
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 0
        GROUP BY customer, category
        ORDER BY customer, category
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Prepare chart data
    chart_data = {
        'labels': [],
        'datasets': [{
            'name': 'Category Distribution',
            'values': {}
        }]
    }

    for row in data:
        customer = row.customer
        category = row.category
        if customer not in chart_data['datasets'][0]['values']:
            chart_data['datasets'][0]['values'][customer] = {}
        if category not in chart_data['datasets'][0]['values'][customer]:
            chart_data['datasets'][0]['values'][customer][category] = 0
        chart_data['datasets'][0]['values'][customer][category] += 1

    # Format the data into rows for the report
    formatted_data = [[d.customer, d.category] for d in data]

    return formatted_data, chart_data
