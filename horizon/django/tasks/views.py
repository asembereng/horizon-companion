"""
Task views.

Chapter 23 (Coding Agent): AI-generated TaskViewSet with review corrections.
"""

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAssigneeOrProjectAdmin


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAssigneeOrProjectAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "assignee"]
    ordering_fields = ["priority", "created_at"]
    ordering = ["-priority", "created_at"]
