# main.py
from invoice_input import read_image_pdf, read_pdf
from ai_extraction import parse_invoice_with_llm
from validation import validate_invoice
from approval import route_invoice
from erp_integration import post_to_erp
from dashboard import log_invoice_status, notify_manager

# Mock PO database
po_database = ["PO1234", "PO5678"]

# Step 1: Upload PDF
invoice_text = read_image_pdf("sample_invoice.pdf")

# Step 2: Extract fields with AI
invoice_data = parse_invoice_with_llm(invoice_text)

# Step 3: Validate
errors = validate_invoice(invoice_data, po_database)
if errors:
    # route to manual approval / show human-in-the-loop
    print("Validation errors:", errors)
else:
    # you can use invoice_data["total_amount_parsed"] safely
    print("Parsed amount:", invoice_data["total_amount_parsed"])

# Step 4: Approval routing
status = route_invoice(invoice_data, errors)

# Step 5: ERP Integration (if approved)
if status == "approved":
    post_to_erp(invoice_data)

# Step 6: Dashboard logging
log_invoice_status(invoice_data, status)

# Step 7: Notify manager if needed
if errors:
    notify_manager(invoice_data, errors)