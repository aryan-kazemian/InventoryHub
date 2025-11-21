from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import CustomTokenObtainPairView, UserSignupView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

@api_view(['GET'])
def accounts_root(request):
    return Response({
        "signup": reverse('user_signup', request=request),
        "profile": reverse('user_profile', request=request),
        "token": reverse('token_obtain_pair', request=request),
        "token_refresh": reverse('token_refresh', request=request),
    })

urlpatterns = [
    path('', accounts_root, name='accounts-root'),

    # Auth endpoints
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
