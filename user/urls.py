from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from user.views import CreateUser

urlpatterns = [
    path('api/register-user/', csrf_exempt(CreateUser.as_view()), name='create_user'),
]
