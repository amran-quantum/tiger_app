// Copyright (c) 2016, amran and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Phonebook report"] = {
	"filters": [
		{
			"fieldname":"fullname",
			"label": __("Fullname"),
			"fieldtype": "Data",
			"width": "100px"
		},
		{
			"fieldname":"code",
			"label": __("Code"),
			"fieldtype": "Data",
			"width": "100px"
		}
	]
};
