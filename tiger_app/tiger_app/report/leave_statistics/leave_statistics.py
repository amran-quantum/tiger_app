# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []

	columns, leave_type_list = get_columns()
	data = get_data(filters,leave_type_list)
	return columns, data
def get_columns():
	leave_type_list = frappe.db.sql("""
	select distinct leave_type from `tabLeave Allocation` order by leave_type asc
	""",as_dict=True)
	cols = ["Employee","Employee Name"]
	for el in leave_type_list:
		cols.append(el.leave_type+" Start")
		cols.append(el.leave_type+" End")
		cols.append(el.leave_type+" Total")
	return cols,leave_type_list

def get_data(filters,leave_type_list):
	data = frappe.db.sql("""
	select employee, employee_name, leave_type, from_date, to_date, total_leave_days from `tabLeave Application` where from_date >= %(from_date)s  and to_date <= %(to_date)s and status=%(status)s
	order by employee, leave_type asc""",{"from_date":filters.from_date,"to_date":filters.to_date,"status":"Approved"},as_dict=1)
	
	result = []
	for idx,item in enumerate(data):
		row = []
		row.append(item.employee)
		row.append(item.employee_name)

		for litem in leave_type_list:
			row.append("")
			row.append("")
			row.append("")
		for index,ritem in enumerate(leave_type_list):
			if ritem.leave_type == item.leave_type:
				row[2+ 3*index] = item.from_date
				row[3+ 3*index] = item.to_date
				row[4+ 3*index] = item.total_leave_days
		result.append(row)
	
					


		
	return result