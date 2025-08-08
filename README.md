# Report Card System

A Django REST Framework based API to manage students, subjects, report cards, and marks — allowing tracking of student performance by term and year.

---

## Tech Stack

- Python 3.12
- Django 5.2.4 
- Django REST Framework  
- SQLite
- pytest + pytest-django for testing  

---

## Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Abishek-Sapkota/Report-Card-System.git
   cd Report-Card-System
   ```

2. Create a virtual environment, activate it and install dependencies:
   - Using `pip`

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   - Using `uv`
   ```bash
   uv init
   uv sync --locked
   ```
   OR
   ```bash
   uv pip install -r requirements.txt
   ```

---

## Database Migrations

Run migrations to create tables:

```bash
python manage.py migrate
```

---

## Running the Server

Start the development server:

```bash
python manage.py runserver
```

## Authentication

* Token Authentication is enabled for all endpoints.
* Token can be obtained using `/api/token` endpoint
* Include header:

  ```
  Authorization: Token <your_token>
  ```

---

## Testing

Run the test suite with:

```bash
pytest
```

Tests cover models, serializers, and API endpoints.

---

## Postman Collection

You can find the Postman collection for this API in [Report_card_system_postman_collection.json](./Report_card_system_postman_collection.json).
Import it into Postman to quickly test and explore all API endpoints.

---