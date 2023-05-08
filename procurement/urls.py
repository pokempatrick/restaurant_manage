from procurement import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('procurements', views.ProcurementsViewSet,
                basename='procurements')
urlpatterns = [
    path('procurements/<str:pk>/validations/',
         views.ValidationAPIView.as_view(), name='validations_procurements'),
]
urlpatterns += router.urls
