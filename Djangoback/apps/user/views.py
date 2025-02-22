import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken


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
            # JWT生成
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'status': 'success',
                'message': '登录成功',
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return JsonResponse({'status': 'error', 'message': '账号或密码错误'})


@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'User logged out successfully'})


@csrf_exempt
def update_user_info(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        user = request.user
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User info updated successfully'})


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Password reset successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Old password is incorrect'})


# 登录检查接口
def check_user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({
                'status': 'success',
                'isLoggedIn': True,
                'username': request.user.username
            })
        else:
            return JsonResponse({
                'status': 'success',
                'isLoggedIn': False
            })
