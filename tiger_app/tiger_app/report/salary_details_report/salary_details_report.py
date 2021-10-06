# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from datetime import date
import calendar
from frappe import _

from frappe.utils.data import flt

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	tdata = get_emp_list(filters)
	row = []

	for item in tdata:
		item_break = item[5]
		sub_item = item_break[1:-1]
		split_sub_item = sub_item.split(', {')
		for elem in split_sub_item:
			if elem.count('{')==0:
				sse = elem[:-1].split(',')
				sc = sse[1].split(':')[1][1:-1]
				if row.count(sc[:-1]) == 0:
					row.append(sc[:-1])
			else:
				esse = elem[1:-1].split(',')
				sc = esse[1].split(':')[1][1:-1]
				if row.count(sc[:-1]) == 0:
					row.append(sc[:-1])
			
	row.sort()
	for item in tdata:
		item_break = item[5]
		sub_item = item_break[1:-1]
		split_sub_item = sub_item.split(', {')
		col = []
		for el in row:
			col.append({'amount':0,'sc':el})

		for elem in split_sub_item:
			if elem.count('{')==0:
				csse = elem[:-1].split(',')
				amount = csse[0].split(':')[1]
				sc = csse[1].split(':')[1][1:-1]
				index = in_dictlist('sc',sc[:-1], col)
				col[index].update({'amount':amount})
			else:
				esse = elem[1:-1].split(',')
				amount = esse[0].split(':')[1]
				sc = esse[1].split(':')[1][1:-1]
				index = in_dictlist('sc',sc[:-1], col)
				col[index].update({'amount':amount})

		total = 0		
        	
		for idx,value in enumerate(row):
			item.append(flt(col[idx]['amount']))
			total = total + flt(col[idx]['amount'])
		item.append(total)

		item.pop(5)

	row.append("Total")
	columns += row

	
	data = tdata


	return columns, data

def in_dictlist(key, value, my_dictlist):
    for index,entry in enumerate(my_dictlist):
        if entry[key] == value:
            return index
    return {}

def get_columns():
	
	columns = ["Department Code",_("Employee")+":Link/Employee:140","Employee Name","Salary Structure","Date of Joining"]
	
	return columns


@frappe.whitelist()
def get_joining_relieving_condition(start_date,end_date):
	cond = """
		and ifnull(t1.date_of_joining, '0000-00-00') <= '%(end_date)s'
		and ifnull(t1.relieving_date, '2199-12-31') >= '%(start_date)s'
	""" % {"start_date": start_date, "end_date": end_date}
	return cond


@frappe.whitelist()
def get_emp_list(filters):
	"""
		Returns list of active employees based on selected criteria
		and for which salary structure exists
	"""
	today = date.today()
	f = calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")))
	start_date = today.strftime("%Y-%m-")+ str(f[0])
	end_date = today.strftime("%Y-%m-")+ str(f[1])
	cond = get_joining_relieving_condition(start_date,end_date)

	condition = ''
	condition = """and payroll_frequency = '%(payroll_frequency)s'"""% {"payroll_frequency": "Monthly"}
	sal_struct = frappe.db.sql_list("""
			select
				name from `tabSalary Structure`
			where
				docstatus = 1 and
				is_active = 'Yes'
				and company = %(company)s
				and currency = %(currency)s and
				ifnull(salary_slip_based_on_timesheet,0) = %(salary_slip_based_on_timesheet)s
				{condition}""".format(condition=condition),
			{"company": "Human Capital Group", "currency": "BDT", "salary_slip_based_on_timesheet":0})
	if sal_struct:
		cond += "and t2.salary_structure IN %(sal_struct)s "
		cond += "and t2.payroll_payable_account = %(payroll_payable_account)s "
		cond += "and %(from_date)s >= t2.from_date"
		emp_list = frappe.db.sql("""
			select
				distinct t1.department_code, t1.name as employee, t1.employee_name, t2.salary_structure, sd.parent, sd.sales,
				t1.date_of_joining, t1.status
			from
				`tabEmployee` t1, `tabSalary Structure Assignment` t2
			LEFT JOIN 
			( SELECT parent, CONCAT( 
			'[', 
			GROUP_CONCAT( CONCAT( '{ "amount":', amount, ', "salary_component":"', salary_component, '" }' ) SEPARATOR ', '),
			']' ) sales  FROM `tabSalary Detail` GROUP BY parent ) sd ON sd.parent = t2.salary_structure
			where
				t1.name = t2.employee
				and t2.docstatus = 1
				and t1.status = "Active"
		%s order by t1.department_code asc, t2.from_date desc
		""" % cond, {"sal_struct": tuple(sal_struct), "from_date": filters.ending_date, "payroll_payable_account": "Payroll Payable - T"}, as_dict=True)
		rdata = []
		names = ""
		for item in emp_list:
			if item.employee not in names:
				names += item.employee
				rdata.append([item.department_code,item.employee,item.employee_name, item.salary_structure, item.date_of_joining, item.sales])
		return rdata