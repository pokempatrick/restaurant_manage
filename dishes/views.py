from django.shortcuts import render
from rest_framework import viewsets, filters, generics
from dishes.models import Dish, Ingredient, ItemIngredients
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
    filterset_field = ['id', 'name',
                       'created_by__first_name',
                       'create_by__last_name', 'description', 'unit_price']

    detail_serializer_class = dishes_serializers.DishDetailsSerializer
    list_serialiser_class = dishes_serializers.DishRetrieveListSerializer
    serializer_class = dishes_serializers.DishSerializer

    def get_queryset(self):
        return Dish.objects.all()


class IngredientViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserTechnicianOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    filterset_field = ['id', 'name',
                       'created_by__first_name',
                       'create_by__last_name', 'description', 'unit_price']
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


class ItemIngredientsListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenficatedOnly,)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['dish_budget__budget__id',
                       'ingredient_name', 'unit_price']
    search_fields = ['id', 'dish_budget__budget__id',
                     'procurement__id', 'ingredient_name', 'unit_price']

    serializer_class = dishes_serializers.ItemIngredientsSerializer

    def get_queryset(self):
        return ItemIngredients.objects.all()
