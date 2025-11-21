from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
)

@api_view(['GET'])
def products_root(request):
    return Response({
        "products": reverse('product-list-create', request=request),
        "categories": reverse('category-list-create', request=request),
    })

urlpatterns = [
    path('', products_root, name='products-root'),

    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    # Products
    path('list/', ProductListCreateView.as_view(), name='product-list-create'),
    path('list/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
]
