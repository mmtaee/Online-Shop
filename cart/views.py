from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import Http404

from main.models import *
from .models import *
from main.views import ModelsObjectMixin

import random
import string

class CartCreateView(View):
    template_name = 'cart_create.html'

    def get(self, request, *args, **kwargs):
        added_product = []
        context = {}
        products = []
        total_price = "0"
        count = 0
        static_cookie = ["csrftoken", "sessionid", "messages"]
        for cookie in request.COOKIES :
            if cookie not in static_cookie :
                instance = request.COOKIES[cookie].split(',')
                if not Product.objects.filter(id=int(instance[0])).exists() or not instance[1].isnumeric() or int(instance[1]) > 3 :
                    raise Http404(f'You added "{cookie}" to cookie, Invalid Cookie.')
                else :
                    count += 1
                    product = Product.objects.filter(id=instance[0]).first()
                    # name = product.name
                    final_price = product.final_price
                    int_price = int(final_price.replace(",","")) * int(instance[1])
                    price = '{0:,}'.format(int_price)
                    total_price = int(total_price.replace(",","")) + int_price
                    total_price = '{0:,}'.format(total_price)

                    # add cookie to cartitem > login user
                    if request.user.is_authenticated:
                        if not Cart.objects.filter(user=request.user, checkout=False).exists():
                            cart = Cart.objects.create(user=request.user, checkout=False)
                        cart = Cart.objects.filter(user=request.user, checkout=False).first()

                        if not CartItem.objects.filter(product=product, cart=cart) :
                            cartitem = CartItem.objects.create(
                                                product=product,
                                                cart=cart,
                                                quantity=instance[1],
                                                price = price,
                                                )
                        else :
                            cartitem = CartItem.objects.filter(product=product, cart=cart).first()
                            cartitem.quantity = instance[1]
                            cartitem.price = price
                            cartitem.save()

                    added_product.append(product)
                    products.append({
                                    'product' : product, # product query
                                    'quantity' : instance[1], # quantity in cookie
                                    'price' : price,  # product.price * quantity
                                    })


        # this part checks item cart that if not in cookie
        if request.user.is_authenticated:
            if not Cart.objects.filter(user=request.user, checkout=False).exists():
                cart = Cart.objects.create(user=request.user, checkout=False)
            cart = Cart.objects.filter(user=request.user, checkout=False).first()
            for item in CartItem.objects.filter(cart=cart):
                if item.product not in added_product :
                    product = Product.objects.filter(name=item.product).first()
                    total_price = int(total_price.replace(",", "")) + int(item.price.replace(",", ""))
                    total_price = '{0:,}'.format(total_price)
                    products.append({
                                    'product' : product,
                                    'quantity' : item.quantity,
                                    'price' : item.price,
                                    })


        if count == 0 :
            context = {
                    "empty" : True
            }
            return render(request, self.template_name, context)

        context["total_price"] = total_price
        context["products"] = products
        return render(request, self.template_name, context)

class CartCheckOutView(View):
    template_name = 'payment_result.html'

    @method_decorator(login_required(login_url='/account/login/'))
    def get(self, request, *args, **kwargs):
         # TODO: after banke payment clear cookie and checkout in cart = True
         # Check Bank resalt ok than make code and clear history and save cart in checkout = True
         # result = ?
        cart = get_object_or_404(Cart, user=request.user, checkout=False)
        key = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        cart.success_code = key
        cart.checkout = True
        cart.save()
        context = {
                'result' : True,
                'code' : cart.success_code,
        }
        return render(request, self.template_name, context)

class CartHistoryView(ListView):
    template_name = 'cart_history.html'
    queryset = Cart.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.queryset.filter(user=self.request.user).order_by('-created')
        return queryset

class CartDetailView(ModelsObjectMixin, ListView):
    template_name = 'cart_detail.html'
    model = Cart
    queryset = CartItem.objects.all()

    def get_queryset(self):
        obj = self.get_object()
        queryset = super().get_queryset()
        queryset = self.queryset.filter(cart=obj.id)
        return queryset
