from django.urls import path
from usm_interface import views

urlpatterns = [
    # Add your URL patterns here
    path("", views.LandingPageView.as_view(), name="landing_page"),
]
