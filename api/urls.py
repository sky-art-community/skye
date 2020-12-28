from django.urls import path
from django.conf import settings
from .views import status, api, images_test, controller_view


urlpatterns = [
    path("", status), path("connect", api),
    path("image_test", images_test),
]


if settings.DEBUG:
    urlpatterns += [
        path("test/<str:command>", controller_view)
    ]
