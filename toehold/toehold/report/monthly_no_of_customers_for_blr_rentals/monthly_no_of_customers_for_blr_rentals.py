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
        _("No of Customers") + ":Int:150"
    ]

def get_data_and_chart(filters):
    # Construct the query to fetch the data
    query = """
        SELECT 
            CONCAT(DATE_FORMAT(si.posting_date, '%M'), '-', DATE_FORMAT(si.posting_date, '%Y')) AS month_year,
            COUNT(DISTINCT(si.customer)) AS no_of_customers
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 0
            AND si.custom_category = 'BLR-Rentals'
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
        GROUP BY month_year
        ORDER BY month_year
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Prepare chart data
    chart_data = {
        'labels': [],
        'datasets': [{
            'name': 'No of Customers',
            'values': []
        }]
    }

    for row in data:
        chart_data['labels'].append(row.month_year)
        chart_data['datasets'][0]['values'].append(row.no_of_customers)

    chart = {
        'data': chart_data,
        'type': 'bar'
    }

    # Format the data into rows for the report
    formatted_data = [[d.month_year, d.no_of_customers] for d in data]

    return formatted_data, chart
