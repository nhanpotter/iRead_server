from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('activate/<uid>/<token>/', account_activate, name='account-activation'),
    path('create/', AccountCreateAPIView.as_view(), name="sign-up"),
    path('password/reset/<uid>/<token>/', reset_password, name='reset-password'),
]