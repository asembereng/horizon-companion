"""
Task permissions.

Chapter 23 (Coding Agent): Corrected version of IsAssigneeOrProjectAdmin.

The AI-generated version (IsAssigneeOrAdmin) used ``request.user.is_staff``
which was too broad.  The review-corrected version below checks the actual
project admin, matching the business rule.
"""

from rest_framework import permissions


class IsAssigneeOrProjectAdmin(permissions.BasePermission):
    """Only the task assignee or the project admin may modify a task."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.assignee == request.user
                or obj.project.admin == request.user)
