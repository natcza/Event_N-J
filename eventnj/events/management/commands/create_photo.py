from django.core.management.base import BaseCommand
# from events.management.commands.create_db import create_organizer

from events.models import Photo, Event


class Command(BaseCommand):
    help = "wypełnij organizer danymi -- python manage.py create_photo n photos, id event"

    def add_arguments(self, parser):

        # parser.add_argument('total', type=int , help='Indicates the number of photos to be created')
        parser.add_argument('total', action="extend", nargs=2, type=int, help="number of photos, event id")


    def handle(self, *args, **options):
        total = options['total']


        len_photos = len(Photo.objects.all())

        # sprawdzaj jaki postfix ma ostatni rekord

        if len_photos != 0:
            ostatni = Photo.objects.last().id
        else:
            ostatni = 0

        # postfix kolejnej wartości
        # https://docs.python.org/3.9/library/string.html
        # postfix = "{:0>5}".format(str(ostatni + 1))
        # print(f"total: {total}")

        print("create_photo")

        for i in range(total[0]):
            postfix = str("{:0>5}".format(str(ostatni + 1 + i)))
            # print(postfix)

            Photo.objects.create(
                name="name_" + postfix,
                image="image_" + postfix,
                event=Event.objects.get(pk=total[1])
            )

        self.stdout.write(self.style.SUCCESS(f"dopisane {total[0]} rekordy, event {total[1]}"))
