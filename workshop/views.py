from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Tool, Workshop, Timeslot
from .forms import  ToolForm, WorkshopForm, RegistrationForm, TimeslotForm, WorkshopFormSet
from .serializers import WorkshopSerializer
import logging

class UserIsWorkshopAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        workshop = self.get_object()

        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        if workshop.tutor != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class MyLoginView(LoginView):
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('login_redirect')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class LoginRedirectView(generic.TemplateView):
    template_name = 'registration/login_redirect.html'

class LogoutRedirectView(generic.TemplateView):
    template_name = 'registration/logout.html'

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('logout_redirect')
    """make logout available via GET"""
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/success')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form": form})

class ListWorkshop(generic.ListView):
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    template_name = "workshop/homepage.html"
    context_object_name = "workshop_list"

    def get_queryset(self):
        logging.info("Get Data")
        query = self.request.GET.get('search', '')
        queryset = Workshop.objects.all().order_by("workshop_title")
        if query:
            queryset = queryset.filter(
                Q(workshop_title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)).order_by("workshop_title")

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_private=False)

        return queryset

class DetailWorkshop(generic.detail.DetailView):
    model = Workshop
    serializer_class = WorkshopSerializer
    template_name = "workshop/detail_workshop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshop_id'] = self.kwargs.get('pk')
        return context


class CreateWorkshop(PermissionRequiredMixin, generic.edit.CreateView):
    form_class = WorkshopForm
    serializer_class = WorkshopSerializer
    template_name = "workshop/create_workshop.html"
    permission_required = 'workshop.add_workshop'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['workshop_formset'] = WorkshopFormSet(self.request.POST)
        else:
            data['workshop_formset'] = WorkshopFormSet()
        return data

    def form_valid(self, form):
        logging.info(f"Saving Form {form}")
        form.instance.tutor = self.request.user

        context = self.get_context_data()
        workshop_formset = context['workshop_formset']
        if workshop_formset.is_valid():
            self.object = form.save()
            timeslots = workshop_formset.save(commit=False)
            for timeslot in timeslots:
                timeslot.workshop = self.object
                timeslot.save()
            return HttpResponseRedirect(reverse('workshop:list'))
        else:
            return self.form_invalid(form)
        # return HttpResponseRedirect(reverse('workshop:list'))

class EditWorkshop(UserIsWorkshopAdminMixin, generic.edit.UpdateView):
    form_class = WorkshopForm
    serializer_class = WorkshopSerializer
    template_name = "workshop/edit_workshop.html"
    success_url = ""
    # permission_required = 'workshop.change_workshop'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['workshop_formset'] = WorkshopFormSet(self.request.POST)
        else:
            data['workshop_formset'] = WorkshopFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        workshop_formset = context['workshop_formset']
        if workshop_formset.is_valid():
            self.object = form.save()
            timeslots = workshop_formset.save(commit=False)
            for timeslot in timeslots:
                timeslot.workshop = self.object
                timeslot.save()
            return HttpResponseRedirect(reverse('workshop:list'))
        else:
            return self.form_invalid(form)
    
    def get_queryset(self):
        return Workshop.objects.all()

class DeleteWorkshop(UserIsWorkshopAdminMixin, generic.edit.DeleteView):
    model = Workshop
    serializer_class = WorkshopSerializer
    template_name = 'workshop/delete_workshop.html'
    success_url= "/workshop/"
    # permission_required = 'workshop.delete_workshop'

    def get_queryset(self):
        return Workshop.objects.all()
    
    def delete():
        return super(DeleteWorkshop, self).delete()
    
class CreateTool(generic.edit.CreateView):
    form_class = ToolForm
    template_name ="workshop/create_tool.html"

    def form_valid(self,form):
        form.save()
        return HttpResponseRedirect(reverse('workshop:list'))
