# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime
from datetime import date

def execute(filters=None):
	columns, data = [], []

	columns, leave_types = get_columns()
	if filters.year:
		filters.update({
			'from_date': filters.year+"-01-01",
			'to_date': filters.year+"-12-31"
		})
	else:
		filters.update({
			'from_date':datetime.now().date().replace(month=1, day=1),    
			'to_date': datetime.now().date().replace(month=12, day=31)
		})
	# fy = frappe.get_list('Fiscal Year',fields={'year_start_date','year_end_date'})
	# filters.update({
	# 	'from_date': fy[0].year_start_date,
	# 	'to_date': fy[0].year_end_date
	# })
	# frappe.msgprint(str(filters))
	# filters = {
	# 	'from_date': str(fy[0].year_start_date),
	# 	'to_date': str(fy[0].year_end_date)
	# }
	fdata = get_data(filters)
	for item in fdata:
		row = [item.department_code,item.employee_name]

		for e in leave_types:
			ldata = ""
			if "Annual" in e:
				leave_details = frappe.get_list('Leave Allocation', filters={'employee_name':item.employee_name,'leave_type':['like', '%Annual%'] }, fields={'leave_type','total_leaves_allocated'})
				ldata = leave_details[0].leave_type
			else:
				leave_details = frappe.db.sql("""select * from `tabLeave Allocation` where leave_type=%(ltn)s and employee_name=%(emp_name)s""",{"ltn":e,"emp_name":item.employee_name},as_dict=1)
				ldata = e
			
			leave_application = frappe.get_list('Leave Application',
			filters={"employee_name": item.employee_name,
						"status": "Approved",
						"leave_type": ldata,
						"from_date": ['>=', filters.from_date],
						"to_date": ['<=', filters.to_date]},
			fields={"total_leave_days"}
						)
			# acm_date = filters.acm_date.split('-')
			# a = date(int(acm_date[0]),int(acm_date[1]),int(acm_date[2]))
			# today = date.today()
			# b = date(int(today.strftime("%Y")),1,1)
			# acm = (a-b).days
			# acm = (leave_details[0].total_leaves_allocated / 365)*acm + (leave_details[0].carry_forwarded_leaves_count or 0)
			# acm = round(acm)
			# row.append(acm)
			if len(leave_application)> 0: 			
				total = leave_details[0].total_leaves_allocated
				cf = leave_details[0].carry_forwarded_leaves_count
				taken = 0

				for elem in leave_application:
					taken += elem.total_leave_days
				remaining = (cf or 0)+ total - taken

				# row.append(cf or 0)
				row.append(total)
				row.append(taken)
				row.append(remaining)
			else:


				if "Annual" in e:
					leave_allocation = frappe.db.count('Leave Allocation', {'employee_name':item.employee_name,'leave_type':['like', '%Annual%'] })
				else:
					leave_allocation = frappe.db.count('Leave Allocation', {'employee_name':item.employee_name,'leave_type': e })
				if leave_allocation > 0:
					# row.append(leave_details[0].carry_forwarded_leaves_count or 0)
					row.append(leave_details[0].total_leaves_allocated)
					row.append(0)
					row.append((leave_details[0].carry_forwarded_leaves_count or 0)+leave_details[0].total_leaves_allocated)
				else:
					# row.append(0)
					row.append(0)
					row.append(0)
					row.append(0)
				
					
		data.append(row)
	return columns, data


def get_columns():
	columns = [
		 _("Department Code") + "::140",
		 _("Employee Name") + "::140",
		#  _("Accumulation") + "::140",
		#  _("Annual Leave Carry Forward") + "::140"
	]
	leave_types = {_("lt_list"): []}
	leave_allocation = frappe.db.sql("""select distinct leave_type from `tabLeave Allocation`""",as_dict=1)
	for component in frappe.db.sql("""select leave_type_name from `tabLeave Type` where leave_type_name in (%s)"""%
		(', '.join(['%s']*len(leave_allocation))), tuple([d.leave_type for d in leave_allocation]),as_dict=1):
		if 'Annual' in component.leave_type_name:
			if leave_types[_("lt_list")].count("Annual Leave") == 0:
				leave_types[_("lt_list")].append("Annual Leave")
		else:
			leave_types[_("lt_list")].append(component.leave_type_name)

	columns = columns + [(e +" "+ f + "::120") for e in leave_types[_("lt_list")] for f in ["Allocation","Taken","Balance"] ]

	return columns, leave_types[_("lt_list")]


def get_data(filters):
	data = frappe.db.sql(
		"""
		select distinct ta.employee_name, em.department_code from `tabLeave Allocation` ta, `tabEmployee` em where from_date>=%(from_date)s and to_date<=%(to_date)s and ta.employee_name=em.employee_name
		"""
	,{"from_date":filters.from_date, "to_date":filters.to_date},as_dict=1)
	
	return data

	


