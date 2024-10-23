from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
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
from .serializers import WorkshopSerializer, ToolSerializer
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

class ListWorkshop(ListAPIView):
    serializer_class = WorkshopSerializer
    template_name = "workshop/homepage.html"
    context_object_name = "workshop_list"
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    filter_backends = [filters.SearchFilter]
    search_fields = ['workshop_title', 'tutor']

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
    
    """def render_to_response(self, context, **response_kwargs):
        # If the request is for JSON, return a JsonResponse
        if self.request.headers.get('Accept') == 'application/json':
            queryset = self.get_queryset()
            serializer = WorkshopSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            # Otherwise, return the regular HTML response
            return super().render_to_response(context, **response_kwargs)
"""

class DetailWorkshop(APIView):
    model = Workshop
    serializer_class = WorkshopSerializer
    template_name = "workshop/detail_workshop.html"

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
    
    def get(self, request, pk, *args, **kwargs):
        # Retrieve the workshop based on the primary key (pk)
        try:
            workshop = Workshop.objects.get(pk=pk)
        except Workshop.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        
        serializer = WorkshopSerializer(workshop)
        return Response(serializer.data)

"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshop_id'] = self.kwargs.get('pk')
        return context
"""

class CreateWorkshop(PermissionRequiredMixin, CreateAPIView):
    form_class = WorkshopForm
    serializer_class = WorkshopSerializer
    template_name = "workshop/create_workshop.html"
    permission_required = 'workshop.add_workshop'
    queryset = Workshop.objects.all()

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

class EditWorkshop(UserIsWorkshopAdminMixin, RetrieveUpdateAPIView):
    form_class = WorkshopForm
    serializer_class = WorkshopSerializer
    template_name = "workshop/edit_workshop.html"
    success_url = ""
    queryset = Workshop.objects.all()
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

class DeleteWorkshop(UserIsWorkshopAdminMixin, DestroyAPIView):
    model = Workshop
    serializer_class = WorkshopSerializer
    template_name = 'workshop/delete_workshop.html'
    success_url= "/workshop/"
    queryset = Workshop.objects.all()
    # permission_required = 'workshop.delete_workshop'

    def get_queryset(self):
        return Workshop.objects.all()
    
    def delete():
        return super(DeleteWorkshop, self).delete()
    
    # naming should be more class-specific, not method specific

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def has_permission(self, request):
        is_staff = request.user.is_staff
        is_workshop_admin = request.user.groups.filter(name='Workshop Administrator').exists()
        return is_staff or in_workshop_admin_group

    @action(detail=False, methods=['get'], serializer_class=ToolSerializer,)
    def get(self, request, pk=None):
        query_params = request.query_params

        if not query_params:
            return Response({"error": "No filtering parameters provided"}, status=status.HTTP_400_BAD_REQUEST)

        filters = Q()
        for field, value in query_params.items():
            filters |= Q(**{f"{field}__icontains": value})

        # Filter the tools based on the query parameters
        tools = Tool.objects.filter(filters)

        if not tools.exists():
            return Response({"error": "No tools found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the results
        serializer = ToolSerializer(tools, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Create a new tool

        if not self.has_permission(request):
            return Response({"error": "You do not have permission."})

        serializer = ToolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, pk):
        # Update an existing tool

        if not self.has_permission(request):
            return Response({"error": "You do not have permission."})

        tool = get_object_or_404(Tool, pk=pk)
        serializer = ToolSerializer(tool, data=request.data, partial=True)  # Enables updating model partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        # Delete a tool

        if not self.has_permission(request):
            return Response({"error": "You do not have permission."})

        tool = get_object_or_404(Tool, pk=pk)
        tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

