# AI-Assisted Learning Log — Engineer A (Registration, Validation & Persistence)

## Cycle 1 — Guaranteeing Atomic File Persistence
Question: How can we guarantee that if a disk write fails halfway through (due to a power loss or disk full error), our existing `requests.json` file isn't wiped out, truncated, or corrupted?

AI Explanation: Suggested writing serialized JSON data to a temporary file in the same directory (`requests.json.tmp`) first, and then using the operating system's atomic rename operation (`os.replace()`) to swap it in place of the target file.

Experiment: Wrote a test script that simulated an exception midway through writing to disk and checked whether the original file remained untouched.

Verification: The test confirmed that atomic replacement protected the original valid file from being partially overwritten or corrupted.

Decision: Implemented the temporary file and `os.replace()` pattern in `save_requests()` to ensure fail-safe atomic persistence.

## Cycle 2 — Strict Input Validation and Regex ID Patterns
Question: How do we prevent malformed IDs, arbitrary Unicode numerals, and blank whitespace strings from bypassing our registration checks?

AI Explanation: Recommended combining string method checks (`.strip()`) with regular expressions (`re.compile(r"^A\d{3}$")`) to strictly enforce ASCII digit patterns (0–9) and reject invalid data types before record creation.
Experiment: Tested passing whitespace strings (`"   "`), incorrect ID formats (`"ABC"`), and non-ASCII characters into `create_request` and `get_request`.

Verification: Unit tests successfully caught all malformed inputs and raised explicit `ValueError` or `KeyError` exceptions.

Decision: Adopted strict regex patterns and type checking across all storage registration functions.


## Engineer B — AI-Assisted Learning Log

### Cycle 1 — Enforcing State Machine Invariants & Atomic Rollback

Question: How do we guarantee that if an invalid state transition is attempted (e.g., issuing a card before approval), dictionary fields are not partially modified?

AI Explanation: Suggested adopting a "validation-first" pattern where all checks occur at the very beginning of the function before any dictionary mutation takes place.

Experiment: Intentionally placed a status modification before the validation check in a test branch and triggered a failure, observing that the record state was corrupted. Moved the validation check to the top.
Verification: Unit tests successfully proved that raising a ValueError left the stored dictionary attributes completely untouched.

Decision: Established a strict validation-first contract across all workflow functions (approve_request, issue_card, return_card).

### Cycle 2 — Building a Resilient CLI Menu Loop

Question: How can we ensure the interactive CLI menu (main.py) doesn't crash when a user enters unexpected text, malformed IDs, or invalid options?

AI Explanation: Recommended wrapping user input handlers in explicit try except blocks catching ValueError and KeyError, combined with continuous loop iteration instead of letting exceptions bubble up to termination.

Experiment: Entered random strings and unknown IDs into prompt fields and observed how the application caught the exception, printed a clear error message, and returned smoothly to the main menu.

Verification: Verified that the CLI remains stable and responsive under incorrect user inputs.

Decision: Implemented clean try except exception boundaries around all menu choice actions in main.py.