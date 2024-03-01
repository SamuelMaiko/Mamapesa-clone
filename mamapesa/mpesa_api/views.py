from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment

# Create your views here.
@csrf_exempt
def getAccessToken(request):
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

@csrf_exempt
def lipa_na_mpesa_online(stat):
    json_data = json.loads(stat.body.decode('utf-8'))
    phone_number = json_data.get('phone_number', '')
    amount = json_data.get('amount', '')
    print("Phone number:", phone_number)
    print("amount:", amount)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone_number,  # replace with your phone number to get stk push
        "CallBackURL": "https://mydomain.com/pth",
        "AccountReference": "MamaPesa",
        "TransactionDesc": "Testing",
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response)
    return HttpResponse('success')
    

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://79372821.ngrok.io/api/v1/c2b/confirmation",
               "ValidationURL": "https://79372821.ngrok.io/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    # Add your callback logic here if needed
    # For now, just return an empty HTTP response
    return HttpResponse( "https://mydomain.com/pth")


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

def home(request):
    return HttpResponse("Welcome to MamaPesa!")


@csrf_exempt
def confirmation(request):
    try:
        mpesa_body = request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)

        payment = MpesaPayment(
            first_name=mpesa_payment.get('FirstName', ''),
            last_name=mpesa_payment.get('LastName', ''),
            middle_name=mpesa_payment.get('MiddleName', ''),
            description=mpesa_payment.get('TransID', ''),
            phone_number=mpesa_payment.get('MSISDN', ''),
            amount=mpesa_payment.get('TransAmount', ''),
            reference=mpesa_payment.get('BillRefNumber', ''),
            organization_balance=mpesa_payment.get('OrgAccountBalance', ''),
            type=mpesa_payment.get('TransactionType', ''),
        )

        payment.save()

        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
