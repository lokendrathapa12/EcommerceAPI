from django.shortcuts import render
from rest_framework import generics, permissions,views,status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import CustomUser,Product,Order
from .serializers import CustomUserSerializer,ProductSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permission import IsSeller,IsBuyer,IsSellerUniqueuser
from .pagination import Mypagenumberpagination
from django.contrib.auth import authenticate, login,logout

# Create your views here.
class RegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_type = serializer.validated_data.get('user_type')

        user = CustomUser.objects.create_user(**serializer.validated_data)
        user.user_type = user_type
        user.save()

        return Response({'message': 'User registered successfully'}, status=HTTP_201_CREATED)





class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # Log the user in
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)  # Log the user out
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)





class ProductListView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticatedOrReadOnly]
   pagination_class = Mypagenumberpagination
   def get(self, request, pk=None, format=None):
    product = Product.objects.all()
    serializer = ProductSerializer(product,many=True)
    return Response(serializer.data)







class ProductView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsSeller]
  pagination_class = Mypagenumberpagination
  def get(self, request, pk=None, format=None):
    id = pk
    if id is not None:
       product = Product.objects.get(pk=id)
       serializer = ProductSerializer(product)
       return Response (serializer.data)       
        
    product = Product.objects.all()
    product = product.filter(seller = request.user)
    serializer = ProductSerializer(product,many=True)
    return Response(serializer.data)
  
  def post(self,request, format=None):
    serializer = ProductSerializer(data= request.data)
    #serializer = ProductSerializer(seller=request.user)
    if serializer.is_valid():
      serializer.validated_data['seller'] = request.user
      serializer.save()
      return Response({'message':'product add succesfully'},status=status.HTTP_201_CREATED)
    return Response({'message':'Product does not add'},status=status.HTTP_400_BAD_REQUEST)

  def put(self, request,pk, format=None):
    id = pk
    product = Product.objects.get(pk=id, product__seller=request.user)
    serializer = ProductSerializer(product, data= request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'message':'Data update succesfully'}, status=status.HTTP_201_CREATED)
    return Response ({'message':'Only valid user can update data'}, status= status.HTTP_400_BAD_REQUEST) 
  
  def patch(self, request, pk, format=None):
    id = pk
    product = Product.objects.get(pk=id, product__seller=request.user)
    serializer = ProductSerializer(product, data = request.data, partial = True)
    if serializer.is_valid():
      serializer.save()
      return Response({'message':'Data update succesfully'}, status=status.HTTP_201_CREATED)
    return Response ({'message':'Data is not valid'}, status= status.HTTP_400_BAD_REQUEST)
 
  def delete(self, request, pk, format= None):
    id =pk
    product = Product.objects.get(pk=id, product__seller=request.user)
    serializer = ProductSerializer(product)
    if serializer.is_valid():
      serializer.delete()
      return Response({'message':'Data deleted succesfully'}, status=status.HTTP_200_OK)
    return Response({"message":'Data is not valid'})    









class OrderView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsBuyer]

  def get(self, request, pk=None, format=None):
    id = pk
    if id is not None:
       order = Order.objects.get(pk=id)
       serializer = OrderSerializer(order)
       return Response (serializer.data)
        
    order = Order.objects.all()
    order = order.filter(buyer = request.user)
    serializer = OrderSerializer(order,many=True)
    return Response(serializer.data)
  
  def post(self,request, format=None):
    serializer = OrderSerializer(data= request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'message':'order add succesfully'},status=status.HTTP_201_CREATED)
    return Response({'message':'order does not add'},status=status.HTTP_400_BAD_REQUEST)
  
  def put(self, request,pk, format=None):
    id = pk
    order = Order.objects.get(pk=id, order__buyer=request.user)
    serializer = ProductSerializer(order, data= request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'message':'Data update succesfully'}, status=status.HTTP_201_CREATED)
    return Response ({'message':'Only valid user can update data'}, status= status.HTTP_400_BAD_REQUEST) 
  
  def delete(self, request, pk, format= None):
    id =pk
    order = Order.objects.get(pk=id, order__buyer=request.user)
    serializer = ProductSerializer(order)
    if serializer.is_valid():
      serializer.delete()
      return Response({'message':'Data deleted succesfully'}, status=status.HTTP_200_OK)
    return Response({"message":'Data is not valid'})   



class SellerOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]
    def get(self, request, product_id, format=None):
        # Retrieve all orders associated with the product owned by the seller
        orders = Order.objects.filter(product__id=product_id, product__seller=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)





class SellerOrderDetailView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsSeller]
  def put(self, request, order_id, format=None):
    order = Order.objects.get(id=order_id, product__seller=request.user)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request, order_id, format=None):
    order = Order.objects.get(id=order_id, product__seller=request.user)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.delete()
      return Response({'message':'Data deleted succesfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    

class SellerTotalRevenueView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]
    def get(self, request, format=None):
        # Retrieve all accepted orders associated with the seller's products
        accepted_orders = Order.objects.filter(product__seller=request.user, status='Accepted')

        # Calculate the total revenue
        total_revenue = sum(Order.product.price for Order in accepted_orders)

        return Response({'total_revenue': total_revenue}, status=status.HTTP_200_OK)