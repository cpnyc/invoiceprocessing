# dashboard.py
def log_invoice_status(invoice_data, status):
    print(f"Invoice {invoice_data['Invoice Number']} status: {status}")

def notify_manager(invoice_data, validation_errors):
    if validation_errors:
        print(f"Notify manager: Invoice {invoice_data['Invoice Number']} has errors: {validation_errors}")