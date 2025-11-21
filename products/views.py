from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from accounts.permissions import IsAdmin

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category', 'sku', 'name']

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = []
        return [p() for p in permission_classes]


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = []
        return [p() for p in permission_classes]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'slug', 'parent']

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = []
        return [p() for p in permission_classes]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'slug', 'parent']

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = []
        return [p() for p in permission_classes]
