# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []

	columns = get_columns()
	data = get_data(filters)
	return columns, data
def get_columns():
	leave_type_list = frappe.db.sql("""
	select distinct leave_type from `tabLeave Allocation` order by leave_type asc
	""",as_dict=True)
	cols = ["Employee","Employee Name"]
	for el in leave_type_list:
		cols.append(el.leave_type+" Start")
		cols.append(el.leave_type+" End")
		cols.append("Total")
	return cols
	# return []

	

def get_data(filters):
	data = frappe.db.sql("""
	select employee, employee_name, leave_type, from_date, to_date, total_leave_days from `tabLeave Application` where from_date >= %(from_date)s  and to_date <= %(to_date)s and status=%(status)s
	""",{"from_date":filters.from_date,"to_date":filters.to_date,"status":"Approved"},as_dict=1)
	
	leave_type_list = frappe.db.sql("""select distinct leave_type from `tabLeave Allocation`""",as_dict=True)
	employee_list = frappe.db.sql("""select distinct employee, employee_name from `tabLeave Allocation`""",as_dict=True)
	
	result = []
	for em in employee_list:
		edata = []
		for elem in data:
			if elem.employee == em.employee:
				edata.append(elem)
		sorted_row = []
		for el in edata:
			if not any(el.employee in d for d in result):
				sorted_row.append(el.employee)
				sorted_row.append(el.employee_name)
			else:
				sorted_row.append("")
				sorted_row.append("")

			for item in leave_type_list:
				if item.leave_type == el.leave_type:
					sorted_row.append(el.from_date)
					sorted_row.append(el.to_date)
					sorted_row.append(el.total_leave_days)
				else:
					sorted_row.append("")
					sorted_row.append("")
					sorted_row.append("")
			result.append(sorted_row)
			# frappe.msgprint(str(sorted_row))
	return result