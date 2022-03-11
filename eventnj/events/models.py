from django.db import models
import uuid

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

STATUS_PARTICIPANT = (
    (SP_IS_NEW, "Is_New"),
    (SP_IS_ACTIVE_MAIL, "Is_Active_Mail"),
    (SP_IS_DEACTIVATE_MAIL, "Is_Deactivate_Mail"),
    (SP_IS_ACTIVE_EVENT, "Is_Active_Event"),
    (SP_IS_DEACTIVATE_EVENT, "Is_Deactivate_Event"),
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













