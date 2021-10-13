# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime
from datetime import date

def execute(filters=None):
	columns, data = [], []
	columns.append("Unpaid Leave")
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
	
	columns, leave_types = get_columns(filters)
	fdata = get_data(filters)
	for item in fdata:
		row = [item.department_code, item.employee, item.employee_name]
		tla = 0
		cf = 0
		for elem in leave_types:
			if "Annual" in elem:
				lal_details = frappe.get_list('Leave Allocation', filters={'employee':item.employee,'from_date':['>=',filters.from_date],'to_date':['<=',filters.to_date],'leave_type':['like', '%Annual%'] }, fields={'leave_type','total_leaves_allocated','unused_leaves'})
				for element in lal_details:
					cf = cf + element.unused_leaves
					tla = tla + element.total_leaves_allocated

		acm_date = filters.acm_date.split('-')
		a = date(int(acm_date[0]),int(acm_date[1]),int(acm_date[2]))
		today = date.today()
		b = date(int(today.strftime("%Y")),1,1)
		jd = str(item.date_of_joining)
		jd_number = jd.split('-')
		jd_num_date = date(int(jd_number[0]),int(jd_number[1]),int(jd_number[2]))
		
		# check date
		diff_joinining_lastday = (b-jd_num_date).days
		tot_days = 0
		if diff_joinining_lastday > 0:
			tot_days = (a-b).days
		else:
			tot_days = (a-jd_num_date).days

		# acm = tot_days
		# acm = (a-b).days
		acm = (tla / 365)*tot_days + (cf)
		acm = round(acm)
		row.append(acm)
		row.append(cf)

		for e in leave_types:
			ldata = ""
			if "Annual" in e:
				leave_details = frappe.get_list('Leave Allocation', filters={'employee':item.employee,'from_date':['>=',filters.from_date],'to_date':['<=',filters.to_date],'leave_type':['like', '%Annual%'] }, fields={'leave_type','total_leaves_allocated','unused_leaves'})
				ldata = leave_details[0].leave_type
			else:
				leave_details = frappe.db.sql("""select * from `tabLeave Allocation` where from_date >= %(from_date)s and to_date <= %(to_date)s and leave_type=%(ltn)s and employee=%(employee)s""",{"from_date":filters.from_date, "to_date":filters.to_date,"ltn":e,"employee":item.employee},as_dict=1)
				ldata = e
			
			leave_application = frappe.get_list('Leave Application',
			filters={"employee": item.employee,
						"status": "Approved",
						"leave_type": ldata,
						"from_date": ['>=', filters.from_date],
						"to_date": ['<=', filters.to_date]},
			fields={"total_leave_days"}
						)
			
			if len(leave_application)> 0: 
				total = 0
				cf = 0	
				for jitem in leave_details:		
					total = total + jitem.total_leaves_allocated
					cf = cf + jitem.unused_leaves
				taken = 0

				for jelem in leave_application:
					taken = taken + jelem.total_leave_days
				remaining = cf + total - taken

				row.append(total)
				row.append(taken)
				row.append(remaining)
			else:
				if "Annual" in e:
					leave_allocation = frappe.db.count('Leave Allocation', {'employee':item.employee,'from_date':['>=',filters.from_date],'to_date':['<=',filters.to_date],'leave_type':['like', '%Annual%'] })
				else:
					leave_allocation = frappe.db.count('Leave Allocation', {'employee':item.employee,'from_date':['>=',filters.from_date],'to_date':['<=',filters.to_date],'leave_type': e })
				if leave_allocation > 0:
					row.append(leave_details[0].total_leaves_allocated)
					row.append(0)
					row.append((leave_details[0].unused_leaves or 0)+leave_details[0].total_leaves_allocated)
				else:
					row.append(0)
					row.append(0)
					row.append(0)
		
		# count leave without pay
		# check and find all leave without pay as list 
		lwp = frappe.get_list('Leave Type',filters={'is_lwp':1},fields={'leave_type_name'},pluck='leave_type_name')		
		
		# calculate sum of unpaid leaves taken by employee
		ul = frappe.db.sql("""
		select sum(total_leave_days) from `tabLeave Application` where
		employee=%(employee)s and
		leave_type in %(leave_types_unpaid)s and
		status=%(status)s
		""",{"employee":item.employee,"leave_types_unpaid":tuple(lwp),"status":"Approved"},as_dict=True)

		# push total unpaid leave in line
		row.append(ul[0]["sum(total_leave_days)"] or 0)
		
		# push full line
		data.append(row)


	return columns, data


def get_columns(filters):
	columns = [
		 _("Department Code") + "::140",
		 _("Employee") + ":Link/Employee:140",
		 _("Employee Name") + "::140",
		 _("Accumulation") + "::140",
		 _("Ballance from last year") + "::140"
	]
	leave_types = {_("lt_list"): []}
	leave_allocation = frappe.db.sql("""select distinct leave_type from `tabLeave Allocation` where from_date >= %(from_date)s and to_date <= %(to_date)s""",{"from_date":filters.from_date, "to_date":filters.to_date},as_dict=1)
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
		select distinct ta.employee_name, ta.employee, em.department_code, em.date_of_joining from `tabLeave Allocation` ta, `tabEmployee` em where from_date>=%(from_date)s and to_date<=%(to_date)s and ta.employee_name=em.employee_name
		 order by em.department_code asc"""
	,{"from_date":filters.from_date, "to_date":filters.to_date},as_dict=1)
	
	return data

	


