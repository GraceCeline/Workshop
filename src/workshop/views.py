from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.middleware.csrf import get_token
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views import generic
from .models import Tool, Workshop, Timeslot
from .forms import  ToolForm, WorkshopForm, RegistrationForm, TimeslotForm, WorkshopFormSet
from .serializers import WorkshopSerializer, ToolSerializer
import logging
import random
from django.views.decorators.csrf import ensure_csrf_cookie

class UserIsWorkshopAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        workshop = self.get_object()

        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        if workshop.tutor != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class CsrfTokenView(APIView):
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)  # Retrieve CSRF token
        return JsonResponse({'csrfToken': csrf_token})  # Return token as JSON

"""
class MyLoginView(LoginView):
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('login_redirect')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
"""
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful.",
                "token": token.key,
                "username": user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

"""
class LoginRedirectView(generic.TemplateView):
    template_name = 'registration/login_redirect.html'

class LogoutRedirectView(generic.TemplateView):
    template_name = 'registration/logout.html'
"""

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "options"]

    def options(self, request, *args, **kwargs):
        response = Response()
        response['Access-Control-Allow-Origin'] = 'http://localhost:4200'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    def post(self, request, *args, **kwargs):
        request.auth.delete()  # Delete the token to log out the user
        logout(request)
        return Response({"message": "Logged out successfully"}, status=200)


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""
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
 """   
class RandomHTTPView(APIView):
    def get(self, request, *args, **kwargs):
        # List of HTTP status codes to randomly choose from
        http_codes = [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ]

        # Select a random HTTP status code
        random_code = random.choice(http_codes)

        # Return the random status code in the response
        return Response({"message": f"Random HTTP Code: {random_code}"}, status=random_code)

class RegisterAPIView (APIView):
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully.",
                "token": token.key
            }, status = status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class ListWorkshop(ListAPIView):
    serializer_class = WorkshopSerializer
    template_name = "workshop/homepage.html"
    context_object_name = "workshop_list"
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny] 
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


class DetailWorkshop(APIView):
    model = Workshop
    serializer_class = WorkshopSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]
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

        # if not self.request.user.is_authenticated:
        #     queryset = queryset.filter(is_private=False)

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

class CreateWorkshop(CreateAPIView):
    form_class = WorkshopForm
    serializer_class = WorkshopSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]
    template_name = "workshop/create_workshop.html"
    permission_required = 'workshop.add_workshop'
    queryset = Workshop.objects.all()

    def get_success_url(self):
        # Return the URL to redirect after successful creation
        return redirect('workshop:list') 

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
            
            return HttpResponse(response_data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)  # or use logging for production
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # return HttpResponseRedirect(reverse('workshop:list'))

class EditWorkshop( RetrieveUpdateAPIView):
    form_class = WorkshopForm
    serializer_class = WorkshopSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]
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
            return HttpResponseRedirect(reverse('workshop:list'), status=status.HTTP_200_OK)
        else:
            return self.form_invalid(form)
    
    def get_queryset(self):
        return Workshop.objects.all()

class DeleteWorkshop(DestroyAPIView):
    model = Workshop
    serializer_class = WorkshopSerializer
    template_name = 'workshop/delete_workshop.html'
    success_url= "/workshop/"
    queryset = Workshop.objects.all()
    # permission_required = 'workshop.delete_workshop'

    def get_queryset(self):
        return Workshop.objects.all()
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # naming should be more class-specific, not method specific

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

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

