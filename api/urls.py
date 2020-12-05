from django.urls import path
from .views import status, api, images_test

urlpatterns = [path("", status), path("connect", api), path("image_test", images_test)]
