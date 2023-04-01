from rest_framework import serializers
from django.contrib.auth.models import User
from apps.website.models import *


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'title')


class MenuItemSerializer(serializers.ModelSerializer):
    category_item = CategorySerializer(source='category', required=False)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'category_item',
                  'featured', 'price', 'category_id')
        extra_kwargs = {
            'category_item': {'read_only': True},
            'category_id': {'min_value': 1},
                        'price': {'min_value': 2},
        }
