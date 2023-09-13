from django.urls import path,include
from .views import RegistrationView,LoginView,LogoutView,ProductView,OrderView,ProductListView,SellerOrderView,SellerOrderDetailView,SellerTotalRevenueView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('productlist/',ProductListView.as_view(),name='productslist'),
    path('product/',ProductView.as_view(),name='products'),
    path('product/<int:pk>/',ProductView.as_view(),name='products'),
    path('order/',OrderView.as_view(),name='orders'),
    path('order/<int:pk>/',OrderView.as_view(),name='order'),
    path('sellerorder/<int:product_id>/',SellerOrderView.as_view(),name='sellerorder'),
    path('sellerdetailorder/<int:order_id>/',SellerOrderDetailView.as_view(),name='sellerorder'),
    path('totalrevenue/', SellerTotalRevenueView.as_view(), name='seller-total-revenue'),
    path('auth/', include('rest_framework.urls',namespace='rest_framework'))
]