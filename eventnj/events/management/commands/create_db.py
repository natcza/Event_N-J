from sys import stdout
from events.models import Organizer, Participant, Event

def create_organizer():
    Organizer.objects.create(name="organizer1", description="description_organizer_1", mail="organizer1@.o2.pl")
    Organizer.objects.create(name="organizer2", description="description_organizer_2", mail="organizer2@.o2.pl")
    Organizer.objects.create(name="organizer3", description="description_organizer_3", mail="organizer3@.o2.pl")
    Organizer.objects.create(name="organizer4", description="description_organizer_4", mail="organizer4@.o2.pl")

# STATUS_PARTICIPANT = (
#     (1, "Is_New"),
#     (2, "Is_Active_Mail"),
#     (3, "Is_Deactivate_Mail"),
#     (4, "Is_Active_Event"),
#     (5, "Is_Deactivate_Event"),
# )

# def create_participant():
#     Participant.objects.create(name="Participant1", mail="participant1@o2.pl")
#     Participant.objects.create(name="Participant2", mail="participant2@o2.pl")
#     Participant.objects.create(name="Participant3", mail="participant3@o2.pl")
#     Participant.objects.create(name="Participant4", mail="participant4@o2.pl")
#     Participant.objects.create(name="Participant5", mail="participant5@o2.pl")
#
# def create_event():
#     Event.objects.create(title="Event1", description="Description1", organizer=1, limit_participant_reserve=0,
#                          limit_participant=10, start="2022-03-17 18:00:00", end="2022-03-17 22:00:00",
#                          start_registration="2022-03-10 18:00:00", end_registration="2022-03-22 18:00:00",
#                          country="Country1", city="City1", street="Street1", Postcode="Postcode1", price=10.00)


