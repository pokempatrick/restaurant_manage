from inventories import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('inventories', views.InventoriesViewSet,
                basename='inventories')
urlpatterns = [
    path('inventories/<str:pk>/validations/',
         views.ValidationAPIView.as_view(), name='validations_inventories'),
]
urlpatterns += router.urls
