from django.urls import path
from . import views

app_name = "workshop"

urlpatterns = [
    path("",views.ListWorkshop.as_view(), name="list"), # Homepage, List of available workshops
    path("create/", views.CreateWorkshop.as_view(), name="create_workshop"), # Creating another workshop to the list
    path("create_tool/", views.CreateTool.as_view(), name="create_tool"), # Create new tools for the workshop
    path("<int:pk>/", views.DetailWorkshop.as_view(), name="details"), # Details of the workshops including all the options
    path("<int:pk>/edit/",views.EditWorkshop.as_view(), name="edit_workshop"), # Editing an existing workshop
    path("<int:pk>/delete/", views.DeleteWorkshop.as_view(), name="delete_workshop"), # Deleting the workshop altogether
]