from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.APPLICATION_PREFIX, include('usm_interface.urls')),
    path(settings.APPLICATION_PREFIX + 'api/user/', include('usm_user.urls')),
]
