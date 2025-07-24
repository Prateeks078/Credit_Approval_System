from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from .models import Loan
from .serializers import RegisterCustomerSerializer
from .serializers import CheckEligibilitySerializer
from .serializers import CreateLoanSerializer
from .serializers import LoanDetailSerializer


class RegisterCustomerView(APIView):
    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(RegisterCustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckEligibilityView(APIView):
    def post(self, request):
        serializer = CheckEligibilitySerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateLoanView(APIView):
    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()
            return Response({
                "loan_id": loan.loan_id,
                "customer_id": loan.customer.id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "tenure": loan.tenure,
                "monthly_installment": loan.monthly_repayment,
                "start_date": loan.start_date,
                "end_date": loan.end_date
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class ViewLoanDetailView(RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanDetailSerializer
    lookup_field = "loan_id"

class ViewCustomerLoans(APIView):
    def get(self, request, customer_id):
        loans = Loan.objects.filter(customer__id=customer_id)
        if not loans.exists():
            return Response({"message": "No loans found for this customer."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LoanDetailSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   