1. Do poprawy:

Zmiana kodu (views.py)w pierwszym mailu do potwierdzenia atutentyczności
użytkownika. Trzeba dopisać warunek, że jeżeli uczestnik nie da odpowiedzi na maila
w przeciągu 48h wówczas status zostanie zmieniony na "Is_Deactivate_Mail".
Aktualnie sytuacja wygląda tak, że brakuje tego warunku, zatem użytkownik klikając w link
jest stanie tylko potwierdzić swoją autentyczność. Czyli, gdy nie kliknie w link status będzie wciąż
"Is_New" zamiast "Is_Deactivate_Mail".

Dopisać należy warunek czasowy --> funkcja do zmiany statusu i do monitorowania tej zmiany

STATUS_PARTICIPANT = (
    (SP_IS_NEW, "Is_New"),
    (SP_IS_ACTIVE_MAIL, "Is_Active_Mail"),  --> 1.1. zalożenie: do 20 losowo wybranych osób z tym statusem
    zostaną wysłane maile z zaproszeniem
    --> 1.2 Reszta osob zostanie dopisana do listy rezerowej
    --> 1.3 Do uczestnika (z listy podstawej randomoe 20 osób) zostaje wysłany mail, zmienia się status z 
"Is_Active_Mail" --> "Is_Awaited_Mail_Reply"
    --> 1.3 Gdy uczestnik otrzyma E-mail z możwliwością dokonania wyboru ma na to założmy 48 h
(tz. ide/nie idę lub nie odpowie na maila) wówczas status zmienia się jak poniżej

idzie --> "Is_Active_Event"
nie idę --> "Is_Deactivate_Event"
nie odpowie --> "Is_Deactivate_Event"

PO wysłaniu pierwszych 20 E-maili zostanie włączona funkcja (task), która zacznie co 1h sprawdzać status eventu.
Gdy,status jest "Is_Deactivate_Event", wówczas funkcja sprawdza ile tych jest rezygnacji 
i tyle samo wyśle nowych i zmieni sie status użtkownika z 
Funkcja bedzie sprawdzała jednego uczestnika, i wysyłala nowego maila. 
maili do randomwych osób już z listy rezerwowej ze statusem "Is_resigned" oraz również zostanie
zmieniony status osób, które potwierdzily swoją obecność z "Is_Active_Event" --> "Is_confirmed". Dzieje się to 
cyklicznie w tle. Nastąpi cykliczne sprawdzanie bazy danych. 

Przepusc przez seler i bedzie git:)

jak dlugo beda dzialac selery? gdy lis†a uczestnikow zostannie zapelniona lub do czasu 'end_registration' eventu.
Czyli do --> 'end_registration' eventu, jaka zostanie przez nas zdefiniowana. 

STATUS_PARTICIPANT = (
    (SP_IS_NEW, "Is_New"),
    (SP_IS_ACTIVE_MAIL, "Is_Active_Mail"),
    (SP_IS_DEACTIVATE_MAIL, "Is_Deactivate_Mail"),
    (SP_IS_AWAITED_MAIL_REPLY, "Is_Awaited_Mail_Reply"),
    (SP_IS_ACTIVE_EVENT, "Is_Active_Event"),
    (SP_IS_DEACTIVATE_EVENT, "Is_Deactivate_Event"),
    (SP_IS_CONFIRMED, "Is_confirmed"),
    (SP_IS_RESIGNED, "Is_resigned"),
)



5. Wysyłanie maila z decyzją, do randomowo wybranych uczestników ze statusem is_active_event, 
którzy wyrazili chęć wzięcia udziału w evencie

- E.mail będzie zawierał dwie opcje
--> biorę udział,
--> rezygnuje
co oznacza, że zostanie zmieniony status w participant

status = models.IntegerField(choices=STATUS_PARTICIPANT, default=SP_IS_NEW)

STATUS_PARTICIPANT = (
    (SP_IS_NEW, "Is_New"),
    (SP_IS_ACTIVE_MAIL, "Is_Active_Mail"),
    (SP_IS_DEACTIVATE_MAIL, "Is_Deactivate_Mail"),
    (SP_IS_ACTIVE_EVENT, "Is_Active_Event"),
    (SP_IS_DEACTIVATE_EVENT, "Is_Deactivate_Event"),
    (SP_IS_CONFIRMED, "Is_confirmed"),
    (SP_IS_RESIGNED, "Is_resigned"),
)
