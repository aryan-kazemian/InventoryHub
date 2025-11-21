from django.urls import path
from .views import CustomTokenObtainPairView, UserSignupView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
