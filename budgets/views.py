from django.shortcuts import render
from rest_framework import viewsets, filters, generics, mixins, response, status
from budgets.models import Budgets, DishBudgets
from authentification.models import User
from django.shortcuts import get_object_or_404
from budgets import serializers as budgets_serializers
from budgets.permissions import IsBudgetEditable
from helpers import permissions
from helpers.view import CreateUpdateMixin


class BudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly, IsBudgetEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'description',
                     'statut', 'start_date', 'end_date',
                     'added_by__first_name', 'added_by__last_name',
                     'dishbudgets__dish_name', 'dishbudgets__dish_quantity', 'dishbudgets__dish_id']

    detail_serializer_class = budgets_serializers.BudgetsDetailsSerializer
    serializer_class = budgets_serializers.BudgetsSerializer

    def get_queryset(self):
        return Budgets.objects.all()


class DishBudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly,
                          IsBudgetEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'total_price',
                     'created_at',
                     'dish_name', 'dish_quantity', 'dish_id']

    detail_serializer_class = budgets_serializers.DishBudgetsDetailsSerializer
    list_serialiser_class = budgets_serializers.DishBudgetsSerializer
    serializer_class = budgets_serializers.DishBudgetsPostSerializer

    def get_queryset(self):
        return DishBudgets.objects.all()


class ValidationAPIView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserManagerOrReadOnly)
    serializer_class = budgets_serializers.ValidationBudSerializer

    def create(self, request, pk=None):
        assign_user_id = request.data.pop("assign_user")
        budgets = get_object_or_404(Budgets, id=pk)
        assign_user = get_object_or_404(User, id=assign_user_id)
        serializer = self.serializer_class(
            data=request.data, context={"budgets": budgets, "assign_user": assign_user})
        if serializer.is_valid():
            if serializer.validated_data['statut']:
                budgets.statut = "VALIDATED"
            else:
                budgets.statut = "REJECTED"
            serializer.save(added_by=self.request.user,
                            budgets=budgets, assign_user=assign_user)
            budgets.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
