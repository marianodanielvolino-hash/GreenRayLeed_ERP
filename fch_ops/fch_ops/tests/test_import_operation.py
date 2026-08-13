import unittest
import frappe
from fch_ops.fch_ops.doctype.fch_import_operation.fch_import_operation import FCHImportOperation


class TestImportOperation(unittest.TestCase):
    def test_landed_cost_calculation(self):
        doc = frappe._dict({
            "goods_value": 10000.0,
            "international_freight": 1500.0,
            "insurance": 200.0,
            "duty": 500.0,
            "customs": 300.0,
            "local_freight": 400.0,
            "other_costs": 100.0,
            "calculate_landed_cost": FCHImportOperation.calculate_landed_cost,
        })
        doc.calculate_landed_cost(doc)
        self.assertEqual(doc.landed_cost, 13000.0)
