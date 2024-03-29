"""
URL configuration for SWBM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from SWBM.sitemaps import MySiteMap

sitemaps = {
    'mysitemap': MySiteMap,
}

urlpatterns = [
    path('admin/', admin.site.urls, name="admin_"),
    path('choose_your_path/', include('choice_of_path.urls'), name="CYP_COP"),
    path('', RedirectView.as_view(url='/choose_your_path/', permanent=True)),
    path('bank/', include('bank.urls'), name="bank_"),
    path('messenger/', include('messenger.urls'), name="messenger_"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
