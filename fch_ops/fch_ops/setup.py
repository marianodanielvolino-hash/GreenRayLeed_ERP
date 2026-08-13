import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

CUSTOM_FIELDS = {
    "Item": [
        {"fieldname": "custom_led_family", "fieldtype": "Data", "label": "LED Family", "insert_after": "item_name"},
        {"fieldname": "custom_led_model", "fieldtype": "Data", "label": "LED Model", "insert_after": "custom_led_family"},
        {"fieldname": "custom_power_w", "fieldtype": "Float", "label": "Power (W)", "insert_after": "custom_led_model"},
        {"fieldname": "custom_lumens", "fieldtype": "Float", "label": "Lumens (lm)", "insert_after": "custom_power_w"},
        {"fieldname": "custom_cct_kelvin", "fieldtype": "Data", "label": "CCT / Kelvin", "insert_after": "custom_lumens"},
        {"fieldname": "custom_cri", "fieldtype": "Data", "label": "CRI", "insert_after": "custom_cct_kelvin"},
        {"fieldname": "custom_ip_rating", "fieldtype": "Data", "label": "IP Rating", "insert_after": "custom_cri"},
        {"fieldname": "custom_voltage", "fieldtype": "Data", "label": "Voltage", "insert_after": "custom_ip_rating"},
        {"fieldname": "custom_optics", "fieldtype": "Data", "label": "Optics / Beam Angle", "insert_after": "custom_voltage"},
        {"fieldname": "custom_driver_brand", "fieldtype": "Data", "label": "Driver Brand/Model", "insert_after": "custom_optics"},
        {"fieldname": "custom_dimensions_mm", "fieldtype": "Data", "label": "Dimensions (mm)", "insert_after": "custom_driver_brand"},
        {"fieldname": "custom_weight_kg", "fieldtype": "Float", "label": "Weight (kg)", "insert_after": "custom_dimensions_mm"},
        {"fieldname": "custom_cbm", "fieldtype": "Float", "label": "Volume / CBM", "insert_after": "custom_weight_kg"},
        {"fieldname": "custom_warranty_years", "fieldtype": "Int", "label": "Warranty (Years)", "insert_after": "custom_cbm"},
        {"fieldname": "custom_preferred_supplier", "fieldtype": "Link", "options": "Supplier", "label": "Preferred Supplier", "insert_after": "custom_warranty_years"},
        {"fieldname": "custom_lead_time_days", "fieldtype": "Int", "label": "Lead Time (Days)", "insert_after": "custom_preferred_supplier"},
    ],
    "Warehouse": [
        {"fieldname": "custom_fch_market", "fieldtype": "Link", "options": "FCH Market", "label": "FCH Market Context", "insert_after": "company"},
    ],
    "Quotation": [
        {"fieldname": "custom_margin_percent", "fieldtype": "Percent", "label": "Margin %", "insert_after": "grand_total"},
        {"fieldname": "custom_minimum_margin_percent", "fieldtype": "Percent", "label": "Minimum Margin %", "insert_after": "custom_margin_percent"},
        {"fieldname": "custom_pricing_approval_status", "fieldtype": "Select", "options": "Not Required\nPending\nApproved\nRejected", "default": "Not Required", "label": "Pricing Approval Status", "insert_after": "custom_minimum_margin_percent"},
        {"fieldname": "custom_pricing_approved_by", "fieldtype": "Link", "options": "User", "label": "Pricing Approved By", "read_only": 1, "insert_after": "custom_pricing_approval_status"},
        {"fieldname": "custom_pricing_approved_on", "fieldtype": "Datetime", "label": "Pricing Approved On", "read_only": 1, "insert_after": "custom_pricing_approved_by"},
    ],
    "Sales Order": [
        {"fieldname": "fch_market", "fieldtype": "Link", "options": "FCH Market", "label": "FCH Market", "insert_after": "company"},
        {"fieldname": "custom_destination_country", "fieldtype": "Link", "options": "Country", "label": "Destination Country", "insert_after": "fch_market"},
        {"fieldname": "custom_gate_status", "fieldtype": "Select", "options": "Not Evaluated\nPending\nGO\nNO GO", "default": "Not Evaluated", "label": "Five Gate Status", "read_only": 1, "in_list_view": 1, "insert_after": "custom_destination_country"},
        {"fieldname": "custom_fch_gate_checks", "fieldtype": "Table", "options": "FCH Gate Check", "label": "Five Gate Checks", "insert_after": "custom_gate_status"},
    ],
    "Project": [
        {"fieldname": "fch_market", "fieldtype": "Link", "options": "FCH Market", "label": "FCH Market", "insert_after": "company"},
    ],
    "Purchase Order": [
        {"fieldname": "fch_market", "fieldtype": "Link", "options": "FCH Market", "label": "FCH Market", "insert_after": "company"},
        {"fieldname": "custom_lead_time_days", "fieldtype": "Int", "label": "Lead Time (Days)", "insert_after": "fch_market"},
    ],
}


def after_install():
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
    seed_reference_data()


def after_migrate():
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
    seed_reference_data()


def seed_reference_data():
    # Seed FCH Markets if empty
    markets = ["Argentina", "Chile", "Puerto Rico", "Costa Rica", "Mexico", "Uruguay", "USA / Offshore"]
    for m in markets:
        if not frappe.db.exists("FCH Market", m):
            doc = frappe.new_doc("FCH Market")
            doc.market_name = m
            doc.name = m
            doc.insert(ignore_permissions=True)

    # Ensure FCH Settings single doc exists
    if not frappe.db.exists("FCH Settings", "FCH Settings"):
        settings = frappe.new_doc("FCH Settings")
        settings.enforce_five_gates = 1
        settings.default_minimum_margin_percent = 25.0
        settings.insert(ignore_permissions=True)
