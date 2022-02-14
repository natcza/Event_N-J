from django.core.management.base import BaseCommand
# from events.management.commands.create_db import create_organizer

from events.models import Organizer


class Command(BaseCommand):

    help = "wypełnij organizer danymi -- python manage.py create_organizer 5"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of organizers to be created')

    def handle(self, *args, **options):
        total = options['total']

        # len_organizers = len(Organizer.objects.all())

        # sprawdzaj jaki postfix ma ostatni rekord
        # ostatni = Organizer.objects.all()[len_organizers - 1:len_organizers].get().id
        ostatni = Organizer.objects.last().id

        # postfix kolejnej wartości
        # https://docs.python.org/3.9/library/string.html
        # postfix = "{:0>5}".format(str(ostatni + 1))

        for i in range(total):
            postfix = str("{:0>5}".format(str(ostatni + 1 + i)))
            # print(postfix)
            Organizer.objects.create(
                name="organizer_" + postfix,
                description="description_" + postfix,
                mail="o_" + postfix + "@o.pl"
            )

        self.stdout.write(self.style.SUCCESS(f"dopisane {total} rekordów"))
