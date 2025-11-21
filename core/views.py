from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


# Main API root
@api_view(['GET'])
def api_root(request):
    return Response({
        "accounts": reverse('accounts-root', request=request),
        "products": reverse('products-root', request=request),
        "erp": request.build_absolute_uri('/api/erp/'),  # ERP main entry
        "docs_swagger": request.build_absolute_uri('/swagger/'),
        "docs_redoc": request.build_absolute_uri('/redoc/'),
    })


# ERP root
@api_view(['GET'])
def erp_root(request):
    return Response({
        "wms": request.build_absolute_uri('/api/erp/wms/'),
        "ims": request.build_absolute_uri('/api/erp/ims/'),
        "oms": request.build_absolute_uri('/api/erp/oms/'),
        "crm": request.build_absolute_uri('/api/erp/crm/'),
    })
