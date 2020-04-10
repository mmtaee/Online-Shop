from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemCreateSerializer(serializers.ModelSerializer):
	quantity = serializers.IntegerField(max_value=3, min_value=1)
	
	class Meta:
		model = CartItem
		fields = ['product', 'quantity']

