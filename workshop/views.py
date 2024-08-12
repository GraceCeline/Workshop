from django.shortcuts import get_object_or_404, render, redirect,reverse
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
        query = self.request.GET.get('search', '')
        return Workshop.objects.filter(workshop_title__icontains=query).order_by("workshop_title")

class DetailWorkshop(generic.detail.DetailView):
    model = Workshop
    template_name = "workshop/detail_workshop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshop_id'] = self.kwargs.get('pk')
        return context

class CreateWorkshop(generic.edit.CreateView):
    form_class = WorkshopForm
    template_name = "workshop/create_workshop.html"

    def form_valid(self, form):
        logging.info(f"Saving Form {form}")
        form.save()
        return HttpResponseRedirect(reverse('workshop:list'))

class EditWorkshop(generic.edit.UpdateView):
    form_class = WorkshopForm
    template_name = "workshop/edit_workshop.html"
    success_url = ""

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('workshop:list'))
    
    def get_queryset(self):
        return Workshop.objects.all()

class DeleteWorkshop(generic.edit.DeleteView):
    model = Workshop
    template_name = 'workshop/delete_workshop.html'
    success_url= "/workshop/"

    def get_queryset(self):
        return Workshop.objects.all()
    
    def delete():
        return super(DeleteWorkshop, self).delete()
    
"""
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
    if request.method == 'POST' and 'delete' in request.POST:
        Workshop.objects.filter(pk=workshop_id).delete()
        return HttpResponseRedirect("workshop:homepage")
"""
