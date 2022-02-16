from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from events.models import Participant, Event


class Command(BaseCommand):
    help = "wypełnij participant danymi -- python manage.py create_participant 5"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of participants to be created')

    def handle(self, *args, **options):
        total = options['total']

        len_participants = len(Participant.objects.all())
        # print(len_participants)

        # sprawdzaj jaki postfix ma ostatni rekord
        if len_participants != 0:
            ostatni = Participant.objects.last().id
        else:
            ostatni = 0

        # postfix kolejnej wartości
        # https://docs.python.org/3.9/library/string.html
        # postfix = "{:0>5}".format(str(ostatni + 1))
        EVENT_ID = 3
        formatedDate = datetime.now(tz=timezone.utc)
        for i in range(total):
            postfix = str("{:0>5}".format(str(ostatni + 1 + i)))
            # print(i + 1)
            Participant.objects.create(
                name="participant_" + postfix,
                mail="p_" + postfix + "@p.pl",
                date_change_status=formatedDate,
                created=formatedDate,
                event=Event.objects.get(pk=EVENT_ID)
            )

        self.stdout.write(self.style.SUCCESS(f"dopisane {total} rekordów"))
