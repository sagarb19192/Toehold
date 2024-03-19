import frappe
import pandas as pd
from frappe.utils.data import nowdate
from datetime import datetime
import csv
import re
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import read_csv_content
@frappe.whitelist(allow_guest=True)
def upload_csv():
    try:
        uploaded_file = frappe.request.files.get("Customer Data")

        if not uploaded_file:
            return {"status": "error", "message": "No file uploaded."}

        
        file_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', uploaded_file.filename)
        file_path = frappe.get_site_path("public", file_name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        
        with open(file_path, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                create_customer_from_csv(row)

        return {"status": "success", "message": "Excel data processed successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def create_customer_from_csv(row):
    try:
        customer_name = row.get('Customer Name')
        customer_group = "Individual"
        territory = "India"

        if not frappe.db.exists("Customer", customer_name):
            customer = frappe.get_doc({
                'doctype': 'Customer',
                'customer_name': customer_name,
                'customer_group': customer_group,
                'territory': territory
            })
            customer.insert(ignore_permissions=True)

        item_code = row.get('Item Name')
        item_qty = "1"
        item_description = row.get('Item Description')
        rate = row.get('Total (BCY)')
        # if rate and float(rate) < 0:
        #     rate = str(abs(float(rate)))  # Convert negative value to positive
        #     item_qty = "-1"  # Set quantity to negative for credit note
        tax_template = row.get('Tax Percentage')
        place = row.get('Place Of Supply')
        customer_email = row.get('Customer Email')
        category_name = row.get('Account')
        date = row.get('Date')  # You need to specify the column name for date
        qty = row.get('Quantity')
        is_return = row.get('Is Return')

        # Check if category exists, if not create it
        category = frappe.get_doc({
            'doctype': 'Category',
            'category_name': category_name
        })
        if not frappe.db.exists("Category", category_name):
            category.insert(ignore_permissions=True)

        if not frappe.db.exists("Item", item_code):
            create_item(item_code)

        sales_invoice = frappe.get_doc({
            'doctype': 'Sales Invoice',
            'customer': customer_name,
            'taxes_and_charges': tax_template,
            'custom_customer_email': customer_email,
            'custom_place_of_supply': place,
            'custom_category': category_name,  # Assign category name here
            'posting_date': date,
            'set_posting_time': 1,
            'is_return': is_return,
            'items': [{
                'item_code': item_code,
                'qty': item_qty,
                "description": item_description,
                'rate': rate,
                'qty': qty,
            }]
        })
        sales_invoice.insert(ignore_permissions=True)

    except Exception as e:
        # If any exception occurs during row processing, log the error and continue
        frappe.log_error(f"Error processing row: {row}. Error: {str(e)}")

def create_item(item_code):
    if not frappe.db.exists("Item", item_code):
       
        new_item = frappe.new_doc("Item")
        new_item.item_code = item_code
        new_item.item_group="All Item Groups"
        new_item.save(ignore_permissions=True)


# def upload_csv_customers():
#         filepath = get_file("salescrm.csv")
#         print(filepath)
#         data = read_csv_content(filepath[1])
#         print(data)
        
#         header = data[0]

        
#         for row in data[1:]:
#             create_customer_from_csv1(row)

# import requests

# def create_customer_from_csv1(row):
#     customer_name = row[5]

#     if not frappe.db.exists("Customer", customer_name):
        
#         customer = frappe.get_doc({
#             'doctype': 'Customer',
#             'customer_name': customer_name
#         })
        
#         customer.save(ignore_permissions=True)
#         frappe.db.commit()

#     item_code = row[8]

#     if not frappe.db.exists("Item", item_code):
#         create_item1(item_code)

#     sales_invoice = frappe.get_doc({
#         'doctype': 'Sales Order',
#         'customer': customer_name,
#         'items': [{
#             'item_code': item_code,
#             'qty': "1"
#         }]
#     })
    
#     sales_invoice.insert(ignore_permissions=True)
#     sales_invoice.save()

# def create_item1(item_code):
#     if not frappe.db.exists("Item", item_code):
#         new_item = frappe.new_doc("Item")
#         new_item.item_code = item_code
#         new_item.item_group = "All Item Groups"
#         new_item.save(ignore_permissions=True)
