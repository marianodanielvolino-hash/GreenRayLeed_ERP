from frappe.model.document import Document
from frappe.utils import flt


class FCHImportCharge(Document):
    def validate(self):
        self.amount_company_currency = flt(self.amount) * flt(self.exchange_rate or 1)
