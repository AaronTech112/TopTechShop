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
    path('favorite_items/', views.favorite_items, name='favorite_items'),
    path('add_favorite/<str:pk>/', views.add_favorite, name='add_favorite'),
    path('<slug:category_slug>/', views.product_list, name = 'product_list_by_category'),
    path('delete_item/<str:pk>/',views.delete_item, name = 'delete_item'),
    path('delete_fav_item/<str:pk>/',views.delete_fav_item, name = 'delete_fav_item'),
    path('confirm_payment/<str:pk>', views.confirm_payment, name= 'confirm_payment'),
    # path('review/', views.review, name= 'review'),
    # path('update_item/', views.update_item,name = 'update_item'),
    path('', views.product_list, name='home'),
]  
