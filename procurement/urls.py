from procurement import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
    path('procurements/<str:pk>/validations/',
         views.ValidationAPIView.as_view(), name='validations_procurements'),
    path('procurements/summary/',
         views.ProcurementsSummaryAPIView.as_view(), name='procurements_summary'),
    path('procurements/<str:pk>/',
         views.ProcurementsAPIRUDView.as_view(), name='procurements'),
    path('procurements/',
         views.ProcurementsListAPIView.as_view(), name='procurements-list'),
]
urlpatterns += router.urls
