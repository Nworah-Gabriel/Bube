from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.http import HttpResponse
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
    template_name = "Website/index.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): 
        ...
        
class ProjectCategory(TemplateView):
    template_name = "Website/project-category.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class ProcessOptimization(TemplateView):
    template_name = "Website/⁠Process-optimization.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...
    
class ProcessOptimizationDetails(TemplateView):
    template_name = "Website/process-optimization-detail.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)

    def post(self, request, ref_email, ref_username): ...


class About(TemplateView):
    template_name = "Website/about.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)



class SKills(TemplateView):
    template_name = "Website/skills.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)



class Certifications(TemplateView):
    template_name = "Website/certifications.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)
    


class Research(TemplateView):
    template_name = "Website/research.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)
    
class DataAnalysisDetail(TemplateView):
    template_name = "Website/data-analytics-projects.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)
    

   
class DataAnalysis(TemplateView):
    template_name = "Website/data-analytics.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)



class DesignEngineering(TemplateView):
    template_name = "Website/design-engineering.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)
    


class DesignEngineeringDetail(TemplateView):
    template_name = "Website/design-engineering-project-detail.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)
    
