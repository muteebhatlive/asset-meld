from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('nasdaq/<str:asset>/', get_nasdaq_ticker, name='get_nasdaq_ticker'),
    path('nse/<str:asset>/', get_nse_ticker, name='get_nse_ticker'),
    # path('crypto/<str:asset>/', get_crypto_ticker, name='get_crypto_ticker'),
    path('crypto/create/', add_crypto, name='create-crypto'),
    
]