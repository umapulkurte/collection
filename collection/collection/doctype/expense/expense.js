cur_frm.cscript.payment_type = function(doc,cdt,cdn)
{
	if (doc.payment_type == "Cash")
	{
		cur_frm.toggle_enable('bank',false);
		cur_frm.toggle_enable('cheque_no');
		cur_frm.toggle_enable('account_no');

		cur_frm.set_value('bank','');
		cur_frm.set_value('bank_name','');
		cur_frm.set_value('account_no','');
		cur_frm.set_value('cheque_no','');
	}
	else
	{
		cur_frm.toggle_enable('bank', true);
		cur_frm.toggle_enable('cheque_no', true);
		cur_frm.set_value('cheque_no','');
		cur_frm.toggle_enable('account_no',true);
	}
}
