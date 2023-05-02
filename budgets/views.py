from django.shortcuts import render
from rest_framework import viewsets, filters, generics, mixins
from budgets.models import Budgets, DishBudgets, Dish, Ingredient
from budgets import serializers
from helpers.permission import IsAuthenficatedOnly, IsUserCookerOrReadOnly, IsUserTechnicianOrReadOnly, IsUserOwner, HasCookerRole
from helpers.view import CreateUpdateMixin


class BudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (IsAuthenficatedOnly, IsUserCookerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'description',
                     'statut', 'start_date', 'end_date',
                     'added_by__first_name', 'added_by__last_name',
                     'dishbudgets__dish_name', 'dishbudgets__dish_quantity']

    detail_serializer_class = serializers.BudgetsDetailsSerializer
    serializer_class = serializers.BudgetsSerializer

    def get_queryset(self):
        return Budgets.objects.all()


class DishBudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (IsAuthenficatedOnly, IsUserCookerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'total_price',
                     'created_at',
                     'dish_name', 'dish_quantity']

    detail_serializer_class = serializers.DishBudgetsDetailsSerializer
    list_serialiser_class = serializers.DishBudgetsSerializer
    serializer_class = serializers.DishBudgetsPostSerializer

    def get_queryset(self):
        return DishBudgets.objects.all()


class DishViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (IsAuthenficatedOnly, IsUserCookerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'name',
                     'created_by__first_name',
                     'create_by__last_name', 'description', 'unit_price']

    detail_serializer_class = serializers.DishDetailsSerializer
    list_serialiser_class = serializers.DishListSerializer
    serializer_class = serializers.DishSerializer

    def get_queryset(self):
        return Dish.objects.all()


class IngredientViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (IsAuthenficatedOnly, IsUserTechnicianOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'name',
                     'created_by__first_name',
                     'create_by__last_name', 'description', 'unit_price']

    detail_serializer_class = serializers.IngredientDetailsSerializer
    list_serialiser_class = serializers.IngredientListSerializer
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        return Ingredient.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (HasCookerRole,)
        return super().destroy(request, *args, **kwargs)
