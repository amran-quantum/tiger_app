# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []

	columns = get_columns()
	data = get_data(filters,columns)
	return columns, data
def get_columns():
	leave_type_list = frappe.db.sql("""
	select distinct leave_type from `tabLeave Allocation` order by leave_type asc
	""",as_dict=True)
	cols = ["Employee Name"]
	for el in leave_type_list:
		cols.append(el.leave_type+" Start")
		cols.append(el.leave_type+" End")
		cols.append("Total")
	return cols

	

def get_data(filters,columns):
	data = frappe.db.sql("""
	select * from `tabLeave Application` where from_date >= %(from_date)s  and to_date <= %(to_date)s and status=%(status)s
	order by leave_type asc""",{"from_date":filters.from_date,"to_date":filters.to_date,"status":"Approved"},as_dict=1)
	result = []

	leave_type_list = frappe.db.sql("""select distinct leave_type from `tabLeave Allocation` order by leave_type asc""",as_list=True)
	for elem in data:
		row = []
		row.append(elem.employee_name)

		for el in leave_type_list:
			if el == elem.leave_type:
				row.append(elem.from_date)
				row.append(elem.to_date)
				row.append(elem.total_leave_days)
			
			
		
		result.append(row)

	
	return result
	
		