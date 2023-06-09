from django.urls import path, include
from budgets import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('budgets', views.BudjetsViewSet, basename='budgets')
router.register('dish_budget', views.DishBudjetsViewSet,
                basename='dish_budget')
urlpatterns = [
    path('budgets/<str:pk>/validations/',
         views.ValidationAPIView.as_view(), name='validations_budget'),
]
urlpatterns += router.urls
