from rest_framework import viewsets, filters
from sale_spoil import serializers
from sale_spoil.models import SpoilDish, SpoilIngredient, Sale
from helpers import permissions
from sale_spoil.permissions import IsAccountable, IsEditable
# from sale_spoil.permissions import IsEditable
from helpers.view import CreateUpdateMixin

# Create your views here.


class SaleViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          IsAccountable, IsEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'added_by__first_name', 'added_by__last_name',
                       'dishlist_set__dish_name']

    search_fields = ['id', 'created_at', 'updated_at',
                     'added_by__first_name', 'added_by__last_name',
                     'dishlist_set__dish_name']

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
