from django.urls import path
from . import views

app_name = "workshop"

urlpatterns = [
    path("",views.ListWorkshop.as_view(), name="list"),
    path("add_workshop/", views.add_workshop, name="add_workshop"),
    #path("<int:pk>/edit_workshop",views.edit_workshop, name="edit_workshop"),
    #path("<int:pk>/delete_workshop"),
]