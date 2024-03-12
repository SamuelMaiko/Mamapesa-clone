from rest_framework import serializers
from newmamapesa.models import CustomUser
from django.contrib.auth import authenticate
from newmamapesa.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=10, write_only=True, required=True)
    first_name = serializers.CharField(max_length=15, required=True)
    last_name = serializers.CharField(max_length=15, required=True)

    def create(self, validated_data):
        user=CustomUser.objects.create_user(**validated_data)
        return user
    class Meta: 
        model = CustomUser
        fields = ['phone_number','email', 'password', "first_name", "last_name"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    