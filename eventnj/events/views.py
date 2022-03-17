import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import FormView

from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from uuid import UUID
from config.settings import HOST


from .models import Event, Participant
from .forms import AddParticipantForm

from .models import (
    SP_IS_NEW,
    SP_IS_ACTIVE_MAIL,
    SP_IS_DEACTIVATE_MAIL,
    SP_IS_ACTIVE_EVENT,
    SP_IS_DEACTIVATE_EVENT,
    STATUS_PARTICIPANT,
)


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


# class EventDetailsView(View):
#     """Funkcja wyswietlajaca opis jednego Eventu"""
#     template_name = 'events/event_details_view.html'
#
#     # test stworzyc pizze kotra ma sie zwrocic
#     def get(self, request, *args, **kwargs):
#         event_id = kwargs['pk']
#         # breakpoint()
#         event = get_object_or_404(Event, pk=event_id)
#
#         ctx = {
#             'event': event,
#         }
#         return render(request, self.template_name, ctx)

class SendMailView(DetailView):
    template_name = 'events/info_send_mail.html'
    model = Event

# https://ccbv.co.uk/projects/Django/3.2/django.views.generic.edit/FormView/

class ParticipantAddView2(FormView):
    """Dodaj jedneuczestnika do eventu"""
    form_class = AddParticipantForm

    # https://www.fullstackpython.com/django-urls-reverse-lazy-examples.html
    # success_url = reverse('dashboard')
    # success_url = reverse_lazy('send-mail')
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
        participant.status = SP_IS_NEW
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
        # wygeneruj link aktywacyjny

        # email = EmailMessage(
        #     subject=f'Invitation to Event - EmailMessage: {event.title}',
        #     body=html_content,
        #     from_email='from@example.com',
        #     to=[mail],
        #     reply_to=['another@example.com'],
        #     headers={'Message-ID': 'Message-ID'},
        # )
        # email.attach_alternative(html_content, "text/html")
        # email.content_subtype = "html"
        # jak używać naprzemiennie plain text i html-a
        #  jak używać MIME

        # TODO Autentiction view --> Participant activation code
        # Link powiniem być postaci:
        # http://127.0.0.1:8000/authenticate-participant/3bf0561aeabf4c49b4fb3b81fb5e08ba/
        # django site
        str_link = f'http://{HOST}/authenticate-participant/{participant.authentication_code}'
        msg = EmailMultiAlternatives(
            f'Invitation to event: {event.title}, link: {str_link}',
            text_content,
            'from@example.com',
            [mail]
        )


        html_content = render_to_string('events/test.html', {'event': event, 'str_link': str_link})
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # email.send()

        # ToDo Connecting with MAILHOG --> SETTINGS
        # Adding HTML and Activation code uuid
        # sending an email after pressing send button Dodaj
        # jak sprawdzić czy dane są zapisane
        # form.send_email()
        return super().form_valid(form)

    # https://stackoverflow.com/questions/46184193/how-to-reverse-lazy-to-a-view-url-with-variable
    def get_success_url(self):
        eventid = self.kwargs['pk']

        # self.success_url)  # success_url may be lazy
        return reverse_lazy('send-mail', kwargs={'pk': eventid})

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
            # return redirect('dashboard')  # -> przekieruj na stronę
            return redirect('send-mail')  # -> przekieruj na stronę


        return render(request, self.template_name, {'form': form})  # tu możemy przekazać kontekst


class AuthenticateParticipantView(View):
    template_name = 'events/authenticateParticipant_view.html'


    def get(self, request, *args, **kwargs):
        # authenticate_code
        authenticate_code = kwargs['authenticate_code']

        # https://gist.github.com/ShawnMilo/7777304
        # uuid.UUID('302a4299-736e-4ef3-84fc-a9f400e84b24').version
        # czy authenticate_code jest uuid
        print(f"----  sprawdzaj UUID")

        # try:
        #     val = UUID(authenticate_code)
        # except ValueError:
        #     msg = f"{authenticate_code} is not uuid"
        #     print(msg)
        #     ctx = {
        #         "msg": msg,
        #     }
        #     return render(request, self.template_name, ctx)

        print(f"kwargs -->: {kwargs}")

        participant = get_object_or_404(Participant, authentication_code=authenticate_code)
        print(f"----  sprawdzaj status")

        # sprawdzaj czy już wcześniej nastąpiła zmiana statusu
        if participant.status == SP_IS_ACTIVE_MAIL:
            msg = f"próba ponownego aktywowania maila"
            print(msg)
            ctx = {
                "msg": msg,
            }
            return render(request, self.template_name, ctx)

        print(f"----  zmień status")
        # zmień status
        participant.status = SP_IS_ACTIVE_MAIL
        participant.date_change_status = timezone.now()

        print(f"----  zachowaj zmiany")
        participant.save()
        # setStatus()
        # zmiana rezerwacji

        ctx = {
            "participant": participant
        }

        return render(request, self.template_name, ctx)

    # def post(self, request, *args, **kwargs):
    #
    #     authenticate_code = kwargs['aauthentication_code']
    #     participant = get_object_or_404(Participant, authentication_code=authenticate_code)
    #
    #     ctx = {}
    #     return render(request, self.template_name, ctx)  # tu możemy przekazać kontekst
