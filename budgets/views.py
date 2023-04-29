from django.shortcuts import render
from rest_framework import viewsets, filters
from budgets.models import Budgets, DishBudgets, ItemIngredients
from budgets.serializers import BudgetsSerializer, BudgetsDetailsSerializer
from helpers.permission import IsAuthenficatedOnly, IsUserCookerOrReadOnly
from helpers.view import CreateUpdateMixin


class BudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (IsAuthenficatedOnly, IsUserCookerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'description',
                     'statut', 'start_date', 'end_date',
                     'added_by__first_name', 'added_by__last_name',
                     'dishbudgets__dish_name']

    detail_serializer_class = BudgetsDetailsSerializer
    serializer_class = BudgetsSerializer
    Object = Budgets
