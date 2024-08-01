from django.contrib import admin
from .models import Tool, Prerequisite, Workshop

admin.site.register(Tool)
admin.site.register(Prerequisite)
admin.site.register(Workshop)

# Register your models here.
