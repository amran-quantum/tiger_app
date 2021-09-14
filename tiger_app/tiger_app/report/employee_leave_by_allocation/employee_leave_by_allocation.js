// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
let years = []
for(let i=2016;i<2026;i++){
	years.push(""+i)
}

frappe.query_reports["Employee Leave By Allocation"] = {
	"filters": [
		{
			"fieldname":"year",
			"label": __("year"),
			"fieldtype": "Select",
			"options": years,
			"width": "50"
		}
		// {
		// 	"fieldname":"from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	"reqd": 1,
		// 	"default": frappe.datetime.year_start()
		// },
		// {
		// 	"fieldname":"to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
		// 	"reqd": 1,
		// 	"default": frappe.datetime.year_end()
		// }
	]
};
