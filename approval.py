# approval.py
def route_invoice(invoice_data, validation_errors):
    if validation_errors:
        print(f"Invoice {invoice_data['Invoice Number']} requires manual approval. Errors: {validation_errors}")
        # Could send email/Slack here
        return "pending"
    else:
        print(f"Invoice {invoice_data['Invoice Number']} auto-approved")
        return "approved"