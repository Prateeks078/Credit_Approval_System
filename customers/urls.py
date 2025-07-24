from django.urls import path
from .views import RegisterCustomerView, CheckEligibilityView, CreateLoanView,ViewLoanDetailView,ViewCustomerLoans

urlpatterns = [
    path('register', RegisterCustomerView.as_view(), name='register'),
    path('check-eligibility', CheckEligibilityView.as_view(), name='check_eligibility'),
    path('create-loan', CreateLoanView.as_view(), name='create_loan'),
    path('view-loan/<int:loan_id>', ViewLoanDetailView.as_view(), name='view_loan'),
    path("view-loans/<int:customer_id>/", ViewCustomerLoans.as_view(), name="view_customer_loans"),
]
