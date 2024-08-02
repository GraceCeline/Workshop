from django.urls import path
from . import views

app_name = "workshop"

urlpatterns = [
    path("",views.ListWorkshop.as_view(), name="list"), #Homepage, List of available workshops
    path("<int:pk>/", views.DetailWorkshop.as_view(), name="details"), #Details of the workshops including all the options
    path("create_workshop/", views.create_workshop, name="create_workshop"), #Creating another workshop to the list
    path("<int:pk>/edit_workshop",views.edit_workshop, name="edit_workshop"), #Editing an existing workshop
    #path("<int:pk>/delete_workshop"), ' Deleting the workshop altogether
]