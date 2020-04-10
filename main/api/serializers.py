from rest_framework import serializers

from main.models import Manufacturer, Category, Product
from taggit.models import Tag


class Representation(object):

	def to_representation(self, instance):
		tags = self.fields['tags']
		rep = super().to_representation(instance)
		name = tags.to_representation(tags.get_attribute(instance))
		rep['tags'] = [name[i]['name'] for i in range(len(name))]
		return rep


class ManufacturerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Manufacturer
		fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = '__all__'

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = ['id', 'name', 'slug']


class ProductSerializer(Representation, serializers.ModelSerializer):
	tags = TagSerializer(many=True,)

	class Meta:
		model = Product
		exclude = ['slug', 'create', 'update', 'stock', 'manufacturer', 'category']

	rep = Representation()

class ProductByManufacturerSerializer(Representation, serializers.ModelSerializer):
	tags = TagSerializer(many=True,)

	class Meta:
		model = Product
		exclude = ['slug', 'create', 'update', 'stock', 'category']

	rep = Representation()


class ProductByCategorySerializer(Representation, serializers.ModelSerializer):
	tags = TagSerializer(many=True,)

	class Meta:
		model = Product
		exclude = ['slug', 'create', 'update', 'stock', 'manufacturer']

	rep = Representation()


class ProductByTagSerializer(Representation, serializers.ModelSerializer):
	tags = TagSerializer(many=True,)
	
	class Meta:
		model = Product
		exclude = ['slug', 'create', 'update', 'stock', 'category', 'manufacturer']

	rep = Representation()

		




