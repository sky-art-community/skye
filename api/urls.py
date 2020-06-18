from django.urls import path
from .views import *

urlpatterns = [
    path('', status),
    path('connect', api),
    path('image_test', images_test)
]