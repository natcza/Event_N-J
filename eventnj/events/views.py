from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Event


# Create your views here.

class EventView(View):
    """Funkcja wyświetlająca liste eventów"""
    template_name = "events/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by("start")
        ctx = {
            "events": events,
        }
        return render(request, self.template_name, ctx)

class EventDetailsView(View):
    """Funckcja wyświetlająca opis jednego eventu"""
    template_name = "events/event_details_view.html"

    def get(self, request, *args, **kwargs):
        event_id = kwargs["pk"]
        event = get_object_or_404(Event, pk=event_id)
        ctx = {
            "event": event
        }
        return render(request, self.template_name, ctx)