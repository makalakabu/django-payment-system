# Django-Based Online Payment Service

This project is a simplified PayPal-like online payment system developed using Django, allowing users to send and request money across multiple currencies (GBP, USD, EUR). It includes user registration, authentication, transaction logging, notifications, and a REST API for currency conversion.

## Features

### Core Functionality
- User registration, login, and logout
- Role-based access control (users vs. admin)
- Dashboard with balance view and notifications
- Send money (currency conversion applied)
- Request payment from other users
- View transaction history

### Admin Features
- View all users
- View all transaction history

### RESTful Web API
- `/conversion/<currency1>/<currency2>/<amount>/`
- Returns JSON with the converted amount and exchange rate

## Security Highlights

- CSRF protection (Django default)
- Secure password storage (hashed)
- XSS and SQL injection protection (via Django middleware)
- Role-based decorators for route access control
- Session-based authentication

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Bootstrap 5, Django Templates, Crispy Forms
- **Database**: SQLite (via Django ORM)
- **API**: REST (built-in Django views)
- **Libraries**:
  - `crispy-bootstrap5`
  - `requests`

## Project Structure

```
webapps2025/
├── converter/             # Currency conversion app
├── payapp/                # Payment logic and dashboard
├── register/              # User registration and login
├── templates/             # HTML templates
├── webapps2025/           # Project settings and routing
├── manage.py
└── setup.py               # Initial data setup script
```


## Setup Instructions

### 1. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 2. Install Dependencies
```bash
pip install django crispy-bootstrap5 requests
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Setup Initial Data
```bash
python setup.py
```

### 5. Run the Server
```bash
python manage.py runserver
```

Open in browser: [http://localhost:8000](http://localhost:8000)


## Sample Admin Login
```
Username: admin1
Password: admin1
```

## API Example

Currency conversion endpoint:
```
GET http://localhost:8000/conversion/GBP/USD/100/
```

Response:
```json
{
  "converted_amount": "125.00",
  "rate": "1.250000",
  "from_currency": "GBP",
  "to_currency": "USD",
  "last_updated": "2025-04-10T20:46:32.367525+00:00"
}
```

---

## Project Report

A full technical report is included:  
**[Final_Report.pdf](./Final_Report.pdf)**

It includes:
- System architecture
- Feature breakdown
- Security design
- API structure
- Screenshots
- Implementation summary table

