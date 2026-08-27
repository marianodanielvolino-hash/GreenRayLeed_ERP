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
    "FCH Import Operation": [
        {"fieldname": "custom_receipts", "fieldtype": "Table", "options": "FCH Import Receipt", "label": "Submitted Purchase Receipts", "insert_after": "purchase_order"},
        {"fieldname": "custom_charges", "fieldtype": "Table", "options": "FCH Import Charge", "label": "Landed Cost Charges", "insert_after": "custom_receipts"},
        {"fieldname": "custom_lcv_distribution_basis", "fieldtype": "Select", "options": "Qty\nAmount", "default": "Amount", "label": "LCV Distribution Basis", "insert_after": "custom_charges"},
    ],
}

GRL_ROLES = [
    "FCH Direction", "FCH PMO", "FCH Finance Manager", "FCH Treasury",
    "FCH Sales", "FCH Purchasing", "FCH Supply", "FCH Warehouse",
    "FCH COMEX", "FCH Country Manager", "FCH Auditor",
]

MARKETS = ["Argentina", "Chile", "Puerto Rico", "Costa Rica", "Mexico", "Uruguay", "USA / Offshore"]


def after_install():
    configure_grl()


def after_migrate():
    configure_grl()


def configure_grl():
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
    seed_roles()
    seed_reference_data()
    ensure_market_accounting_dimension()
    seed_demo_data()


def seed_roles():
    for role_name in GRL_ROLES:
        if not frappe.db.exists("Role", role_name):
            role = frappe.new_doc("Role")
            role.role_name = role_name
            role.desk_access = 1
            role.insert(ignore_permissions=True)


def seed_reference_data():
    for market in MARKETS:
        if not frappe.db.exists("FCH Market", market):
            doc = frappe.new_doc("FCH Market")
            doc.market_name = market
            doc.name = market
            doc.insert(ignore_permissions=True)

    if not frappe.db.exists("FCH Settings", "FCH Settings"):
        settings = frappe.new_doc("FCH Settings")
        settings.enforce_five_gates = 1
        settings.default_minimum_margin_percent = 25.0
        settings.insert(ignore_permissions=True)


def ensure_market_accounting_dimension():
    if not frappe.db.exists("DocType", "Accounting Dimension"):
        return
    if frappe.db.exists("Accounting Dimension", {"document_type": "FCH Market"}):
        return
    dimension = frappe.new_doc("Accounting Dimension")
    dimension.document_type = "FCH Market"
    dimension.label = "Market"
    dimension.insert(ignore_permissions=True)


def seed_demo_data():
    """Seeds sample/demo master data for GRL Argentina and GRL LLC."""
    # 1. Companies
    companies = [
        {"company_name": "GRL Argentina S.A.", "default_currency": "ARS", "country": "Argentina", "tax_id": "30-71999999-8"},
        {"company_name": "GRL LLC", "default_currency": "USD", "country": "United States", "tax_id": "99-8887776"},
    ]
    for c in companies:
        if not frappe.db.exists("Company", c["company_name"]):
            try:
                doc = frappe.new_doc("Company")
                doc.company_name = c["company_name"]
                doc.default_currency = c["default_currency"]
                doc.country = c["country"]
                doc.tax_id = c["tax_id"]
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Error creating demo company {c['company_name']}: {e}")

    # 2. Warehouses
    warehouses = [
        {"warehouse_name": "Depósito Central Buenos Aires", "company": "GRL Argentina S.A.", "custom_fch_market": "Argentina"},
        {"warehouse_name": "Miami Main Logistics Hub", "company": "GRL LLC", "custom_fch_market": "USA / Offshore"},
    ]
    for w in warehouses:
        abbr = frappe.get_value("Company", w["company"], "abbr") or "GRL"
        name = f"{w['warehouse_name']} - {abbr}"
        if not frappe.db.exists("Warehouse", name):
            try:
                doc = frappe.new_doc("Warehouse")
                doc.warehouse_name = w["warehouse_name"]
                doc.company = w["company"]
                doc.custom_fch_market = w["custom_fch_market"]
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Error creating demo warehouse {w['warehouse_name']}: {e}")

    # 3. Item Group & Items
    if not frappe.db.exists("Item Group", "LED Luminaires"):
        try:
            ig = frappe.new_doc("Item Group")
            ig.item_group_name = "LED Luminaires"
            ig.parent_item_group = "All Item Groups"
            ig.insert(ignore_permissions=True)
        except Exception:
            pass

    items = [
        {
            "item_code": "GRL-LED-HIGHBAY-200W",
            "item_name": "Campana LED Industrial 200W HighBay",
            "item_group": "LED Luminaires",
            "stock_uom": "Nos",
            "custom_led_family": "HighBay",
            "custom_led_model": "HB-200W-PRO",
            "custom_power_w": 200.0,
            "custom_lumens": 32000.0,
            "custom_cct_kelvin": "5000K",
            "custom_cri": ">80",
            "custom_ip_rating": "IP65",
            "custom_voltage": "100-277V",
            "custom_warranty_years": 5,
            "custom_lead_time_days": 30,
        },
        {
            "item_code": "GRL-LED-STREET-150W",
            "item_name": "Luminaria Vial LED 150W StreetLight",
            "item_group": "LED Luminaires",
            "stock_uom": "Nos",
            "custom_led_family": "StreetLight",
            "custom_led_model": "SL-150W-ECO",
            "custom_power_w": 150.0,
            "custom_lumens": 22500.0,
            "custom_cct_kelvin": "4000K",
            "custom_cri": ">70",
            "custom_ip_rating": "IP66",
            "custom_voltage": "100-277V",
            "custom_warranty_years": 5,
            "custom_lead_time_days": 45,
        },
    ]

    for it in items:
        if not frappe.db.exists("Item", it["item_code"]):
            try:
                doc = frappe.new_doc("Item")
                doc.update(it)
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Error creating demo item {it['item_code']}: {e}")

    # 4. Customers & Suppliers
    customers = [
        {"customer_name": "Distribuidora Iluminación S.A.", "customer_group": "All Customer Groups", "territory": "Argentina"},
        {"customer_name": "Caribbean Energy Solutions Inc.", "customer_group": "All Customer Groups", "territory": "United States"},
    ]
    for cust in customers:
        if not frappe.db.exists("Customer", cust["customer_name"]):
            try:
                doc = frappe.new_doc("Customer")
                doc.update(cust)
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Error creating demo customer {cust['customer_name']}: {e}")

    suppliers = [
        {"supplier_name": "Shenzhen GreenRay Tech Co. Ltd.", "supplier_group": "All Supplier Groups", "country": "China"},
    ]
    for sup in suppliers:
        if not frappe.db.exists("Supplier", sup["supplier_name"]):
            try:
                doc = frappe.new_doc("Supplier")
                doc.update(sup)
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Error creating demo supplier {sup['supplier_name']}: {e}")

    # 5. Price List & Item Prices
    price_lists = [
        {"price_list_name": "Standard Selling GRL", "selling": 1, "currency": "USD"},
        {"price_list_name": "Standard Buying GRL", "buying": 1, "currency": "USD"},
    ]
    for pl in price_lists:
        if not frappe.db.exists("Price List", pl["price_list_name"]):
            try:
                doc = frappe.new_doc("Price List")
                doc.update(pl)
                doc.insert(ignore_permissions=True)
            except Exception:
                pass

    item_prices = [
        {"item_code": "GRL-LED-HIGHBAY-200W", "price_list": "Standard Selling GRL", "price_list_rate": 185.0, "currency": "USD"},
        {"item_code": "GRL-LED-HIGHBAY-200W", "price_list": "Standard Buying GRL", "price_list_rate": 95.0, "currency": "USD"},
        {"item_code": "GRL-LED-STREET-150W", "price_list": "Standard Selling GRL", "price_list_rate": 145.0, "currency": "USD"},
        {"item_code": "GRL-LED-STREET-150W", "price_list": "Standard Buying GRL", "price_list_rate": 72.0, "currency": "USD"},
    ]
    for ip in item_prices:
        if not frappe.db.exists("Item Price", {"item_code": ip["item_code"], "price_list": ip["price_list"]}):
            try:
                doc = frappe.new_doc("Item Price")
                doc.update(ip)
                doc.insert(ignore_permissions=True)
            except Exception:
                pass

    # 6. Compliance Requirement Sample
    if not frappe.db.exists("FCH Compliance Requirement", {"destination_country": "Argentina", "item": "GRL-LED-HIGHBAY-200W"}):
        try:
            req = frappe.new_doc("FCH Compliance Requirement")
            req.destination_country = "Argentina"
            req.item = "GRL-LED-HIGHBAY-200W"
            req.requirement_type = "Certification"
            req.title = "Certificado Seguridad Eléctrica (IRAM / TUV)"
            req.status = "Approved"
            req.mandatory = 1
            req.insert(ignore_permissions=True)
        except Exception:
            pass

