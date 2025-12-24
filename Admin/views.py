from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User as theUSer

# from .forms import UserForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Research,Project, Certificate
import cloudinary.uploader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

# ============== RESEARCH VIEWS ==============

class ResearchListView(ListView):
    """View for listing all research articles"""
    model = Research
    template_name = "Website/research.html"
    context_object_name = 'research_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Research.objects.filter(status='published').order_by('-publication_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured research
        featured_research = Research.objects.filter(
            status='published', 
            is_featured=True
        ).order_by('-publication_date')[:3]
        
        context['featured_research'] = featured_research
        
        # Group by type for filtering
        research_types = Research.TYPE_CHOICES
        context['research_types'] = research_types
        
        # Get filter parameters
        research_type = self.request.GET.get('type', '')
        year = self.request.GET.get('year', '')
        
        if research_type:
            context['current_type'] = research_type
        if year:
            context['current_year'] = year
            
        return context

class ResearchCreateView(TemplateView):
    """View for creating new research"""
    template_name = "Admin/research-create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['research'] = None
        context['research_types'] = Research.TYPE_CHOICES
        return context

class ResearchEditView(TemplateView):
    """View for editing existing research"""
    template_name = "Admin/research-create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        research_id = self.kwargs.get('id')
        
        if research_id:
            try:
                research = Research.objects.get(id=research_id)
                context['research'] = research
            except Research.DoesNotExist:
                context['research'] = None
        
        context['research_types'] = Research.TYPE_CHOICES
        return context

class ResearchListViewAdmin(TemplateView):
    """Admin view for listing all research"""
    template_name = "Admin/research-list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters
        status_filter = self.request.GET.get('status', '')
        type_filter = self.request.GET.get('type', '')
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', '-publication_date')
        
        # Get stats
        total_count = Research.objects.count()
        published_count = Research.objects.filter(status='published').count()
        draft_count = Research.objects.filter(status='draft').count()
        archived_count = Research.objects.filter(status='archived').count()
        featured_count = Research.objects.filter(is_featured=True).count()
        
        # Get recent research for menu
        recent_research = Research.objects.all().order_by('-created_at')[:5]
        
        # Base querysets
        published_research = Research.objects.filter(status='published')
        draft_research = Research.objects.filter(status='draft')
        archived_research = Research.objects.filter(status='archived')
        
        # Apply search
        if search_query:
            published_research = published_research.filter(
                models.Q(title__icontains=search_query) |
                models.Q(abstract__icontains=search_query) |
                models.Q(authors__icontains=search_query) |
                models.Q(keywords__icontains=search_query)
            )
            draft_research = draft_research.filter(
                models.Q(title__icontains=search_query) |
                models.Q(abstract__icontains=search_query) |
                models.Q(authors__icontains=search_query) |
                models.Q(keywords__icontains=search_query)
            )
            archived_research = archived_research.filter(
                models.Q(title__icontains=search_query) |
                models.Q(abstract__icontains=search_query) |
                models.Q(authors__icontains=search_query) |
                models.Q(keywords__icontains=search_query)
            )
        
        # Apply type filter
        if type_filter:
            published_research = published_research.filter(research_type=type_filter)
            draft_research = draft_research.filter(research_type=type_filter)
            archived_research = archived_research.filter(research_type=type_filter)
        
        # Apply sorting
        published_research = published_research.order_by(sort_by)
        draft_research = draft_research.order_by(sort_by)
        archived_research = archived_research.order_by(sort_by)
        
        # Paginate
        published_page = self.request.GET.get('published_page', 1)
        draft_page = self.request.GET.get('draft_page', 1)
        archived_page = self.request.GET.get('archived_page', 1)
        
        published_paginator = Paginator(published_research, 10)
        draft_paginator = Paginator(draft_research, 10)
        archived_paginator = Paginator(archived_research, 10)
        
        try:
            published_research_page = published_paginator.page(published_page)
        except (PageNotAnInteger, EmptyPage):
            published_research_page = published_paginator.page(1)
        
        try:
            draft_research_page = draft_paginator.page(draft_page)
        except (PageNotAnInteger, EmptyPage):
            draft_research_page = draft_paginator.page(1)
        
        try:
            archived_research_page = archived_paginator.page(archived_page)
        except (PageNotAnInteger, EmptyPage):
            archived_research_page = archived_paginator.page(1)
        
        context.update({
            'published_research': published_research_page,
            'draft_research': draft_research_page,
            'archived_research': archived_research_page,
            'published_paginator': published_paginator,
            'draft_paginator': draft_paginator,
            'archived_paginator': archived_paginator,
            'research_types': Research.TYPE_CHOICES,
            'current_status': status_filter,
            'current_type': type_filter,
            'current_sort': sort_by,
            'current_search': search_query,
            'total_count': total_count,
            'published_count': published_count,
            'draft_count': draft_count,
            'archived_count': archived_count,
            'featured_count': featured_count,
            'recent_research': recent_research,
        })
        
        return context
# ============== RESEARCH API VIEWS ==============

@method_decorator(csrf_exempt, name='dispatch')
class CreateUpdateResearchView(TemplateView):
    """API view for creating/updating research"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            research_id = data.get('id')
            
            # Check if updating existing research
            if research_id:
                try:
                    research = Research.objects.get(id=research_id)
                except Research.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Research not found'
                    }, status=404)
            else:
                research = Research()
            
            # Update fields
            research.title = data.get('title', '')
            research.authors = data.get('authors', '')
            research.abstract = data.get('abstract', '')
            research.full_text = data.get('full_text', '')
            research.research_type = data.get('research_type', 'article')
            research.journal_name = data.get('journal_name', '')
            research.conference_name = data.get('conference_name', '')
            research.publisher = data.get('publisher', '')
            research.doi = data.get('doi', '')
            
            # Handle date
            pub_date = data.get('publication_date')
            if pub_date:
                research.publication_date = datetime.strptime(pub_date, '%Y-%m-%d')
            
            research.volume = data.get('volume', '')
            research.issue = data.get('issue', '')
            research.pages = data.get('pages', '')
            research.url = data.get('url', '')
            research.keywords = data.get('keywords', '')
            research.status = data.get('status', 'draft')
            research.is_featured = data.get('is_featured', False)
            
            # Handle image uploads
            thumbnail_image = data.get('thumbnail_image')
            if thumbnail_image and thumbnail_image.startswith('data:image'):
                thumbnail_url = Research.upload_base64_image(thumbnail_image)
                if thumbnail_url:
                    research.thumbnail_image = thumbnail_url
            
            featured_image = data.get('featured_image')
            if featured_image and featured_image.startswith('data:image'):
                featured_url = Research.upload_base64_image(featured_image, folder="research/featured/")
                if featured_url:
                    research.featured_image = featured_url
            
            # Handle PDF upload
            pdf_file = data.get('pdf_file')
            if pdf_file and pdf_file.startswith('data:application/pdf'):
                pdf_url = Research.upload_pdf(pdf_file)
                if pdf_url:
                    research.pdf_file = pdf_url
            
            research.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Research saved successfully',
                'research_id': str(research.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteResearchView(TemplateView):
    """API view for deleting research"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            research_id = data.get('id')
            
            if not research_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Research ID is required'
                }, status=400)
            
            try:
                research = Research.objects.get(id=research_id)
                research.delete()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Research deleted successfully'
                })
                
            except Research.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Research not found'
                }, status=404)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ToggleResearchStatusView(TemplateView):
    """API view for toggling research status"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            research_id = data.get('id')
            new_status = data.get('status')
            
            if not research_id or not new_status:
                return JsonResponse({
                    'success': False,
                    'error': 'Research ID and status are required'
                }, status=400)
            
            try:
                research = Research.objects.get(id=research_id)
                research.status = new_status
                
                if new_status == 'published' and not research.published_at:
                    research.published_at = datetime.now()
                
                research.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Research status updated to {new_status}',
                    'new_status': new_status
                })
                
            except Research.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Research not found'
                }, status=404)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ToggleFeaturedStatusView(TemplateView):
    """API view for toggling featured status"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            research_id = data.get('id')
            
            if not research_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Research ID is required'
                }, status=400)
            
            try:
                research = Research.objects.get(id=research_id)
                research.is_featured = not research.is_featured
                research.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Featured status toggled to {research.is_featured}',
                    'is_featured': research.is_featured
                })
                
            except Research.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Research not found'
                }, status=404)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

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
