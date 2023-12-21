from django.urls import path, include
from . import views

# this router are used with the ModelViewSet Views in the views.py , because the ModelViewSet does not use normal path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("products",views.ProductViewSet)
router.register("categories", views.CategoryViewSet)
router.register("cart", views.CartViewSet)
router.register("users",views.UsersViewSet)
product_router = routers.NestedDefaultRouter(router, "products", lookup = "product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

# cart_router = routers.NestedDefaultRouter(router,"cart", lookup="cart")
# cart_router.register("cartitems",views.CartItemViewSet, basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    # path("", include(cart_router.urls)),
]



# urlpatterns = [
#     # path('', views.getData),
#     # path('products/', views.ApiProducts.as_view()),
#     # path('users/', views.getUser,),
#     # path('products/<str:pk>/', views.ApiProduct.as_view()),
#     # # path('categories/', views.ApiCategories.as_view()),
#     # path('categories/<str:pk>/', views.ApiCategory.as_view()),
# ]

