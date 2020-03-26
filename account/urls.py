from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('activate/<uid>/<token>/', account_activate, name='account-activation')
]