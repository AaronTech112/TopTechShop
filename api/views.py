from django.http import JsonResponse
# the Response Class will take in any python data or already serialized data and wil render it out a json data
from rest_framework.response import Response 
from rest_framework import status
# cuz we are using a function based view
from rest_framework.decorators import api_view
# we import the model we want to use 
from shop.models import Product, User, Category, Review, Cart
# and import the model Serializer class that was created i serializers.py 
from .serializers import ProductSerializer, UserSerializer, CategorySerializer, ReviewSerializer, CartSerializer
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

# We pass in the "GET" method into the list of allowed methods, we can always add others like , PUT, POST,DELETE
# @api_view(['GET'])
# def getData(request):
#     # we then get the data from our database so we can serialize it  
#     products = Product.objects.all()
#     # create the serializer variable and use the ProductSerializer Class and pass in the model we want to serialize followed by setting many= True , which tells it that we want to serialize multiple items, if we want to return item, we'll set it to false   
#     serializer = ProductSerializer(products , many = True)

#     # person = {'name':'Dennis', 'age':28}
#     # the response object will be output as jason data

#     # we then return the data of the serializer(serializer.data) 
#     return Response(serializer.data)

from rest_framework.views import APIView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from api.filters import ProductFilter, CategoriesFilter, UsersFilter, ReviewFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


# class generic views base view
# <<< Start of Products Api >>       
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name','description']
    ordering_fields = [ 'price', 'id' ]
    pagination_class = PageNumberPagination




# class ApiProducts(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
# <<<End of  Products API>>>
 

# <<< Start of Category  Api >>
# we inherit from the ModelViewSet Class which helps us to handle the 
# CRUD that was previously handled by 2 Generic Views having the same queryset and serializer class 
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_class = CategoriesFilter
    search_fields = ['name']
    ordering_fields = ['id']
    pagination_class = PageNumberPagination

class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UsersFilter

    search_fields = ['username','email']
    pagination_class = PageNumberPagination

class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = ReviewFilter
    search_fields = ['user','rating']

    def get_queryset(self):
        return Review.objects.filter(product_id= self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id":self.kwargs["product_pk"]}
    
class CartViewSet(CreateModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# class ApiCategory(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
# <<< End of  Categories API >>>






    # def get_queryset(self):
    #     return super().get_queryset()
    

    # def get(self , request):
    #     product = Product.objects.all()
    #     serializer = ProductSerializer(product, many = True)
    #     return Response(serializer.data)
    
    # def post(self , request):
    #     serializer = ProductSerializer(data = request.data) # we pass in the data that was sent from the front end o that post request
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)   



    # def get(self ,request, pk):
    #     product = get_object_or_404(Product, id = pk)
    #     serializer = ProductSerializer(product,)
    #     return Response(serializer.data)
        
    # def put(self , request,pk):
    #     product = get_object_or_404(Product, id = pk)
    #     serializer = ProductSerializer(product, data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
        
    # def delete(self , request,pk):
    #     product = get_object_or_404(Product, id = pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)  
        
# class ApiCategories(APIView):
#     def get(self , request):
#         category = Category.objects.all()
#         # if request.method == 'GET':
#         serializer = CategorySerializer(category, many = True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = CategorySerializer(data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
        
# class ApiCategory(APIView):
#     def get(self , request , pk):
#         category = get_object_or_404(Category, id = pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
    
#     def put(self , request , pk ):
#         category = get_object_or_404(Category, id = pk)
#         serializer = CategorySerializer( category, data = request.data )
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
        
#     def delete( self, request , pk):
#         category = get_object_or_404(Category, id = pk )
#         category.delete()
#         return Response( status=status.HTTP_204_NO_CONTENT )
    


# @api_view(['GET'])
# def getUser(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many = True)

#     return Response(serializer.data)

#<<< THIS WAS COMMENTED CAUSE IT WAS REPLACED BY THE CLASS BASE VIEW ABOVE >>>>
# @api_view(['POST', 'GET'])
# def products(request):
#     # we pass in the all the data to the serializer class, that will deal with creating  and validating the data that was sent from the frontend 
#     if request.method == 'GET':
#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = ProductSerializer(data = request.data) # we pass in the data that was sent from the front end o that post request
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        


# @api_view(['GET','PUT', 'DELETE'])
# def api_product(request, pk):
#     product = get_object_or_404(Product, id = pk)
#     if request.method == 'GET': 
#         serializer = ProductSerializer(product, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     if request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['POST','GET'])    
# def categories(request):
#     category = Category.objects.all()
#     if request.method == 'GET':
#         serializer = CategorySerializer(category, many = True)
#         return Response(serializer.data)
    
    # if request.method == 'POST':
    #     serializer = CategorySerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)   

# @api_view(['PUT','GET', 'DELETE'])    
# def category(request, pk):
#     category = get_object_or_404(Category, id = pk)
#     if request.method == 'PUT':
#         serializer = CategorySerializer(category, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
               
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     if request.method == 'DELETE':
#         category.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)
    

# @api_view()
# def drink_list(request):
#     #get all the drinks
#     #serialize them 
#     #return Json
#     drink = Product.objects.all()
#     serializer = ProductSerializer(drink , many= True)
#     return Response(serializer.data) 

# @api_view(['POST'])
# def add_drink(request):
#     drink_list = Product.objects.all()
#     serializer = ProductSerializer(data = request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer)
