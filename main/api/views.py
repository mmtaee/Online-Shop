from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models import Q

from main.api import serializers
from main.models import Manufacturer, Category, Product
from taggit.models import Tag

class ManufacturerListApiView(generics.ListAPIView):
	serializer_class = serializers.ManufacturerSerializer
	queryset = Manufacturer.objects.all()

class ManufacturerDetailApiView(generics.RetrieveAPIView):
	serializer_class = serializers.ManufacturerSerializer
	queryset = Manufacturer.objects.all()
	lookup_field = 'id'

class CategoryListApiView(generics.ListAPIView):
	serializer_class = serializers.CategorySerializer
	queryset = Category.objects.all()

class CategoryDetailApiView(generics.RetrieveAPIView):
	serializer_class = serializers.CategorySerializer
	queryset = Category.objects.all()
	lookup_field = 'id'

class ProductListApiView(generics.ListAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = Product.objects.all()

class ProductDetailApiView(generics.RetrieveAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = Product.objects.all()
	lookup_field = 'id'

class ProductListByManufacturerApiView(generics.ListAPIView):
	serializer_class = serializers.ProductSerializer
	lookup_field = 'id'

	def get_queryset(self):
		id = self.kwargs.get('id')
		self.queryset = Product.objects.filter(manufacturer__id=id)
		return super().get_queryset()

class ProductListByManufacturerApiView(generics.ListAPIView):
	serializer_class = serializers.ProductByManufacturerSerializer
	lookup_field = 'id'

	def get_queryset(self):
		id = self.kwargs.get('id')
		self.queryset = Product.objects.filter(manufacturer_id=id)
		return super().get_queryset()

class ProductListByCategoryApiView(generics.ListAPIView):
	serializer_class = serializers.ProductByCategorySerializer
	lookup_field = 'id'

	def get_queryset(self):
		id = self.kwargs.get('id')
		self.queryset = Product.objects.filter(category_id=id)
		return super().get_queryset()

class ProductListByTagNameApiView(generics.ListAPIView):
	serializer_class = serializers.ProductByTagSerializer
	lookup_field = 'name'

	def get_queryset(self):
		tag_name = self.kwargs.get('name')
		# tag = Tag.objects.filter(name=tag_name).first()
		tag = get_object_or_404(Tag, name=tag_name)
		self.queryset = Product.objects.filter(tags=tag)
		return super().get_queryset()


class TagsListApiView(generics.ListAPIView):
	serializer_class = serializers.TagSerializer
	queryset = Tag.objects.all()