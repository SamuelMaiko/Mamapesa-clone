# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoanRequestSerializer, LoanRepaymentSerializer, LoanSerializer
from newmamapesa.models import Loan, LoanRepayment
from rest_framework.permissions import IsAuthenticated

class LoanRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LoanRequestSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            loan = serializer.save()
            return Response({'success': 'Loan request successful', 'loan_id': loan.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanRepaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LoanRepaymentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            loan = request.user.loans.filter(is_active=True, disbursed=True).first()

            if not loan:
                return Response({'error': 'No active loan found for the user'}, status=status.HTTP_400_BAD_REQUEST)

            amount_paid = serializer.validated_data['amount_paid']  # Correct field name
            loan.make_repayment(amount_paid)

            return Response({'success': 'Loan repayment successful', 'repayment_amount': amount_paid}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, loan_id, *args, **kwargs):
        loan = Loan.objects.filter(user=request.user, id=loan_id).first()

        if not loan:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LoanSerializer(loan)
        return Response(serializer.data)