# Python REST API Data Integration Tool

A small, runnable **personal portfolio project** that retrieves JSON records from a REST API, validates the response, selects useful fields, and writes them to a UTF-8 CSV file. The default source is the public [JSONPlaceholder posts endpoint](https://jsonplaceholder.typicode.com/posts).

## Features

- Calls a configurable HTTP JSON endpoint using `requests`.
- Sets a request timeout and reports timeout, HTTP, connection, and invalid-response errors.
- Exports `id`, `userId`, `title`, and `body` columns; ignores other fields.
- Creates the output directory when needed and writes a header even for an empty result.
- Includes pytest tests that mock HTTP calls, so tests do not depend on the API or network.

## Requirements

- Python 3.10 or newer
- pip

## Setup

From this project directory, create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then install packages:

```bash
python -m pip install -r requirements.txt
```

## Run

Fetch the sample posts and create `data/posts.csv`:

```bash
python api_to_csv.py
```

Choose a different endpoint, destination, or timeout:

```bash
python api_to_csv.py --url https://jsonplaceholder.typicode.com/posts --output output/posts.csv --timeout 5
```

The endpoint must return a JSON array of objects. The script prints a concise success message and returns a nonzero exit status if the request or response fails.

## Test

```bash
python -m pytest -v
```

All HTTP calls in the tests are mocked. The suite covers timeout handling, HTTP errors, malformed response shape, selected CSV fields, directory creation, and empty results.

## Project layout

```text
.
├── api_to_csv.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_api_to_csv.py
```

## Scope and limitations

This is a compact learning/portfolio example. It processes one response in memory and expects a JSON array; pagination, authentication, retries, streaming, and scheduling are outside its current scope. The default endpoint is a public demo API. No deployment or production use is claimed.

## Portfolio disclosure

Describe this as a **personal project**. Do not imply it was built for a client, deployed, or used to achieve business results. If you extend it, update the README and portfolio description to match what you actually implemented and verified.
