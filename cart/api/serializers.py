from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemCreateSerializer(serializers.ModelSerializer):
	quantity = serializers.IntegerField(max_value=3, min_value=1)

	class Meta:
		model = CartItem
		fields = ['product', 'quantity']

class CartItemListSerializer(serializers.ModelSerializer):

	class Meta:
		model = CartItem
		fields = ['product', 'price', 'quantity',]

class CartListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Cart
		fields = ['id', 'success_code', 'total_item', 'total_price', 'checkout', 'created']

class CartDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = CartItem
		exclude = ['cart', 'id']
