
from django.urls import path, include
from .views import (
    encoder
    )

app_name = 'encoder'

urlpatterns = [
    path('', encoder, name='encoder'),
    
]