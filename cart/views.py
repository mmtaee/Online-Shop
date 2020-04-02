from django.shortcuts import render, Http404
from django.views import View

from main.models import *
from .models import *

class CartCreateView(View):
    template_name = 'cart_create.html'

    def get(self, request, *args, **kwargs):
        context = {}
        products = []
        total_price = "0"
        count = 0
        static_cookie = ["csrftoken", "sessionid", "messages"]
        for cookie in request.COOKIES :
            if cookie not in static_cookie :
                instance = request.COOKIES[cookie].split(',')
                if not Product.objects.filter(id=int(instance[0])).exists() or not instance[1].isnumeric() or int(instance[1]) > 3 :
                    raise Http404(f'You added {items} to cookie, Invalid Cookie.')
                else :
                    count += 1
                    product = Product.objects.filter(id=instance[0]).first()
                    name = product.name
                    final_price = product.final_price
                    int_price = int(final_price.replace(",","")) * int(instance[1])
                    price = '{0:,}'.format(int_price)
                    total_price = int(total_price.replace(",","")) + int_price
                    total_price = '{0:,}'.format(total_price)
                    products.append({
                                    'product' : product, # product query
                                    'quantity' : instance[1], # quantity in cookie
                                    'price' : price,  # product.price * quantity
                                    })

        if count == 0 :
            context = {
                    "empty" : True
            }
            return render(request, self.template_name, context)

        context["total_price"] = total_price
        context["products"] = products
        return render(request, self.template_name, context)


# class CartCheckOutView(View):
#     template_name = 'payment_result.html'
#
#     def post(self, request, *args, **kwargs):
#         ids = request.POST.get('id').split(",")
#         quantity = request.POST.get('quantity').split(",")
#         if not Cart.objects.filter(user=self.request.user, checkout=False).exists():
#             cart = Cart.objects.create(user=self.request.user)
#         cart = Cart.objects.filter(user=request.user, checkout=False).first()
#         for id,quantity in zip(ids, quantity):
#             product = get_object_or_404(Product, id=id)
#             if not CartItem.objects.filter(cart=cart, product=product).exists() :
#                 price = '{0:,}'.format(int(product.final_price.replace("," , "")) * int(quantity))
#                 cartitem = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=price)
#             else :
#                 cartitem = CartItem.objects.filter(cart=cart, product=product).first()
#                 cartitem.quantity = int(quantity)
#                 cartitem.price = '{0:,}'.format(int(product.final_price.replace("," , "")) * cartitem.quantity)
#                 cartitem.save()
#
#     # TODO: after banke payment clear cookie and checkout in cart = True
#         # # TODO:  Check Bank resalt ok than make code and clear history and save cart in checkout = True
#         # result = ?  # TODO: chek api bank result True make code
#         key = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
#         cart = get_object_or_404(Cart, user=self.request.user, checkout=False)
#         cart.code = key
#         cart.checkout = True
#         cart.save()
#         return render(request, 'payment_result.html', {'result' : True, 'code' : cart.code})
#     else :
#         raise Http404(
#
#         )
