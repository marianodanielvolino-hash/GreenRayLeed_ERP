import frappe
from frappe.model.document import Document


class FCHCountrySKUMapping(Document):
    def validate(self):
        duplicate = frappe.db.exists(
            "FCH Country SKU Mapping",
            {"item": self.item, "country": self.country, "name": ["!=", self.name]},
        )
        if duplicate:
            frappe.throw("Ya existe un mapping para este SKU global y país.")
