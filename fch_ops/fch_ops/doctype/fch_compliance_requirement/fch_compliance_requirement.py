import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, today


class FCHComplianceRequirement(Document):
    def validate(self):
        duplicate = frappe.db.exists(
            "FCH Compliance Requirement",
            {
                "item": self.item,
                "destination_country": self.destination_country,
                "requirement": self.requirement,
                "name": ["!=", self.name],
            },
        )
        if duplicate:
            frappe.throw("Ya existe este requisito para el mismo SKU y país.")
        if self.valid_until and getdate(self.valid_until) < getdate(today()) and self.status == "Approved":
            self.status = "Expired"
        if self.status == "Approved" and not self.approved_on:
            self.approved_on = now_datetime()
            self.approved_by = self.approved_by or frappe.session.user
