# Copyright (c) 2013, Frappe
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import datediff, nowdate, format_date, add_days
from frappe import sendmail


#def daily():
	#receiver = email_id = frappe.db.get_value("Add Owner", owner_name, "email_id")
	#new_rv=self
	#ath = frappe.get_doc("Add Owner","OW001")
#	receiver = 'umapulkurte@gmail.com'
#	if receiver:
#		subj = 'Owner Details :- '
#		sendmail([receiver], subject=subj, 
#		message = 'Welcome to SatyaPuram Society'+'\n'+'\nYour Login Details Are:\n'+'\nEmail Id:'+ email_id +'\n'+'\nPassword:\n' + n_password +'\n'+'\nPlease Find Attachment of your House Details'+'\n'+'\nThanks & Regards,'+'\n'+'\nSatyaPuram Society',
#		attachments='')
#		frappe.msgprint("Mail Send")
#	else:
#		frappe.msgprint(_("Email ID not found, hence mail not sent"))


def all():
	#receiver = email_id = frappe.db.get_value("Add Owner", owner_name, "email_id")
	#new_rv=self
	#ath = frappe.get_doc("Add Owner","OW001")
	receiver = 'wayzonwitherpnext@gmail.com'
	email_id = 'umapulkurte@gmail.com'
	n_password = '123456'
	if receiver:
		subj = 'Owner Details :- '
		sendmail([receiver], subject=subj, 
		message = 'Welcome to SatyaPuram Society'+'\n'+'\nYour Login Details Are:\n'+'\nEmail Id:'+ email_id +'\n'+'\nPassword:\n' + n_password +'\n'+'\nPlease Find Attachment of your House Details'+'\n'+'\nThanks & Regards,'+'\n'+'\nSatyaPuram Society',
		attachments='')
		#frappe.msgprint("Mail Send")
	else:
		a=0
		#frappe.msgprint(_("Email ID not found, hence mail not sent"))

def hourly():
	#receiver = email_id = frappe.db.get_value("Add Owner", owner_name, "email_id")
	#new_rv=self
	#ath = frappe.get_doc("Add Owner","OW001")
	receiver = 'wayzonwitherpnext@gmail.com'
	email_id = 'umapulkurte@gmail.com'
	n_password = '123456'
	if receiver:
		subj = 'Owner Details :- '
		sendmail([receiver], subject=subj, 
		message = 'Welcome to Satyapuram Society'+'\n'+'\nYour Login Details Are:\n'+'\nEmail Id:'+ email_id +'\n'+'\nPassword:\n' + n_password +'\n'+'\nPlease Find Attachment of your House Details'+'\n'+'\nThanks & Regards,'+'\n'+'\nSatyaPuram Society',
		attachments='')
		#frappe.msgprint("Mail Send")
	else:
		a=0
		#frappe.msgprint(_("Email ID not found, hence mail not sent"))
