from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from django_project.category_app.views import CategoryViewSet

router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
