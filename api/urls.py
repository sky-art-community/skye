from django.urls import path
from .views import *

urlpatterns = [
    path('', status),
    path('test', test),
    path('connect', api),
]