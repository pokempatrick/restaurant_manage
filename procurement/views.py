from django.shortcuts import render
from rest_framework import viewsets, filters, generics, mixins, response, status
from procurement import serializers
from helpers import permissions
from helpers.view import CreateUpdateMixin
from procurement.models import Procurements
from procurement.permissions import IsProcurementEditable
from django.shortcuts import get_object_or_404

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
