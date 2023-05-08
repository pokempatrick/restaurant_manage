from dishes import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('ingredient', views.IngredientViewSet, basename='ingredient')
router.register('dish', views.DishViewSet, basename='dish')
urlpatterns = [
    path('itemingredient/',
         views.ItemIngredientsListView.as_view(), name='item_ingredient'),

]
urlpatterns += router.urls
