from datetime import datetime
from random import random, shuffle

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from django.core.paginator import Paginator
from django.http import HttpResponse


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from jedzonko.models import Recipe, Plan, RecipePlan, DayName, Page


class IndexView(View):
    pass


class LandingPage(View):
    def get(self, request):
        recipe = list(Recipe.objects.all())
        shuffle(recipe)
        recipe_details = recipe[1]
        recipe_details2 = recipe[2]
        recipe_details3 = recipe[3]
        if recipe_details:
            ctx = {
                'recipe': recipe_details,
                'recipe2': recipe_details2,
                'recipe3': recipe_details3,
            }
            return render(request, 'index.html', ctx)


class AboutAndContact(View):
    def get(self, request, the_slug):
        if Page.objects.get(slug=the_slug):
            page = get_object_or_404(Page, slug=the_slug)
            ctx = {
                "title": page.title,
                "description": page.description,
            }
            return render(request, 'contact_about.html', ctx)
        else:
            if the_slug == "o-aplikacji":
                return redirect(reverse("home") + "#about")
            if the_slug == "kontakt":
                return redirect(reverse("home") + "#contact")


class Dashboard(View):
    def get(self, request):
        num_of_recipes = Recipe.objects.count()
        num_of_schedules = Plan.objects.count()
        plans = Plan.objects.order_by('-created').first()
        days = {}
        plan_details = RecipePlan.objects.filter(plan_id=plans).order_by("day_name")
        for day in DayName.objects.all().order_by("order"):
            days[day.get_name_display()] = plan_details.filter(day_name=day.order).order_by("order")
        context = {
            'num_of_recipes': num_of_recipes,
            'num_of_schedules': num_of_schedules,
            'plans': plans,
            'days': days,
        }
        return render(request, 'dashboard.html', context)


class RecipesList(View):
    def get(self, request):
        recipe_list = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipe_list, 50)
        
        page = request.GET.get("page")
        recipes = paginator.get_page(page)
        ctx = {
            "recipes": recipes,
        }
        return render(request, "app-recipes.html", ctx)

    def post(self, request):
        recipe_to_delete = get_object_or_404(Recipe, pk=request.POST.get("del"))
        recipe_name = recipe_to_delete.name
        recipe_to_delete.delete()
        messages.add_message(request, messages.INFO, f"Przepis {recipe_name} usunięty")
        return redirect("recipes_list")


class RecipeDetails(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        ingredients = list(recipe.ingredient.split("; "))
        ctx = {
            "r_id": recipe.id,
            "r_name": recipe.name,
            "r_description": recipe.description,
            "r_vote": recipe.votes,
            "r_ingredients": ingredients,
            "r_added": recipe.created,
            "r_updated": recipe.updated,
            "r_time": recipe.preparation_time,
            "r_preparation": recipe.preparation,
        }
        return render(request, "app-recipe-details.html", ctx)

    def post(self, request, id):
        if int(request.POST.get("recipe_id")) != id:
            return HttpResponse("Błąd, coś poszło nie tak przy polubieniu przepisu.")
        recipe = Recipe.objects.get(pk=id)
        if request.POST.get("like"):
            recipe.votes += 1
            recipe.save()
            messages.add_message(request, messages.INFO, "Polubiono przepis")
        elif request.POST.get("dislike"):
            recipe.votes -= 1
            recipe.save()
            messages.add_message(request, messages.INFO, "Zmniejszono ocene przepisu")
        else:
            messages.add_message(request, messages.INFO, "Błąd.")
        return redirect("details_recipe", id=recipe.id)


class AddRecipeToSchedule(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.DAY_OF_THE_WEEK_CHOICES
        context = {
            "plans": plans,
            "recipes": recipes, 
            "days": days
            }
        return render(request, 'app-schedules-meal-recipe.html', context)

    def post(self, request):
        plan_temp = get_object_or_404(Plan, pk=int(request.POST.get("plan")))
        meal = request.POST.get("meal")
        meal_order = request.POST.get("meal_order")
        recipe_temp = get_object_or_404(Recipe, pk=int(request.POST.get("recipe")))
#       day_name_temp = get_object_or_404(DayName, order="day_order")
        day_name = DayName.objects.get_or_create(name=request.POST.get("day"), order=int(request.POST.get("day")))
        day_name_temp = day_name[0]
        if meal and int(meal_order) > 0:
            new_recipe_at_schedule = RecipePlan.objects.create(
                plan_id=plan_temp,
                recipe_id=recipe_temp,
                day_name=day_name_temp,
                meal_name=meal,
                order=meal_order,
            )
            new_recipe_at_schedule.save()
            messages.add_message(request, messages.INFO, f"Przepis {recipe_temp.name} dodany do planu")
            return redirect("add_recipe_to_schedule") #, id=new_recipe_at_schedule.id)
        else:
            messages.add_message(request, messages.INFO, "Błąd - nieporpawny format danych")
            return render(request, "app-schedules-meal-recipe.html")


class AddRecipe(View):
    def get(self, request):
        context = {}
        return render(request, 'app-add-recipe.html', context)

    def post(self, request):
        recipe_name = request.POST.get("recipe_name")

        recipe_preparation = request.POST.get("recipe_preparation")
        recipe_time = request.POST.get("recipe_preparation_time")
        recipe_ingredients = request.POST.get("recipe_ingredients")
        recipe_description = request.POST.get("recipe_description")
        if recipe_name and recipe_description and recipe_time and recipe_ingredients and recipe_description \
                and recipe_preparation:
            recipe = Recipe.objects.create(
                name=recipe_name,
                ingredient=recipe_ingredients,
                description=recipe_description,
                preparation_time=recipe_time,
                preparation=recipe_preparation,
            )
            recipe.save()
            messages.add_message(request, messages.INFO, "Przepis pomyślnie dodany")
            return redirect("recipes_list")
        else:
            messages.add_message(request, messages.INFO, "Błąd prosze poprawnie wypełnic formularz")
            return redirect("add_recipe")


class EditRecipe(View):
    
    def get(self, request, id ):
        recipe = get_object_or_404(Recipe,pk=id)
        context = {
            'recipe': recipe
            }
        return render(request, 'app-edit-recipe.html', context)

    def post(self, request, id):
        recipe = get_object_or_404(Recipe,pk=id)
        recipe_name= request.POST.get("name")
        recipe_description = request.POST.get("description")
        recipe_preparation_time = request.POST.get("preparation_time")
        recipe_preparation = request.POST.get("preparation")
        recipe_ingredient = request.POST.get("ingredient")
        if recipe_name and recipe_description and recipe_preparation_time and recipe_ingredient and recipe_description \
                and recipe_preparation:
                Recipe.objects.filter(pk=id).update(
                    name=recipe_name, 
                    description=recipe_description,
                    preparation=recipe_preparation,
                    ingredient = recipe_ingredient,
                    preparation_time=int(recipe_preparation_time),
                    )
                messages.add_message(request, messages.SUCCESS, "Przepis zaktualizowano pomyślnie")
                return redirect("details_recipe", id=recipe.id)
        else:
            context = {"message": "Oops, coś poszlo ne tak"}
            return render(request, "app-edit-recipe.html", context)


class ScheduleDetails(View):
    
    def get(self, request, id):
        plan = get_object_or_404(Plan, pk=id)
        days = {}
        plan_details = RecipePlan.objects.filter(plan_id=id).order_by("day_name")
        for day in DayName.objects.all().order_by("order"):
            days[day.get_name_display()] = plan_details.filter(day_name=day.order).order_by("order")

        ctx = {
            "name": plan.name,
            "description": plan.description,
            "days": days
        }
        return render(request, 'app-details-schedules.html', ctx)

    def post(self, request, id):
        if "del" in request.POST:
            recipe_to_del = get_object_or_404(RecipePlan, pk=request.POST.get("del"))
            recipe_to_del.delete()
            messages.add_message(request, messages.SUCCESS, "Przepis zaktualizowano pomyślnie")
            return redirect("plan_id", id=id)
        else:
            return HttpResponse("Cos poszlo nie tak")


class SchedulesList(View):
    def get(self, request):
        plan_list = Plan.objects.all().order_by('name')
        page = request.GET.get('page')
        paginator = Paginator(plan_list, 50)

        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)
        context = {'plans': plans}
        return render(request, 'app-schedules.html', context)


class ScheduleAdd(View):
    def get(self, request):
        context = {}
        return render(request, 'app-add-schedules.html', context)

    def post(self, request):
        plan_name = request.POST.get("plan_name")
        plan_description = request.POST.get("plan_description")
        if plan_name and plan_description:
            if len(plan_name) > 255:
                ctx = {
                    "msg": "Za długa nazwa planu",
                }
                return render(request, "app-add-schedules.html", ctx)
            plan = Plan.objects.create(
                name=plan_name,
                description=plan_description,
            )
            plan.save()
            new_id = plan.id
            return redirect("plan_id", id=new_id)
        ctx = {
            "msg": "Nie wypełniono wszytkich wymaganych pól",
        }
        return render(request, "app-add-schedules.html", ctx)


class EditSchedule(View):
    
    def get(self, request):
        context = {}
        return render(request, 'app-edit-schedules.html', context)
