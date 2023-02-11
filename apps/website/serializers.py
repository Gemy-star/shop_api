from rest_framework import serializers
from apps.website.models import *
from decimal import Decimal


# class CustomerSerializer(serializers.ModelSerializer):
#     line = serializers.IntegerField(source='phone')

#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'line']


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
