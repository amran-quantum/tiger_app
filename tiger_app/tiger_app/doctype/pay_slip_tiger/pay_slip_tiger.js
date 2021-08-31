// Copyright (c) 2021, amran and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pay Slip Tiger', {
	refresh: function(frm) {
		frm.add_custom_button(__("Button"), function() {
			let mon = ["January","February","March","April","May","June","July","August","September","Octeber","November","December"]
			let d = new Date();
  			let n = `${mon[d.getMonth()]} - ${d.getFullYear()}`;
			// console.log(frm.doc);
			// console.log(frm.doc);
			frappe.db.insert({
				"doctype": "Shadow Slip",
				"ps_date": n,
				"employee": frm.doc.employee ? frm.doc.employee : "",
				"code": frm.doc.code ? frm.doc.code : "",
				"employee_name": frm.doc.employee_name ? frm.doc.employee_name : "",
				"payment_days": frm.doc.payment_days ? frm.doc.payment_days : 0,
				"salary": frm.doc.salary ? frm.doc.salary : 0,
				"eligible": frm.doc.eligible ? frm.doc.eligible : 0,
				"earnings": frm.doc.earnings ? frm.doc.earnings : 0,
				"deductions": frm.doc.deductions ? frm.doc.deductions : 0,
				"payables": frm.doc.payables ? frm.doc.payables : 0,
				"earning_note": frm.doc.earning_note ? frm.doc.earning_note : "",
				"deduction_note": frm.doc.deduction_note ? frm.doc.deduction_note : "",
				"leave_note": frm.doc.leave_note ? frm.doc.leave_note : "",
				"basic": frm.doc.basic ? frm.doc.basic : 0,
				"qid": frm.doc.qid ? frm.doc.qid : 0,
				"bank_name": frm.doc.bank_name ? frm.doc.bank_name : "",
				"iban": frm.doc.iban ? frm.doc.iban : 0,
				"payroll_status": frm.doc.payroll_status ? frm.doc.payroll_status : "",
				"department": frm.doc.department ? frm.doc.department : "",
				"net_pay": Number(frm.doc.salary) + Number(frm.doc.earnings) - Number(frm.doc.deductions),
				"docstatus":1
			}).then(function(doc) {
				// console.log(doc);
				// doc.save('Submit')
				frappe.set_route(`app/print/Shadow Slip/${doc.name}`)
			});
		});
	}
});
