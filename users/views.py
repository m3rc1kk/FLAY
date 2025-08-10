import hmac
import hashlib
import time
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView

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


from django.http import HttpResponse

def telegram_auth(request):
    data = request.GET.dict()
    print("Telegram data:", data)

    if 'hash' not in data:
        return HttpResponse("Ошибка: отсутствует hash", status=400)

    if not check_telegram_auth(data):
        return HttpResponse("Ошибка: подпись не совпадает", status=400)

    telegram_id = data['id']
    username = data.get('username', f"user_{telegram_id}")

    user, created = User.objects.get_or_create(
        username=username,
        defaults={'first_name': data.get('first_name', ''), 'last_name': data.get('last_name', '')}
    )
    login(request, user)
    print(f"User {'создан' if created else 'найден'} и залогинен: {user}")

    return redirect('index')  # Или в существующий URL

