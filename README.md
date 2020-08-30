# Django_Jedzonko

## Project description

Ms. Maria Iksińska wrote a cookbook that has become a bestseller on the cookbook market in Poland and asked us to prepare a meal planning application for her readers. Mrs. Iksinska's book promotes healthy eating and emphasizes the important role of meal planning in it. She wants to start conducting workshops all over the country where she will teach participants how to plan their meals.
Maria wants to develop her business and to achieve her goals she needs a business card page and a simple meal planning application.
The project was created as part of the Scrum workshop.

## Requirements

Requirements have been listed in requirements.txt.
It should work with Django 3.1.

## Configuration

Look at **settings.py** file, you will find the following section in it:

```python
try:
    from your.local_settings import DATABASES
except ModuleNotFoundError:
    print("Brak konfiguracji bazy danych w pliku local_settings.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)
```

This means that Django will try to import
The constant `DATABASES` from the file **local_settings.py**. Keep the data for connection there.
Do not put this file under Git's control.


--- 
