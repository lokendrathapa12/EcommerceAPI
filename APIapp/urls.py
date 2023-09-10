from django.urls import path,include
from .views import RegistrationView,LoginView,LogoutView,ProductView,OrderView,OrderAPIView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('product/',ProductView.as_view(),name='products'),
    path('productt/<int:pk>/',ProductView.as_view(),name='products'),
    path('order/',OrderView.as_view(),name='orders'),
    path('order/<int:pk>/',OrderView.as_view(),name='order'),
    path('orderdetail/<int:order_id>/',OrderAPIView.as_view(),name='orders'),
    path('auth/', include('rest_framework.urls',namespace='rest_framework'))
]