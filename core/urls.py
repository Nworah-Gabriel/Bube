"""
URL configuration for House4Rent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Website.views import custom_500, custom_403, custom_404
from django.http import HttpResponse


handler404 = custom_404
handler500 = custom_500
handler403 = custom_403

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path("api/api-auth/", include("rest_framework.urls")),
    path("admin/", include("Admin.urls"), name="admin"),
    path("", include("Website.urls")),
    path('health/', lambda request: HttpResponse('OK'), name='health_check'),

]


if settings.DEBUG:
    urlpatterns += [
        path('404/', custom_404, name='404'),
        path('500/', custom_500, name='500'),
        path('403/', custom_403, name='403'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
