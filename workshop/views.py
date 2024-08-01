from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Tool, Prerequisite, Workshop
from .forms import WorkshopForm
import logging
class ListWorkshop(generic.ListView):
    template_name = "workshop/homepage.html"
    context_object_name = "workshop_list"

    def get_queryset(self):

        logging.info("Get Data")
        query = self.request.GET.get('')
        return Workshop.objects.all().order_by("date")

def add_workshop(request):
    logging.info("Add Workahop Data")

    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        """
        tool_formset = ToolFormSet(request.POST, instance=form.instance)
        prerequisite_formset = PrerequisiteFormSet(request.POST, instance=form.instance)

        if form.is_valid() and tool_formset.is_valid() and prerequisite_formset.is_valid():
            workshop = form.save()
            tool_formset.instance = workshop
            tool_formset.save()
            prerequisite_formset.instance = workshop
            prerequisite_formset.save()
            return HttpResponseRedirect('/saved/')
        else:
            form = WorkshopForm()
            tool_formset = ToolFormSet(instance=form.instance)
            prerequisite_formset = PrerequisiteFormSet(instance=form.instance)

    return render(request, 'workshop/add_workshop.html', {
            'form': form,
            'tool_formset': tool_formset,
            'prerequisite_formset': prerequisite_formset,
        })
    """
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/saved/")
        else:
            logging.info(f"Found errors: {form.errors}")
            return HttpResponse(status=500)
    else:
        form = WorkshopForm()
    return render(request, "workshop/add_workshop.html", {'form': form })

def edit_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)

    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Workshop edited successfully")
    return render(request, "workshop/edit_workshop.html", { 'form' : form })

