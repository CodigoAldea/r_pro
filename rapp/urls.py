from django.urls import path
from rapp.views import *

urlpatterns = [
    path("", home, name='home')
]
