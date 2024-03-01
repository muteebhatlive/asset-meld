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
from rest_framework_simplejwt.tokens import RefreshToken

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






# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({'message': 'Login successful.'})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful.',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET'])
def get_nse_ticker(request, asset):
    
    pass

@api_view(['GET'])
def get_crypto_ticker(request, asset):
    print(asset)
    url = f'https://api.twelvedata.com/time_series?apikey=04ed091e9cac49aead575a1d1e1a3aa8&interval=1min&symbol={asset}/USD&outputsize=1&format=JSON'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if 'values' in data and data['values']:
            close_price = data['values'][0]['close']
            return Response({'close_price': close_price})
        else:
            return Response({'error': 'No data available for the given asset symbol.'}, status=404)
    else:
        return Response({'error': 'Failed to fetch data from the API.'}, status=response.status_code)

    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_nasdaq_ticker(request, asset):
    print(asset)
    url = f'https://api.twelvedata.com/time_series?apikey=04ed091e9cac49aead575a1d1e1a3aa8&interval=1min&exchange=NASDAQ&outputsize=1&symbol={asset}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'values' in data and data['values']:
            close_price = data['values'][0]['close']
            return Response({'close_price': close_price})
        else:
            return Response({'error': 'No data available for the given asset symbol.'}, status=404)
    else:
        return Response({'error': 'Failed to fetch data from the API.'}, status=response.status_code)
    
@api_view(['POST'])
def add_crypto(request):
    if request.method == 'POST':
        serializer = CryptoSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve the authenticated user from the request
            user = request.user
            print(user)
            print('1')
            # Assign the user to the serializer's validated data
            serializer.validated_data['user'] = user
            print('1')
            print(user.id)
            # Save the serializer instance to create the Crypto object
            serializer.save()
            # Return a success response with the created data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return a bad request response if the serializer data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    