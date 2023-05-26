from django.contrib import admin
from .models import Category , Cart, CartItem,Product,User

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created','updated']
    list_editable = ['price', 'available']
    list_filter = ['available', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register([Cart,CartItem])
admin.site.register(User)