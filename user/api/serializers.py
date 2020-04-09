from rest_framework import serializers

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from user.api.decorators import password_validator, email_validator



class UserListSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('id', 'username', 'email', 'is_active')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, style={'input_type': 'password', 'placeholder': 'Password'})
    email = serializers.EmailField(required=True)
    class Meta :
        model = User
        fields = ('username', 'password', 'email')

    def validate_username(self, username):
        if User.objects.filter(username=username) :
            error = "User Exists"
            raise serializers.ValidationError(error)
        return username

    @password_validator
    def validate_password(self, value):
        return value

    @email_validator
    def validate_new_email(self, value):
        return value


class UserChangePassword(serializers.ModelSerializer):
        new_password = serializers.CharField(required=False, style={'input_type': 'password', 'placeholder': 'Password'})
        class Meta:
            model = User
            fields = ('username', 'password', 'new_password')
            read_only_fields = ['username', 'password',]

        @password_validator
        def validate_new_password(self, value):
            return value


class UserMangerSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=False, style={'input_type': 'password', 'placeholder': 'Password'})
    new_email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'new_password', 'email', 'new_email')
        read_only_fields = ['username', 'password', 'email',]

    @password_validator
    def validate_new_password(self, value):
        return value

    @email_validator
    def validate_new_email(self, value):
        return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password', 'placeholder': 'Password'})
    email = serializers.EmailField(required=True)

    class Meta :
        model = User
        fields = ['username', 'password', 'email']

    def validate_username(self, username):
        if User.objects.filter(username=username) :
            error = "User Exists"
            raise serializers.ValidationError(error)
        return username

    @password_validator
    def validate_password(self, value):
        return value

    @email_validator
    def validate_new_email(self, value):
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password', 'placeholder': 'Password'})

    def validate(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        if not authenticate(username=username, password=password):
            error = "Invalid Username or Password"
            raise serializers.ValidationError(error)
        return super().validate(validated_data)


class DeleteAccountSerializer(serializers.Serializer):
    confirm = serializers.CharField(
                write_only=True, 
                required=True, 
                help_text=f"Type Your Username Here to Delete Your Account",
                )

    def validate_confirm(self, confirm):
        user = None
        self.request = self.context.get("request")
        if self.request and hasattr(self.request, "user"):
            user = str(self.request.user)

        if confirm != user :
            error = "Invalid Username"
            raise serializers.ValidationError(error)
        return confirm
