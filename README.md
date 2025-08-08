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
   git clone https://github.com/yourusername/reportcard-system.git
   cd reportcard-system
````

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your database settings in `settings.py` (default is PostgreSQL).

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

---

## API Endpoints

| Endpoint                                     | Method | Description                                          |
| -------------------------------------------- | ------ | ---------------------------------------------------- |
| `/api/students/`                             | GET    | List all students                                    |
| `/api/students/`                             | POST   | Create a new student                                 |
| `/api/students/{id}/`                        | GET    | Retrieve a specific student                          |
| `/api/students/{id}/`                        | PUT    | Update a student                                     |
| `/api/students/{id}/`                        | DELETE | Delete a student                                     |
| `/api/students/{id}/avg-overview/?year=YYYY` | GET    | Get average marks overview for the student in a year |

\| `/api/subjects/`               | GET    | List all subjects                             |
\| `/api/subjects/`               | POST   | Create a new subject                          |
\| `/api/subjects/{id}/`          | GET    | Retrieve a specific subject                   |

\| `/api/report-cards/`           | GET    | List report cards                             |
\| `/api/report-cards/`           | POST   | Create a report card                          |

\| `/api/marks/`                 | GET    | List marks                                   |
\| `/api/marks/`                 | POST   | Add a mark                                   |

### Filtering & Searching

* Students: filter by `name`, `email` (search)
* Subjects: filter by `name`, `code` (search)
* ReportCards: filter by `student`, search by `term`
* Marks: no filters by default

---

## Authentication

* Token Authentication is enabled for all endpoints.
* Obtain token using DRF’s token obtain endpoint or your custom login.
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

You can find the Postman collection for this API in `postman_collection.json`.
Import it into Postman to quickly test and explore all API endpoints.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests.
Make sure tests pass before submitting.

---

## License

MIT License

---

*Created by Your Name*

```

---

If you want, I can also generate:  
- A `requirements.txt` file  
- Example `.env` for settings  
- Postman collection JSON export  

Just ask!
```
