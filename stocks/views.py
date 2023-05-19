from rest_framework import filters, generics
from stocks import serializers
from helpers import permissions
from stocks.models import Stocks

# Create your views here.


class StocksListAPIView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['id', 'ingredient__name', 'ingredient__group',
                     'ingredient__unit_price', 'dish__name', 'dish__unit_price',
                     'updated_at', 'created_at', 'quantity',
                     ]
    filterset_field = ['id', 'quantity', ]
    serializer_class = serializers.StocksSerializer

    def get_queryset(self):
        return Stocks.objects.all()
