from rest_framework import filters, generics, response, status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from procurement import serializers
from helpers.utils import get_objet_summary
from helpers import permissions
from helpers.view import CreateUpdateMixin
from procurement.models import Procurements
from procurement.permissions import IsProcurementEditable

# Create your views here.


class ProcurementsAPIRUDView(CreateUpdateMixin,
                             generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly,
                          IsProcurementEditable)

    detail_serializer_class = serializers.ProcurementsDetailsSerializer
    serializer_class = serializers.ProcurementsPostSerializer

    def get_queryset(self):
        return Procurements.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return self.serializer_class


class ProcurementsListAPIView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['id', 'total_price', 'comment', 'statut',
                     'added_by__first_name', 'added_by__last_name', 'budget', 'created_at']
    filterset_field = ['id', 'statut']
    serializer_class = serializers.ProcurementsListSerializer

    def get_queryset(self):
        return Procurements.objects.all()


class ProcurementsSummaryAPIView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,)
    serializer_class = serializers.ProcurementsPostSerializer

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get(
            'start_date', timezone.now()-timedelta(hours=8))
        end_date = request.GET.get('end_date', timezone.now())
        ingeredient_ids = request.GET.get('ingeredient_ids', '')
        if ingeredient_ids:
            spoil_ingredients = get_objet_summary(Procurements, start_date, end_date).filter(
                itemingredients__ingredient_id__in=ingeredient_ids, statut="APPROVED")
        else:
            spoil_ingredients = get_objet_summary(
                Procurements, start_date, end_date).filter(statut="APPROVED")
        total_price = 0
        for spoil_ingredient in spoil_ingredients:
            total_price += spoil_ingredient.total_price

        serializer = self.serializer_class(data={"number_items": len(spoil_ingredients),
                                                 "total_price": total_price})

        return response.Response(serializer.initial_data, status=status.HTTP_200_OK)


class ValidationAPIView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserManagerOrReadOnly)
    serializer_class = serializers.ValidationProcSerializer

    def create(self, request, pk=None):
        procurements = get_object_or_404(Procurements, id=pk)
        serializer = self.serializer_class(
            data=request.data, context={"procurements": procurements, })
        if serializer.is_valid():
            if serializer.validated_data['statut']:
                procurements.statut = "CLOSED"
            else:
                procurements.statut = "REJECTED"
            serializer.save(added_by=self.request.user,
                            procurements=procurements, )
            procurements.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
