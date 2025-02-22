from apps.charging.views import ChargingStationViewSet
# 导入视图
from apps.charging.views import get_charging_records
from apps.repair.views import submit_repair
from apps.user.views import profile
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 初始化路由
router = DefaultRouter()
router.register(r'api/stations', ChargingStationViewSet, basename='station')

urlpatterns = [
    path('admin/', admin.site.urls),

    # 基础API端点
    path('api/charging/records/', get_charging_records),
    path('api/repair/', submit_repair),
    path('api/user/', profile),

    # 包含视图集路由
    path('', include(router.urls)),
]