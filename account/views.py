from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from requests_oauthlib import OAuth2Session
from server.settings import AUTH_API_URL

import requests
# Create your views here.

def account_activate(request, uid, token):
    url = AUTH_API_URL + 'users/activation/'
    kwargs = {
        'uid': uid,
        'token': token,
    }
    requests.post(url, data=kwargs)

    return HttpResponse('Activation Successful')