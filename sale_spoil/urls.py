from sale_spoil import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('sale', views.SaleViewSet, basename='sale')
router.register('spoil-dish', views.SpoilDishViewSet, basename='spoil-dish')
router.register('spoil-ingredient', views.SpoilIngredientViewSet,
                basename='spoil-ingredient')
urlpatterns = [
    path('dish-summary/',
         views.DishListSummaryView.as_view(), name='dish_summary'),
]
urlpatterns += router.urls
