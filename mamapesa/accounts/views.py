from django.shortcuts import render
from rest_framework.decorators import api_view
from . serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data = request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Account has been Succesfully created'
            data['username'] = account.username
            data['email'] = account.email

            token, created = Token.objects.get_or_create(user=account)
            data['token'] = token.key
        else:
            data = serializer.errors

        return Response(data)    

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            # Token already exists, no need to create a new one
            # You can handle this situation if needed
            pass

        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)    

