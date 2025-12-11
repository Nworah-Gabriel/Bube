import base64
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils.timezone import now
from .managers import CustomUserManager
from cryptography.fernet import Fernet, InvalidToken
from uuid import uuid4
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # user details
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    verification_code = models.CharField(max_length=10, null=True, blank=True)
    is_password_changed = models.BooleanField(default=False)
    kyc_status = models.CharField(max_length=20, default="unverified", help_text="unverified, verified, pending")
    is_activated = models.BooleanField(default=False)
    profile_photo = models.CharField(max_length=300, default="")
    gender = models.CharField(max_length=245, default="male", blank=True, null=True)
    status = models.CharField(max_length=256, default="pending", blank=True, null=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    Designation = models.CharField(max_length=50, null=True, blank=True)
    
    # user role
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    admin_role = models.CharField(max_length=200, null=True, blank=True)

    # user status
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(null=True, blank=True)

    fcm_token = models.CharField(max_length=256, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # ADMIN AUTH CODE STORAGE
    admin_auth_code = models.IntegerField(null=True, blank=True)
    admin_auth_code_expiry = models.DateTimeField(null=True, blank=True)
    

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.first_name} - {self.last_name}"

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)