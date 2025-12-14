from django.contrib import admin
import django.shortcuts
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView,
    ProjectCategory,
    ProcessOptimization,
    ProcessOptimizationDetails,
    About,
    SKills,
    Certifications,
    Research,
    DataAnalysis,
    DataAnalysisDetail,
    DesignEngineering,
    DesignEngineeringDetail
    )

urlpatterns = [
    path("", HomeView.as_view(), name=""),
    path("", HomeView.as_view(), name="home-view"),
    path("about", About.as_view(), name="about"),
    path("skills", SKills.as_view(), name="skills"),
    path("certifications", Certifications.as_view(), name="certifications"),
    path("research", Research.as_view(), name="research"),
    path("project-category", ProjectCategory.as_view(), name="project-category"),
    path("process-optimization", ProcessOptimization.as_view(), name="process-optimization"),
    path("process-optimization/<uuid:id>/", ProcessOptimizationDetails.as_view(), name="process-optimization-detail"),
    path("data-analysis/<uuid:id>/", DataAnalysisDetail.as_view(), name="data-analysis-detail"),
    path("data-analysis", DataAnalysis.as_view(), name="data-analysis"),
    path("design-engineering", DesignEngineering.as_view(), name="design-engineering"),
     path("design-engineering-detail/<uuid:id>", DesignEngineeringDetail.as_view(), name="design-engineering-detail"),
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
