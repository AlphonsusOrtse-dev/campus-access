from storage import get_request, update_request


def approve_request(request_id: str, approved_by: str) -> dict:
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approval requires a non-empty approver identifier (e.g., M01).")

    req = get_request(request_id)
    
    if req["status"] != "requested":
        raise ValueError(f"Cannot approve request in status '{req['status']}'. Must be 'requested'.")

    return update_request(request_id, "approved", approved_by)


def issue_card(request_id: str) -> dict:
    req = get_request(request_id)

    if req["status"] != "approved":
        raise ValueError(f"Cannot issue card from status '{req['status']}'. Must be 'approved'.")

    if not req.get("approved_by"):
        raise ValueError("Cannot issue card without an authorized approver.")

    return update_request(request_id, "issued", req["approved_by"])


def return_card(request_id: str) -> dict:
    req = get_request(request_id)

    if req["status"] != "issued":
        raise ValueError(f"Cannot return card from status '{req['status']}'. Must be 'issued'.")

    return update_request(request_id, "returned", req["approved_by"])