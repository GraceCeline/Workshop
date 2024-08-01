from django import forms
from django.forms import inlineformset_factory
from .models import Workshop, Tool, Prerequisite

class WorkshopForm(forms.ModelForm): 
    tool = forms.ModelMultipleChoiceField(
        queryset=Tool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    prerequisite = forms.ModelMultipleChoiceField(
        queryset=Prerequisite.objects.all(),
        widget=forms.CheckboxSelectMultiple
    ) 
    class Meta:
        model = Workshop
        fields = "__all__"

"""
class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['tool']

class PrerequisiteForm(forms.ModelForm):
    class Meta:
        model = Prerequisite
        fields = ['prerequisite']

ToolFormSet = inlineformset_factory(
    Workshop, Tool, form=ToolForm, extra=3
)

PrerequisiteFormSet = inlineformset_factory(
    Workshop, Prerequisite, form=PrerequisiteForm, extra=3
)
"""