from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView, 
    CreateProjectView, 
    CertificateList, 
    CreateResearch, 
    ResearchList, 
    Preview, 
    CertificateUpload, 
    ProjectAPIView, 
    CertificateAPIView,
    EditProjectView,
    ResearchCreateView,
    ResearchEditView,
    ResearchListViewAdmin,
    CreateUpdateResearchView,
    DeleteResearchView,
    ToggleResearchStatusView,
    ToggleFeaturedStatusView
)

urlpatterns = [
    path("", HomeView.as_view(), name="admin"),
    path("", HomeView.as_view(), name="home"),
    path("create/", CreateProjectView.as_view(), name="create-project"),
    path("edit/<uuid:id>/", EditProjectView.as_view(), name="edit-project"),
    path("certificate/list/", CertificateList.as_view(), name="cert-list"),
    path("preview/", Preview.as_view(), name="preview"),
    path("certificate/upload/", CertificateUpload.as_view(), name="upload-certificate"),
    path('api/certificates/upload/', CertificateAPIView.as_view(), name='upload_certificate_api'),
    
    # Project API endpoints
    path('api/projects/save/', ProjectAPIView.as_view(), name='save_project_api'),
    path('api/projects/<uuid:project_id>/delete/', ProjectAPIView.as_view(), name='delete_project_api'),
    path('api/projects/delete/', ProjectAPIView.as_view(), name='delete_project_api_no_id'),
    
    path('research/create/', ResearchCreateView.as_view(), name='create-research'),
    path('research/edit/<uuid:id>/', ResearchEditView.as_view(), name='research-edit'),
    path('research/list/', ResearchListViewAdmin.as_view(), name='research-list-admin'),
    
    # Research API URLs
    path('api/research/save/', CreateUpdateResearchView.as_view(), name='research-save'),
    path('api/research/delete/', DeleteResearchView.as_view(), name='research-delete'),
    path('api/research/toggle-status/', ToggleResearchStatusView.as_view(), name='research-toggle-status'),
    path('api/research/toggle-featured/', ToggleFeaturedStatusView.as_view(), name='research-toggle-featured'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)