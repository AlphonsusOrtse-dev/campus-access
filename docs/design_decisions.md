Design Decisions — Campus Access Engineering Challenge

1. Request Dictionary Structure: Contains keys `id`, `fellow_id`, `card_type`, `status`, and `approved_by`.

2. Error Reporting: Functions raise explicit standard exceptions (`ValueError`, `KeyError`, `IOError`).

3. ID Generation: Automatically computed using pattern `^A\d{3}$`.

4. Storage Integration: `workflow.py` imports retrieval functions from `storage.py` to ensure centralized control.

5. Atomic Persistence: `save_requests` writes to a `.tmp` file first and uses `os.replace()`.

6. Corrupted File Defense: `load_requests` aborts immediately on `JSONDecodeError` or schema violations.

7. Validation-First Invariant: All workflow validation checks occur before dictionary mutation to guarantee atomic rollback.