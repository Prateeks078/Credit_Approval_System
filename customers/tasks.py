from celery import shared_task
import pandas as pd
from .models import Customer,Loan

@shared_task
def ingest_excel_data():
    # Load Customer Data
    df_customers = pd.read_excel("customer_data.xlsx")

    for _, row in df_customers.iterrows():
        salary = int(row["Monthly Salary"])
        approved_limit = round((36 * salary) / 100000) * 100000  # round to nearest lakh

        Customer.objects.update_or_create(
            phone_number=str(row["Phone Number"]),
            defaults={
                "first_name": row["First Name"],
                "last_name": row["Last Name"],
                "age": int(row["Age"]),
                "monthly_salary": salary,
                "approved_limit": approved_limit,
                "current_debt": 0  # default value
            }
        )

       # Load Loan Data
    df_loans = pd.read_excel("loan_data.xlsx")

    for _, row in df_loans.iterrows():
        try:
            customer = Customer.objects.get(id=int(row["Customer ID"]))  # match by DB ID
        except Customer.DoesNotExist:
            continue

        Loan.objects.update_or_create(
            loan_id=int(row["Loan ID"]),
            defaults={
                "customer": customer,
                "loan_amount": float(row["Loan Amount"]),
                "tenure": int(row["Tenure"]),
                "interest_rate": float(row["Interest Rate"]),
                "monthly_repayment": float(row["Monthly payment"]),  # ✅ exact
                "emis_paid_on_time": int(row["EMIs paid on Time"]),  # ✅ exact
                "start_date": pd.to_datetime(row["Date of Approval"]),
                "end_date": pd.to_datetime(row["End Date"])
            }
        )
