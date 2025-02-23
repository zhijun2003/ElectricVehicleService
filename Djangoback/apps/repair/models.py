# --------------- models.py ---------------
from django.conf import settings
from django.db import models


class RepairOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('in_progress', '维修中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='关联用户'
    )
    vehicle_model = models.CharField(max_length=100, verbose_name='车型')
    license_plate = models.CharField(max_length=20, verbose_name='车牌号')
    issue_description = models.TextField(verbose_name='问题描述')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='工单状态'
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='问题图片'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    assigned_staff = models.ForeignKey(
        'Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='负责人员'
    )

    def __str__(self):
        return f"{self.license_plate} - {self.get_status_display()}"

    class Meta:
        verbose_name = '维修工单'
        verbose_name_plural = '维修工单'
        ordering = ['-created_at']

class Staff(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    specialization = models.CharField(max_length=100, verbose_name='专业技能')
    work_schedule = models.JSONField(verbose_name='工作时间表', default=dict)

    def __str__(self):
        return self.user.phone
