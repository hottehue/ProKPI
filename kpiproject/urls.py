"""
URL configuration for kpiproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('kpiprj/', include('kpiprj.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# urlpatterns += [
#     path('', include('kpiprj.urls')),
# ]

# To redirect root URL of  site (i.e. 127.0.0.1:8000) to URL 127.0.0.1:8000/kpiprj/
# Add below this URL maps to redirect the base URL to the application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='kpiprj/', permanent=True)),
]

