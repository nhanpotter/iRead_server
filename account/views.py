from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from server.settings import BASE_SERVER_URL
from .forms import ResetPasswordForm
import requests
# Create your views here.

def account_activate(request, uid, token):
    url = BASE_SERVER_URL + 'auth/users/activation/'
    kwargs = {
        'uid': uid,
        'token': token,
    }
    requests.post(url, data=kwargs)

    return HttpResponse('Activation Successful')

class AccountCreateAPIView(APIView):
    def get(self, request, format=None):
        return Response("TODO")


def reset_password(request, uid, token):
    error = None
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            url = BASE_SERVER_URL + 'auth/users/reset_password_confirm'
            password = form.cleaned_data['password']
            kwargs = {
                'uid': uid,
                'token': token,
                'new_password': password,
            }
            req = requests.post(url, data=kwargs)
            if req.status_code == 400:
                error = req.json()
                form = ResetPasswordForm()
            return HttpResponse("Reset Password Sucessfully! Thank you")

    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {
        'form': form, 'error': error
    })
    
