# Custom Sale Order PDF Report – Odoo 19

This document describes the configuration of a fully customized QWeb PDF report for the `sale.order` model.

---

## 📦 Module Assumption

Module technical name:

```
reporting
```

---

# 🧾 Paper Format

Defines the page layout for the PDF.

```xml
<record id="report_paperformat_a4" model="report.paperformat">
    <field name="name">A4</field>
    <field name="format">A4</field>
    <field name="orientation">Portrait</field>
    <field name="margin_top">20</field>
    <field name="margin_bottom">20</field>
    <field name="margin_left">15</field>
    <field name="margin_right">15</field>
    <field name="header_line">False</field>
</record>
```

### 🔎 Key Fields

| Field | Purpose |
|-------|---------|
format | Page size |
orientation | Portrait / Landscape |
margin_* | PDF margins |
header_line | Show/hide header separator |

---

# ⚙️ Report Action

Binds the report to the model and makes it available in the **Print** menu.

```xml
<record id="action_report_saleorder" model="ir.actions.report">
    <field name="name">Sale Order Report</field>
    <field name="model">sale.order</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">reporting.report_saleorder</field>
    <field name="paperformat_id" ref="reporting.report_paperformat_a4"/>
    <field name="binding_model_id" ref="sale.model_sale_order"/>
    <field name="binding_type">report</field>
</record>
```

### 🔎 Key Fields

| Field | Description |
|--------|------------|
model | Source model |
report_type | Output type |
report_name | QWeb template external ID |
binding_model_id | Adds to Print menu |

---

# 🧩 QWeb Report Template

```xml
<template id="report_saleorder">

    <t t-call="web.html_container">

        <t t-foreach="docs" t-as="o">

            <t t-call="web.external_layout">

                <div class="page">

                    <h2 style="text-align:center;">
                        Sale Order Report
                    </h2>

                    <strong>Order:</strong>
                    <span t-field="o.name"/>

                    <br/>

                    <strong>Customer:</strong>
                    <span t-field="o.partner_id.name"/>

                    <br/>

                    <strong>Date:</strong>
                    <span t-field="o.date_order"/>

                    <br/><br/>

                    <table class="table table-sm table-bordered">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Quantity</th>
                                <th>Unit Price</th>
                                <th>Subtotal</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr t-foreach="o.order_line" t-as="line">
                                <td><span t-field="line.product_id"/></td>
                                <td><span t-field="line.product_uom_qty"/></td>
                                <td><span t-field="line.price_unit"/></td>
                                <td><span t-field="line.price_subtotal"/></td>
                            </tr>
                        </tbody>
                    </table>

                    <div style="text-align:right; margin-top:20px;">
                        <strong>Total :</strong>
                        <span t-field="o.amount_total"/>
                    </div>

                    <div class="text-center" style="margin-top:30px;">
                        Page <span class="page"/> of <span class="topage"/>
                    </div>

                </div>

            </t>

        </t>

    </t>

</template>
```

---

# 🧠 Rendering Flow

```
Print Button
   → ir.actions.report
      → Fetch sale.order record(s)
         → QWeb template
            → HTML
               → wkhtmltopdf
                  → PDF
```

---

# ✅ Required in `__manifest__.py`

```python
'data': [
    'report/sale_order_report.xml',
],
```

---

# ▶️ How to Use

1. Upgrade module:

```
./odoo-bin -u reporting -d your_database
```

2. Go to:

```
Sales → Sale Order → Print → Sale Order Report
```

---

# 🧪 Common Errors & Fixes

### ❌ `IndexError: //main`

Cause:

Missing:

```xml
<t t-call="web.html_container">
```

---

### ❌ Report not visible in Print menu

Check:

```
binding_model_id
binding_type = report
```

---

### ❌ External ID mismatch

Must match:

```
report_name = reporting.report_saleorder
template id = report_saleorder
```

---

# 🎯 Features Included

✔ Custom paper format  
✔ Print menu integration  
✔ Header & footer  
✔ Page numbering  
✔ Order line table  
✔ Total amount  

---

# 🚀 Possible Enhancements

- Company branding
- Landscape format
- Wizard-based filters
- Barcode / QR
- Multi-language support
- Excel export version

---

# 📌 Developer Notes

Always:

- Prepare heavy logic in Python
- Keep QWeb for rendering only
- Upgrade module after changes
