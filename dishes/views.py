from dishes.utils import root_query_set
from rest_framework import viewsets, filters, generics, request
from datetime import timedelta
from django.utils import timezone
from dishes.models import Dish, Ingredient, ItemIngredients
from dishes import serializers
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

    detail_serializer_class = serializers.DishDetailsSerializer
    list_serialiser_class = serializers.DishRetrieveListSerializer
    serializer_class = serializers.DishSerializer

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

    detail_serializer_class = serializers.IngredientDetailsSerializer
    list_serialiser_class = serializers.IngredientListSerializer
    serializer_class = serializers.IngredientSerializer

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

    serializer_class = serializers.ItemIngredientsSerializer

    def get_queryset(self):
        return ItemIngredients.objects.all()


class ItemIngredientsListSummaryView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenficatedOnly,)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['ingredient_id', 'ingredient_name', ]
    search_fields = ['ingredient_name']

    serializer_class = serializers.ItemIngredientsSummarySerializer

    def get_queryset(self):
        start_date = self.request.GET.get(
            'start_date', timezone.now()-timedelta(hours=24))
        end_date = self.request.GET.get('end_date', timezone.now())
        process = self.request.GET.get('process', 'inventory')
        return root_query_set(
            start_date=start_date,
            end_date=end_date,
            process=process)
