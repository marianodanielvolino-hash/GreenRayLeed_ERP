import unittest
import frappe
from fch_ops.events.sales_order import validate, before_submit


class TestFiveGates(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def test_ensure_five_gates(self):
        doc = frappe._dict({
            "doctype": "Sales Order",
            "name": "TEST-SO-001",
            "items": [],
            "custom_fch_gate_checks": [],
            "meta": frappe._dict({"has_field": lambda f: True}),
            "get_doc_before_save": lambda: None,
            "get": lambda k, d=None: [] if k == "custom_fch_gate_checks" else d,
            "append": lambda field, row: doc.custom_fch_gate_checks.append(frappe._dict(row)),
        })
        validate(doc)
        self.assertEqual(len(doc.custom_fch_gate_checks), 5)
        gates = {r.gate for r in doc.custom_fch_gate_checks}
        self.assertEqual(gates, {"Commercial", "Stock", "Compliance", "Finance", "Logistics"})

    def test_block_on_no_go(self):
        doc = frappe._dict({
            "doctype": "Sales Order",
            "name": "TEST-SO-002",
            "items": [],
            "custom_fch_gate_checks": [
                frappe._dict({"gate": "Commercial", "status": "GO", "is_required": 1}),
                frappe._dict({"gate": "Stock", "status": "NO GO", "is_required": 1}),
                frappe._dict({"gate": "Compliance", "status": "GO", "is_required": 1}),
                frappe._dict({"gate": "Finance", "status": "GO", "is_required": 1}),
                frappe._dict({"gate": "Logistics", "status": "GO", "is_required": 1}),
            ],
            "meta": frappe._dict({"has_field": lambda f: True}),
            "get_doc_before_save": lambda: None,
            "get": lambda k, d=None: doc.custom_fch_gate_checks if k == "custom_fch_gate_checks" else d,
        })
        with self.assertRaises(frappe.ValidationError):
            before_submit(doc)
