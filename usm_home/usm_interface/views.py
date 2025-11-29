from django.shortcuts import render
from django.views import View
from usm_home import settings


# Create your views here.
class LandingPageView(View):
    def get(self, request):
        context = {"summarizer_host": settings.SUMMARIZER_HOST}
        return render(request, "landing_page.html", context=context)
