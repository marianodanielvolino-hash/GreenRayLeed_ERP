import frappe
from frappe import _
from frappe.utils import now_datetime, today

GATES = ["Commercial", "Stock", "Compliance", "Finance", "Logistics"]

GATE_ROLES = {
    "Commercial": {"FCH CEO", "FCH Sales Manager", "FCH Country Manager"},
    "Stock": {"FCH CEO", "FCH Supply", "FCH Warehouse"},
    "Compliance": {"FCH CEO", "FCH COMEX", "FCH Supply"},
    "Finance": {"FCH CEO", "FCH Finance Manager", "FCH Treasury"},
    "Logistics": {"FCH CEO", "FCH COMEX", "FCH Supply"},
}


def _settings():
    return frappe.get_single("FCH Settings")


def _ensure_gates(doc):
    if not doc.meta.has_field("custom_fch_gate_checks"):
        return
    existing = {row.gate for row in (doc.get("custom_fch_gate_checks") or [])}
    for gate in GATES:
        if gate not in existing:
            doc.append(
                "custom_fch_gate_checks",
                {"gate": gate, "status": "Pending", "is_required": 1},
            )


def _stamp_checked_rows(doc):
    for row in doc.get("custom_fch_gate_checks") or []:
        if row.status in ("GO", "NO GO") and not row.checked_on:
            row.checked_on = now_datetime()
            row.checked_by = frappe.session.user



def _validate_gate_authority(doc):
    previous = doc.get_doc_before_save()
    previous_status = {}
    if previous:
        previous_status = {row.gate: row.status for row in (previous.get("custom_fch_gate_checks") or [])}

    user_roles = set(frappe.get_roles(frappe.session.user))
    for row in doc.get("custom_fch_gate_checks") or []:
        old = previous_status.get(row.gate, "Pending")
        if row.status != old and row.status in ("GO", "NO GO"):
            allowed = GATE_ROLES.get(row.gate, {"FCH CEO"})
            if not user_roles.intersection(allowed):
                frappe.throw(
                    _("No tenés rol autorizado para resolver el gate {0}.").format(row.gate)
                )


def _validate_compliance(doc):
    country = doc.get("custom_destination_country")
    if not country:
        return []

    failures = []
    for row in doc.items:
        reqs = frappe.get_all(
            "FCH Compliance Requirement",
            filters={"item": row.item_code, "destination_country": country, "required": 1},
            fields=["name", "requirement", "status", "valid_from", "valid_until"],
        )
        for req in reqs:
            invalid = req.status != "Approved"
            if req.valid_from and str(req.valid_from) > today():
                invalid = True
            if req.valid_until and str(req.valid_until) < today():
                invalid = True
            if invalid:
                failures.append(f"{row.item_code}: {req.requirement} ({req.status})")
    return failures


def _set_gate(doc, gate, status, notes=None):
    for row in doc.get("custom_fch_gate_checks") or []:
        if row.gate == gate:
            row.status = status
            if notes:
                row.notes = notes
            if status in ("GO", "NO GO"):
                row.checked_on = now_datetime()
                row.checked_by = frappe.session.user
            return


def _update_summary(doc):
    rows = doc.get("custom_fch_gate_checks") or []
    if not rows:
        doc.custom_gate_status = "Not Evaluated"
    elif any(row.status == "NO GO" for row in rows):
        doc.custom_gate_status = "NO GO"
    elif all(row.status == "GO" for row in rows if row.is_required) and len([r for r in rows if r.is_required]) >= 5:
        doc.custom_gate_status = "GO"
    else:
        doc.custom_gate_status = "Pending"


def validate(doc, method=None):
    _ensure_gates(doc)
    _validate_gate_authority(doc)
    _stamp_checked_rows(doc)

    compliance_failures = _validate_compliance(doc)
    if compliance_failures:
        _set_gate(doc, "Compliance", "NO GO", " | ".join(compliance_failures[:10]))

    _update_summary(doc)


def before_submit(doc, method=None):
    settings = _settings()
    if not settings.enforce_five_gates:
        return

    _ensure_gates(doc)
    compliance_failures = _validate_compliance(doc)
    if compliance_failures:
        frappe.throw(
            _("Compliance NO GO. Requisitos pendientes/vencidos: {0}").format("; ".join(compliance_failures[:10]))
        )

    statuses = {row.gate: row.status for row in (doc.get("custom_fch_gate_checks") or []) if row.is_required}
    missing = [gate for gate in GATES if statuses.get(gate) != "GO"]
    if missing:
        frappe.throw(
            _("No se puede confirmar el pedido. Gates pendientes o NO GO: {0}").format(", ".join(missing))
        )
