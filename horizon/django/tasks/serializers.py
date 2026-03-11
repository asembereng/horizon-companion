"""
Task serializers.

Chapter 18 (Bridge Section): serializer evaluation example.
Chapter 23 (Coding Agent): AI-generated serializer with explicit field lists.
"""

from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status", "priority", "assignee", "project", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
