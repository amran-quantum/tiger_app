# Copyright (c) 2013, amran and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = ["Fruit Name","Point"], []
	data = get_all()
	return columns, data

def get_all():
	return frappe.db.sql(""" 
		SELECT
		 fruit_name, point
		FROM
		`tabChutney`
		""")

