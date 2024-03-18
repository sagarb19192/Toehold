// Copyright (c) 2024, Helloapps and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly total no of customers for photo tour items"] = {
	"filters": [
		{
            "fieldname": "custom_category",
            "label": __("Category"),
            "fieldtype": "Link",
            "options": "Category",
			"default":"Photo tour"
        },
		{
            "fieldname": "item_code",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item"
        },

	]
};
