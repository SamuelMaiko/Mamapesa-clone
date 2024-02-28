from rest_framework import serializers
from newmamapesa.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=CustomUser
        fields=['username','email','phonenumber']