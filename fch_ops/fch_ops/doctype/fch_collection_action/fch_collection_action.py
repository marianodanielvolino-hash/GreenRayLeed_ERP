import frappe
from frappe.model.document import Document


class FCHCollectionAction(Document):
    def validate(self):
        if self.sales_invoice:
            fields = ["customer", "company", "currency", "outstanding_amount"]
            if frappe.get_meta("Sales Invoice").has_field("fch_market"):
                fields.append("fch_market")
            invoice = frappe.db.get_value("Sales Invoice", self.sales_invoice, fields, as_dict=True)
            if invoice:
                self.customer = invoice.customer
                self.company = invoice.company
                self.currency = invoice.currency
                self.outstanding_amount = invoice.outstanding_amount
                self.market = invoice.get("fch_market") or self.market
        if self.status not in ("Paid", "Closed") and (not self.next_action or not self.next_action_date):
            frappe.throw("Toda cobranza abierta debe tener próxima acción y fecha.")
