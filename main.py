import sys
from storage import create_request, get_request, list_requests, save_requests, load_requests
from workflow import approve_request, issue_card, return_card

DATA_FILE = "data/requests.json"


def print_menu():
    print("   CAMPUS ACCESS MANAGER      ")
    print("1. Create Request")
    print("2. View Request")
    print("3. Approve Request")
    print("4. Issue Card")
    print("5. Return Card")
    print("6. List All Requests")
    print("7. Save to JSON")
    print("8. Reload from JSON")
    print("0. Quit Safely")


def run_menu():
    try:
        load_requests(DATA_FILE)
    except Exception as e:
        print(f"[Warning] Could not load existing data: {e}")

    while True:
        print_menu()
        choice = input("Enter your choice (1-0): ").strip()

        if choice == "1":
            fellow_id = input("Enter Fellow ID (e.g., F001): ").strip()
            card_type = input("Enter Card Type (visitor, student, staff): ").strip().lower()
            try:
                req = create_request(fellow_id, card_type)
                print(f"Success! Created request {req['id']} for {req['fellow_id']} ({req['card_type']}).")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            req_id = input("Enter Request ID (e.g., A001): ").strip().upper()
            try:
                req = get_request(req_id)
                print(f"\nRequest Details:")
                for k, v in req.items():
                    print(f"  {k}: {v}")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "3":
            req_id = input("Enter Request ID to approve: ").strip().upper()
            approver = input("Enter Approver ID (e.g., M01): ").strip()
            try:
                req = approve_request(req_id, approver)
                print(f"Success! Request {req['id']} approved by {req['approved_by']}.")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            req_id = input("Enter Request ID to issue card: ").strip().upper()
            try:
                req = issue_card(req_id)
                print(f"Success! Card issued for request {req['id']}.")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "5":
            req_id = input("Enter Request ID to return card: ").strip().upper()
            try:
                req = return_card(req_id)
                print(f"Success! Card returned for request {req['id']} (Final).")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "6":
            reqs = list_requests()
            if not reqs:
                print("No requests found.")
            else:
                print(f"\n--- All Requests ({len(reqs)}) ---")
                for r in reqs:
                    print(f"[{r['id']}] Fellow: {r['fellow_id']} | Type: {r['card_type']} | Status: {r['status']} | Approver: {r['approved_by']}")

        elif choice == "7":
            try:
                save_requests(DATA_FILE)
                print(f"Successfully saved requests to {DATA_FILE}.")
            except Exception as e:
                print(f"Error saving file: {e}")

        elif choice == "8":
            confirm = input("Reloading will overwrite unsaved changes. Proceed? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    load_requests(DATA_FILE)
                    print(f"Successfully reloaded requests from {DATA_FILE}.")
                except Exception as e:
                    print(f"Error loading file (Data preserved): {e}")

        elif choice == "0":
            try:
                save_requests(DATA_FILE)
                print("Data saved safely. Goodbye!")
            except Exception as e:
                print(f"Warning: Auto-save on exit failed: {e}")
            sys.exit(0)

        else:
            print("Invalid option! Please enter a number between 1 and 9.")


if __name__ == "__main__":
    run_menu()