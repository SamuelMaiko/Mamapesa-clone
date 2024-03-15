from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from newmamapesa.models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from mamapesa.settings import EMAIL_HOST_USER

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class LoginWithToken(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number=request.data.get('phone_number')
        password=request.data.get('password')
        user=authenticate(request, phone_number=phone_number, password=password)
        # if user exists in db = correct credentials
        if user is not None:
            login(request, user)
            # getting user token 
            token, created_token=Token.objects.get_or_create(user=user)
            user_instance=get_object_or_404(CustomUser, phone_number=phone_number)
            serializer=UserSerializer(user_instance)
            
            response_dict={"user":serializer.data}
            # using an existing token
            if token:
                response_dict["token"]=token.key
            # using a created token if not existed before  
            elif created_token:
                response_dict["token"]=created_token.key
            return JsonResponse(response_dict, status=status.HTTP_200_OK)
        # If user returns NONE = wrong credentials
        else:
            response_dict={"error": "Invalid phone number or password"}
            return JsonResponse(response_dict, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        id_number=request.data.get("id_number")
        if not id_number:
            response_dict=dict(error="id_number is required")
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
        if len(id_number)!=8:
            response_dict=dict(error="id_number length should be 8")
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
            
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            response_dict = { 
                'message': 'Account has been successfully created',
                "user":serializer.data
                # 'username': account.username,
                # 'email': account.email,
            }
            user.customer.id_number=id_number
            user.customer.save()

            return Response(response_dict, status=status.HTTP_201_CREATED)
        else:
            data = {
                'error': 'Invalid data',
                'errors': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        response_dict=dict(message="User logged out successfully")
        return Response(response_dict, status=status.HTTP_200_OK)
    
class PasswordReset(APIView):
    def post(self, request):
        phone_number=request.data.get("phone_number")

        if not phone_number:
            response_dict=dict(error="Phone number is  required")
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            response_dict=dict(error="User with this phone number does not exist")
            return Response(response_dict, status=status.HTTP_404_NOT_FOUND)
        
        token=default_token_generator.make_token(user)
        
        
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        domain=get_current_site(request).domain
        
        context={
                    'user':user,
                    'domain':domain,
                    'token':token,
                    'uid':uid,
                }
        subject="Mamapesa Password Reset"        
        message=render_to_string('accounts/password_reset_email.html', context) 
        sender=EMAIL_HOST_USER
        recipient_list=[user.email]
        
        email=EmailMessage(subject, message, sender, recipient_list)
        email.fail_silently=True
        email.send()
        
        response_dict=dict(message="Password reset email sent")
        return Response(response_dict, status=status.HTTP_200_OK)
        
def AccountActivation(request, uid,token):
    user_id=force_str(urlsafe_base64_decode(uid))
    specific_user=get_object_or_404(CustomUser, pk=int(user_id))
    
    
    # try:
    #     user=CustomUser.objects.get(pk=uid)
    # except CustomUser.DoesNotExist:
    #     print("User non_existent")
    #     return 0
    
    
    
    context={
        
    }
    
    return render(request, 'accounts/password-reset.html', context)
    
