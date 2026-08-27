import frappe
from frappe.model.document import Document


class FCHImportOperation(Document):
    def validate(self):
        self.calculate_landed_cost()

    def calculate_landed_cost(self):
        self.landed_cost = (
            (self.goods_value or 0)
            + (self.international_freight or 0)
            + (self.insurance or 0)
            + (self.duty or 0)
            + (self.customs or 0)
            + (self.local_freight or 0)
            + (self.other_costs or 0)
        )
