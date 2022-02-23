from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Event, Participant
from .forms import addParticipantForm

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


class ParticipantAddView(View):
    template_name = 'addParticipant_view.html'

    def get(self, request, *args, **kwargs):
        form = addParticipantForm()

        event_id = kwargs['pk']
        event = get_object_or_404(Event, pk=event_id)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = addParticipantForm(request.POST)
        event_id = kwargs['pk']
        event = get_object_or_404(Event, pk=event_id)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            mail = form.cleaned_data.get('mail')

            participant = Participant()
            participant.name = name
            participant.mail = mail
            # participant.event = event
            # .save()

            # tu nie możemy przesłać kontekstu

            # return redirect('student', student_id=student.id)  # -> przekieruj na stronę

        return render(request, self.template_name, {'form': form})  # tu możemy przekazać kontekst