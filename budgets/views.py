from django.shortcuts import render
from rest_framework import viewsets, filters, generics, mixins, response, status
from budgets.models import Budgets, DishBudgets, Dish, Ingredient
from django.shortcuts import get_object_or_404
from budgets import serializers
from helpers import permissions
from helpers.view import CreateUpdateMixin


class BudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly, permissions.IsBudgetEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'description',
                     'statut', 'start_date', 'end_date',
                     'added_by__first_name', 'added_by__last_name',
                     'dishbudgets__dish_name', 'dishbudgets__dish_quantity', 'dishbudgets__dish_id']

    detail_serializer_class = serializers.BudgetsDetailsSerializer
    serializer_class = serializers.BudgetsSerializer

    def get_queryset(self):
        return Budgets.objects.all()


class DishBudjetsViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly,
                          permissions.IsBudgetEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'total_price',
                     'created_at',
                     'dish_name', 'dish_quantity', 'dish_id']

    detail_serializer_class = serializers.DishBudgetsDetailsSerializer
    list_serialiser_class = serializers.DishBudgetsSerializer
    serializer_class = serializers.DishBudgetsPostSerializer

    def get_queryset(self):
        return DishBudgets.objects.all()


class DishViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly)
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
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserTechnicianOrReadOnly)
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
        self.permission_classes = (permissions.HasCookerRole,)
        return super().destroy(request, *args, **kwargs)


class ValidationAPIView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserManagerOrReadOnly)
    serializer_class = serializers.ValidationSerializer

    def create(self, request, pk=None):
        budgets = get_object_or_404(Budgets, id=pk)
        serializer = self.serializer_class(
            data=request.data, context={"budgets": budgets})
        if serializer.is_valid():
            if serializer.validated_data['statut']:
                budgets.statut = "VALIDATED"
            else:
                budgets.statut = "REJECTED"
            serializer.save(added_by=self.request.user, budgets=budgets)
            budgets.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
