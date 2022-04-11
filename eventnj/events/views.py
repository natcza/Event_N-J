import logging
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import FormView

from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import Http404
from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from uuid import UUID
from django.conf import settings


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
        participant.event = event
        participant.status = SP_IS_NEW
        participant.save()
        participant.invite_by_email()
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


class AuthenticateParticipantView(DetailView):
    template_name = 'events/authenticateParticipant_view.html'
    model = Participant
    # query_pk_and_slug = False
    # query_pk_and_slug = "authenticate_code"
    slug_field = 'authentication_code'
    slug_url_kwarg = 'authenticate_code'
# <<<<<<< registration_model_view


#     def getup(self, request, *args, **kwargs):
#         # authenticate_code
#         authenticate_code = kwargs['authenticate_code']

#         # https://gist.github.com/ShawnMilo/7777304
#         # uuid.UUID('302a4299-736e-4ef3-84fc-a9f400e84b24').version
#         # czy authenticate_code jest uuid
#         print(f"----  sprawdzaj UUID")

#         # try:
#         #     val = UUID(authenticate_code)
#         # except ValueError:
#         #     msg = f"{authenticate_code} is not uuid"
#         #     print(msg)
#         #     ctx = {
#         #         "msg": msg,
#         #     }
#         #     return render(request, self.template_name, ctx)

#         print(f"kwargs -->: {kwargs}")

#         participant = get_object_or_404(Participant, authentication_code=authenticate_code)
#         print(f"----  sprawdzaj status")

#         # sprawdzaj czy już wcześniej nastąpiła zmiana statusu
# =======

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        participant = self.object

# >>>>>>> develop
        if participant.status == SP_IS_ACTIVE_MAIL:
            raise Http404('Question does not exists')

        participant.status = SP_IS_ACTIVE_MAIL
        participant.date_change_status = timezone.now()
        participant.save()

        self.object = participant

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


