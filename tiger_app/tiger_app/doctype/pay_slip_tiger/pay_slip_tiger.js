// Copyright (c) 2021, amran and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pay Slip Tiger', {
	refresh: function(frm) {
		frm.add_custom_button(__("Button"), function() {
			let mon = ["January","February","March","April","May","June","July","August","September","Octeber","November","December"]
			let d = new Date();
  			let n = `${mon[d.getMonth()]} - ${d.getFullYear()}`;
			// console.log(frm.doc);
			let employee_data = {
				name: "",
				employee_name: "",
				department: "",
				salary_mode: "Cheque",
				bank_name: ""
			}
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					'doctype': 'Employee',
					'filters': {'name': frm.doc.employee},
					'fieldname': [
						'name',
						'employee_name',
						'department',
						'salary_mode',
						'bank_name'
					]
				},
				callback: function(r) {
					if (!r.exc) {
						// code snippet
						// console.log("thisis r = ",r.message.name)
						if(r.message){
							employee_data.name = r.message.name;
							employee_data.employee_name = r.message.employee_name;
							employee_data.department = r.message.department;
							employee_data.salary_mode = r.message.salary_mode;
							employee_data.bank_name = r.message.bank_name;

							frappe.call({
								method: 'frappe.client.get_value',
								args: {
									'doctype': 'Shadow Slip',
									'filters': {'employee_name': employee_data.employee_name,'ps_date': n,},
									'fieldname': [
										'name'
										// 'employee_name',
										// 'ps_date'
									]
								},
								callback: function(re) {
									if (!re.exc) {
										// code snippet
										// console.log("thisis r = ",r.message.name)
										if(re.message){
											// console.log(re.message);
											frappe.set_route(`app/print/Shadow Slip/${re.message.name}`)
											// frappe.throw("Already Added!")
										}else{
											frappe.db.insert({
												"doctype": "Shadow Slip",
												"ps_date": n,
												"employee": employee_data.name,
												"code": employee_data.name,
												"employee_name": employee_data.employee_name,
												"payment_days": frm.doc.payment_days ? frm.doc.payment_days : 0.0,
												"salary": frm.doc.salary ? frm.doc.salary : 0.0,
												"eligible": frm.doc.eligible ? frm.doc.eligible : 0.0,
												"earnings": frm.doc.earnings ? frm.doc.earnings : 0.0,
												"deductions": frm.doc.deductions ? frm.doc.deductions : 0.0,
												"payables": frm.doc.payables ? frm.doc.payables : 0.0,
												"earning_note": frm.doc.earning_note ? frm.doc.earning_note : "",
												"deduction_note": frm.doc.deduction_note ? frm.doc.deduction_note : "",
												"leave_note": frm.doc.leave_note ? frm.doc.leave_note : "",
												"basic": frm.doc.basic ? frm.doc.basic : 0.0,
												"qid": frm.doc.qid ? frm.doc.qid : 0.0,
												"bank_name": employee_data.bank_name,
												"iban": frm.doc.iban ? frm.doc.iban : 0.0,
												"payroll_status": frm.doc.payroll_status ? frm.doc.payroll_status : "",
												"department": employee_data.department,
												"payment_mode": employee_data.salary_mode,
												"net_pay": Number(frm.doc.eligible) + Number(frm.doc.earnings) - Number(frm.doc.deductions ? frm.doc.deductions : 0.0),
												"docstatus":1
											}).then(function(doc) {
												// console.log(doc);
												// doc.save('Submit')
												frappe.set_route(`app/print/Shadow Slip/${doc.name}`)
											});
										}
										
									}
								}
							});
						}
						
					}
				}
			});		
		});
	}
});
