# validation.py
# validation.py (or utils.py)
import re
from decimal import Decimal, InvalidOperation

CURRENCY_RE = re.compile(r"[^\d,.\-\(\)]")  # allow digits, comma, dot, minus, parentheses

def parse_amount(amount_str):
    """
    Parse a human-written currency string into a float value (USD-style).
    Handles inputs like:
      "$5,832.00", "5,832.00", "5832", "-$1,234.50", "(1,234.50)", "€1.234,56" (best-effort)
    Returns: float
    Raises ValueError on irrecoverable formats.

    Strategy (best-effort):
    - Remove currency symbols/letters.
    - Keep digits, comma, dot, minus, parentheses.
    - If parentheses -> negative number.
    - If both '.' and ',' exist: assume the right-most separator is decimal.
      e.g. "1.234,56" -> '.' thousands, ',' decimal -> 1234.56
            "1,234.56" -> ',' thousands, '.' decimal -> 1234.56
    - If only ',' exists:
      - If there are exactly 2 digits after the comma -> treat comma as decimal.
      - Else treat comma as thousands separator and remove it.
    - If only '.' exists:
      - Normal float conversion.
    """
    if amount_str is None:
        raise ValueError("amount_str is None")

    s = str(amount_str).strip()

    # detect parentheses for negative numbers like "(1,234.56)"
    is_negative = False
    if s.startswith("(") and s.endswith(")"):
        is_negative = True
        s = s[1:-1].strip()

    # Remove currency letters/symbols except digits and separators
    s = CURRENCY_RE.sub("", s)

    # Quick sanity
    if s == "" or s == "-" or s == "." or s == ",":
        raise ValueError(f"Could not parse amount: '{amount_str}' -> cleaned to empty")

    # Count separators
    has_dot = "." in s
    has_comma = "," in s

    normalized = s

    try:
        if has_dot and has_comma:
            # Use rightmost separator as decimal separator
            last_dot = s.rfind(".")
            last_comma = s.rfind(",")
            if last_comma > last_dot:
                # comma is decimal, dot is thousands
                normalized = s.replace(".", "")           # remove thousands dots
                normalized = normalized.replace(",", ".")  # make decimal point
            else:
                # dot is decimal, comma thousands
                normalized = s.replace(",", "")
            value = Decimal(normalized)
        elif has_comma and not has_dot:
            # Only comma present: decide whether comma is decimal or thousands
            parts = s.split(",")
            if len(parts[-1]) == 2:
                # looks like decimal cents -> treat comma as decimal separator
                normalized = s.replace(".", "")  # remove unexpected dots (if any)
                normalized = normalized.replace(",", ".")
                value = Decimal(normalized)
            else:
                # probably thousands separator -> remove commas
                normalized = s.replace(",", "")
                value = Decimal(normalized)
        else:
            # Only dot or no separator -> straightforward
            normalized = s.replace(",", "")
            value = Decimal(normalized)

        float_val = float(value)
        if is_negative:
            float_val = -float_val
        return float_val

    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"Failed to parse amount '{amount_str}' cleaned='{normalized}': {e}")
    

# validation.py (continued)
from typing import Dict, List

def validate_invoice(invoice_data: Dict[str, str], po_database: List[str]):
    errors = []
    
    # Validate presence of required fields. 
    # For now we will skip this, since we are not checking exact field names
    #
    # required = ["invoice_number", "po_number", "total_amount"]
    #for field in required:
    #    if not invoice_data.get(field):
    #        errors.append(f"Missing required field: {field}")

    # Validate PO Number
    po_num = invoice_data.get("po_number") or invoice_data.get("PO Number") or invoice_data.get("po")
    if po_num:
        # normalize PO formats if you have rules, else raw check
        if po_num not in po_database:
            errors.append(f"PO Number mismatch: {po_num}")

    # Validate amount (robust parsing)
    amt_raw = invoice_data.get("total_amount") or invoice_data.get("Total Amount") or invoice_data.get("amount")
    if amt_raw:
        try:
            amt_val = parse_amount(amt_raw)
            # Example business rule: amount must be > 0
            if amt_val <= 0:
                errors.append(f"Invalid invoice amount: {amt_raw} -> {amt_val}")
            else:
                # attach parsed amount back into invoice_data for downstream use
                invoice_data["total_amount_parsed"] = amt_val
        except ValueError as e:
            errors.append(str(e))
    else:
        errors.append("Total amount missing")

    return errors