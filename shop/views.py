from django.shortcuts import render, get_list_or_404, redirect
from .models import Category,Product, Cart, CartItem, FavoriteItem, Favorite, Review
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, UpdateItemForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import uuid
from django.db.models import Q
# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    else:    
        if request.method == "POST":
            email = request.POST["email" ]
            password = request.POST["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None: 
                try:
                    cart = Cart.objects.get(session_id = request.session['nonuser'], completed = False)
                    if Cart.objects.filter(user=request.user,completed=False).exists():
                        cart.user=None
                        cart.save()
                    else:
                        cart.user=request.user
                        cart.save()
                except:
                    print("login_user function failed")
                login(request,user)
                
                return redirect('shop:home')
            else:
                error_message = "Invalid Username Or Password"
                return render(request,"shop/login-signup.html",{"error_message":error_message})

        return render(request,'shop/login-signup.html')


def signup_user(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    else:
        form = SignupForm()
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.info(request, "Account was create for " + form.cleaned_data.get('username'))
                login(request, user)
                return redirect('shop:home')
            else:
                error_message = "Invalid Credentials or Format" 
                context = {"error_message":error_message}
            
        context = {"form":form}
        return render(request,"shop/signup.html",context)

def logout_user(request):
    logout(request)

    return redirect('shop:home')

def product_list(request, category_slug=None):
    if request.GET.get('search') !=None:
        search = request.GET.get('search') 
    else: 
        search = ''
    global cart
    global num_of_item

    if request.user.is_authenticated:
        user = request.user
        fav_item_c = Favorite.objects.get_or_create(user = request.user)
        fav_item = Favorite.objects.get(user = request.user)
        fav_count = fav_item.fav_items.count()
    else:
        fav_count = 0
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(Q(name__icontains=search) )
    if category_slug:
        try:    
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        except:
            category =  Category.objects.all()
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, completed=False)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
    except:
        cart = {'num_of_items': 0}

    if request.method == "POST":
        product_id = request.POST['product_id']
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=request.user,
                completed=False,
            )
            cartitem, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
            )
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_items
        else:
            try:
                cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
                cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cartitem.quantity += 1
                cartitem.save()
                num_of_item = cart.num_of_items
            except:
                request.session['nonuser'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id=request.session['nonuser'], user_id=request.user.id, completed=False)
                cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cartitem.quantity += 1
                cartitem.save()
                num_of_item = cart.num_of_items

    # num_of_item = cart.num_of_items
    return render(request,
                'shop/product/list.html',
                {
                    'categories': categories,
                    'category': category,
                    'products': products,
                    'cart': cart,
                    'fav_count':fav_count,
                    'products':products,
                    # 'num_of_item': num_of_item,
                }
            )

def product_detail(request,id,slug):
    global num_of_item
    global cart
    product = Product.objects.get(
        id = id,
        slug = slug,
        available = True
    )
    related_product = Product.objects.filter(category=product.category)
    category = Category.objects.get(name=product.category.name)
    # stars = product.reviews.rating
    # star_count = ['']
    # for char in range(stars):
    #    star_count =  star_count.append('1')
 
    if request.POST.get("form_type") == 'review':
        user = request.user
        item_id = request.POST.get('item_id')
        item = Product.objects.get(id=item_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        rev = Review.objects.create(user=user, product=item, rating=rating, comment=comment)
        rev.save()
        messages.success(request, 'Thanks For The Review')
        return redirect('shop:product_detail',id = id , slug = slug )

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST['quantity'])
        product = Product.objects.get(id = product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user = request.user,
                completed = False,
            )
            cart.save()
            cartitem , created = CartItem.objects.get_or_create(
                cart = cart,
                product = product,
            )
            cartitem.quantity += quantity
            cartitem.save()
            num_of_item = cart.num_of_items
        else:
            try:    
                cart = Cart.objects.get(session_id = request.session['nonuser'], completed = False)
                cartitem, created = CartItem.objects.get_or_create(cart=cart,product=product)
                cartitem.quantity += quantity
                cartitem.save()
                num_of_item = cart.num_of_items 
            except:
                request.session['nonuser'] = str(uuid.uuid4)
                cart = Cart.objects.create(session_id = request.session['nonuser'] ,completed=False)
                cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cart.save()
                cartitem.quantity += quantity
                cartitem.save()
                num_of_item = cart.num_of_items  
                
    # num_of_item = num_of_item
    context = {
        'product' : product,
        'related_product':related_product,
        'category':category,
        # 'star_count':star_count,
        # 'num_of_item':num_of_item,
    }
    return render(request,
                  'shop/product/detail.html',
                  context,
                  )
@login_required(login_url='shop:login')
def favorite_items(request):
    fav= Favorite.objects.get(user=request.user)
    fav_list = FavoriteItem.objects.filter(favorite = fav)
    context = {'fav_list':fav_list}
    return render(request, 'shop/favorite_items.html', context)

@login_required(login_url='shop:login')
def add_favorite(request, pk):
    item = Product.objects.get(id = pk)
    if request.method == "POST":
        fav_list , created = Favorite.objects.get_or_create(user = request.user)
        fav_list.save()
        fav_item , created = FavoriteItem.objects.get_or_create(favorite = fav_list, product = item)
        fav_item.save()
        return redirect('shop:home')

    context = {'item':item}
    return render(request, 'shop/add_favorite.html', context)

def delete_fav_item(request, pk):
    item = FavoriteItem.objects.get(id = pk)
    if request.method == 'POST':    
        item.delete()
        return redirect('shop:favorite_items')
    context = {'item':item}
    return render(request,'shop/delete.html',context ) 

def shopping_cart(request):
    cart = None
    cartitems = []

    if request.user.is_authenticated:
        fav_item = Favorite.objects.get(user = request.user )
        fav_count = fav_item.fav_items.count()
    else:
        fav_count = 0

    if request.method == "POST":
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')
        item = CartItem.objects.get(id=cart_item_id)
        item.quantity = quantity
        item.save()
        return redirect('shop:cart')
    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user = request.user, completed=False)
        
    try:
        if request.user.is_authenticated:
            final_price = 0
            cart = Cart.objects.get(user=request.user, completed=False)
            cartitems = cart.cartitems.all()
            final_price = cart.final_price
            context = {'cart':cart,'cartitems':cartitems,"final_price":final_price ,'fav_count':fav_count}
            return render(request,'shop/cart.html',context)
        else:
            final_price = 0
            cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
            cartitems = cart.cartitems.all()
            final_price = cart.final_price
            context = {'cart':cart,'cartitems':cartitems,"final_price":final_price,'fav_count':fav_count }
            return render(request,'shop/cart.html',context)
    except:
        final_price = 0
        cart = {'num_of_items': 0}
    

        context = {'cart':cart,'cartitems':cartitems,"final_price":final_price, 'fav_count':fav_count }
        
        return render(request,'shop/cart.html',context)


def delete_item(request, pk):
    item = CartItem.objects.get(id = pk)
    if request.method == "POST":
        item.delete()
        return redirect ('shop:cart')
    context = {'item':item}
    return render (request, 'shop/delete.html', context )

def confirm_payment(request, pk):
    cart = Cart.objects.get( id = pk )
    cart.completed = True
    cart.save()
    messages.success(request, 'Payment Made Successfully')
    return redirect ('shop:home')


# def review(request):
#     if request.method == "POST":
#         user = request.user
#         item_id = request.POST.get('item_id')
#         item = Product.objects.get(id=item_id)
#         rating = request.POST.get('rating')
#         comment = request.POST.get('comment')
#         rev = Review.objects.create(user=user, product=item, rating=rating, comment=comment)
#         rev.save()
#         messages.success(request, 'Thanks For The Review')
#         return redirect('shop:product_detail' )
#     else:
#         return redirect('shop:product_detail')


# def instagram_posts(request):
#     api = InstagramAPI(access_token=settings.INSTAGRAM_ACCESS_TOKEN)
#     recent_media, _ = api.user_recent_media(user_id=api.user().id, count=10)
#     context = {
#         'posts': recent_media,
#     }
#     return render(request, 'shop/index.html', context)



