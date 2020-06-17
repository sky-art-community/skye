from django.urls import path
from .views import *

urlpatterns = [
    path('', status),
    path('test', test),
    path('connect', api),
    path('image_test', images_test)
]