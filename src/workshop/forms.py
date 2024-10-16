from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import Workshop, Tool, Timeslot
from django.forms.widgets import DateInput, TimeInput

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

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

class TimeslotForm(forms.ModelForm):
    class Meta:
        model = Timeslot
        fields = ['topic', 'start_time', 'end_time']

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['tool']
        
class WorkshopForm(forms.ModelForm): 
    tool = forms.ModelMultipleChoiceField(
        queryset=Tool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Workshop
        exclude = ('tutor',)
        widgets = {
            'date': DateInput(format='%d/%m/%Y'),
            'start_time' : TimeInput(format='%H:%M'),
            'end_time' : TimeInput(format='%H:%M'),
            'registration_deadline' : DateInput(),
        }

WorkshopFormSet = inlineformset_factory(Workshop, Timeslot, form=WorkshopForm, extra=3, can_delete=False)
