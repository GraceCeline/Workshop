from .models import Workshop, Tool
from django.contrib.auth.models import User
from rest_framework import serializers

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        exclude = ('tutor',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        tools=validated_data["tool"]
        del validated_data["tool"]
        workshop= Workshop.objects.create(**validated_data)
        workshop.tool.set(tools)
        return workshop

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = "__all__"

    def create(self, validated_data):
        tool = Tool.objects.create(**validated_data)
        return tool