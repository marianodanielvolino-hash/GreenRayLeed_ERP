import frappe


@frappe.whitelist()
def get_control_tower(company=None, market=None):
    filters = {}
    if company:
        filters["company"] = company
    if market and frappe.get_meta("Sales Order").has_field("fch_market"):
        filters["fch_market"] = market

    sales = frappe.get_all(
        "Sales Order",
        filters={**filters, "docstatus": 1},
        fields=["grand_total", "currency", "custom_gate_status"],
    )
    blocked = sum(1 for row in sales if row.custom_gate_status == "NO GO")

    return {
        "sales_orders": len(sales),
        "blocked_orders": blocked,
        "open_cases": frappe.db.count("FCH Case", {"status": ["not in", ["Resolved", "Closed"]]}),
        "open_imports": frappe.db.count("FCH Import Operation", {"status": ["not in", ["Received", "Closed", "Cancelled"]]}),
        "open_collections": frappe.db.count("FCH Collection Action", {"status": ["not in", ["Paid", "Closed"]]}),
        "active_contracts": frappe.db.count("FCH Contract Register", {"status": ["in", ["Active", "Renewal Due"]]}),
    }
