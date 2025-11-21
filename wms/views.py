from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Warehouse, Location, Stock
from .serializers import WarehouseSerializer, LocationSerializer, StockSerializer
from accounts.permissions import IsAdmin

class WarehouseListCreateView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all().order_by('id')
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']
    permission_classes = [IsAuthenticated, IsAdmin]


class WarehouseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all().order_by('id')
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.select_related('warehouse').all().order_by('id')
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'code', 'warehouse']
    permission_classes = [IsAuthenticated, IsAdmin]


class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.select_related('warehouse').all().order_by('id')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.select_related('product', 'location').all().order_by('id')
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'product', 'location']
    permission_classes = [IsAuthenticated, IsAdmin]


class StockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.select_related('product', 'location').all().order_by('id')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
