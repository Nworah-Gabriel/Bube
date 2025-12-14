from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from django.contrib.auth.models import User as theUSer

from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from Admin.models import Certificate, Project
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render

def custom_404(request, exception=None):
    return render(request, 'Website/404.html', status=404)

def custom_500(request, exception=None):
    return render(request, 'Website/500.html', status=500)

def custom_403(request, exception=None):
    return render(request, 'Website/401.html', status=403)

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all certificates ordered by date
        certificates = Certificate.objects.all().order_by('-issue_date', '-created_at')
        context['certificates'] = certificates
        return context



class Research(TemplateView):
    template_name = "Website/research.html"
    new_user = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Additional logic for handling GET requests
        return super().get(request, *args, **kwargs)



class DataAnalysis(TemplateView):
    template_name = "Website/data-analytics.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get only published projects with Data Analysis category
        projects = Project.objects.filter(
            status='published',
            project_category='Data Analysis'
        ).order_by('-date')
        
        # Optional search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(owners__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(projects, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'projects': page_obj,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
            'paginator': paginator,
            'total_projects': projects.count(),
        })
        
        return context


class DataAnalysisDetail(DetailView):
    template_name = "Website/data-analytics-projects.html"
    model = Project
    context_object_name = 'project'
    
    def get_object(self):
        # Get the project by UUID, only if published
        return get_object_or_404(
            Project, 
            id=self.kwargs['id'],
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        
        # Get 2 related projects from the same category (excluding current project)
        related_projects = Project.objects.filter(
            status='published',
            project_category=project.project_category
        ).exclude(id=project.id).order_by('-date')[:2]
        
        # If not enough related projects in same category, get from any category
        if related_projects.count() < 2:
            additional_needed = 2 - related_projects.count()
            additional_projects = Project.objects.filter(
                status='published'
            ).exclude(
                id__in=[p.id for p in related_projects] + [project.id]
            ).order_by('-date')[:additional_needed]
            
            # Combine the querysets
            from itertools import chain
            related_projects = list(chain(related_projects, additional_projects))
        
        context['related_projects'] = related_projects
        return context
class DesignEngineering(TemplateView):
    template_name = "Website/design-engineering.html"
    paginate_by = 6  # Number of projects per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get only published projects with Design Engineering category
        projects = Project.objects.filter(
            status='published',
            project_category='Design Engineering'
        ).order_by('-date')  # Show newest first
        
        # Optional: Add search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(owners__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(projects, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'projects': page_obj,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
            'paginator': paginator,
            'total_projects': projects.count(),
        })
        
        return context

class DesignEngineeringDetail(DetailView):
    template_name = "Website/design-engineering-project-detail.html"
    model = Project
    context_object_name = 'project'
    
    def get_object(self):
        # Get the project by UUID, only if published
        return get_object_or_404(
            Project, 
            id=self.kwargs['id'],
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        
        related_projects = Project.objects.filter(
            status='published',
            project_category=project.project_category
        ).exclude(id=project.id).order_by('-date')[:2]
        
        
        if related_projects.count() < 2:
            additional_needed = 2 - related_projects.count()
            additional_projects = Project.objects.filter(
                status='published'
            ).exclude(
                id__in=[p.id for p in related_projects] + [project.id]
            ).order_by('-date')[:additional_needed]
            
            # Combine the querysets
            from itertools import chain
            related_projects = list(chain(related_projects, additional_projects))
        
        context['related_projects'] = related_projects
        return context
    



class ProcessOptimization(TemplateView):
    template_name = "Website/⁠Process-optimization.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get only published projects with Process Optimization category
        projects = Project.objects.filter(
            status='published',
            project_category='Process Optimization'
        ).order_by('-date')
        
        # Optional search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(owners__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(projects, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'projects': page_obj,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
            'paginator': paginator,
            'total_projects': projects.count(),
        })
        
        return context


class ProcessOptimizationDetails(DetailView):
    template_name = "Website/process-optimization-detail.html"
    model = Project
    context_object_name = 'project'
    
    def get_object(self):
        # Get the project by UUID, only if published
        return get_object_or_404(
            Project, 
            id=self.kwargs['id'],
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        
       
        related_projects = Project.objects.filter(
            status='published',
            project_category=project.project_category
        ).exclude(id=project.id).order_by('-date')[:2]
        
        if related_projects.count() < 2:
            additional_needed = 2 - related_projects.count()
            additional_projects = Project.objects.filter(
                status='published'
            ).exclude(
                id__in=[p.id for p in related_projects] + [project.id]
            ).order_by('-date')[:additional_needed]
            
            from itertools import chain
            related_projects = list(chain(related_projects, additional_projects))
        
        context['related_projects'] = related_projects
        return context