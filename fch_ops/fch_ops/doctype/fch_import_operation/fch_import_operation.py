import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class FCHImportOperation(Document):
    def validate(self):
        self._validate_company_consistency()
        self.calculate_landed_cost()

    def calculate_landed_cost(self):
        charges = self.get("custom_charges") or []
        if charges:
            self.landed_cost = sum(
                flt(row.amount_company_currency)
                or (flt(row.amount) * flt(row.exchange_rate or 1))
                for row in charges
            )
            return

        self.landed_cost = (
            flt(self.goods_value)
            + flt(self.international_freight)
            + flt(self.insurance)
            + flt(self.duty)
            + flt(self.customs)
            + flt(self.local_freight)
            + flt(self.other_costs)
        )

    def _validate_company_consistency(self):
        for row in self.get("custom_receipts") or []:
            if not row.purchase_receipt:
                continue
            company = frappe.db.get_value("Purchase Receipt", row.purchase_receipt, "company")
            if company and self.company and company != self.company:
                frappe.throw(
                    _("Purchase Receipt {0} belongs to company {1}, not {2}.").format(
                        frappe.bold(row.purchase_receipt), frappe.bold(company), frappe.bold(self.company)
                    )
                )

    @frappe.whitelist()
    def load_purchase_receipts(self):
        if not self.purchase_order:
            frappe.throw(_("Select a Purchase Order first."))

        receipt_names = frappe.get_all(
            "Purchase Receipt Item",
            filters={"purchase_order": self.purchase_order},
            pluck="parent",
        )
        receipt_names = list(dict.fromkeys(receipt_names))

        self.set("custom_receipts", [])
        for name in receipt_names:
            data = frappe.db.get_value(
                "Purchase Receipt",
                name,
                ["docstatus", "company", "posting_date", "supplier", "base_grand_total"],
                as_dict=True,
            )
            if not data or data.docstatus != 1:
                continue
            if self.company and data.company != self.company:
                continue
            self.append(
                "custom_receipts",
                {
                    "purchase_receipt": name,
                    "posting_date": data.posting_date,
                    "supplier": data.supplier,
                    "grand_total": data.base_grand_total,
                },
            )

        if not self.get("custom_receipts"):
            frappe.throw(_("No submitted Purchase Receipts were found for Purchase Order {0}.").format(self.purchase_order))

        self.save(ignore_permissions=True)
        return [row.purchase_receipt for row in self.get("custom_receipts")]

    @frappe.whitelist()
    def create_landed_cost_voucher(self):
        if self.landed_cost_voucher and frappe.db.exists("Landed Cost Voucher", self.landed_cost_voucher):
            return self.landed_cost_voucher

        if not self.company:
            frappe.throw(_("Company is required."))

        if not self.get("custom_receipts"):
            self.load_purchase_receipts()

        charges = self.get("custom_charges") or []
        if not charges:
            frappe.throw(_("Add at least one Landed Cost Charge with an Expense Account."))

        company_currency = frappe.get_cached_value("Company", self.company, "default_currency")
        lcv = frappe.new_doc("Landed Cost Voucher")
        lcv.company = self.company
        lcv.posting_date = self.actual_arrival or nowdate()
        lcv.distribute_charges_based_on = self.custom_lcv_distribution_basis or "Amount"

        for row in self.get("custom_receipts"):
            data = frappe.db.get_value(
                "Purchase Receipt",
                row.purchase_receipt,
                ["docstatus", "company", "posting_date", "supplier", "base_grand_total"],
                as_dict=True,
            )
            if not data or data.docstatus != 1:
                frappe.throw(_("Purchase Receipt {0} must be submitted.").format(row.purchase_receipt))
            if data.company != self.company:
                frappe.throw(_("Purchase Receipt {0} belongs to another company.").format(row.purchase_receipt))

            lcv.append(
                "purchase_receipts",
                {
                    "receipt_document_type": "Purchase Receipt",
                    "receipt_document": row.purchase_receipt,
                    "supplier": data.supplier,
                    "posting_date": data.posting_date,
                    "grand_total": data.base_grand_total,
                },
            )

        for row in charges:
            if not row.expense_account:
                frappe.throw(_("Every Landed Cost Charge requires an Expense Account."))

            account_company, account_currency = frappe.get_cached_value(
                "Account", row.expense_account, ["company", "account_currency"]
            )
            if account_company != self.company:
                frappe.throw(
                    _("Expense Account {0} belongs to {1}, not {2}.").format(
                        row.expense_account, account_company, self.company
                    )
                )

            charge_currency = row.currency or company_currency
            exchange_rate = flt(row.exchange_rate or 1)
            company_amount = flt(row.amount_company_currency) or (flt(row.amount) * exchange_rate)

            if account_currency == company_currency:
                amount = company_amount
                tax_exchange_rate = 1
            elif account_currency == charge_currency:
                amount = flt(row.amount)
                tax_exchange_rate = exchange_rate
            else:
                frappe.throw(
                    _("Charge currency {0} is incompatible with account currency {1} for {2}.").format(
                        charge_currency, account_currency, row.expense_account
                    )
                )

            lcv.append(
                "taxes",
                {
                    "expense_account": row.expense_account,
                    "description": row.description or row.charge_type,
                    "amount": amount,
                    "exchange_rate": tax_exchange_rate,
                },
            )

        lcv.get_items_from_purchase_receipts()
        lcv.insert()
        self.db_set("landed_cost_voucher", lcv.name)
        return lcv.name
