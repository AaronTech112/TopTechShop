# we are using this serializers because the rest_framework Response Class that we imported in the views can not natively handle complex data types like the django models instances, so we first need to serialize the data before we can render it out

from rest_framework import serializers
from shop.models import Product, User, Category, Cart, Review, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Review
        fields = ["user","comment","rating"]

        def create(self, validated_data):
            product_id = self.context["product_id"]
            return Review.objects.create(product_id=product_id,  **validated_data)

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many = True)
    class Meta:
        model = Product
        fields = ['name','description','price','category','id','slug','reviews']
    category = serializers.StringRelatedField()
    
class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id','username','email','phone_number'] 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug','name']
    
class SimpleProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many = True)
    class Meta:
        model = Product
        fields = ["id","name","price","reviews"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many= False )
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = CartItem
        fields = ["id","product","quantity","sub_total",]

    def total(self,cartitem:CartItem):
        return cartitem.quantity * cartitem.product.price
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True )
    cartitems = CartItemSerializer( many = True,read_only = True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")
    class Meta:
        model = Cart
        fields = ["id","cartitems","grand_total"]

    def main_total(self,cart:Cart):
        return cart.final_price
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Product With Given  ID does Not Exist")
        return  value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        quantity = self.validated_data["quantity"]
        product = self.validated_data["product"]

        try:        
            cartitem = CartItem.objects.get(product = product, cart_id=cart_id,)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem
        except:        
            self.instance = CartItem.objects.create(product=product, cart_id= cart_id, quantity=quantity)
            return self.instance 
    
    class Meta:
        model = CartItem 
        fields = ["id","product","quantity",]
 


            
         

