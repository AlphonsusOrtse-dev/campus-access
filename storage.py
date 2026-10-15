"""Storage for Campus Access requests (Engineer A).

All requests live in one dictionary, _requests, keyed by request ID.
Other modules (Engineer B) must go through the functions below and never
touch _requests directly.

Every function that can fail raises ValueError (bad input / bad file).
save_requests can also raise OSError if the disk write fails.
"""

import json
import os

from validation import (
    validate_approver,
    validate_card_type,
    validate_fellow_id,
    validate_record,
    validate_request_id,
)

_requests = {}


def reset_storage():
    """Empty the in-memory store. Used by tests (setUp)."""
    _requests.clear()


def _sorted_ids():
    """IDs in numeric order (A002 before A010)."""
    return sorted(_requests, key=lambda request_id: int(request_id[1:]))


def _next_id():
    """One more than the highest number in use, so IDs never repeat.
    Works after loading a file because it looks at the loaded data."""
    highest = 0
    for request_id in _requests:
        number = int(request_id[1:])
        if number > highest:
            highest = number
    return "A" + str(highest + 1).zfill(3)


def create_request(fellow_id, card_type):
    """Validate first, then create. Returns a COPY of the new request."""
    fellow_id = validate_fellow_id(fellow_id)
    card_type = validate_card_type(card_type)
    record = {
        "id": _next_id(),
        "fellow_id": fellow_id,
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }
    _requests[record["id"]] = record
    return dict(record)


def get_request(request_id):
    """Read-only lookup. Returns a COPY, so changing it changes nothing."""
    validate_request_id(request_id)
    if request_id not in _requests:
        raise ValueError("Unknown request ID: " + request_id)
    return dict(_requests[request_id])


def list_requests():
    """All requests as copies, in ID order."""
    return [dict(_requests[request_id]) for request_id in _sorted_ids()]


def update_request(request_id, status, approved_by):
    """The ONLY way to change a stored request (Engineer B calls this).

    Engineer B decides whether the move is legal (requested->approved, etc).
    This function double-checks the final record is valid, and only then
    stores it. If anything is wrong, the stored record is left untouched.
    Returns a copy of the updated request.
    """
    validate_request_id(request_id)
    if request_id not in _requests:
        raise ValueError("Unknown request ID: " + request_id)

    candidate = dict(_requests[request_id])  # work on a copy
    candidate["status"] = status
    if approved_by is None:
        candidate["approved_by"] = None
    else:
        candidate["approved_by"] = validate_approver(approved_by)

    validate_record(candidate)  # raises ValueError if invalid
    _requests[request_id] = candidate  # only reached if everything was valid
    return dict(candidate)


def save_requests(path):
    """Write all requests to a JSON file.

    It writes to a temporary file first and swaps it in only when the write
    succeeded, so a failed save cannot damage an existing good file.
    """
    if not isinstance(path, str) or path.strip() == "":
        raise ValueError("File path must be non-empty text.")

    records = [dict(_requests[request_id]) for request_id in _sorted_ids()]
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    temp_path = path + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)
        os.replace(temp_path, path)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


def load_requests(path):
    """Load requests from a JSON file. Returns how many were loaded.

    - File does not exist: nothing is loaded, store unchanged, returns 0
      (normal on the very first run).
    - File empty, not valid JSON, not a list, bad record, or duplicate IDs:
      raises ValueError and the current store is left untouched.
    The new data replaces the store only after EVERYTHING checked out.
    """
    if not isinstance(path, str) or path.strip() == "":
        raise ValueError("File path must be non-empty text.")

    try:
        with open(path, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        return 0
    except UnicodeDecodeError:
        raise ValueError("File is not readable text: " + path)

    if text.strip() == "":
        raise ValueError("File is empty: " + path)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("File is not valid JSON (" + str(error) + ").")

    if not isinstance(data, list):
        raise ValueError("File must contain a list of requests.")

    loaded = {}
    for position, record in enumerate(data, start=1):
        try:
            validate_record(record)
        except ValueError as error:
            raise ValueError("Request #" + str(position) + " is invalid: " + str(error))
        if record["id"] in loaded:
            raise ValueError("Duplicate request ID in file: " + record["id"])
        loaded[record["id"]] = dict(record)

    _requests.clear()
    _requests.update(loaded)
    return len(loaded)
