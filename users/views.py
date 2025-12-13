import hmac
import hashlib
import time
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import UserProfile
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

class LoginView(TemplateView):
    template_name = 'users/login.html'


def check_telegram_auth(data: dict) -> bool:
    auth_data = data.copy()
    hash_ = auth_data.pop('hash')
    sorted_data = sorted([f"{k}={v}" for k, v in auth_data.items()])
    data_check_string = '\n'.join(sorted_data)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == hash_

def telegram_auth(request):
    data = request.GET.dict()

    if 'hash' not in data:
        return HttpResponse("Ошибка: отсутствует hash", status=400)

    if not check_telegram_auth(data):
        return HttpResponse("Ошибка: подпись не совпадает", status=400)

    telegram_id = data['id']
    username = data.get('username', f"user_{telegram_id}")

    try:
        profile = UserProfile.objects.get(telegram_id=telegram_id)
        user = profile.user
    except UserProfile.DoesNotExist:
        user = User.objects.create(
            username=username,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        UserProfile.objects.create(user=user, telegram_id=telegram_id)

    login(request, user)
    return redirect('index')

