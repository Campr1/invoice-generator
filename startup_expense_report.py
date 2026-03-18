from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import date


def money(x):
    return f"${x:,.2f}"


def build_pdf(filename="startup_expense_report_Jamrock.pdf"):

    # --- Business Info ---
    business_name = "Keystone World Inc. & Jamrock Caribbean Grocery Market"
    business_address = "2464 Weston Rd, Unit 117, Toronto, ON  M9N 0A2"
    report_title = "Startup Expense Report (Purchases to Date)"
    report_date = date.today().strftime("%B %d, %Y")

    # --- Purchases ---
    purchases = [
        {"item": "Grocery store shelves", "category": "Fixtures & Equipment", "amount": 2000.00},
        {"item": "Survey certificate", "category": "Permits & Professional Fees", "amount": 700.00},
        {"item": "Building permit", "category": "Permits & Professional Fees", "amount": 950.00},
        {"item": "Business bank account checks", "category": "Banking & Admin", "amount": 191.00},
        {"item": "Zoning permit", "category": "Permits & Professional Fees", "amount": 800.00},
        {"item": "Cashier counter", "category": "Fixtures & Equipment", "amount": 1000.00},
        {"item": "Single phase meat cutting saw", "category": "Fixtures & Equipment", "amount": 1600.00},
        {"item": "Produce tables", "category": "Fixtures & Equipment", "amount": 600.00},
        {"item": "Commercial sink", "category": "Fixtures & Equipment", "amount": 450.00},
        {"item": "Fresh fish display tables", "category": "Fixtures & Equipment", "amount": 1800.00},
        {"item": "Grocery shopping baskets", "category": "Supplies", "amount": 200.00},
        {"item": "Open/Closed sign", "category": "Signage & Branding", "amount": 120.00},
        {"item": "3 phase meat cutting saw", "category": "Fixtures & Equipment", "amount": 2000.00},
        {"item": "Digital scale", "category": "Fixtures & Equipment", "amount": 450.00},
    ]

    # --- Totals ---
    grand_total = sum(p["amount"] for p in purchases)

    category_totals = {}
    for p in purchases:
        category_totals[p["category"]] = category_totals.get(p["category"], 0) + p["amount"]

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    elements = []

    # Header
    elements.append(Paragraph(report_title, styles["Title"]))
    elements.append(Paragraph(f"<b>{business_name}</b>", styles["Normal"]))
    elements.append(Paragraph(business_address, styles["Normal"]))
    elements.append(Spacer(1, 0.15 * inch))
    elements.append(Paragraph(f"<b>Report Date:</b> {report_date}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------- Purchases Table ----------
    table_data = [["Item", "Category", "Amount (CAD)"]]

    for p in purchases:
        table_data.append([p["item"], p["category"], money(p["amount"])])

    # Grand Total row (NO HTML TAGS)
    table_data.append(["", "Grand Total", money(grand_total)])

    tbl = Table(table_data, colWidths=[3.3 * inch, 2.3 * inch, 1.4 * inch])

    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E1E8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("FONTSIZE", (0, 1), (-1, -2), 9),

        # Bold Grand Total row
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F2F4F7")),
    ]))

    elements.append(tbl)
    elements.append(Spacer(1, 0.35 * inch))

    # ---------- Category Totals ----------
    elements.append(Paragraph("Category Totals", styles["Heading2"]))

    cat_data = [["Category", "Total (CAD)"]]

    for cat in sorted(category_totals.keys()):
        cat_data.append([cat, money(category_totals[cat])])

    # Grand Total row
    cat_data.append(["Grand Total", money(grand_total)])

    cat_tbl = Table(cat_data, colWidths=[4.8 * inch, 2.2 * inch])

    cat_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E1E8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),

        # Bold Grand Total row
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F2F4F7")),
    ]))

    elements.append(cat_tbl)

    elements.append(Spacer(1, 0.25 * inch))
    elements.append(Paragraph(
        "Prepared for bookkeeping, reimbursement tracking, and startup cost documentation.",
        styles["Normal"]
    ))

    doc.build(elements)
    print(f"Created: {filename}")


if __name__ == "__main__":
    build_pdf()