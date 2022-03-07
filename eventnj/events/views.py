import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import FormView

from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import Event, Participant
from .forms import AddParticipantForm

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.core.mail import EmailMessage

# Create your views here.

class DashboardView(View):
    template_name = "events/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by("start")
        ctx = {
            "events": events,
        }
        return render(request, self.template_name, ctx)

# class EventDetailsView_(DetailView):
#     model = Event
#     template_name = 'event_details_view.html'
#
#     def dispatch(self, request, *args, **kwargs):
#
#         # try:
#         print(kwargs)
#         # breakpoint()
#
#         obj = super().dispatch(request, *args, **kwargs)
#         # print(obj)
#         # except Event.DoesNotExist:
#         #     raise Http404('dupa, nie ma Eventu')
#
#         return obj
#     # def get_context_data(self, **kwargs):
#     #     # breakpoint()
#     #     print(self.object)
#     #     context = super().get_context_data(**kwargs)
#     #
#     #     return context
#     # def get_object(self, queryset=None):
#     #     # breakpoint()
#     #     # if queryset is None:
#     #     #     queryset = self.get_queryset()
#     #
#     #
#     #     try:
#     #         obj = super().get_object()
#     #     except Event.DoesNotExist:
#     #
#     #         raise Http404('dupa nie ma Eventu')
#     #
#     #     return obj



class EventDetailsView_(DetailView):
    model = Event
    template_name = 'events/event_details_view.html'


    # template_name = 'event_details_view.html'

    # def dispatch(self, request, *args, **kwargs):
    #     # event_slug = self.kwargs.get("slug")
    #     self.event = get_object_or_404(Event)
    #     return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
        # return context

class EventDetailsView(View):
    """Funkcja wyswietlajaca opis jednego Eventu"""
    template_name = 'events/event_details_view.html'

    # test stworzyc pizze kotra ma sie zwrocic
    def get(self, request, *args, **kwargs):
        event_id = kwargs['pk']
        # breakpoint()
        event = get_object_or_404(Event, pk=event_id)

        ctx = {
            'event': event,
        }
        return render(request, self.template_name, ctx)

# https://ccbv.co.uk/projects/Django/3.2/django.views.generic.edit/FormView/

class ParticipantAddView2(FormView):
    """Dodaj jedneuczestnika do eventu"""
    form_class = AddParticipantForm

    # https://www.fullstackpython.com/django-urls-reverse-lazy-examples.html
    success_url = reverse_lazy('dashboard')
    template_name = 'events/addParticipant_view.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        event_id = self.kwargs['pk']
        event = get_object_or_404(Event, pk=event_id)

        name = form.cleaned_data.get('name')
        mail = form.cleaned_data.get('mail')

        # modelForm
        # event którego nie ma

        ''' uczestnik jeste nie jest określony 
            czy należy do listy dodatkowej czy rezerwowej
            przypisanie po zamknięciu rezerwacji
        '''
        participant = Participant()
        participant.name = name
        participant.mail = mail
        participant.date_change_status = timezone.now()
        # participant.created = formatedDate
        participant.event = event
        participant.save()
        # send_mail(
        #     subject = f'Invitation to Event: {event.title}',
        #     message = f'We would like to invite you to {event.title}. '
        #               f'If you want to active your account please click the link {participant.authentication_code}',
        #     from_email='from@example.com',
        #     recipient_list = [mail],
        #
        # )
        text_content = f'We would like to invite you to {event.title}. '
        html_content = f'<p>We would like to invite you to <strong>{event.title}</strong> message.</p>'
        email = EmailMessage(
            subject=f'Invitation to Event - EmailMessage: {event.title}',
            body=html_content,
            from_email='from@example.com',
            to =[mail],
            reply_to=['another@example.com'],
            headers={'Message-ID': 'foo'},
        )
        # email.attach_alternative(html_content, "text/html")
        email.content_subtype = "html"
        # jak używać naprzemiennie plain text i html-a
        #  jak używać MIME

        email.send()



        # ToDo Connecting with MAILHOG --> SETTINGS
        # Adding HTML and Activation code uuid
        # sending an email after pressing send button Dodaj
        # jak sprawdzić czy dane są zapisane
        # form.send_email()

        return super().form_valid(form)



# https://docs.djangoproject.com/en/3.2/ref/class-based-views/
class ParticipantAddView(View):
    template_name = 'events/addParticipant_view.html'

    def get(self, request, *args, **kwargs):
        form = AddParticipantForm()

        # event_id = kwargs['pk']

        # event = get_object_or_404(Event, pk=event_id)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddParticipantForm(request.POST)
        event_id = kwargs['pk']
        event = get_object_or_404(Event, pk=event_id)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            mail = form.cleaned_data.get('mail')

            formatedDate = datetime.now(tz=timezone.utc)

            participant = Participant()
            participant.name = name
            participant.mail = mail
            participant.date_change_status = formatedDate
            # participant.created = formatedDate
            participant.event = event
            participant.save()

            # tu nie możemy przesłać kontekstu
            # wracamy do listy eventów
            # return redirect('student', student_id=student.id)  # -> przekieruj na stronę
            return redirect('dashboard')  # -> przekieruj na stronę

        return render(request, self.template_name, {'form': form})  # tu możemy przekazać kontekst
