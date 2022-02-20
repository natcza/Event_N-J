from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Event


# Create your views here.

class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by("start")
        ctx = {
            "events": events,
        }
        return render(request, self.template_name, ctx)


class EventDetailsView(View):
    """Funkcja wyswietlajaca opis jednego Eventu"""
    template_name = 'event_details_view.html'

    # test stworzyc pizze kotra ma sie zwrocic
    def get(self, request, *args, **kwargs):
        event_id = kwargs['pk']
        event = get_object_or_404(Event, pk=event_id)

        ctx = {
            'event': event,
        }
        return render(request, self.template_name, ctx)
