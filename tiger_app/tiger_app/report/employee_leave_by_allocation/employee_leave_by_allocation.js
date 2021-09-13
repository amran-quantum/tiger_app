// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Leave By Allocation"] = {
	"filters": [
		// {
		// 	"fieldname":"employee",
		// 	"label": __("Employee"),
		// 	"fieldtype": "Link",
		// 	"options": "Employee",
		// 	"width": "80"
		// }
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.year_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.year_end()
		}
	]
};
