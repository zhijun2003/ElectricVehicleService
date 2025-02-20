from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'status': 'success', 'message': 'User registered successfully'})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'User logged in successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'User logged out successfully'})