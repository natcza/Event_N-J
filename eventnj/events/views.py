from django.shortcuts import render
from django.views import View
from .models import Event


# Create your views here.

# class DashboardView(View):
#     template_name = "events/dashboard.html"
#
#     def get(self, request, *args, **kwargs):
#         events = Event.objects.all().order_by("start")
#         ctx = {
#             "events": events,
#         }
#         return render(request, self.template_name, ctx)
