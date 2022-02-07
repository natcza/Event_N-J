from django.db import models
import uuid

STATUS_EVENT = (
    (1, "Pending"),
    (2, "Published"),
    (3, "Archive")
)

STATUS_PARTICIPANT = (
    (1, "Is_New"),
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
    status_id = models.IntegerField(choices=STATUS_PARTICIPANT, default=1)
    date_change_status = models.DateTimeField(editable=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    # authentication_code = models.UUIDField(default=uuid.uuid4, editable=False)
    authentication_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    confirmation_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    non_confirmation_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    identification_code = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    date = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    # organizer_id = models.ForeignKey("Organizer", related_name="organizer", on_delete=models.CASCADE)
    limit_participant_reserve = models.IntegerField()
    limit_participant = models.IntegerField()
    # participant_id = models.ForeignKey("Participant", related_name="participant", on_delete=models.CASCADE, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    start_registration = models.DateTimeField()
    end_registration = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_EVENT, default=1)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    postcode = models.CharField(max_length=12)
    room = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_online = models.BooleanField(default=False)
    online_link = models.CharField(max_length=500, default=False)
    date = models.DateTimeField(auto_now_add=True)

class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    mail = models.CharField(max_length=255)
#     TODO: widget do pola mail

# class Status_Participant(models.Model):
#     status = models.IntegerField(choices=STATUS_PARTICIPANT)
#     date = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    # event_id = models.ForeignKey("Event", related_name="photo", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # image = models.ImageField()
    date = models.DateTimeField(auto_now_add=True)













