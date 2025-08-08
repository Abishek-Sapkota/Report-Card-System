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

---

# Query Optimization Techniques


### 1. **Using `select_related` for Foreign Key Joins**

* **Purpose:** Reduce the number of database queries when accessing related objects with `ForeignKey`.
* **Example:**

  ```python
  queryset = ReportCard.objects.select_related("student")
  ```
* **Why:** Without `select_related`, Django executes additional queries for each related object. Using it performs an SQL join, fetching all required data in a single query.

---

### 2. **Using `prefetch_related` for Many-to-Many & Reverse Foreign Keys**

* **Purpose:** Optimize retrieval of related collections such as marks, subjects and student.
* **Example:**

  ```python
  queryset = Student.objects.prefetch_related("marks", "subjects")
  ```
* **Why:** Without `prefetch_related`, Django would run a new query per related set. Prefetching batches them in advance.

---

### 3. **Aggregation at the Database Level**

* **Purpose:** Perform calculations (like average, sum, grade counts) inside the database instead of Python loops.
* **Example:**

  ```python
  from django.db.models import Avg, Sum

  overall_average = Marks.objects.aggregate(overall_average=Avg("score"))["overall_average"]
  ```
* **Why:** SQL databases are optimized for aggregation. This avoids loading all data into Python memory before processing, reducing RAM usage and query time.

---

### 4. **Avoiding N+1 Query Problem**

* **Technique:** Combine `select_related`/`prefetch_related` to prevent unnecessary repeated queries.
* **Example:**

  ```python
  marks = ReportCard.objects.select_related("student").prefetch_related("marks")
  ```
* **Why:** Prevents repeated queries for each iteration.

---

### 5. **Indexing Frequently Queried Fields**

* **Purpose:** Speed up lookups and filtering.
* **Implementation:**

  * Added `db_index=True` to fields like `student_id`, `subject_id`, and term field.

---

### 6. **Using QuerySet Caching When Appropriate**

* **Purpose:** Prevent running the same query multiple times in a single request cycle.
* **Example:**

  ```python
  qs = Student.objects.all()
  count = qs.count()
  first_student = qs.first()
  ```
* **Why:** Django evaluates the queryset once and reuses results when stored in a variable.

---