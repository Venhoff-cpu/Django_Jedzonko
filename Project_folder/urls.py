"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko.views import (IndexView, Dashboard, LandingPage,
RecipeDetails, RecipesList, AddRecipe, EditRecipe, AddRecipeToSchedule,
ScheduleDetails, SchedulesList, ScheduleAdd, EditSchedule, AboutAndContact)


urlpatterns = [
    path('index/', IndexView.as_view()),
    path('', LandingPage.as_view(), name='home'),
    path('<slug:the_slug>', AboutAndContact.as_view(), name='contact_about'),
    path('main/', Dashboard.as_view(), name='dashboard'),
    
    path('recipe/<int:id>/', RecipeDetails.as_view(), name='details_recipe'),
    path('recipe/list/', RecipesList.as_view(), name='recipes_list'),
    path('recipe/add/', AddRecipe.as_view(), name='add_recipe'),
    path('recipe/modify/<int:id>', EditRecipe.as_view(), name="modify_recipe"),
    path('plan/add-recipe/', AddRecipeToSchedule.as_view(), name='add_recipe_to_schedule'),
    path('plan/list/', SchedulesList.as_view(), name='schedules_list'),
    path('plan/<int:id>', ScheduleDetails.as_view(), name='plan_id'),
    path('plan/add/', ScheduleAdd.as_view(), name='add_schedule'),
    path('admin/', admin.site.urls),
]
