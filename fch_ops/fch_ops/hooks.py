app_name = "fch_ops"
app_title = "FCH Ops"
app_publisher = "GreenRay / FCH"
app_description = "GreenRay Operations and Five-Gate Sales Control Engine"
app_email = "ops@greenrayleed.com"
app_license = "GPL-3.0"

# Lifecycle Hooks
after_install = "fch_ops.setup.after_install"
after_migrate = "fch_ops.setup.after_migrate"

# Document Events
doc_events = {
    "Sales Order": {
        "validate": "fch_ops.events.sales_order.validate",
        "before_submit": "fch_ops.events.sales_order.before_submit",
    },
    "Quotation": {
        "validate": "fch_ops.events.quotation.validate",
        "before_submit": "fch_ops.events.quotation.before_submit",
    },
}

# Roles
has_permission = {
    "FCH Import Operation": "frappe.permissions.has_permission",
    "FCH Collection Action": "frappe.permissions.has_permission",
    "FCH Compliance Requirement": "frappe.permissions.has_permission",
    "FCH Contract Register": "frappe.permissions.has_permission",
}
