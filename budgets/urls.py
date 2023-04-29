from django.urls import path
from budgets import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('budgets', views.BudjetsViewSet, basename='budgets')

urlpatterns = router.urls
