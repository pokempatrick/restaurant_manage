from django.shortcuts import render
from rest_framework import viewsets, filters, generics, mixins, response, status
from procurement import serializers
from helpers import permissions
from helpers.view import CreateUpdateMixin
from procurement.models import Procurements
from procurement.permissions import IsProcurementEditable
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# Create your views here.


class DishResultViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = None
    search_fields = None
    detail_serializer_class = None
    serializer_class = None

    @action(detail=True, methods=['post'], url_path='dish_result_list', url_name='dish_result_list_create')
    def dish_result_list_create(self, request, pk=None):
        pass

    pass


class DishResultListAPIRUDView(CreateUpdateMixin,
                               generics.RetrieveUpdateDestroyAPIView):
    permission_classes = None
    detail_serializer_class = None
    serializer_class = None
    pass


class DishResultListListAPIView(generics.ListAPIView):
    permission_classes = None
    filter_backends = (filters.SearchFilter,)
    filterset_field = None
    search_fields = None
    detail_serializer_class = None
    serializer_class = None

    pass


class ValidationAPIView(generics.CreateAPIView):
    permission_classes = None
    serializer_class = None

    pass
