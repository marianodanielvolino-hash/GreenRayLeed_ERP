import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class FCHCase(Document):
    def validate(self):
        if self.status in ("Resolved", "Closed") and not self.resolved_on:
            self.resolved_on = now_datetime()
        elif self.status not in ("Resolved", "Closed"):
            self.resolved_on = None
