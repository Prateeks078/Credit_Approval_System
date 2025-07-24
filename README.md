# Credit Approval System (Django REST API)

This project is a backend system designed to manage customer registration, loan approval eligibility, and loan management. It is built using Django, Django REST Framework, and PostgreSQL (or SQLite for local testing).

## Features

- Register customers and auto-calculate approved credit limits
- Check loan eligibility based on income, tenure, and interest rate
- Create loans with EMI calculations
- View loan details and customer loan history
- Ingest customer and loan data from Excel (via Celery background task)
- RESTful APIs with clean architecture

## API Endpoints

| Endpoint              | Method | Description                              |
|-----------------------|--------|------------------------------------------|
| `/register`           | POST   | Register a new customer                  |
| `/check-eligibility`  | POST   | Check if a customer is eligible for loan |
| `/create-loan`        | POST   | Create a new loan for a customer         |
| `/view-loan/<loan_id>`| GET    | View loan details                        |
| `/view-loans/<cust_id>`| GET   | View all loans for a customer            |




