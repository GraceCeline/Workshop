from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Tool, Workshop
from .forms import  ToolForm,WorkshopForm, RegistrationForm
import logging

class UserIsWorkshopAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        workshop = self.get_object()

        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        if workshop.workshop_admin != request.user:
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
    template_name = "workshop/detail_workshop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshop_id'] = self.kwargs.get('pk')
        return context


class CreateWorkshop(PermissionRequiredMixin, generic.edit.CreateView):
    form_class = WorkshopForm
    template_name = "workshop/create_workshop.html"
    permission_required = 'workshop.add_workshop'

    def form_valid(self, form):
        logging.info(f"Saving Form {form}")
        form.instance.workshop_admin = self.request.user
        form.save()
        return HttpResponseRedirect(reverse('workshop:list'))

class EditWorkshop(UserIsWorkshopAdminMixin, generic.edit.UpdateView):
    form_class = WorkshopForm
    template_name = "workshop/edit_workshop.html"
    success_url = ""
    # permission_required = 'workshop.change_workshop'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('workshop:list'))
    
    def get_queryset(self):
        return Workshop.objects.all()

class DeleteWorkshop(UserIsWorkshopAdminMixin, generic.edit.DeleteView):
    model = Workshop
    template_name = 'workshop/delete_workshop.html'
    success_url= "/workshop/"
    # permission_required = 'workshop.delete_workshop'

    def get_queryset(self):
        return Workshop.objects.all()
    
    def delete():
        return super(DeleteWorkshop, self).delete()
    
class CreateTool(UserIsWorkshopAdminMixin, generic.edit.CreateView):
    form_class = ToolForm
    template_name ="workshop/create_tool.html"

    def form_valid(self):
        return HttpResponseRedirect(reverse('workshop:list'))
