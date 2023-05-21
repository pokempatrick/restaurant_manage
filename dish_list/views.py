from django.db.models import Sum, Count
from datetime import timedelta
from helpers.utils import get_objet_summary
from django.utils import timezone
from rest_framework import viewsets, filters, generics, response, status, request
from dish_list import serializers
from dish_list.models import DishResult, DishListResult
from helpers import permissions
from dish_list.permissions import IsDishResultEditable
from helpers.view import CreateUpdateMixin
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# Create your views here.


class DishResultViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly, IsDishResultEditable)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'statut',
                       'added_by__first_name', 'added_by__last_name',]
    search_fields = ['id', 'comment',
                     'statut', 'start_date', 'end_date',
                     'added_by__first_name', 'added_by__last_name',
                     'dishlistresult__dish_name', 'dishlistresult__dish_quantity',
                     'dishlistresult__dish_id']
    detail_serializer_class = serializers.DishResultDetailsSerializer
    serializer_class = serializers.DishResultSerializer

    def get_queryset(self):
        return DishResult.objects.all()

    @action(detail=True, methods=['post'], url_path='dish_list_result', url_name='dish_list_result_create')
    def dish_result_list_create(self, request, pk=None):
        self.serializer_class = serializers.DishListResultPostSerializer
        self.permission_classes = (IsDishResultEditable,)
        dish_result = self.get_object()
        return super().create(request, dish_result=dish_result)


class DishListResultAPIRUDView(CreateUpdateMixin,
                               generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserCookerOrReadOnly, IsDishResultEditable)
    detail_serializer_class = serializers.DishListResultDetailsSerializer
    serializer_class = serializers.DishListResultPostSerializer

    def get_queryset(self):
        return DishListResult.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return self.serializer_class


class DishListResultListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenficatedOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['id', 'dish_result__id']
    search_fields = ['id', 'total_price',
                     'created_at',
                     'dish_name', 'dish_quantity', 'dish_id']
    serializer_class = serializers.DishListResultSerializer

    def get_queryset(self):
        return DishListResult.objects.all()


class DishResultSummaryAPIView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenficatedOnly,)
    serializer_class = serializers.DishListResultSerializer

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get(
            'start_date', timezone.now()-timedelta(hours=8))
        end_date = request.GET.get('end_date', timezone.now())
        dish_ids = request.GET.get('dish_ids', '')
        if dish_ids:
            dish_results = get_objet_summary(DishResult, start_date, end_date).filter(
                dishlistresult__dish_id__in=dish_ids, statut="APPROVED")
        else:
            dish_results = get_objet_summary(
                DishResult, start_date, end_date).filter(statut="APPROVED")
        total_price = 0
        for dish_result in dish_results:
            total_price += dish_result.total_price

        serializer = self.serializer_class(data={"number_items": len(dish_results),
                                                 "total_price": total_price})

        return response.Response(serializer.initial_data, status=status.HTTP_200_OK)


class ValidationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenficatedOnly,
                          permissions.IsUserManagerOrReadOnly)
    serializer_class = serializers.ValidationDishResultSerializer

    def create(self, request, pk=None):
        dish_result = get_object_or_404(DishResult, id=pk)
        serializer = self.serializer_class(
            data=request.data, context={"dish_result": dish_result, })
        if serializer.is_valid():
            if serializer.validated_data['statut']:
                dish_result.statut = "APPROVED"
            else:
                dish_result.statut = "REJECTED"
            serializer.save(added_by=self.request.user,
                            dish_result=dish_result, )
            dish_result.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
