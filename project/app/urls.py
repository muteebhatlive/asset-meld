from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('nasdaq/<str:asset>/', get_nasdaq_ticker, name='get_nasdaq_ticker'),
    
]