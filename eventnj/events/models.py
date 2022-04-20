from django.db import models
import uuid
# from config.settings import HOST
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


SE_PENDING = 1
SE_PUBLISHED = 2
SE_ARCHIVE = 3

STATUS_EVENT = (
    (SE_PENDING, "Pending"),
    (SE_PUBLISHED, "Published"),
    (SE_ARCHIVE, "Archive")
)

SP_IS_NEW = 1
SP_IS_ACTIVE_MAIL = 2
SP_IS_DEACTIVATE_MAIL = 3
SP_IS_ACTIVE_EVENT = 4
SP_IS_DEACTIVATE_EVENT = 5
SP_IS_CONFIRMED = 6
SP_IS_RESIGNED = 7

STATUS_PARTICIPANT = (
    (SP_IS_NEW, "Is_New"),
    (SP_IS_ACTIVE_MAIL, "Is_Active_Mail"),
    (SP_IS_DEACTIVATE_MAIL, "Is_Deactivate_Mail"),
    (SP_IS_ACTIVE_EVENT, "Is_Active_Event"),
    (SP_IS_DEACTIVATE_EVENT, "Is_Deactivate_Event"),
    (SP_IS_CONFIRMED, "Is_confirmed"),
    (SP_IS_RESIGNED, "Is_resigned"),
)

# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    # status_id = models.ForeignKey("Status_participant", related_name="participant", on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_PARTICIPANT, default=SP_IS_NEW)
    date_change_status = models.DateTimeField(null=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    # authentication_code = models.UUIDField(default=uuid.uuid4, editable=False)
    authentication_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    confirmation_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    non_confirmation_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    identification_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey("Event", related_name="participants", on_delete=models.CASCADE)

    def invite_by_email(self):
        text_content = f'We would like to invite you to {self.event.title}. '
        html_content = f'<p>We would like to invite you to <strong>{self.event.title}</strong> message.</p>'
        str_link = f'http://{settings.HOST}/authenticate-participant/{self.authentication_code}'
        msg = EmailMultiAlternatives(
            f'Invitation to event: {self.event.title}, link: {str_link}',
            text_content,
            'from@example.com',
            [self.mail]
        )

        html_content = render_to_string('events/test.html', {'event': self.event, 'str_link': str_link})
        msg.attach_alternative(html_content, "text/html")
        return msg.send()

    def decision_by_mail(self):
        text_content = f'We would like to invite you of for you chosen event: {self.event.title}. '
        html_content = f'<p>We would like to invite you to <strong>{self.event.title}</strong> message.</p>'
        str_confirmation_link = f'http://{settings.HOST}/confirmate/{self.confirmation_code}'
        str_non_confirmation_link = f'http://{settings.HOST}/confirmate/{self.non_confirmation_code}'
        msg = EmailMultiAlternatives(
            f'Invitation to event: {self.event.title}, if you want to confirm your presence '
            f'at the event please click on the following link: {str_confirmation_link}, '
            f'if you resign please click here: {str_non_confirmation_link}',
            text_content,
            'from@example.com',
            [self.mail]
        )

        html_content = render_to_string('events/decision_by_mail.html', {'event': self.event,
                                                                         'str_confirmation_link': str_confirmation_link,
                                                                         'str_non_confirmation_link': str_non_confirmation_link}),
        msg.attach_alternative(html_content, "text/html")
        return msg.send()


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizers = models.ManyToManyField("Organizer", related_name="events")
    limit_participant_reserve = models.IntegerField()
    limit_participant = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    start_registration = models.DateTimeField()
    end_registration = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_EVENT, default=SE_PENDING)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    postcode = models.CharField(max_length=12)
    room = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)

class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, blank=True)
    mail = models.EmailField(max_length=255)
#     TODO: widget do pola mail

# class Status_Participant(models.Model):
#     status = models.IntegerField(choices=STATUS_PARTICIPANT)
#     date = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    event = models.ForeignKey("Event", related_name="photos", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="photos")
    # TODO podaj sciezke
    date = models.DateTimeField(auto_now_add=True)













