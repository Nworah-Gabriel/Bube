from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import User
from django.contrib.auth.models import User as theUSer

# from .forms import UserForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.urls import reverse
from sqlite3 import IntegrityError

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.template.loader import get_template, render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

# modules for mailing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class HomeView(TemplateView):
    template_name = "Admin/project-dashboard.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class CreateProject(TemplateView):
    template_name = "Admin/editor.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class CertificateList(TemplateView):
    template_name = "Admin/cert-list.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class CreateResearch(TemplateView):
    template_name = "Admin/research-create.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class ResearchList(TemplateView):
    template_name = "Admin/research-list.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class Preview(TemplateView):
    template_name = "Admin/preview.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class CertificateUpload(TemplateView):
    template_name = "Admin/cert-upload.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...
