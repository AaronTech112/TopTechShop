from django.shortcuts import render, get_list_or_404, redirect
from .models import Category,Product, Cart, CartItem
from instagram.client import InstagramAPI
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
import json
import uuid
# Create your views here.

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
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
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
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
    global cart
    global num_of_item
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
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

    if request.method == "POST":
        product_id = request.POST['product_id']
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
        # 'num_of_item':num_of_item,
    }
    return render(request,
                  'shop/product/detail.html',
                  context,
                  )

def shopping_cart(request):
    cart = None
    cartitems = []
    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user = request.user, completed=False)
        
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, completed=False)
            cartitems = cart.cartitems.all()
            final_price = cart.final_price
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
            cartitems = cart.cartitems.all()
            final_price = cart.final_price
    except:
        cart = {'num_of_items': 0}
    

    context = {'cart':cart,'cartitems':cartitems,"final_price":final_price }
    
    return render(request,'shop/cart.html',context)

# def instagram_posts(request):
#     api = InstagramAPI(access_token=settings.INSTAGRAM_ACCESS_TOKEN)
#     recent_media, _ = api.user_recent_media(user_id=api.user().id, count=10)
#     context = {
#         'posts': recent_media,
#     }
#     return render(request, 'shop/index.html', context)

