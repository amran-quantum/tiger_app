# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = ["Fruit Name"], []
	data = get_all(filters)
	return columns, data

def get_all(filters):
	return frappe.db.sql(""" 
		SELECT
 fruit_name
FROM
 `tabChutney`
 WHERE fruit_name=%(fruit_name)s
""",values=filters, as_dict=0)

