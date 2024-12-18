from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from booking_app.user.model import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['id', 'user', 'description']
        # exclude = ['id', 'role', 'user',]

    def create(self, validated_data):
        # role = validated_data.pop('role')
        profile = Profile.objects.create_profile(role=validated_data['role'],description=validated_data['description'])
        # Profile.objects.create(user=user, **role)
        return profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer('role')
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'profile_url']
        read_only_fields = ['username', 'email']

    # def create(self, validated_data):  #Переопределение метода create
    #     profile_data = validated_data.pop('profile', {})
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user

    def update(self, instance, validated_data):
        profile_data = validated_data.get('profile', {})
        profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
        return instance

    def get_profile_url(self, obj) -> str:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('user-detail', kwargs={'pk': obj.pk}))
        return None


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {'email': {'required': True, 'allow_blank': False,
                                  'validators': [UniqueValidator(queryset=User.objects.all())]},
                        'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']

        )
        return user

    # def create(self, validated_data):
    #     role = validated_data.pop('role')
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         profile=validated_data['profile'],
    #         password=validated_data['password'],
    #         email=validated_data['email'])
    #     Profile.objects.create(user=user, **role)
    #     return user


class LoginSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['profile', 'email', 'password']
        extra_kwargs = {'email': {'required': True, 'allow_blank': False},
                        'password': {'write_only': True, 'style': {'input_type': 'password'}}}


class EmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    @classmethod
    def get_token(cls, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')
        user = authenticate(username=user.username, password=password)
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
