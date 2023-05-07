from dishes import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('ingredient', views.IngredientViewSet, basename='ingredient')
router.register('dish', views.DishViewSet, basename='dish')

urlpatterns = router.urls
