from django.contrib import admin
import django.shortcuts
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, CreateProject, CertificateList, CreateResearch, ResearchList, Preview, CertificateUpload

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("create/", CreateProject.as_view(), name="create-project"),
    path("certificate/list/", CertificateList.as_view(), name="cert-list"),
    path("research/create/", CreateResearch.as_view(), name="create-research"),
    path("research/list/", ResearchList.as_view(), name="research-list"),
    path("preview/", Preview.as_view(), name="preview"),
    path("certificate/upload/", CertificateUpload.as_view(), name="upload-certificate"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
