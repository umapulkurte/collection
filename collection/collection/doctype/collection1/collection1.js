//Payment Type
cur_frm.cscript.payment_type = function (doc,cdt,cdn)
{
	
	if (doc.payment_type=="Cash")
	{
		cur_frm.toggle_enable('bank');
		cur_frm.toggle_enable('cheque_no');

		cur_frm.set_value('bank','');
		cur_frm.set_value('bank_name','');
		cur_frm.set_value('account_no','');
	}

	if (doc.payment_type=="Cheque")
	{
		cur_frm.toggle_enable('bank', true);
		cur_frm.toggle_enable('cheque_no', true);
		cur_frm.set_value('cheque_no','');
	}
}

/*cur_frm.cscript.paid_amount=function(doc,cdt,cdn)
{
	var a=parseInt(doc.amount)
	var p=parseInt(doc.paid_amount);
	if(p<a)
	{
		var r=a-p
		cur_frm.set_value('remaining_amount',r)
	}
	else
	{
		cur_frm.set_value('remaining_amount','')
	}
	if(p>a)
	{
		var d=(p-a)
		cur_frm.set_value('deposit',d)
	}
	else
	{
		cur_frm.set_value('deposit','')
	}
}*/
/*cur_frm.cscript.collection_type=function(doc,cdt,cdn)
{
	var o=doc.select_owner
	var c=doc.collection
	var a=doc.amount
	var ctype=doc.collection_type;
	var cname=doc.collection
	var date1=doc.date;
	var d=date1.split("-");
	var day=d[2];
	frappe.call({
		method:'collection.collection.doctype.collection1.collection1.get_interest',
		args:{o:o,c:c,a:a,ctype:ctype,day:day,cname:cname},
		callback:function(r)
		{
			set_field_options('info',r.message)
		}
	})
}*/

cur_frm.cscript.collection_type=function(doc,cdt,cdn)
{
	var date=doc.date
	var o_id=doc.select_owner
	var h=doc.house_no
	var c_type=doc.collection_type
	var c_name=doc.collection
	var amount=doc.amount
	frappe.call({
		method:'collection.collection.doctype.collection1.collection1.show_table',
		args:{o_id:o_id,h:h,c_name:c_name,date:date,amount:amount},
		callback:function(r)
		{
			set_field_options('info',r.message)
		}
	})
}

cur_frm.cscript.paid_amount=function(doc,cdt,cdn)
{
	var n=doc.paid_amount;
	frappe.call({
		method:'collection.collection.doctype.collection1.collection1.get_money_in_words',
		args:{n:n},
		callback:function(r)
		{
			cur_frm.set_value('amount_in_words',r.message)
		}
	})
}