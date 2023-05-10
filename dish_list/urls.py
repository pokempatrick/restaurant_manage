from dish_list import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()


router.register('dish_result', views.DishResultViewSet, basename='dish_result')

urlpatterns = [
    path('dish_result/<str:pk>/validations/',
         views.ValidationAPIView.as_view(), name='validations_dish_result'),
    path('dish_list_result/<str:pk>/',
         views.DishListResultAPIRUDView.as_view(), name='dish_list_result'),
    path('dish_list_result/',
         views.DishListResultListAPIView.as_view(), name='dish_list_result-list'),
]
urlpatterns += router.urls
