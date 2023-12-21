from django_filters.rest_framework import FilterSet
from shop.models import Product, Category, User, Review

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "category_id":["exact"],
            "price":['gt','lt']
        }
class CategoriesFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            "name":["exact"],
            "id":['gt','lt'],
        }
class UsersFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            "username":["exact"],
            "id":['gt','lt'],
        }

class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = {
            "user":["exact"],
            "id":['gt','lt']
        }