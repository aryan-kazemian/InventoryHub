from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    PaymentListCreateView,
    PaymentRetrieveUpdateDestroyView
)

@api_view(['GET'])
def oms_root(request):
    return Response({
        "orders": reverse('order-list-create', request=request),
        "payments": reverse('payment-list-create', request=request)
    })

urlpatterns = [
    path('', oms_root, name='oms-root'),

    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),

    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-detail')
]
