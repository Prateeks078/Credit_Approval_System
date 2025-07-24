from rest_framework import serializers
from .models import Customer,Loan
import pandas as pd
import random
import math

class RegisterCustomerSerializer(serializers.ModelSerializer):
    monthly_income = serializers.IntegerField(write_only=True)
    approved_limit = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age', 'monthly_income', 'phone_number', 'approved_limit']

    def create(self, validated_data):
        salary = validated_data.pop('monthly_income')
        approved_limit = round((36 * salary) / 100000) * 100000

        customer = Customer.objects.create(
            monthly_salary=salary,
            approved_limit=approved_limit,
            **validated_data
        )
        return customer


class CheckEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()  # in months

    def validate(self, data):
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")

        total_debt = customer.current_debt + data['loan_amount']
        approved = total_debt <= customer.approved_limit

        # EMI formula
        P = data['loan_amount']
        R = data['interest_rate'] / (12 * 100)
        N = data['tenure']
        EMI = P * R * ((1 + R) ** N) / ((1 + R) ** N - 1)

        data['approval'] = approved
        data['monthly_installment'] = round(EMI, 2)

        if not approved:
            # Bump rate by 3% if not eligible
            new_rate = data['interest_rate'] + 3
            data['corrected_interest_rate'] = new_rate
        else:
            data['corrected_interest_rate'] = None

        return data
    
class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()  # in months

    def validate(self, data):
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")

        if customer.current_debt + data['loan_amount'] > customer.approved_limit:
            raise serializers.ValidationError("Loan exceeds approved limit.")

        data['customer'] = customer
        return data

    def create(self, validated_data):
        customer = validated_data['customer']
        amount = validated_data['loan_amount']
        rate = validated_data['interest_rate'] / (12 * 100)
        months = validated_data['tenure']

        emi = amount * rate * ((1 + rate) ** months) / ((1 + rate) ** months - 1)
        monthly_repayment = round(emi, 2)

        loan = Loan.objects.create(
            customer=customer,
            loan_id=random.randint(1000, 9999),
            loan_amount=amount,
            interest_rate=validated_data['interest_rate'],
            tenure=months,
            monthly_repayment=monthly_repayment,
            emis_paid_on_time=0,
            start_date=pd.Timestamp.now().date(),
            end_date=pd.Timestamp.now().date() + pd.DateOffset(months=months)
        )

        # Update current debt
        customer.current_debt += amount
        customer.save()

        return loan
    
class LoanDetailSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "customer",
            "loan_amount",
            "interest_rate",
            "monthly_repayment",
            "tenure",
            "start_date",
            "end_date"
        ]

    def get_customer(self, obj):
        return {
            "first_name": obj.customer.first_name,
            "last_name": obj.customer.last_name,
            "phone_number": obj.customer.phone_number
        }