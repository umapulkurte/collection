# -*- coding: utf-8 -*-
# Copyright (c) 2015, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date, timedelta, datetime
import calendar
from calendar import monthrange
from dateutil import relativedelta as rdelta
from frappe import sendmail


class Collection1(Document):
	def on_submit(self):
		#*********** INITIALIZATION ********************
		dte=self.date
		c_id=self.name
		o_id=self.select_owner
		o_name=self.owner_name
		h=self.house_no
		c=self.collection
		a=b=amt=self.amount
		cash=p_amt=self.paid_amount
		pay_type=self.payment_type
		chq_no=self.cheque_no
		bk_id=self.bank
		acc_no=self.account_no
		g_cash_id=''
		g_cheque_id=''
		#rm_amt=self.remaining_amount
		collect_date=self.collection_month_year
		#------------------------------------
		dte=str(dte)
		var1=dte.split('-')
		cur_yr=int(var1[0])
		cur_mnth=int(var1[1])
		cur_dte=int(var1[2])
		collect_date=str(collect_date)
		var=collect_date.split('-')	
		collect_yr=int(var[0])
		collect_mnth=int(var[1])
		collect_dte=int(var[2])
		#--------------------------------------
		d0=date(int(var1[0]),int(var1[1]),int(var1[2]))
		d1=date(int(var[0]),int(var[1]),int(var[2]))
		rd = rdelta.relativedelta(d0,d1)
		if(rd.days>10):
			rd.months=rd.months+1
		#x=monthdelta(d0,d1)
		#frappe.msgprint(rd.months)
		#frappe.throw(rd.days)
		#frappe.throw(x)
		#***************************************************************************
		#------------------------------For CASH--------------------------------------
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
			s1=frappe.db.sql("""
				insert into `tabCash` 
				set name=%s, cash_id=%s, transaction=1, owner_id=%s, date=%s, amount=%s""",(n2,c0,o_id,dte,cash))
			g_cash_id=frappe.db.sql("""
				select cash_id from `tabCash` 
				where date=%s and amount=%s and owner_id=%s""",(dte,cash,o_id))[0][0]
		#------------------------------For CHEQUE---------------------------------------
		if(pay_type=='Cheque'):
			#---------Inserting entry in ChequeDeatil-------------
			s0=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Detail`""")[0][0]
			if s0:
				n1=int(s0)+1;
			else:
				n1=1;
			s1=frappe.db.sql("""select max(cheque_id) from `tabCheque Detail`""")[0][0]
			if s1:
				c11=int(s1)+1;
			else:
				c11=1;
			s3=frappe.db.sql("""
				insert into `tabCheque Detail` 
				set name=%s, date=%s, owner_id=%s, cheque_id=%s, cheque_no=%s, bank_id=%s, balance=%s, account_no=%s, cheque_status='Unclear', transaction=1""",(n1,dte,o_id,c11,chq_no,bk_id,cash,acc_no))
			g_cheque_id=frappe.db.sql("""
				select cheque_id from `tabCheque Detail` 
				where name=%s and date=%s and owner_id=%s and cheque_id=%s and cheque_no=%s and bank_id=%s and balance=%s and account_no=%s and cheque_status='Unclear' and transaction=1""",(n1,dte,o_id,c11,chq_no,bk_id,cash,acc_no))
		#**********************************************************************************
		if(rd.months<=0):
			q0=frappe.db.sql('''select remaining_amount,month,collection_id,collection,paid_amount from `tabCollection Info` where remaining_amount >%s and owner_id=%s and collection=%s order by remaining_amount DESC limit 1''',(0,o_id,c))
			if q0:
				s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
				if s2:
					n2=int(s2)+1
				else:
					n2=1
				if(self.paid_amount>=int(q0[0][0])):
					q1=frappe.db.sql("""insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s,owner_name=%s,collection=%s, amount=%s,
					paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,int(q0[0][0]),int(q0[0][0]),self.paid_amount-self.amount,collect_date))
					self.paid_amount=self.paid_amount-int(q0[0][0])
					collect_date=str(collect_date)
					var=collect_date.split('-')	
					collect_date=date(int(var[0]),int(var[1]),int(var[2]))
					days_in_month = calendar.monthrange(collect_date.year, collect_date.month)[1]
					collect_date=collect_date+timedelta(days=days_in_month)
			#---------------------------------------------
			#---------------------------------------------
			s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
			if s2:
				n2=int(s2)+1
			else:
				n2=1
			if(self.paid_amount<=self.amount):
				s1=frappe.db.sql("""
					insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
					paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,amt,p_amt,self.amount-self.paid_amount,collect_date))
			else:
				div=(self.paid_amount)/(self.amount)
				mod=(self.paid_amount)%(self.amount)
				if(mod>0):
					div=div+1
				else:
					div=div
				for i in range (div):
					if(i==0):
						s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
						if s2:
							n2=int(s2)+1
						else:
							n2=1
						s1=frappe.db.sql("""
						insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
						paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,amt,self.amount,self.remaining_amount,collect_date))
						self.paid_amount=self.paid_amount-self.amount
						if(self.paid_amount==0):
							break
					else:
						collect_date=str(collect_date)
						var=collect_date.split('-')	
						collect_date=date(int(var[0]),int(var[1]),int(var[2]))
						days_in_month = calendar.monthrange(collect_date.year, collect_date.month)[1]
						collect_date=collect_date+timedelta(days=days_in_month)
						if(self.paid_amount>self.amount):
							s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
							if s2:
								n2=int(s2)+1
							else:
								n2=1
							s1=frappe.db.sql("""
								insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
								paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,amt,self.amount,self.remaining_amount,collect_date))
							self.paid_amount=self.paid_amount-self.amount
							if(self.paid_amount==0):
								break
						else:
							s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
							if s2:
								n2=int(s2)+1
							else:
								n2=1
							s1=frappe.db.sql("""
								insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
								paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,amt,self.paid_amount,self.amount-self.paid_amount,collect_date))
							self.paid_amount=self.paid_amount-self.amount
							if(self.paid_amount==0):
								break
					#-----------------------------------
					#----------------------------------------
		else:
			if(c=='Temple Fund'):
				q0=frappe.db.sql('''select remaining_amount,month,collection_id,collection,paid_amount from `tabCollection Info` where remaining_amount >%s and owner_id=%s and collection=%s order by remaining_amount DESC limit 1''',(0,o_id,c))
				if q0:
					s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
					if s2:
						n2=int(s2)+1
					else:
						n2=1
					if(self.paid_amount>=int(q0[0][0])):
						t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
						a=int(q0[0][0])
						interest1=0
						for j in range(rd.months):
							interest=(float(a)*t)
							a=float(a)+float(interest)
							interest1=float(interest1)+float(interest)
						q1=frappe.db.sql("""insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
						paid_amount=%s,remaining_amount=%s,month=%s,interest=%s""",(n2,dte,c_id,o_id,h,o_name,c,int(q0[0][0]),a,0,collect_date,interest1))
						self.paid_amount=self.paid_amount-a
						collect_date=str(collect_date)
						var=collect_date.split('-')	
						collect_date=date(int(var[0]),int(var[1]),int(var[2]))
						days_in_month = calendar.monthrange(collect_date.year, collect_date.month)[1]
						collect_date=collect_date+timedelta(days=days_in_month)
						rd.months=rd.months-1
						a=int(q0[0][0])
				else:
					a=0
				#-----------------gfjjfgj
			else:
				q0=frappe.db.sql('''select remaining_amount,month,collection_id,collection,paid_amount from `tabCollection Info` where remaining_amount >%s and owner_id=%s and collection=%s order by remaining_amount DESC limit 1''',(0,o_id,c))
				if q0:
					s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
					if s2:
						n2=int(s2)+1
					else:
						n2=1
					if(self.paid_amount>=int(q0[0][0])):
						t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
						a=int(q0[0][0])
						interest1=0
						for j in range(rd.months):
							interest=(float(a)*t)
							a=float(a)+float(interest)
							interest1=float(interest1)+float(interest)
						q1=frappe.db.sql("""insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
						paid_amount=%s,remaining_amount=%s,month=%s,interest=%s""",(n2,dte,c_id,o_id,h,o_name,c,int(q0[0][0]),a,0,collect_date,interest1))
						self.paid_amount=self.paid_amount-a
						collect_date=str(collect_date)
						var=collect_date.split('-')	
						collect_date=date(int(var[0]),int(var[1]),int(var[2]))
						days_in_month = calendar.monthrange(collect_date.year, collect_date.month)[1]
						collect_date=collect_date+timedelta(days=days_in_month)
						rd.months=rd.months-1
						a=int(q0[0][0])
				else:
					a=self.amount
				s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
				if s2:
					n2=int(s2)+1
				else:
					n2=1
				t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
				#a=int(q0[0][0])
				interest1=0
				for j in range(rd.months):
					interest=(float(a)*t)
					a=float(a)+float(interest)
					interest1=float(interest1)+float(interest)
				if(self.paid_amount<=a):
					s1=frappe.db.sql("""
						insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
						paid_amount=%s,remaining_amount=%s,month=%s,interest=%s""",(n2,dte,c_id,o_id,h,o_name,c,amt,a,a-self.paid_amount,collect_date,interest1))		
					self.paid_amount=self.paid_amount-a
					rd.months=rd.months-1
				else:
					div=int(self.paid_amount)/int(self.amount)
					mod=int(self.paid_amount)%int(self.amount)
					if(mod>0):
						div=int(div+1)
					else:
						div=int(div)
					for i in range (div):
						if(rd.months > 0):
							if(i==0):
								t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
								a=float(self.amount)
								interest1=0
								for j in range(rd.months):
									interest=(float(a)*t)
									a=float(a)+float(interest)
									interest1=float(interest1)+float(interest)
								s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
								if s2:
									n2=int(s2)+1
								else:
									n2=1
								s1=frappe.db.sql("""
								insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
								paid_amount=%s,remaining_amount=%s,month=%s,interest=%s""",(n2,dte,c_id,o_id,h,o_name,c,self.amount,a,0,collect_date,interest1))
								self.paid_amount=self.paid_amount-a
								rd.months=rd.months-1
								if(self.paid_amount==0):
									break
							else:
								collect_date=str(collect_date)
								var=collect_date.split('-')	
								collect_date=date(int(var[0]),int(var[1]),int(var[2]))
								days_in_month = calendar.monthrange(collect_date.year, collect_date.month)[1]
								collect_date=collect_date+timedelta(days=days_in_month)
								t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
								a=float(self.amount)
								interest1=0
								for j in range(rd.months):
									interest=(float(a)*t)
									a=float(a)+float(interest)
									interest1=float(interest1)+float(interest)
								if(self.paid_amount>a):
									s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
									if s2:
										n2=int(s2)+1
									else:
										n2=1
									s1=frappe.db.sql("""
										insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
										paid_amount=%s,remaining_amount=%s,month=%s,interest=%s""",(n2,dte,c_id,o_id,h,o_name,c,self.amount,a,0,collect_date,interest1))
									rd.months=rd.months-1
									self.paid_amount=self.paid_amount-a
									if(self.paid_amount==0):
										break
								else:
									t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
									a=float(self.amount)
									interest1=0
									for j in range(rd.months):
										interest=(float(a)*t)
										a=float(a)+float(interest)
										interest1=float(interest1)+float(interest)
									s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
									if s2:
										n2=int(s2)+1
									else:
										n2=1
									s1=frappe.db.sql("""
										insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
										paid_amount=%s,remaining_amount=%s,month=%s,interest=%s""",(n2,dte,c_id,o_id,h,o_name,c,self.amount,self.paid_amount,self.paid_amount-a,collect_date,interest1))
									rd.months=rd.months-1
									self.paid_amount=self.paid_amount-a
									if(self.paid_amount==0):
										break
						else:
							collect_date=str(collect_date)
							var=collect_date.split('-')	
							collect_date=date(int(var[0]),int(var[1]),int(var[2]))
							days_in_month = calendar.monthrange(collect_date.year, collect_date.month)[1]
							collect_date=collect_date+timedelta(days=days_in_month)
							if(self.paid_amount>self.amount):
								s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
								if s2:
									n2=int(s2)+1
								else:
									n2=1
								s1=frappe.db.sql("""
								insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
								paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,amt,self.amount,self.remaining_amount,collect_date))
								self.paid_amount=self.paid_amount-self.amount
								if(self.paid_amount==0):
									break
							else:
								s2=frappe.db.sql("""select max(cast(name as int)) from `tabCollection Info`""")[0][0]
								if s2:
									n2=int(s2)+1
								else:
									n2=int(1)
								s1=frappe.db.sql("""
								insert into `tabCollection Info` set name=%s, date=%s, collection_id=%s, owner_id=%s, house_no=%s, owner_name=%s,collection=%s, amount=%s,
								paid_amount=%s,remaining_amount=%s,month=%s""",(n2,dte,c_id,o_id,h,o_name,c,int(amt),int(self.paid_amount),int(self.amount)-int(self.paid_amount),collect_date))
								self.paid_amount=int(self.paid_amount)-int(self.amount)
								if(self.paid_amount==0):
									break

		#=================================================================================
		def mail_send(email_id,n_password):
			
			receiver = self.email_id
			new_rv=self
			#ath = frappe.get_doc("Add Owner","OW001")
			#receiver = 'umapulkurte@gmail.com'
			if receiver:
				subj = 'Payment Details :- '
				sendmail([receiver], subject=subj, 
				message = 'Hello Sir/Madam,'+'\n'+'\nYour Payment Details Are Attached\n'+'\n'+'\nThanks & Regards,'+'\n'+'\nSahara Prestige Co-Op Housing Society',
				attachments=[frappe.attach_print(new_rv.doctype, new_rv.name, file_name=new_rv.name, print_format='')])
				frappe.msgprint("Mail Send")
			else:
				frappe.msgprint(_("Email ID not found, hence mail not sent"))
		email = self.email_id
		if(self.email_id):
			mail_send(email,'fkljghlsdfghsl')
		else:
			frappe.msgprint("Payment Details Not sent")
		#====================================================================================

@frappe.whitelist()
def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta
@frappe.whitelist()
def show_table(o_id,h,c_name,date,amount):
	#---Table Heading------------------------
	head="""<table border=3>
			<tr bgcolor=LightBlue align=center>
			<td width=80><b>Date</td><td width=80><b>Amount</td><td width=130><b>Paid Amt</td><td width=160><b>Remaining Amt</td><td width=80><b>Interest</td><td width=90><b>Month</td></tr>"""
	#-----------------------------------------
	h_str1=""
	h_str2=""
	h_str3=""
	a=p=r=itr=0;
	#----------------------------------------
	q=frappe.db.sql("""select owner_name,house_no,date,collection,amount,paid_amount,remaining_amount,interest,month,month(month) from `tabCollection Info` where owner_id=%s and collection=%s order by month asc""",(o_id,c_name))
	fgh=0
	if q:
		l=len(q)
		for i in range(0, l):
			h_str0="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(q[i][2],q[i][4],q[i][5],q[i][6],q[i][7],q[i][8])
			h_str1+=h_str0
			b=q[i][6]
			c=q[i][7]
			if(b>0):
				b=b
			else:
				b=0
			if(c>0):
				c=c
			else:
				c=0
			p=float(p)+float(q[i][5])
			itr=float(itr)+float(c)
		ta=float(q[l-1][4])*float(q[l-1][9])
		r=float(b)
		total1="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %('Total',ta,p,r,itr,'')
		#return (head+h_str1+total+"""</table>""")
		fd=datetime.today().month
		if(int(q[l-1][9])>=int(fd)):
			return (head+h_str1+total1+"""</table>""")
		else:
			q1=frappe.db.sql("""select owner_name,house_no,date,collection,amount,paid_amount,remaining_amount,interest,month,month(month) from `tabCollection Info` where owner_id=%s and collection=%s order by month desc limit 1""",(o_id,c_name))
			if q1:
				tr=titr=0;
				z=str(q[l-1][8])
				dte=date
				var1=dte.split("-")
				var=str(z).split("-")
				d0=datetime(int(var1[0]),int(var1[1]),int(var1[2]))
				d1=datetime(int(var[0]),int(var[1]),int(var[2]))
				rd = rdelta.relativedelta(d0,d1)
				rd.months=rd.months+1
				if(rd.months>0):
					from datetime import date
					import calendar
					from calendar import monthrange
					z1=str(q1[0][8])
					for i in range(rd.months):
						if(i==0 and q1[0][6]>0):
							a=float(q1[0][6])
							pmt1=float(amount)-float(q1[0][6])
							rmt1=pmt1
							z1=str(z1)
							var=z1.split('-')
							z1=date(int(var[0]),int(var[1]),int(var[2]))
							days_in_month = calendar.monthrange(z1.year, z1.month)[1]
							z1=z1-timedelta(days=days_in_month)
						else:
							a=float(amount)
							pmt1=0
							rmt1=a
						t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
						interest1=0
						if(rd.months==1 and rd.days<10):
							a=float(a)
							z1=str(z1)
							var=z1.split('-')
							z1=date(int(var[0]),int(var[1]),int(var[2]))
							days_in_month = calendar.monthrange(z1.year, z1.month)[1]
							z1=z1+timedelta(days=days_in_month)
							h_str0="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %('',amount,pmt1,a,0,z1)				
							h_str2=h_str2+h_str0
						else:
							if(c_name=='Temple Fund'):
								x=frappe.db.sql("""select amount from `tabCollection Type` where collection_type=%s""",(c_name))[0][0]
								t=float(frappe.db.sql("""select interest_rate_per_month from `tabSociety`""")[0][0])
								n=rd.months
								a=float(q1[0][6])
								for j in range(n):
									interest=(float(a)*t)
									a=float(a)+float(interest)
									interest1=float(interest1)+float(interest)
								h_str0="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %('',0,0,a,interest1,dte)
								h_str3=h_str3+h_str0
								if(str(q1[0][8])==str(z1)):
									ta=float(ta)
								else:
									ta=float(ta)+float(amount)
								tr=float(tr)+float(a)
								titr=float(titr)+float(interest1)
								total="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %('Total',x,p,tr,titr,'')
								tbl=head+h_str1+h_str3+h_str2+total+"""</table>"""
								return(tbl)
								#frappe.msgprint(head+h_str1+h_str0+"""</table>""")
							else:
								z1=str(z1)
								var=z1.split('-')	
								z1=date(int(var[0]),int(var[1]),int(var[2]))
								days_in_month = calendar.monthrange(z1.year, z1.month)[1]
								z1=z1+timedelta(days=days_in_month)
								n=rd.months
								for j in range(n):
									interest=(float(a)*t)
									a=float(a)+float(interest)
									interest1=float(interest1)+float(interest)
									g=str(q[l-1][8])
									n=n-1
								h_str0="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %('',amount,pmt1,a,interest1,z1)				
								h_str3=h_str3+h_str0
								rd.months=rd.months-1
						if(str(q1[0][8])==str(z1)):
							ta=float(ta)
						else:
							ta=float(ta)+float(amount)
						tr=float(tr)+float(a)
						titr=float(titr)+float(interest1)
						total="""<tr align=center><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %('Total',ta,p,tr,titr,'')
					tbl=head+h_str1+h_str3+h_str2+total+"""</table>"""
					return(tbl)
	else:	
		frappe.msgprint("No previous records to display for selected collection type")
		return (head)

@frappe.whitelist()
def get_money_in_words(n):
	from frappe.utils import money_in_words
	from frappe.utils import in_words
	x=money_in_words(n)
	return (x)