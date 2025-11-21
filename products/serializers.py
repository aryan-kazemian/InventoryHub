from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children']
        read_only_fields = ['slug', 'children']

    def get_children(self, obj):
        if obj.get_children():
            return CategorySerializer(obj.get_children(), many=True).data
        return []

    def validate_name(self, value):
        # Prevent duplicate names
        if self.instance:
            if Category.objects.exclude(id=self.instance.id).filter(name=value).exists():
                raise serializers.ValidationError("Category with this name already exists.")
        else:
            if Category.objects.filter(name=value).exists():
                raise serializers.ValidationError("Category with this name already exists.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'sku', 'price', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_by', 'created_at', 'updated_at']

    def validate_sku(self, value):
        if self.instance:
            if Product.objects.exclude(id=self.instance.id).filter(sku=value).exists():
                raise serializers.ValidationError("SKU must be unique.")
        else:
            if Product.objects.filter(sku=value).exists():
                raise serializers.ValidationError("SKU must be unique.")
        return value

    def validate_name(self, value):
        if self.instance:
            if Product.objects.exclude(id=self.instance.id).filter(name=value).exists():
                raise serializers.ValidationError("Product with this name already exists.")
        else:
            if Product.objects.filter(name=value).exists():
                raise serializers.ValidationError("Product with this name already exists.")
        return value
