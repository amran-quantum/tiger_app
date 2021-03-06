# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []

	columns = get_columns()
	data = get_data(filters)
	return columns, data
def get_columns():
	return ["Department Code",_("Employee")+":Link/Employee:140","Employee Name","Leave Type","Absent From","Absent To","Total Leave Days"]

def get_data(filters):
	return frappe.db.sql("""
	select e.department_code,e.employee, la.employee_name, la.leave_type,  la.from_date, la.to_date, la.total_leave_days from `tabEmployee` e, `tabLeave Application` la where la.employee_name=e.employee_name 
	 and %(from_date)s <=la.to_date and %(to_date)s>=la.from_date and la.status=%(status)s
	group by la.employee_name
	order by e.department_code asc
	""",{"from_date":filters.from_date,"to_date":filters.to_date,"status":"Approved"})
