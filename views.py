from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Tool, Prerequisite, Workshop
from .forms import WorkshopForm

class ListWorkshop(generic.ListView):
    template_name = "workshop/homepage.html"
    context_object_name = "workshop_list"

    def get_queryset(self):
        query = self.request.GET.get('')
        return Workshop.objects.all().order_by("date")

def add_workshop(request):
    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        if form.is_valid():
            form.save()
             # Adjust the redirect as needed
            return HttpResponseRedirect("/saved/")
    else:
        form = WorkshopForm()
    return render(request, "workshop/add_workshop.html", {'form': form })


