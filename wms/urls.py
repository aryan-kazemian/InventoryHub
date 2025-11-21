from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import (
    WarehouseListCreateView,
    WarehouseRetrieveUpdateDestroyView,
    LocationListCreateView,
    LocationRetrieveUpdateDestroyView,
    StockListCreateView,
    StockRetrieveUpdateDestroyView,
)

@api_view(['GET'])
def wms_root(request):
    return Response({
        "warehouses": reverse('warehouse-list-create', request=request),
        "locations": reverse('location-list-create', request=request),
        "stocks": reverse('stock-list-create', request=request),
    })

urlpatterns = [
    path('', wms_root, name='wms-root'),

    path('warehouses/', WarehouseListCreateView.as_view(), name='warehouse-list-create'),
    path('warehouses/<int:pk>/', WarehouseRetrieveUpdateDestroyView.as_view(), name='warehouse-detail'),

    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-detail'),

    path('stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('stocks/<int:pk>/', StockRetrieveUpdateDestroyView.as_view(), name='stock-detail'),
]
