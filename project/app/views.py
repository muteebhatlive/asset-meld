from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework import status
import requests
# Create your views here.



@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists.'}, status=400)

            # Create a new user
            serializer.save()
            return JsonResponse({'message': 'User registered successfully.'}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)






@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'message': 'Login successful.'})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

# def get_nse_ticker(request, asset_name):
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_nasdaq_ticker(request, asset):
    print(asset)
    response = requests.get("https://api.twelvedata.com/time_series?apikey=04ed091e9cac49aead575a1d1e1a3aa8&interval=1min&symbol={asset}&type=stock&format=JSON&exchange=NASDAQ&outputsize=1")
    return Response(response)
    