"""
Horizon URL configuration.

Chapter 23 (Coding Agent): urlpatterns + ViewSet auto-routing.
The DRF router automatically generates URL patterns for CRUD operations.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from tasks.views import TaskViewSet
from projects.views import ProjectViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/health/", lambda request: __import__("django.http", fromlist=["JsonResponse"]).JsonResponse(
        {"status": "ok", "service": "horizon-django"}
    )),
]
