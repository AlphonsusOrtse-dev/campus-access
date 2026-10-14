from storage import get_request


def approve_request(request_id: str, approved_by: str) -> dict:
 
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approval requires a non-empty approver identifier (e.g., M01).")

    req = get_request(request_id)  
    
    if req["status"] != "requested":
        raise ValueError(f"Cannot approve request in status '{req['status']}'. Must be 'requested'.")

    req["status"] = "approved"
    req["approved_by"] = approved_by.strip()
    return req


def issue_card(request_id: str) -> dict:
    
    req = get_request(request_id)

    if req["status"] != "approved":
        raise ValueError(f"Cannot issue card from status '{req['status']}'. Must be 'approved'.")

    if not req.get("approved_by"):
        raise ValueError("Cannot issue card without an authorized approver.")

    req["status"] = "issued"
    return req


def return_card(request_id: str) -> dict:
   
    req = get_request(request_id)

    if req["status"] != "issued":
        raise ValueError(f"Cannot return card from status '{req['status']}'. Must be 'issued'.")

    req["status"] = "returned"
    return req