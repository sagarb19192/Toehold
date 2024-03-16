import frappe
#sales invoice tax and total calculation
def update_sales_taxes(self, method):
    taxes = frappe.get_all("Sales Taxes and Charges", {"parent": self.taxes_and_charges}, ["*"])
    for tax in taxes:
        if not self.taxes:
            self.append("taxes",{
                "charge_type": tax.charge_type,
                "account_head": tax.account_head,
                "rate": tax.rate,
                "description": "Tax",
                "amount": tax.rate * self.total,
                "total": self.total + (tax.rate * self.total)
            })
            self.save(ignore_permissions=True)