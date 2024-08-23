from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import Workshop, Tool
from django.forms.widgets import DateInput, TimeInput

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "groups"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    
class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

class WorkshopForm(forms.ModelForm): 
    tool = forms.ModelMultipleChoiceField(
        queryset=Tool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Workshop
        fields = "__all__"
        widgets = {
            'date': DateInput(format='%d/%m/%Y'),
            'start_time' : TimeInput(format='%H:%M'),
            'end_time' : TimeInput(format='%H:%M'),
            'registration_deadline' : DateInput(),
        }

"""
class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['tool']

"""