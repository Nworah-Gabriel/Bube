from django.views.generic import TemplateView
from django.contrib.auth.models import User as theUSer

# from .forms import UserForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project, Certificate
import cloudinary.uploader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomeView(TemplateView):
    template_name = "Admin/project-dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get page number from request
        published_page = self.request.GET.get('published_page', 1)
        draft_page = self.request.GET.get('draft_page', 1)
        
        # Get all projects
        published_projects = Project.objects.filter(status='published').order_by('-created_at')
        draft_projects = Project.objects.filter(status='draft').order_by('-created_at')
        
        # Paginate published projects
        published_paginator = Paginator(published_projects, 6)
        try:
            published_projects_page = published_paginator.page(published_page)
        except PageNotAnInteger:
            published_projects_page = published_paginator.page(1)
        except EmptyPage:
            published_projects_page = published_paginator.page(published_paginator.num_pages)
        
        # Paginate draft projects
        draft_paginator = Paginator(draft_projects, 6)
        try:
            draft_projects_page = draft_paginator.page(draft_page)
        except PageNotAnInteger:
            draft_projects_page = draft_paginator.page(1)
        except EmptyPage:
            draft_projects_page = draft_paginator.page(draft_paginator.num_pages)
        
        context['published_projects'] = published_projects_page
        context['draft_projects'] = draft_projects_page
        context['published_paginator'] = published_paginator
        context['draft_paginator'] = draft_paginator
        
        return context

# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView
from .models import Project

class CreateProjectView(TemplateView):
    """View for creating a new project"""
    template_name = "Admin/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For create view, no project data needed
        context["project"] = None
        return context

class EditProjectView(TemplateView):
    """View for editing an existing project"""
    template_name = "Admin/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('id')
        
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                context["project"] = project
            except Project.DoesNotExist:
                context["project"] = None
        
        return context

@method_decorator(csrf_exempt, name='dispatch')
class ProjectAPIView(View):
    """API view for handling project CRUD operations"""
    
    def post(self, request, *args, **kwargs):
        """Handle project creation and updates"""
        try:
            data = json.loads(request.body)
            project_id = data.get('id')
            
            # Get or create project
            if project_id and project_id != 'null':
                try:
                    project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    project = Project()
            else:
                project = Project()
            
            # Update fields
            project.title = data.get('title', '')
            project.owners = data.get('owners', '')
            project.project_category = data.get('projectCategory', '')
            
            # Handle date field
            date_str = data.get('date', '')
            if date_str:
                from datetime import datetime
                try:
                    project.date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    project.date = datetime.strptime(datetime.now(), '%Y-%m-%d').date()
            else:
                project.date = None
            
            project.content = data.get('content', '')
            project.status = data.get('status', 'draft')
            
            # Handle Base64 images
            featured_image_base64 = data.get('featuredImage')
            gallery_image_base64 = data.get('galleryImage')
            
            # Handle featured image
            if data.get('removeFeatured'):
                project.featured_image = None
            elif featured_image_base64 and featured_image_base64.startswith('data:image'):
                try:
                    project.featured_image = Project.upload_base64_image(
                        featured_image_base64, 
                        folder="projects/featured/"
                    )
                except Exception as e:
                    print(f"Error uploading featured image: {e}")
            
            # Handle gallery image
            if data.get('removeGallery'):
                project.gallery_image = None
            elif gallery_image_base64 and gallery_image_base64.startswith('data:image'):
                try:
                    project.gallery_image = Project.upload_base64_image(
                        gallery_image_base64,
                        folder="projects/gallery/"
                    )
                except Exception as e:
                    print(f"Error uploading gallery image: {e}")
            
            project.save()
            
            return JsonResponse({
                'success': True,
                'message': f"Project {'updated' if project_id else 'created'} successfully!",
                'project': {
                    'id': str(project.id),
                    'title': project.title,
                    'status': project.status,
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    def delete(self, request, *args, **kwargs):
        """Handle project deletion"""
        try:
            project_id = kwargs.get('project_id') or request.GET.get('project_id')
            
            if not project_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Project ID is required'
                }, status=400)
            
            project = get_object_or_404(Project, id=project_id)
            project_title = project.title
            
            # Delete the project
            project.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Project "{project_title}" has been deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
class CertificateList(TemplateView):
    template_name = "Website/certifications.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all certificates ordered by date
        certificates = Certificate.objects.all().order_by('-issue_date', '-created_at')
        context['certificates'] = certificates
        return context


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get recent projects for menu
        context['recent_projects'] = Project.objects.filter(
            status='published'
        ).order_by('-created_at')[:6]
        return context

# API View for certificate upload
@method_decorator(csrf_exempt, name='dispatch')
class CertificateAPIView(TemplateView):
    """API view for handling certificate uploads"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            # Create new certificate
            certificate = Certificate()
            
            # Update fields
            certificate.title = data.get('title', '')
            certificate.issuer = data.get('issuer', '')
            certificate.description = data.get('description', '')
            
            # Handle date field
            date_str = data.get('issue_date', '')
            if date_str:
                from datetime import datetime
                try:
                    certificate.issue_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    certificate.issue_date = None
            else:
                certificate.issue_date = None
            
            # Handle Base64 certificate image
            certificate_base64 = data.get('certificate_image')
            
            if certificate_base64 and certificate_base64.startswith('data:image'):
                try:
                    certificate.certificate_image = Certificate.upload_base64_certificate(
                        certificate_base64, 
                        folder="certificates/"
                    )
                except Exception as e:
                    print(f"Error uploading certificate image: {e}")
            
            certificate.save()
            
            return JsonResponse({
                'success': True,
                'message': "Certificate uploaded successfully!",
                'certificate': {
                    'id': str(certificate.id),
                    'title': certificate.title,
                    'issuer': certificate.issuer,
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
