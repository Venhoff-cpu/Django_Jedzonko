from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    preparation = models.TextField()
    ingredient = models.TextField(blank=False)
    preparation_time = models.IntegerField(validators=[MinValueValidator(1)], blank=False)
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')
    
    def __str__(self):
        return f'{self.name}'


class DayName(models.Model):
    PONIEDZIALEK = "1"
    WTOREK = "2"
    SRODA = "3"
    CZWARTEK = "4"
    PIATEK = "5"
    SOBOTA = "6"
    NIEDZIELA = "7"
    DAY_OF_THE_WEEK_CHOICES = [
        (PONIEDZIALEK, 'Poniedziałek'),
        (WTOREK, 'Wtorek'),
        (SRODA, 'Środa'),
        (CZWARTEK, 'Czwartek'),
        (PIATEK, 'Piątek'),
        (SOBOTA, 'Sobota'),
        (NIEDZIELA, 'Niedziela')
    ]
    name = models.CharField(max_length=1, choices=DAY_OF_THE_WEEK_CHOICES)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name}'


class RecipePlan(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return f'{self.meal_name}'


class Page(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}, slug: {self.slug}'
