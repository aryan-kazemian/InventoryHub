from django.urls import path, include
from .views import api_root, erp_root

urlpatterns = [
    path('', api_root, name='root'),
    path('api/', api_root, name='api-root'),
    path('api/erp/', erp_root, name='erp-root'),
]
