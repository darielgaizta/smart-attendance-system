from django.urls import path, include

from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
	TokenVerifyView
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('auth/', obtain_auth_token),

	path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
	path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),

	# Internal apps
	path('attendance/', include('attendance.urls')),
]