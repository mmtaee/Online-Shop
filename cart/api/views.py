from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from cart.models import Cart, CartItem
from main.models import Product
from cart.api import serializers


class CratItemCreateApiView(generics.CreateAPIView):
	permission_classes = [IsAuthenticated,]
	queryset = CartItem.objects.all()
	serializer_class = serializers.CartItemCreateSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			if not Cart.objects.filter(user=request.user, checkout=False).exists():
				cart = Cart.objects.create(user=request.user, checkout=False)

			cart = Cart.objects.filter(user=request.user, checkout=False).first()

			product_id = serializer.data.get("product")
			product = get_object_or_404(Product, id=product_id)

			quantity = serializer.data.get("quantity")
			price = int(product.final_price.replace(",", "")) * quantity
			price = '{0:,}'.format(price)

			if not CartItem.objects.filter(cart=cart, product=product):

				cartitem = CartItem.objects.create(
							cart=cart,
							product=product,
							quantity=quantity,
							price=price,
						)
				result = "added"

			else:
				cartitem = CartItem.objects.filter(cart=cart, product=product).first()
				cartitem.quantity = quantity
				cartitem.price = price
				cartitem.save()
				result = f"updated with quantity {quantity}"

			response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Product in cart {result} successfully',
        		}

			return Response(response)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
