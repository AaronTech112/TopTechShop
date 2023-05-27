from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings

class User(AbstractUser):
    fullname = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.IntegerField(null=True, unique=True)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name= 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE,)
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', default = '',blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:        
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index( fields=['-created']), 
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    session_id = models.CharField(max_length=100, null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True, )
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def final_price(self):
        cartitems = self.cartitems.all()
        final = sum(item.total_price for item in cartitems)
        return final                        
    
    # @property
    # def cart_count(self):
    #     cartitems = self.cartitems.all()
    #     num = 0
    #     for item in cartitems:
    #         num += 1
    #     return num
    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum(item.quantity for item in cartitems)
        return quantity
           
    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='items')
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitems')
    quantity = models.IntegerField(default=0,) 
     
    
    def __str__(self):
        return str(self.product.name)
    
    @property
    def total_price(self):
        total_price = self.product.price * self.quantity
        return total_price
