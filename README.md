# Campus Access Management System

## 1. Project Overview

The Campus Access Management System is a Python command-line application
that manages campus access-card requests for visitors, students, and staff.

The application allows users to create and view access-card requests,
approve requests, issue cards, process returns, and list requests.

It is designed to prevent invalid operations, maintain accurate records,
and preserve request data between program sessions.

This project is being developed collaboratively by two engineers using
Python, automated testing, and GitHub.

## 2. Project Objectives

The objectives of this project are to:

- Create and manage campus access-card requests.
- Validate request information before storing it.
- Enforce the correct access-card approval and return process.
- Prevent unauthorized or invalid workflow transitions.
- Store request records in JSON so data can persist between sessions.
- Generate unique request IDs that remain unique across restarts.
- Handle invalid input and errors without corrupting existing data.
- Use automated tests to verify application behavior.
- Practise professional Git branching, code review, and collaboration.

## 3. Key Features

### 3.1 Request Management

The application should allow users to:

- Create a new access-card request.
- View an individual request.
- List all requests.
- Identify each request using a unique ID.
- Track the current status of a request.

Each request contains:

- Request ID
- Fellow ID
- Card type
- Request status
- Approver identifier

### 3.2 Request Validation

Request validation ensures that submitted information meets the
project's requirements.

The application must reject:

- Blank fellow IDs.
- Invalid card types.
- Malformed request IDs.
- Duplicate request IDs.
- Requests containing invalid data.

The permitted card types are:

- `visitor`
- `student`
- `staff`

Request IDs follow this format:

- `A001`
- `A002`
- `A003`

IDs must remain unique, including after the application restarts.

### 3.3 Access-Card Workflow

Every request follows a defined sequence of states:

`requested → approved → issued → returned`

The application must enforce the following rules:

- A new request begins with the status `requested`.
- Only a request in the `requested` state can be approved.
- Approval requires a non-empty approver identifier.
- Only an approved request with an approver can be issued.
- A card can only be returned after it has been issued.
- A returned request cannot be issued or returned again.
- Invalid state transitions must be rejected.
- A rejected operation must not modify the existing request.

### 3.4 Data Storage and Persistence

Request records must be saved in JSON and reloaded when the application
starts again.

The storage component must ensure that:

- Request records are saved and retrieved correctly.
- Request IDs remain unique across restarts.
- Invalid or corrupted JSON data produces a clear error.
- Duplicate IDs and malformed records are rejected.
- Invalid data is never silently replaced with an empty collection.

### 3.5 Error Handling

The application should provide helpful feedback when users enter
invalid information, choose an unsupported menu option, or attempt
an operation that is not permitted.

Recoverable input errors should allow users to try again rather
than unexpectedly terminating the application.

## 4. Technology Stack

- **Programming language:** Python 3
- **Data storage:** JSON
- **Automated testing:** Python `unittest`
- **Version control:** Git
- **Collaboration and code review:** GitHub

The project uses Python's standard library and does not require
third-party packages for its core functionality.

## 5. Project Structure

The intended project structure is:

```text
campus-access/
├── main.py
├── storage.py
├── validation.py
├── workflow.py
├── tests/
│   ├── test_storage.py
│   ├── test_validation.py
│   └── test_workflow.py
├── docs/
│   ├── design_decisions.md
│   └── ai_learning_log.md
├── .gitignore
└── README.md
```

### Module Responsibilities

- **`main.py`** — Provides the command-line interface and connects
  user actions to the application logic.

- **`storage.py`** — Manages request records, unique IDs, JSON saving,
  and JSON loading.

- **`validation.py`** — Checks request data and rejects invalid inputs.

- **`workflow.py`** — Implements approval, card issuance, returns,
  and the rules governing valid status transitions.

- **`tests/`** — Contains automated tests for the application's
  storage, validation, and workflow behavior.

- **`docs/design_decisions.md`** — Documents important design decisions.

- **`docs/ai_learning_log.md`** — Records AI-assisted learning,
  experiments, verification, and final decisions.

The structure above describes the intended completed project.
Individual files and tests may still be under development.

## 6. Requirements and Setup

### Requirements

- Python 3
- Git
- Access to the project's GitHub repository

### Clone the Repository

```bash
git clone https://github.com/AlphonsusOrtse-dev/campus-access.git
cd campus-access
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

No third-party package installation should be necessary for the core
application because it uses Python's standard library.

## 7. Running the Application

From the project directory, run:

```bash
python3 main.py
```

Follow the command-line menu to perform the operations supported
by the application.

Available functionality in the completed application should include:

1. Creating an access-card request.
2. Viewing a request.
3. Approving a request.
4. Issuing an access card.
5. Returning an access card.
6. Listing requests.
7. Saving and reloading request data.
8. Exiting the application safely.

## 8. Running the Tests

Run the automated test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The tests should cover valid operations, invalid inputs, workflow
transitions, persistence, and error handling.

Important cases include:

- Creating a valid request.
- Rejecting a blank fellow ID.
- Rejecting an invalid card type.
- Preventing duplicate request IDs.
- Rejecting attempts to issue a card before approval.
- Rejecting approval with a blank approver.
- Completing the full approval, issuance, and return workflow.
- Rejecting a second return.
- Confirming that rejected operations leave records unchanged.
- Preserving unique IDs after restarting the application.
- Handling malformed JSON without silently discarding valid data.
- Allowing users to recover from invalid menu input.

Tests should use isolated data so that one test does not accidentally
affect another test or overwrite important application records.

Only report tests as passing after they have actually been run
and their results verified.

## 9. Team Responsibilities

The project is divided between two engineers.

### Engineer A — Request Validation and Storage

Responsibilities include:

- Implementing `validation.py`.
- Implementing `storage.py`.
- Writing tests for validation and storage.
- Ensuring that request data is valid and stored safely.
- Ensuring that IDs remain unique across restarts.
- Handling invalid or corrupted JSON data.

### Engineer B — Access Workflow

Responsibilities include:

- Implementing and testing the access-card workflow.
- Enforcing valid request status transitions.
- Preventing unauthorized or invalid operations.
- Ensuring that failed operations do not modify existing records.
- Integrating workflow behavior with the validation and storage modules.
- Testing the complete request lifecycle.

Both engineers are responsible for understanding their code,
verifying their changes, documenting their learning, and participating
in code review.

## 10. Git and GitHub Collaboration

Each engineer works on a separate feature branch.

- **Engineer A:** `feat/1-request-validation`
- **Engineer B:** `feat/2-access-workflow`

The collaboration process is:

1. Make changes on the appropriate feature branch.
2. Run relevant automated tests.
3. Review the changes before committing.
4. Commit changes with clear, descriptive messages.
5. Push the feature branch to GitHub.
6. Open a pull request.
7. Have the other engineer review the code and tests.
8. Address review feedback.
9. Obtain approval before merging.
10. Run the complete test suite after integration.

Feature work should be merged through reviewed pull requests rather
than pushed directly to `main`.

Example commit messages:

```text
feat: validate access-card requests
feat: enforce access-card workflow
test: cover invalid workflow transitions
docs: update project documentation
```

## 11. Testing and Final Demonstration

The completed project should demonstrate that:

- A new request receives a unique ID and starts as `requested`.
- An unapproved request cannot be issued.
- A request cannot be approved without an approver identifier.
- An approved request can be issued.
- An issued card can be returned.
- Invalid transitions are rejected without changing the record.
- Request data survives application restarts.
- Invalid JSON data is handled safely.
- Invalid menu input produces helpful feedback.
- The full test suite runs successfully after integration.

Both engineers should be able to explain their implementations,
demonstrate their tests, and describe how code review improved
the project.

## 12. Learning and Documentation

This project is also a Python learning exercise.

The engineers should use AI to understand concepts, explore edge cases,
review designs, and investigate test failures—not simply to generate
code without understanding it.

Each engineer should record at least two verified AI learning cycles
in `docs/ai_learning_log.md`.

Each learning cycle should include:

- The question or problem investigated.
- The explanation or suggestion received.
- The experiment performed independently.
- The observed result.
- The verification and final decision.

Important design choices should be recorded in
`docs/design_decisions.md`.

## 13. Project Status

The project is being developed in separate feature branches.
The final application is considered complete only after the required
modules are integrated, the tests have been run successfully, and
the GitHub review and merge process has been completed.