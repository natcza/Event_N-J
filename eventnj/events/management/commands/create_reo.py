# Create Relation Event Organizer


from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Event, Organizer

from datetime import datetime
from random import choice, randint


# from django.conf import settings
# from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "wypełnij organizer danymi -- python manage.py create_reo 1"

    def add_arguments(self, parser):

        parser.add_argument('choice', choices=['e', 'o'])
        parser.add_argument('total', action="extend", nargs=2, type=int, help="total")

    def handle(self, *args, **options):
        opt_total = options['total']

        opt_choice = options['choice']

        print(f'options: {options}')

        if opt_choice == 'e':
            print('event')
        elif opt_choice == 'o':
            print('organizer')



        # var_flag = options['flag']
        #
        # var_e = var_event[0]
        # var_o = var_event[1]

        # return
        # print(f'var_flag: {var_flag}')
        # print(f'options: {options}')
        len_events = len(Event.objects.all())
        len_organizers = len(Organizer.objects.all())
        m = 0
        n = 0

        if opt_choice == 'e':
            # dla losowych eventów m wybierz losowo n organizatorów
            # e m n
            m = opt_total[0]
            n = opt_total[1]
            result = set_change(opt_total, len_events, len_organizers)

            if result[0] == False:
                self.stdout.write(self.style.ERROR(result[1]))
            else:
                self.stdout.write(self.style.SUCCESS(result[1]))

        elif opt_choice == 'o':
            # dla losowych organizatorów n wybierz m losowych eventów
            #  o n m
            m = opt_total[1]
            n = opt_total[0]

            result = set_change(opt_total, len_organizers, len_events)

            if result[0] == False:
                self.stdout.write(self.style.ERROR(result[1]))
            else:
                self.stdout.write(self.style.SUCCESS(result[1]))

        print(n, m)
        counter = 0
        # return

        for i_e in range(1, m + 1):
            # print(i_e)
            events = Event.objects.get(pk=i_e)
            # jeśli nie ma pk to powinno się go pominąć
            for i_o in range(1, n + 1):
                # events.models.Organizer.DoesNotExist: Organizer matching query does not exist.
                # https://stackoverflow.com/questions/17813919/django-error-matching-query-does-not-exist
                try:
                    organizer = Organizer.objects.get(pk=i_o)
                    counter += 1
                except Organizer.DoesNotExist:
                    organizer = None

                events.organizers.add(organizer)


        #     print(i_o)

        # return
        # https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/



        #  dla listy eventów wybierz listę organizatorów
        # -e [e] [o]

        #  dla listy organozatorów wybierz listę eventów
        #  -o [o] [e]

        #  dla wybranego eventu wybierz organizatora
        # -E id id
        #  dla wybranego organizatora wybierz event
        # -O id id

        # sprawdzaj jaki postfix ma ostatni rekord
        # ostatni = Event.objects.last().id

        self.stdout.write(self.style.SUCCESS(f"dopisane {counter} rekordów"))


def set_change(var_flag, len_m, len_n):
    #  sprawdzaj czy liczba argumentów się zgadza

    m = int(var_flag[0])
    n = int(var_flag[1])

    if m > len_m:
        return [False, f"wartość event jest zbyt duża nie powinna przekraczać {len_m} rekordów"]

    if n > len_n:
        return [False, f"wartość organizer jest zbyt duża nie powinna przekraczać {len_n} rekordów"]

    return [True, f"OK"]
