from django import forms
from django.forms import inlineformset_factory
from .models import Workshop, Tool, Prerequisite

class WorkshopForm(forms.ModelForm):
    tools = forms.ModelMultipleChoiceField(
        queryset=Tool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    prerequisites = forms.ModelMultipleChoiceField(
        queryset=Prerequisite.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Workshop
        fields = "__all__"
