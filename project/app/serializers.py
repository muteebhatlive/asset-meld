from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ['asset_name','purchase_price', 'quantity_purchased']
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
