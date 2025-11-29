from django.views import View
from django.shortcuts import redirect


class Redirect(View):
    def get(self, request):
        return redirect("landing_page")
