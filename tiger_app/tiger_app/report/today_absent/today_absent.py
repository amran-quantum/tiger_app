# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []

	columns = get_columns()
	data = get_data(filters)
	return columns, data
def get_columns():
	return ["Department Code","Employee Name","Absent From","To", "Num"]

def get_data(filters):
	return frappe.db.sql("""
	select e.department_code,la.employee_name,  la.from_date, la.to_date, 1 from `tabEmployee` e, `tabLeave Application` la where la.employee_name=e.employee_name 
	 and %(from_date)s <=la.to_date and %(to_date)s>=la.from_date and la.status=%(status)s
	group by la.employee_name
	""",{"from_date":filters.from_date,"to_date":filters.to_date,"status":"Approved"})