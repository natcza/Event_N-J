from django.core.management.base import BaseCommand
from events.management.commands.create_db import create_organizer
# create_participant, create_event

class Command(BaseCommand):
    help = 'wypełnij bazę danymi'

    def handle(self, *args, **options):
        create_organizer()
        # create_participant()
        # create_event()
        self.stdout.write(self.style.SUCCESS("dopisane"))


