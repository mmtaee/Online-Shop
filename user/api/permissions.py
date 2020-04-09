from rest_framework import permissions
from rest_framework import exceptions

from django.urls import reverse


class AnonymousUserRequired(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			detail = {
					'message' : "AnonymousUser Required",
					'logout' : request.build_absolute_uri(reverse('user_api:logout'))
			}
			raise exceptions.PermissionDenied(detail)
		return True


	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return False



