from django.shortcuts import render
from rest_framework import viewsets, filters, generics, mixins
from budgets.models import Budgets, DishBudgets
from budgets import serializers
from helpers.permission import IsAuthenficatedOnly, IsUserCookerOrReadOnly
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
