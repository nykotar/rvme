"""rvme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from django.views.generic.base import TemplateView

from . import views

admin.site.site_header = 'RVMe admin'
admin.site.site_title = 'RVMe admin'
admin.site.site_url = 'https://rvme.app/pool/'
admin.site.index_title = 'RVMe administration'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('pool/', include('pool.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)