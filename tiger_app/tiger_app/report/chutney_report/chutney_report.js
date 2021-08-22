// Copyright (c) 2016, amran and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Chutney Report"] = {
	"filters": [
		{
            "fieldname":"fruit_name",
            "label": __("Fruit Name"),
            "fieldtype": "Data",
			"default": "",
			"reqd": 1
        }
	]
};
