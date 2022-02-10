from django.db import models
import uuid

PENDING = 1

STATUS_EVENT = (
    (PENDING, "Pending"),
    (2, "Published"),
    (3, "Archive")
)

IS_NEW = 1

STATUS_PARTICIPANT = (
    (IS_NEW, "Is_New"),
    (2, "Is_Active_Mail"),
    (3, "Is_Deactivate_Mail"),
    (4, "Is_Active_Event"),
    (5, "Is_Deactivate_Event"),
)

# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    # status_id = models.ForeignKey("Status_participant", related_name="participant", on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_PARTICIPANT, default=IS_NEW)
    date_change_status = models.DateTimeField(null=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    # authentication_code = models.UUIDField(default=uuid.uuid4, editable=False)
    authentication_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    confirmation_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    non_confirmation_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    identification_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey("Event", related_name="participants", on_delete=models.CASCADE)

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
    status = models.IntegerField(choices=STATUS_EVENT, default=PENDING)
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













