from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChargingStationViewSet

# 创建子路由实例
charging_router = DefaultRouter()
charging_router.register(r'stations', ChargingStationViewSet, basename='charging-station')

urlpatterns = [
    path('', include(charging_router.urls)),
]
