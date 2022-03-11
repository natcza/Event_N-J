# aby plik był wykonywalny
# chmod +x script_eventnj.sh

# uruchamianie skryptu
#./script_eventnj.sh
# -----------------------------------------------


#migracja
python manage.py migrate


# utwórz 5 eventów
python manage.py create_event 5

# utwórz 2 eventy
python manage.py create_event 2

# utwórz 5 organizatorów
python manage.py create_organizer 5

# utwórz relację między 5 kolejnymi eventami i 5 kolejnymi organizatorami
# tworzy hurtowo - jest to nieracjonalne
python manage.py create_reo e 5 5

# tworzy relację między eventem o pk=6 i organizatorem o pk=2
# tworzy pojedynczo - jest większa kotrola
python manage.py create_reo e1 6 2

# utwórz 1 uczestnika i przypisz do eventu o pk=5
python manage.py create_participant 1 5

# utwórz 3 zdjęcia i przypisz do eventu o pk=2
python manage.py create_photo 3 2
