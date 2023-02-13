from rest_framework import serializers
from apps.website.models import *
from django.contrib.auth import models
from decimal import Decimal
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group, User
# class CustomerSerializer(serializers.ModelSerializer):
#     line = serializers.IntegerField(source='phone')

#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'line']


class UserManagementSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=Group.objects.get(name='Manager').user_set.all())]
    )
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')
        extra_kwargs = {
            'username': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'],
                                email=validated_data['email'])
        if user.groups.filter(name='Manager').exists():
            return user
        else:
            manager_group = Group.objects.get(name__icontains='Manager')
            user.groups.add(manager_group)
            user.save()
            return user


# #Create New User
# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#             required=True,
#             validators=[UniqueValidator(queryset=User.objects.all())]
#             )

#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )


#         user.set_password(validated_data['password'])
#         user.save()

#         return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug']
# class ItemSerializer(serializers.ModelSerializer):
#     avaliable_stock_items = serializers.IntegerField(source='inventory')
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.IntegerField(write_only=True)
#     pice_after_tax = serializers.SerializerMethodField(
#         method_name='get_price_with_tax', read_only=True)

#     class Meta:
#         model = Items
#         fields = ['name', 'price', 'category',
#                   'avaliable_stock_items', 'pice_after_tax', 'category_id',]

#     def create(self, validated_data):
#         cat_obj = Category.objects.get(pk=validated_data['category_id'])
#         result = Items.objects.create(name=validated_data['name'], price=validated_data['price'],
#                                       category=cat_obj, inventory=validated_data['inventory'])
#         return result

#     def update(self, instance, validated_data):
#         cat_obj = Category.objects.get(pk=validated_data['category_id'])
#         Items.objects.update_or_create(name=validated_data['name'], price=validated_data['price'],
#                                        category=cat_obj, inventory=validated_data['inventory'])
#         return super().update(instance, validated_data)

#     def get_price_with_tax(self, item: Items):
#         return Decimal(item.price) * Decimal(1.1)


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured',
                  'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'category_id': {'min_value': 1},
        }

    def create(self, validated_data):
        result = MenuItem.objects.create(title=validated_data['title'], price=validated_data['price'],
                                         category__pk=validated_data['category_id'], featured=validated_data['featured'])
        return result


# class OrderSerializer(serializers.ModelSerializer):
#     customer = CustomerSerializer(read_only=True)
#     customer_id = serializers.IntegerField(write_only=True)
#     items = ItemSerializer(many=True,  required=False)

#     class Meta:
#         model = Order
#         fields = ['id', 'tax', 'customer', 'items', 'customer_id']
#         extra_kwargs = {
#             'tax': {'min_value': 2},
#         }
