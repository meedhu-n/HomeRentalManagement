from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the core app's URLs for the root path
    path('', include('core.urls')),
]