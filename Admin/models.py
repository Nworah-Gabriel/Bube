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
import base64
from io import BytesIO
from django.core.files.base import ContentFile
import cloudinary.uploader

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
    kyc_status = models.CharField(
        max_length=20, default="unverified", help_text="unverified, verified, pending"
    )
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


class Project(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    
    CATEGORY_CHOICES = [
        ("Design Engineering", "Design Engineering"),
        ("Data Analysis", "Data Analysis"),
        ("Process Optimization", "Process Optimization")
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    owners = models.CharField(max_length=500, blank=True)
    date = models.DateField()
    content = models.TextField()
    project_category = models.TextField(max_length=300, choices=CATEGORY_CHOICES, default="Design Engineering")
    featured_image = models.URLField(blank=True, null=True)
    gallery_image = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    @classmethod
    def upload_base64_image(cls, base64_string, folder="projects/"):
        """Upload base64 image to Cloudinary and return URL"""
        try:
            if base64_string.startswith("data:image"):
                # Extract the base64 data
                format, imgstr = base64_string.split(";base64,")
                ext = format.split("/")[-1]

                # Decode base64
                data = base64.b64decode(imgstr)

                # Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    ContentFile(data, name=f"temp.{ext}"),
                    folder=folder,
                    resource_type="image",
                )
                return upload_result["secure_url"]
        except Exception as e:
            print(f"Error uploading image: {e}")
        return None



class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    issuer = models.CharField(max_length=255, blank=True)
    issue_date = models.DateField(blank=True, null=True)
    certificate_image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.issuer}" if self.title else f"Certificate {self.id}"
    
    @classmethod
    def upload_base64_certificate(cls, base64_string, folder="certificates/"):
        """Upload base64 image to Cloudinary and return URL"""
        try:
            if base64_string.startswith("data:image"):
                # Extract the base64 data
                format, imgstr = base64_string.split(";base64,")
                ext = format.split("/")[-1]

                # Decode base64
                data = base64.b64decode(imgstr)

                # Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    ContentFile(data, name=f"certificate.{ext}"),
                    folder=folder,
                    resource_type="image",
                )
                return upload_result["secure_url"]
        except Exception as e:
            print(f"Error uploading certificate: {e}")
        return None