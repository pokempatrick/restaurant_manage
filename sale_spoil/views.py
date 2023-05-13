from rest_framework import viewsets, filters, response, status
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from helpers.utils import get_objet_summary
from sale_spoil import serializers
from sale_spoil.models import SpoilDish, SpoilIngredient, Sale
from helpers import permissions
from sale_spoil.permissions import IsAccountable, IsEditable
from helpers.view import CreateUpdateMixin

# Create your views here.


class SaleViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          IsAccountable, IsEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'added_by__first_name', 'added_by__last_name',
                       'dishlist__dish_name']

    search_fields = ['id', 'created_at', 'updated_at',
                     'added_by__first_name', 'added_by__last_name',
                     'dishlist__dish_name']

    detail_serializer_class = serializers.SaleDetailsSerializer
    list_serialiser_class = serializers.SaleSerializer
    serializer_class = serializers.SalePostSerializer

    def get_queryset(self):
        return Sale.objects.all()

    def update(self, request, pk=None, **kwargs):
        self.permission_classes = (permissions.HasOWNERRole,)
        return super().update(request, pk, **kwargs)

    def partial_update(self, request, pk=None, **kwargs):
        self.permission_classes = (permissions.HasOWNERRole,)
        return super().partial_update(request, pk, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (permissions.HasOWNERRole,)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_name='sale_summary')
    def summary(self, request):
        start_date = request.GET.get(
            'start_date', timezone.now()-timedelta(hours=8))
        end_date = request.GET.get('end_date', timezone.now())
        dish_ids = request.GET.get('dish_ids', '')
        if dish_ids:
            sales = get_objet_summary(Sale, start_date, end_date).filter(
                dishlist__dish_id__in=dish_ids)
        else:
            sales = get_objet_summary(Sale, start_date, end_date)
        total_price = 0
        for sale in sales:
            total_price += sale.total_price

        serializer = self.serializer_class(data={"number_items": len(sales),
                                                 "total_price": total_price})

        return response.Response(serializer.initial_data, status=status.HTTP_200_OK)


class SpoilDishViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly, IsEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'added_by__first_name', 'added_by__last_name',
                       'dishlist_set__dish_name']

    search_fields = ['id', 'created_at', 'updated_at',
                     'added_by__first_name', 'added_by__last_name',
                     'dishlist_set__dish_name']

    detail_serializer_class = serializers.SpoilDishDetailsSerializer
    list_serialiser_class = serializers.SpoilDishSerializer
    serializer_class = serializers.SpoilDishPostSerializer

    def get_queryset(self):
        return SpoilDish.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsUserOwnerOrReadOnly,)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_name='spoil_dish_summary')
    def summary(self, request):
        start_date = request.GET.get(
            'start_date', timezone.now()-timedelta(hours=8))
        end_date = request.GET.get('end_date', timezone.now())
        dish_ids = request.GET.get('dish_ids', '')
        if dish_ids:
            spoil_dishes = get_objet_summary(SpoilDish, start_date, end_date).filter(
                dishlist__dish_id__in=dish_ids)
        else:
            spoil_dishes = get_objet_summary(SpoilDish, start_date, end_date)
        total_price = 0
        for spoil_dish in spoil_dishes:
            total_price += spoil_dish.total_price

        serializer = self.serializer_class(data={"number_items": len(spoil_dishes),
                                                 "total_price": total_price})

        return response.Response(serializer.initial_data, status=status.HTTP_200_OK)


class SpoilIngredientViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          IsEditable, permissions.IsUserTechnicianOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'added_by__first_name', 'added_by__last_name',
                       'itemingredients_set__ingredient_name']

    search_fields = ['id', 'created_at', 'updated_at',
                     'added_by__first_name', 'added_by__last_name',
                     'itemingredients_set__ingredient_name']

    detail_serializer_class = serializers.SpoilIngredientDetailsSerializer
    list_serialiser_class = serializers.SpoilIngredientSerializer
    serializer_class = serializers.SpoilIngredientPostSerializer

    def get_queryset(self):
        return SpoilIngredient.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsUserOwnerOrReadOnly,)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_name='spoil_dish_summary')
    def summary(self, request):
        start_date = request.GET.get(
            'start_date', timezone.now()-timedelta(hours=8))
        end_date = request.GET.get('end_date', timezone.now())
        ingeredient_ids = request.GET.get('ingeredient_ids', '')
        if ingeredient_ids:
            spoil_ingredients = get_objet_summary(SpoilIngredient, start_date, end_date).filter(
                itemingredients__ingredient_id__in=ingeredient_ids)
        else:
            spoil_ingredients = get_objet_summary(
                SpoilIngredient, start_date, end_date)
        total_price = 0
        for spoil_ingredient in spoil_ingredients:
            total_price += spoil_ingredient.total_price

        serializer = self.serializer_class(data={"number_items": len(spoil_ingredients),
                                                 "total_price": total_price})

        return response.Response(serializer.initial_data, status=status.HTTP_200_OK)
