# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Expense(Document):
	def on_submit(self):
		d=self.date
		person=self.person_name
		pay_type=self.payment_type
		bank_id=self.bank
		bank_name=self.bank_name
		acc_no=self.account_no
		cheque_no=self.cheque_no
		amt=self.amount
		desc=self.description
		g_cash_id=''
		g_cheque_id=''
		#---------------------
		# For CASH
		#---------------------
		if(pay_type=='Cash'):
			#---------Inserting entry in Cash-------------
			s2=frappe.db.sql("""select max(cast(name as int)) from `tabCash`""")[0][0]
			if s2:
				n2=int(s2)+1;
			else:
				n2=1;
			s3=frappe.db.sql("""select max(cash_id) from `tabCash`""")[0][0]
			if s3:
				c0=int(s3)+1;
			else:
				c0=1;
			s1=frappe.db.sql("""insert into `tabCash` 
				set name=%s, cash_id=%s, transaction=2, date=%s, amount=%s ,description=%s""",(n2,c0,d,amt,desc))
			g_cash_id=frappe.db.sql("""select cash_id from `tabCash` where date=%s and amount=%s and description=%s""",(d,amt,desc))[0][0]
		#----------------------
		# For CHEQUE
		#----------------------
		if(pay_type=='Cheque'):
			#---------Inserting entry in ChequeDeatil-------------
			s0=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Detail`""")[0][0]
			if s0:
				n1=int(s0)+1;
			else:
				n1=1;
			s1=frappe.db.sql("""select max(cheque_id) from `tabCheque Detail`""")[0][0]
			if s1:
				c=int(s1)+1;
			else:
				c=1;
			s3=frappe.db.sql("""insert into `tabCheque Detail` set name=%s, date=%s, cheque_id=%s, cheque_no=%s, bank_id=%s, balance=%s, account_no=%s, cheque_status='Unclear', transaction=2""",(n1,d,c,cheque_no,bank_id,amt,acc_no))
			g_cheque_id=frappe.db.sql("""select cheque_id from `tabCheque Detail` 
			where name=%s and date=%s and cheque_id=%s and cheque_no=%s and bank_id=%s and balance=%s and account_no=%s and cheque_status='Unclear' and transaction=2""",(n1,d,c,cheque_no,bank_id,amt,acc_no))[0][0]
		#----------------------------------
		# Updating `TabExpense` table
		#----------------------------------
		s2=frappe.db.sql("""update `tabExpense` 
		set cash_id=%s, cheque_id=%s 
		where date=%s and person_name=%s and payment_type=%s and amount=%s""",(g_cash_id,g_cheque_id,d,person,pay_type,amt))