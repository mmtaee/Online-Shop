from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from user.api import serializers
from user.api.permissions import AnonymousUserRequired


# admin user
class SuperUserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = [IsAdminUser]

# admin user
class SuperUserCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [IsAdminUser]

# admin user
class SuperUserMangerApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserMangerSerializer
    permission_classes = [IsAdminUser,]
    lookup_field = 'id'
    queryset = User.objects.all()

    def get_object(self):
        id = self.kwargs.get('id')
        try:
            obj = User.objects.get(id=id)
            return obj
        except User.DoesNotExist:
            raise NotFound('User does not exists')

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'User updated successfully',
            }
        if serializer.is_valid():
            if serializer.data.get("new_password") :
                new_password = serializer.data.get("new_password")
                self.object.set_password(new_password)
                response['password']= 'Change successfully'
            if serializer.data.get("new_email") :
                new_email = serializer.data.get("new_email")
                self.object.email = new_email
                response['email']= f'Change email to : {new_email}'
            self.object.save()
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(request, *args, **kwargs):
            self.object = self.get_object()
            self.object.delete()
            response = {
                    'status': 'success',
                    'code': status.HTTP_204_NO_CONTENT,
                    'message': f'{self.object.username} deleted successfully',
                }
            return Response(response)

class SignUpApiView(generics.CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    permission_classes = [AnonymousUserRequired,]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'User created successfully',
            }

        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            email = serializer.data.get("email")
            user = User(
                username=username,
                email = email,
                )
            user.set_password(password)
            user.save()
            _user = User.objects.get(username=user.username)
            if _user is not None:
                login(request, _user)
                response['login'] = "Login Successfully"
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AnonymousUserRequired,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Login successfully',
            }
        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            user = User.objects.get(username=username)
            if user:
                login(request, user)
                return Response(response)
                # return HttpResponseRedirect(redirect_to='/account/api/change_password/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(redirect_to='/account/api/login/')

class DeleteAccountApiView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.DeleteAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = request.user
            user = User.objects.get(username=username)
            user.delete()
            logout(request)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'You Account Deleted successfully',
                'signup' : request.build_absolute_uri(reverse('user_api:signup')),
            }
            return Response(response)
            # return HttpResponseRedirect(redirect_to='/account/api/signup/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordApiView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserChangePassword
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.queryset.get(pk=self.request.user.id)
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.data.get("new_password")
            self.object.set_password(new_password)
            self.object.save()
            new = authenticate(username=self.object.username, password=new_password)
            if new:
                login(self.request, new)
                response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'Password updated successfully',
                        'data': []
                    }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
