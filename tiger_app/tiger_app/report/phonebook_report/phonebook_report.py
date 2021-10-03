# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = [_("Fullname") + "::140",_("Code") + ":Data:70"]
	data = get_data()
	return columns, data

def get_data():
	udata = frappe.db.sql("""
	select fullname, code from `tabPhonebook`
	""",as_dict=True)

	data = []
	for el in udata:
		data.append([el.fullname, int(el.code)])

	return data