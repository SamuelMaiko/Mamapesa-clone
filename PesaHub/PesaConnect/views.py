

"""
API Views for Mamapesa-backend

These views define the endpoints and logic for handling API requests.

Usage:
    These views are used within Django REST Framework to define API endpoints and handle requests.

Overview:
    - custom_user_list_create: API endpoint for listing or creating CustomUser instances.
    - custom_user_detail: API endpoint for retrieving, updating, or deleting a specific CustomUser instance.
    - trust_score_list_create: API endpoint for listing or creating TrustScore instances.
    - trust_score_detail: API endpoint for retrieving, updating, or deleting a specific TrustScore instance.
    - savings_list_create: API endpoint for listing or creating Savings instances.
    - savings_detail: API endpoint for retrieving, updating, or deleting a specific Savings instance.
    - transaction_list_create: API endpoint for listing or creating Transaction instances.
    - transaction_detail: API endpoint for retrieving, updating, or deleting a specific Transaction instance.
    - item_list_create: API endpoint for listing or creating Item instances.
    - item_detail: API endpoint for retrieving, updating, or deleting a specific Item instance.
    - loan_list_create: API endpoint for listing or creating Loan instances.
    - loan_detail: API endpoint for retrieving, updating, or deleting a specific Loan instance.
    - loan_item_list_create: API endpoint for listing or creating LoanItem instances.
    - loan_item_detail: API endpoint for retrieving, updating, or deleting a specific LoanItem instance.
    - savings_item_list_create: API endpoint for listing or creating SavingsItem instances.
    - savings_item_detail: API endpoint for retrieving, updating, or deleting a specific SavingsItem instance.
    - withdrawal_list_create: API endpoint for listing or creating Withdrawal instances.
    - withdrawal_detail: API endpoint for retrieving, updating, or deleting a specific Withdrawal instance.
    - user_details_list_create: API endpoint for listing or creating UserDetails instances.
    - user_details_detail: API endpoint for retrieving, updating, or deleting a specific UserDetails instance.
    - savings_payment_list_create: API endpoint for listing or creating SavingsPayment instances.
    - savings_payment_detail: API endpoint for retrieving, updating, or deleting a specific SavingsPayment instance.

Each view function corresponds to a specific HTTP method (GET, POST, PUT, DELETE) and performs appropriate actions on the associated model instances.

For more information on Django REST Framework views, refer to the official documentation: https://www.django-rest-framework.org/api-guide/views/

"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import CustomUser, TrustScore, Savings, Loan, Item, LoanItem, Transaction, SavingsItem, Withdrawal, UserDetails, SavingsPayment
from .serializers import CustomUserSerializer, TrustScoreSerializer, SavingsSerializer, LoanSerializer, ItemSerializer, LoanItemSerializer, TransactionSerializer, SavingsItemSerializer, WithdrawalSerializer, UserDetailsSerializer, SavingsPaymentSerializer
@api_view(['GET', 'POST'])
def custom_user_list_create(request):
    if request.method == 'GET':
        custom_users = CustomUser.objects.all()
        serializer = CustomUserSerializer(custom_users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def custom_user_detail(request, pk):
    custom_user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'GET':
        serializer = CustomUserSerializer(custom_user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(custom_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        custom_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def trust_score_list_create(request):
    if request.method == 'GET':
        trust_scores = TrustScore.objects.all()
        serializer = TrustScoreSerializer(trust_scores, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TrustScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def trust_score_detail(request, pk):
    trust_score = get_object_or_404(TrustScore, pk=pk)
    if request.method == 'GET':
        serializer = TrustScoreSerializer(trust_score)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TrustScoreSerializer(trust_score, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        trust_score.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def savings_list_create(request):
    if request.method == 'GET':
        savings = Savings.objects.all()
        serializer = SavingsSerializer(savings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SavingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def savings_detail(request, pk):
    savings = get_object_or_404(Savings, pk=pk)
    if request.method == 'GET':
        serializer = SavingsSerializer(savings)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SavingsSerializer(savings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        savings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def transaction_list_create(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def item_list_create(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def loan_list_create(request):
    if request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'GET':
        serializer = LoanSerializer(loan)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def loan_item_list_create(request):
    if request.method == 'GET':
        loan_items = LoanItem.objects.all()
        serializer = LoanItemSerializer(loan_items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LoanItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def loan_item_detail(request, pk):
    loan_item = get_object_or_404(LoanItem, pk=pk)
    if request.method == 'GET':
        serializer = LoanItemSerializer(loan_item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LoanItemSerializer(loan_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        loan_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def savings_item_list_create(request):
    if request.method == 'GET':
        savings_items = SavingsItem.objects.all()
        serializer = SavingsItemSerializer(savings_items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SavingsItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def savings_item_detail(request, pk):
    savings_item = get_object_or_404(SavingsItem, pk=pk)
    if request.method == 'GET':
        serializer = SavingsItemSerializer(savings_item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SavingsItemSerializer(savings_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        savings_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def withdrawal_list_create(request):
    if request.method == 'GET':
        withdrawals = Withdrawal.objects.all()
        serializer = WithdrawalSerializer(withdrawals, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def withdrawal_detail(request, pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    if request.method == 'GET':
        serializer = WithdrawalSerializer(withdrawal)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WithdrawalSerializer(withdrawal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        withdrawal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def user_details_list_create(request):
    if request.method == 'GET':
        user_details = UserDetails.objects.all()
        serializer = UserDetailsSerializer(user_details, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_details_detail(request, pk):
    user_details = get_object_or_404(UserDetails, pk=pk)
    if request.method == 'GET':
        serializer = UserDetailsSerializer(user_details)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserDetailsSerializer(user_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def savings_payment_list_create(request):
    if request.method == 'GET':
        savings_payments = SavingsPayment.objects.all()
        serializer = SavingsPaymentSerializer(savings_payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SavingsPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def savings_payment_detail(request, pk):
    savings_payment = get_object_or_404(SavingsPayment, pk=pk)
    if request.method == 'GET':
        serializer = SavingsPaymentSerializer(savings_payment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SavingsPaymentSerializer(savings_payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        savings_payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
