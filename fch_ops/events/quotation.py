import frappe
from frappe import _
from frappe.utils import now_datetime

APPROVER_ROLES = {"FCH CEO", "FCH Sales Manager"}


def _minimum(doc):
    settings = frappe.get_single("FCH Settings")
    minimum = doc.get("custom_minimum_margin_percent")
    if minimum in (None, 0):
        minimum = settings.default_minimum_margin_percent or 0
    return minimum


def validate(doc, method=None):
    margin = doc.get("custom_margin_percent") or 0
    minimum = _minimum(doc)

    if margin < minimum and doc.get("custom_pricing_approval_status") == "Not Required":
        doc.custom_pricing_approval_status = "Pending"

    if doc.get("custom_pricing_approval_status") == "Approved" and doc.has_value_changed("custom_pricing_approval_status"):
        roles = set(frappe.get_roles(frappe.session.user))
        if not roles.intersection(APPROVER_ROLES):
            frappe.throw(_("Sólo Dirección o Sales Manager pueden aprobar excepciones de pricing."))
        doc.custom_pricing_approved_by = frappe.session.user
        doc.custom_pricing_approved_on = now_datetime()

    if doc.get("custom_pricing_approval_status") != "Approved":
        doc.custom_pricing_approved_by = None
        doc.custom_pricing_approved_on = None


def before_submit(doc, method=None):
    minimum = _minimum(doc)
    margin = doc.get("custom_margin_percent") or 0
    if margin < minimum and doc.get("custom_pricing_approval_status") != "Approved":
        frappe.throw(
            _("Margen {0}% por debajo del mínimo {1}%. Requiere aprobación de pricing.").format(margin, minimum)
        )
