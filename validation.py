"""Validation rules for Campus Access requests (Engineer A).

Every function here either returns a good value or raises ValueError
with a clear message. Nothing in this file changes stored data.
"""

ALLOWED_CARD_TYPES = ("visitor", "student", "staff")
ALLOWED_STATUSES = ("requested", "approved", "issued", "returned")
RECORD_KEYS = ("id", "fellow_id", "card_type", "status", "approved_by")
ASCII_DIGITS = "0123456789"  # only these count as digits (not Unicode numerals)


def validate_fellow_id(fellow_id):
    """Must be non-blank text. Returns the text with outer spaces removed."""
    if not isinstance(fellow_id, str):
        raise ValueError("Fellow ID must be text.")
    cleaned = fellow_id.strip()
    if cleaned == "":
        raise ValueError("Fellow ID cannot be blank.")
    return cleaned


def validate_approver(approved_by):
    """Must be non-blank text. Returns the text with outer spaces removed."""
    if not isinstance(approved_by, str):
        raise ValueError("Approver must be text.")
    cleaned = approved_by.strip()
    if cleaned == "":
        raise ValueError("Approver cannot be blank.")
    return cleaned


def validate_card_type(card_type):
    """Must be visitor, student or staff. Returns it in lower case."""
    if not isinstance(card_type, str):
        raise ValueError("Card type must be text.")
    cleaned = card_type.strip().lower()
    if cleaned not in ALLOWED_CARD_TYPES:
        raise ValueError(
            "Card type must be one of: " + ", ".join(ALLOWED_CARD_TYPES) + "."
        )
    return cleaned


def validate_request_id(request_id):
    """Must look like A001: the letter A, then at least 3 ASCII digits.
    A000 is rejected (numbering starts at 1). Returns the ID unchanged."""
    if not isinstance(request_id, str):
        raise ValueError("Request ID must be text.")
    digits = request_id[1:]
    if (
        request_id[:1] != "A"
        or len(digits) < 3
        or any(ch not in ASCII_DIGITS for ch in digits)
        or int(digits) < 1
    ):
        raise ValueError("Request ID must look like A001 (got " + repr(request_id) + ").")
    return request_id


def validate_status(status):
    """Must be one of the four known statuses."""
    if status not in ALLOWED_STATUSES:
        raise ValueError("Unknown status: " + repr(status) + ".")
    return status


def validate_record(record):
    """Check a whole request dictionary. Used before storing anything and
    when loading a file. Raises ValueError if anything is wrong."""
    if not isinstance(record, dict):
        raise ValueError("A request must be a dictionary.")
    if set(record.keys()) != set(RECORD_KEYS):
        raise ValueError(
            "A request must have exactly these keys: " + ", ".join(RECORD_KEYS) + "."
        )

    validate_request_id(record["id"])
    validate_fellow_id(record["fellow_id"])
    if record["card_type"] not in ALLOWED_CARD_TYPES:
        raise ValueError("Invalid card type: " + repr(record["card_type"]) + ".")
    validate_status(record["status"])

    approved_by = record["approved_by"]
    if approved_by is not None:
        validate_approver(approved_by)

    # Business rules that must always be true:
    if record["status"] == "requested" and approved_by is not None:
        raise ValueError("A 'requested' request cannot have an approver yet.")
    if record["status"] != "requested" and approved_by is None:
        raise ValueError("Status '" + record["status"] + "' needs a non-empty approved_by.")
