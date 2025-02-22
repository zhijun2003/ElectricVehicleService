from django.contrib import admin
from apps.user.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'is_admin', 'last_login')
    search_fields = ('phone',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')


# 注册到默认admin站点
admin.site.register(CustomUser, CustomUserAdmin)
