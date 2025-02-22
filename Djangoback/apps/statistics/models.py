# D:\Workspace\ElectricVehicleService\Djangoback\apps\statistics\models.py
from django.db import models
from django.conf import settings  # 统一使用配置引用

class UserStatistics(models.Model):
    """用户行为统计模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 标准化用户模型引用
        on_delete=models.CASCADE,
        verbose_name='关联用户'
    )
    login_count = models.PositiveIntegerField(
        default=0,
        verbose_name='登录次数'
    )
    service_usage = models.JSONField(
        default=dict,
        verbose_name='服务使用统计'
    )
    last_active = models.DateTimeField(
        auto_now=True,
        verbose_name='最后活跃时间'
    )

    class Meta:
        verbose_name = '用户统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.phone} 使用统计"
