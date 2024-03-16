import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
    columns = get_columns()
    data, chart = get_data_and_chart(filters)
    return columns, data, None, chart

def get_columns():
    return [
        _("Month-Year") + ":Data:150",
        _("Category") + ":Data:150",
        _("Total Revenue") + ":Currency:150"
    ]

def get_data_and_chart(filters):
    # Construct the query to fetch the data
    query = """
        SELECT 
            CONCAT(DATE_FORMAT(si.posting_date, '%M'), '-', DATE_FORMAT(si.posting_date, '%Y')) AS month_year,
            si.custom_category AS category,
            SUM(si.grand_total) AS total_revenue
        FROM `tabSales Invoice` si
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
        GROUP BY month_year, category
        ORDER BY month_year, category
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Format the data into rows for the report
    formatted_data = [[d.month_year, d.category, d.total_revenue] for d in data]

    # Prepare chart data
    chart = {
        'data': {
            'labels': [f"{d.month_year} - {d.category}" for d in data],
            'datasets': [{
                'name': 'Total Revenue',
                'values': [d.total_revenue for d in data],
            }]
        },
        'type': 'bar'
    }

    return formatted_data, chart
