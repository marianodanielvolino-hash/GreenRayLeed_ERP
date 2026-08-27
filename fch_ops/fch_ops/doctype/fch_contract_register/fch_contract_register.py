import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, today


class FCHContractRegister(Document):
    def validate(self):
        self.update_derived_status()

    def update_derived_status(self):
        if self.status == "Terminated" or not self.expiration_date:
            return
        exp = getdate(self.expiration_date)
        now = getdate(today())
        if exp < now:
            self.status = "Expired"
            self.next_alert_date = None
            return
        settings = frappe.get_single("FCH Settings")
        try:
            alert_days = sorted({int(x.strip()) for x in (settings.contract_alert_days or "90,60,30").split(",") if x.strip()}, reverse=True)
        except ValueError:
            alert_days = [90, 60, 30]
        days_left = (exp - now).days
        if days_left <= max(alert_days):
            self.status = "Renewal Due"
        elif self.effective_date and getdate(self.effective_date) <= now:
            self.status = "Active"
        future_alerts = [add_days(exp, -d) for d in alert_days if add_days(exp, -d) >= now]
        self.next_alert_date = min(future_alerts) if future_alerts else None
