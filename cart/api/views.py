from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.urls import reverse

from cart.models import Cart, CartItem
from main.models import Product
from cart.api import serializers

import random
import string

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
				'checkout' : request.build_absolute_uri(reverse('cart_api:cart_checkout')),
				}
			return Response(response)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CratItemListApiView(generics.ListAPIView):
	permission_classes = [IsAuthenticated,]
	serializer_class = serializers.CartItemListSerializer

	def get_queryset(self):
		user = self.request.user
		cart = Cart.objects.filter(user=user, checkout=False).first()
		queryset = CartItem.objects.filter(cart=cart)
		return queryset

	def list(self, request, *args, **kwargs):
		response = super().list(request, *args, **kwargs)
		if not response.data :
			data = {
				'message' : 'Your cart is empty'
			}
			return Response(data,  status=status.HTTP_400_BAD_REQUEST)
		response = {
			'checkout' : request.build_absolute_uri(reverse('cart_api:cart_checkout')),
			'cartitems': response.data,
		}
		return Response(response)

class CartCheckOutApiView(APIView):
	permission_classes = [IsAuthenticated,]

	def get(self, request, *args, **kwargs):
		 # TODO: after banke payment clear cookie and checkout in cart = True
		 # Check Bank resalt ok than make code and clear history and save cart in checkout = True
		 # result = ?
		cart = get_object_or_404(Cart, user=request.user, checkout=False)
		key = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
		cart.success_code = key
		cart.checkout = True
		cart.save()
		response = {
			'status': 'success',
			'code': status.HTTP_200_OK,
			'message': 'Checkout successfully',
			'success_code' : cart.success_code,
			}
		return Response(response)

class CartListApiView(generics.ListAPIView):
	permission_classes = [IsAuthenticated,]
	serializer_class = serializers.CartListSerializer

	def get_queryset(self):
		return Cart.objects.filter(user=self.request.user).order_by('-created')

class CartDetailApiView(generics.ListAPIView):
	permission_classes = [IsAuthenticated,]
	serializer_class = serializers.CartDetailSerializer

	def get_queryset(self):
		id = self.kwargs.get('id')
		cart = get_object_or_404(Cart, user=self.request.user, id=id)
		queryset = CartItem.objects.filter(cart=cart)
		return queryset

	def list(self, request, *args, **kwargs):
		response = super().list(request, *args, **kwargs)
		if not response.data :
			data = {
				'cart crete' : self.request.build_absolute_uri(reverse('cart_api:cart_create')),
				'message': 'This cart has not any products',
			}
			return Response(data,  status=status.HTTP_400_BAD_REQUEST)
		response = {
			'cartitems': response.data,
		}
		return Response(response)
