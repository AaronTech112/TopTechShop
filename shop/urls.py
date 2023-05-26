from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # path('instagram-posts/', views.instagram_posts, name='instagram_posts'),
    path('cart/', views.shopping_cart, name='cart'),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('signup/', views.signup_user, name = 'signup'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name = 'product_list_by_category'),
    path('', views.product_list, name='home'),
]
