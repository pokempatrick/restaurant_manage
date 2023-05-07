from django.shortcuts import render
from rest_framework import viewsets, filters
from dishes.models import Dish, Ingredient
from dishes import serializers as dishes_serializers
from helpers import permissions
from helpers.view import CreateUpdateMixin


class DishViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'name',
                     'created_by__first_name',
                     'create_by__last_name', 'description', 'unit_price']

    detail_serializer_class = dishes_serializers.DishDetailsSerializer
    list_serialiser_class = dishes_serializers.DishListSerializer
    serializer_class = dishes_serializers.DishSerializer

    def get_queryset(self):
        return Dish.objects.all()


class IngredientViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserTechnicianOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'name',
                     'created_by__first_name',
                     'create_by__last_name', 'description', 'unit_price']

    detail_serializer_class = dishes_serializers.IngredientDetailsSerializer
    list_serialiser_class = dishes_serializers.IngredientListSerializer
    serializer_class = dishes_serializers.IngredientSerializer

    def get_queryset(self):
        return Ingredient.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (permissions.HasCookerRole,)
        return super().destroy(request, *args, **kwargs)
