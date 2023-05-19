from rest_framework import viewsets, filters, generics, response, status
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from helpers.utils import get_objet_summary
from inventories import serializers
from inventories.models import Inventories
from helpers import permissions
from inventories.permissions import IsInventoriesEditable
from helpers.view import CreateUpdateMixin

# Create your views here.


class InventoriesViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          IsInventoriesEditable, permissions.IsUserTechnicianOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'added_by__first_name', 'added_by__last_name',
                       'itemingredients_set__ingredient_name']

    search_fields = ['id', 'created_at', 'updated_at',
                     'added_by__first_name', 'added_by__last_name',
                     'itemingredients_set__ingredient_name']

    detail_serializer_class = serializers.InventoriesDetailsSerializer
    list_serialiser_class = serializers.InventoriesListSerializer
    serializer_class = serializers.InventoriesPostSerializer

    def get_queryset(self):
        return Inventories.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsUserOwnerOrReadOnly,)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_name='inventories_summary')
    def summary(self, request):
        start_date = request.GET.get(
            'start_date', timezone.now()-timedelta(hours=8))
        end_date = request.GET.get('end_date', timezone.now())
        ingredient_ids = request.GET.get('ingredient_ids', '')
        if ingredient_ids:
            inventories = get_objet_summary(Inventories, start_date, end_date).filter(
                itemingredients__ingredient_id__in=ingredient_ids, statut="APPROVED")
        else:
            inventories = get_objet_summary(
                Inventories, start_date, end_date).filter(statut="APPROVED")

        total_lost = 0
        for inventory in inventories:
            total_lost += inventory.total_lost

        serializer = self.serializer_class(data={"number_items": len(inventories),
                                                 "total_lost": total_lost})

        return response.Response(serializer.initial_data, status=status.HTTP_200_OK)


class ValidationAPIView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserManagerOrReadOnly)
    serializer_class = serializers.ValidationInvSerializer

    def create(self, request, pk=None):
        inventory = get_object_or_404(Inventories, id=pk)
        serializer = self.serializer_class(
            data=request.data, context={"inventory": inventory, })
        if serializer.is_valid():
            if serializer.validated_data['statut']:
                inventory.statut = "APPROVED"
            else:
                inventory.statut = "REJECTED"
            serializer.save(added_by=self.request.user,
                            inventory=inventory, )
            inventory.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
