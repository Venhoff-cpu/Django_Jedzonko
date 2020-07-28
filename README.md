# Django - Strona Jedzonko

## Opis projektu

Pani Maria Iksińska napisała książkę kucharską, która stała się bestsellerem na rynku książek kucharskich w Polsce i zwróciła się do nas z prośba o przygotowanie dla jej czytelników aplikacji do planowania posiłków. Książka Pani Iksińskiej promuje zdrowe odżywianie i podkreśla jak ważną rolę odgrywa w nim planowanie posiłków. Chce zacząć przeprowadzać w całym kraju warsztaty, na których będzie uczyć uczestników planowania posiłków.

Pani Maria chce rozwijać swój biznes, a do zrealizowania swoich celów potrzebuje strony-wizytówki oraz prostej aplikacji do planowania posiłków.

## Co do skonfigurowania?

Nie konfigurowaliśmy bazy danych. Należy skonfigurowac ją lokalnie.

Zajrzyj do pliku **settings.py**, znajdziesz w nim następującą sekcję:

```python
try:
    from scrumlab.local_settings import DATABASES
except ModuleNotFoundError:
    print("Brak konfiguracji bazy danych w pliku local_settings.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)
```

Oznacza to, że Django podczas każdego uruchomienia będzie próbowało zaimportować
stałą `DATABASES` z pliku **local_settings.py**. Tam trzymaj dane do połączenia.

--- 
