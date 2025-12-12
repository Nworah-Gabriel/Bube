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
from .models import Project
import cloudinary.uploader


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


# views.py
import json
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Project
from django.views import View

class CreateProject(TemplateView):
    template_name = "Admin/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("id")

        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                context["project"] = project
                # Pass project data as JSON for JavaScript
                context["project_data"] = {
                    "id": str(project.id),
                    "title": project.title,
                    "owners": project.owners,
                    "date": project.date.strftime("%Y-%m-%d") if project.date else "",
                    "content": project.content,
                    "featured_image": project.featured_image,
                    "gallery_image": project.gallery_image,
                    "status": project.status,
                    "project_category": project.project_category
                }
            except Project.DoesNotExist:
                pass

        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON data
            data = json.loads(request.body)

            # Get or create project
            project_id = data.get("id")
            if project_id:
                project = get_object_or_404(Project, id=project_id)
            else:
                project = Project()

            # Update fields
            project.title = data.get("title", "")
            project.owners = data.get("owners", "")
            project.date = data.get("date", "")
            project.content = data.get("content", "")
            project.status = data.get("status", "draft")

            # Handle Base64 images
            featured_image_base64 = data.get("featuredImage")
            gallery_image_base64 = data.get(
                "galleryImage"
            )  # Changed from galleryImages

            if featured_image_base64 and featured_image_base64.startswith("data:image"):
                # Upload to Cloudinary
                project.featured_image = Project.upload_base64_image(
                    featured_image_base64, folder="projects/featured/"
                )

            if gallery_image_base64 and gallery_image_base64.startswith("data:image"):
                # Upload to Cloudinary
                project.gallery_image = Project.upload_base64_image(
                    gallery_image_base64, folder="projects/gallery/"
                )

            project.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": f"Project {'updated' if project_id else 'created'} successfully!",
                    "project": {
                        "id": str(project.id),
                        "title": project.title,
                        "featured_image": project.featured_image,
                        "gallery_image": project.gallery_image,
                    },
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ProjectAPIView(View):
    """API view for handling project CRUD operations"""
    
    def post(self, request, *args, **kwargs):
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
                    project.date = None
            else:
                project.date = None
            
            project.content = data.get('content', '')
            project.status = data.get('status', 'draft')
            
            # Handle Base64 images
            featured_image_base64 = data.get('featuredImage')
            gallery_image_base64 = data.get('galleryImage')
            
            if featured_image_base64 and featured_image_base64.startswith('data:image'):
                try:
                    project.featured_image = Project.upload_base64_image(
                        featured_image_base64, 
                        folder="projects/featured/"
                    )
                except Exception as e:
                    print(f"Error uploading featured image: {e}")
            
            if gallery_image_base64 and gallery_image_base64.startswith('data:image'):
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
