from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Tool, Workshop
from .forms import WorkshopForm
import logging

class ListWorkshop(generic.ListView):
    template_name = "workshop/homepage.html"
    context_object_name = "workshop_list"

    def get_queryset(self):
        logging.info("Get Data")
        query = self.request.GET.get('')
        return Workshop.objects.all().order_by("date")

class DetailWorkshop(generic.ListView):
    model = Workshop
    template_name = "workshop/detail_workshop.html"

def create_workshop(request):
    logging.info("Add Workshop Data")

    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/saved/")
        else:
            logging.info(f"Found errors: {form.errors}")
            return HttpResponse(status=500)
    else:
        form = WorkshopForm()
    return render(request, "workshop/create_workshop.html", {'form': form })

def edit_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)

    if request.method == 'POST':
        form = WorkshopForm(request.POST, instance=workshop)
        if form.is_valid():
            form.save()
            messages.success(request,"Workshop edited successfully")
        else:
            logging.info(f"Found errors: {form.errors}")
            return HttpResponse(status=500)
    return render(request, "workshop/edit_workshop.html", { 'form' : form, 'workshop' : workshop})

def delete_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    workshop.delete()
    return HttpResponseRedirect("workshop:homepage")
