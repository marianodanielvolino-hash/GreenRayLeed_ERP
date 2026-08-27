frappe.ui.form.on('FCH Import Operation', {
  refresh(frm) {
    if (frm.is_new()) return;

    if (frm.doc.purchase_order) {
      frm.add_custom_button(__('Load Purchase Receipts'), async () => {
        await frm.call('load_purchase_receipts');
        await frm.reload_doc();
        frappe.show_alert({ message: __('Purchase Receipts loaded'), indicator: 'green' });
      }, __('COMEX'));
    }

    if (!frm.doc.landed_cost_voucher && (frm.doc.custom_receipts || []).length) {
      frm.add_custom_button(__('Create Landed Cost Voucher'), async () => {
        const result = await frm.call('create_landed_cost_voucher');
        if (result.message) {
          await frm.reload_doc();
          frappe.set_route('Form', 'Landed Cost Voucher', result.message);
        }
      }, __('COMEX'));
    }

    if (frm.doc.landed_cost_voucher) {
      frm.add_custom_button(__('Open Landed Cost Voucher'), () => {
        frappe.set_route('Form', 'Landed Cost Voucher', frm.doc.landed_cost_voucher);
      }, __('COMEX'));
    }
  }
});
