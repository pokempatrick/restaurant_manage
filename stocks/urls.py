from stocks import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
    path('stocks/',
         views.StocksListAPIView.as_view(), name='stocks-list'),
]
urlpatterns += router.urls
