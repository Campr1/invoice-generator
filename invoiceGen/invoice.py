from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas


# ---------- text helpers ----------
def wrap_to_width(text, font_name, font_size, max_width):
    """Wrap text into lines that fit within max_width (in points)."""
    words = text.replace("\n", " \n ").split()
    lines = []
    current_line = ""

    for word in words:
        if word == "\n":
            lines.append(current_line.rstrip())
            current_line = ""
            continue

        test_line = (current_line + " " + word).strip()
        if pdfmetrics.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=9, leading=11):
    """Draw wrapped text starting at (x, y) and return the updated y position."""
    c.setFont(font, size)
    wrapped_lines = wrap_to_width(text, font, size, width)

    for line in wrapped_lines:
        c.drawString(x, y, line)
        y -= leading

    return y


def money(amount):
    """Format a numeric amount as CAD currency."""
    return f"${amount:,.2f}"


# ---------- invoice data ----------
CONTRACTOR_NAME = "ACME RENOVATIONS INC."
CONTRACTOR_PHONE = "Tel: 555-123-4567"

BILL_TO = [
    "Sample Client Corporation",
    "123 Business Street, Suite 400",
    "Toronto, ON  M1A 1A1",
]

INVOICE_REF = "ACME-2026-001"
INVOICE_DATE = date.today().strftime("%B %d, %Y")

RE_LINE = "Renovation Services – Bathroom & Meat/Fish Station Scope"

SUBTOTAL = 15600.00
HST_RATE = 0.13

PAYMENT_TERMS = [
    "50% deposit upon start of project",
    "25% at halfway completion",
    "25% upon final completion and customer inspection",
]

SCOPE = {
    "Bathroom #1": [
        "Demolish existing bathroom walls and flooring.",
        "Complete new plumbing rough-ins and relocate toilet as discussed.",
        "Install new vanity.",
        "Complete new electrical rough-ins and install new industrial exhaust fan.",
        "Install new lighting fixtures.",
        "Install two (2) new electrical outlets.",
        "Remove existing door and trims; supply and install new door and trims.",
        "Remove existing floor tiles and install new floor tiles.",
        "Install wall tiles up to 4 feet high around bathroom walls.",
        "Install new toilet.",
        "Paint bathroom in customer’s selected colour.",
        "Enlarge doorway to make it handicap and wheelchair accessible.",
    ],
    "Meat & Fish Station": [
        "Excavate floor and install brand new plumbing system with proper drainage.",
        "Install all required sinks and stainless steel countertops.",
        "Run new dedicated electrical outlets for industrial fridge and meat saw.",
        "Electrical permit required.",
        "Properly slope and tile fish station floor.",
        "Build raised platform to create additional upper space for meat and fish ordering.",
    ],
    "Additional Work": [
        "Build new cashier counter area.",
        "Paint main areas upon completion.",
    ],
}


# ---------- PDF generation ----------
def build_pdf(filename="invoice_ACME_RENO_INC.pdf"):
    c = canvas.Canvas(filename, pagesize=LETTER)
    page_width, page_height = LETTER

    # Page margins
    left_margin = 54
    right_margin = page_width - 54
    top_margin = page_height - 54

    # Top-right background title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColorRGB(0.85, 0.88, 0.90)
    c.drawRightString(right_margin, top_margin + 10, "INVOICE")
    c.setFillColor(colors.black)

    # Contractor details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, top_margin, CONTRACTOR_NAME)
    c.setFont("Helvetica", 10)
    c.drawString(left_margin, top_margin - 14, CONTRACTOR_PHONE)

    # Invoice metadata
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(right_margin, top_margin - 2, f"Project Ref Invoice   {INVOICE_REF}")
    c.drawRightString(right_margin, top_margin - 16, f"DATE:   {INVOICE_DATE}")

    # Bill to section
    current_y = top_margin - 50
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin, current_y, "Bill to:")
    current_y -= 14

    c.setFont("Helvetica", 10)
    for bill_to_line in BILL_TO:
        c.drawString(left_margin, current_y, bill_to_line)
        current_y -= 12

    # Subject line
    current_y -= 10
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, current_y, f"Re: {RE_LINE}")
    current_y -= 10

    # Table layout
    table_top = current_y
    table_left = left_margin
    table_right = right_margin
    table_width = table_right - table_left

    expenses_column_width = 130
    description_column_width = table_width - expenses_column_width
    description_x = table_left
    expenses_x = table_left + description_column_width

    # Header row
    header_height = 18
    c.setFillColorRGB(0.85, 0.88, 0.90)
    c.rect(table_left, table_top - header_height, table_width, header_height, fill=1, stroke=1)
    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(description_x + 6, table_top - 13, "Description")
    c.drawString(expenses_x + 6, table_top - 13, "Expenses")

    # Description body
    body_top = table_top - header_height
    current_y = body_top - 10

    current_y = draw_wrapped(
        c,
        "1. Renovation Services:",
        description_x + 6,
        current_y,
        description_column_width - 12,
        font="Helvetica-Bold",
        size=9,
        leading=11,
    )
    current_y -= 2

    for section_name, section_items in SCOPE.items():
        current_y = draw_wrapped(
            c,
            f"{section_name}:",
            description_x + 12,
            current_y,
            description_column_width - 18,
            font="Helvetica-Bold",
            size=9,
            leading=11,
        )

        for item in section_items:
            current_y = draw_wrapped(
                c,
                f"• {item}",
                description_x + 18,
                current_y,
                description_column_width - 24,
                font="Helvetica",
                size=9,
                leading=11,
            )

        current_y -= 4

    # Totals section
    hst_amount = round(SUBTOTAL * HST_RATE, 2)
    total_amount = round(SUBTOTAL + hst_amount, 2)

    current_y -= 6
    totals_top_y = current_y

    reserved_totals_height = 78
    body_bottom = totals_top_y - reserved_totals_height
    if body_bottom < 140:
        body_bottom = 140

    c.line(table_left, totals_top_y, table_right, totals_top_y)

    row_height = 16
    totals_label_x = expenses_x - 6
    totals_amount_x = table_right - 8

    # Subtotal row
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(totals_label_x, totals_top_y - 12, "Subtotal")
    c.setFont("Helvetica", 9)
    c.drawRightString(totals_amount_x, totals_top_y - 12, money(SUBTOTAL))

    # HST row
    c.line(expenses_x, totals_top_y - row_height, table_right, totals_top_y - row_height)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(description_x + 6, totals_top_y - row_height - 12, f"HST  {int(HST_RATE * 100)}%")
    c.setFont("Helvetica", 9)
    c.drawRightString(totals_amount_x, totals_top_y - row_height - 12, money(hst_amount))

    # Total row
    c.line(table_left, totals_top_y - row_height * 2, table_right, totals_top_y - row_height * 2)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(totals_label_x, totals_top_y - row_height * 2 - 12, "Total")
    c.drawRightString(totals_amount_x, totals_top_y - row_height * 2 - 12, money(total_amount))

    # Full table outline
    table_bottom = totals_top_y - row_height * 2 - 18
    c.rect(table_left, table_bottom, table_width, table_top - table_bottom, fill=0, stroke=1)
    c.line(expenses_x, table_bottom, expenses_x, table_top)

    # Payment terms
    current_y = table_bottom - 22
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin, current_y, "Payment Terms")
    current_y -= 14

    c.setFont("Helvetica", 10)
    for payment_term in PAYMENT_TERMS:
        c.drawString(left_margin, current_y, f"• {payment_term}")
        current_y -= 12

    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(left_margin, 80, "Thank you")

    c.showPage()
    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    build_pdf()