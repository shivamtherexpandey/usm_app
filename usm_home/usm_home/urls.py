from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from usm_home.view import Redirect

urlpatterns = [
    path("", Redirect.as_view()),
    path("admin/", admin.site.urls),
    path(settings.APPLICATION_PREFIX, include("usm_interface.urls")),
    path(settings.APPLICATION_PREFIX + "api/user/", include("usm_user.urls")),
]
