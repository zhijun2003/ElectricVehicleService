from django.urls import path, include

urlpatterns = [
    path('api/charging/', include('apps.charging.urls')),
    path('api/repair/', include('apps.repair.urls')),
    path('api/statistics/', include('apps.statistics.urls')),
    path('api/user/', include('apps.user.urls')),
]
