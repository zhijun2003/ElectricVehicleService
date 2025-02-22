
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 初始化路由
router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),

    # 包含视图集路由
    path('', include(router.urls)),
]