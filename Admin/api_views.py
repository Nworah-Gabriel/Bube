# api_views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Project

@csrf_exempt
def create_project_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get or create project
            project_id = data.get('id')
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
            project.date = data.get('date', '')
            project.content = data.get('content', '')
            project.status = data.get('status', 'draft')
            
            # Handle Base64 images
            featured_image_base64 = data.get('featuredImage')
            gallery_image_base64 = data.get('galleryImage')
            
            if featured_image_base64 and featured_image_base64.startswith('data:image'):
                project.featured_image = Project.upload_base64_image(
                    featured_image_base64, 
                    folder="projects/featured/"
                )
            
            if gallery_image_base64 and gallery_image_base64.startswith('data:image'):
                project.gallery_image = Project.upload_base64_image(
                    gallery_image_base64,
                    folder="projects/gallery/"
                )
            
            project.save()
            
            return JsonResponse({
                'success': True,
                'message': f"Project {'updated' if project_id else 'created'} successfully!",
                'project': {
                    'id': str(project.id),
                    'title': project.title,
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)