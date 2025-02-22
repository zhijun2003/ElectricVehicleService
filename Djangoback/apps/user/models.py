from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # 用户类型选项
    class UserType(models.TextChoices):
        CUSTOMER = 'CU', _('普通用户')
        ADMIN = 'AD', _('系统管理员')
        TECH = 'TE', _('维修技师')
        MAINT = 'MA', _('设备维护员')

    # 基础字段扩展
    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.CUSTOMER,
        verbose_name='用户类型'
    )
    department = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='所属部门'
    )

    # 权限字段重定义
    is_admin = models.BooleanField(
        default=False,
        verbose_name='超级管理员',
        help_text='拥有所有权限的超级管理员'
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['user_type']),
        ]

    def save(self, *args, **kwargs):
        """自动同步权限字段"""
        if self.user_type == self.UserType.ADMIN:
            self.is_staff = True
            self.is_admin = True
        elif self.user_type in [self.UserType.TECH, self.UserType.MAINT]:
            self.is_staff = True
        super().save(*args, **kwargs)

# 员工扩展信息模型
class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='工号'
    )
    certification = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='资质证书'
    )
    work_schedule = models.JSONField(
        default=dict,
        verbose_name='排班表'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.get_user_type_display()})"
