from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, Payment
from .serializers import OrderSerializer, PaymentSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related('items__product', 'payments').all().order_by('-id')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'status', 'customer']
    permission_classes = [IsAuthenticated]

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.prefetch_related('items__product', 'payments').all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.select_related('order').all().order_by('-id')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'order', 'status']
    permission_classes = [IsAuthenticated]

class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.select_related('order').all().order_by('-id')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
