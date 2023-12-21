from django.contrib import admin
from .models import Category , Cart, CartItem,Product,User,FavoriteItem, Favorite,Review

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
admin.site.register(FavoriteItem)
admin.site.register(Favorite)
# admin.site.register(Review)
@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display = ['user','rating', 'comment', 'product']