# apps/user/models.py
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)
