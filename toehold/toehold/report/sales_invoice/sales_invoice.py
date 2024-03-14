import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        _("Date") + ":Date:100",
        _("Customer") + ":Link/Customer:200",
        _("Item") + ":Link/Item:120",
        _("Place of Supply") + ":Data:180",  # New column
        _("HSN/SAC") + ":Data:120",          # New column
        _("Quantity") + ":Float:100",
        _("Amount") + ":Currency:120",
        _("Sales Taxes and Charges") + ":Currency:180",
        _("Total Taxes and Charges") + ":Currency:180",
        _("Grand Total") + ":Currency:150"
    ]

    return columns

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND si.posting_date >= '{0}'".format(filters["from_date"])
    if filters.get("to_date"):
        conditions += " AND si.posting_date <= '{0}'".format(filters["to_date"])
    if filters.get("customer"):
        conditions += " AND si.customer = '{0}'".format(filters["customer"])
    if filters.get("item"):
        conditions += " AND si_item.item_code = '{0}'".format(filters["item"])

    data_query = """
        SELECT si.posting_date, si.customer, si_item.item_code, si_item.qty, si_item.amount,
               si.taxes_and_charges, si.total_taxes_and_charges, si.grand_total,
               item.custom_place_of_supply AS place_of_supply, item.custom_hsn_sac AS hsn_sac
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Item` si_item ON si.name = si_item.parent
        LEFT JOIN `tabItem` item ON si_item.item_code = item.name
        WHERE 1=1 {0}
    """.format(conditions)

    sales_invoices = frappe.db.sql(data_query, as_dict=True)

    data = []
    for invoice in sales_invoices:
        row = [
            invoice.posting_date,
            invoice.customer,
            invoice.item_code,
            invoice.place_of_supply,
            invoice.hsn_sac,
            invoice.qty,
            invoice.amount,
            invoice.taxes_and_charges,
            invoice.total_taxes_and_charges,
            invoice.grand_total
        ]
        data.append(row)

    return data
