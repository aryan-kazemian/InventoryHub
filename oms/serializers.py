from rest_framework import serializers
from .models import Order, OrderItem, Payment
from products.models import Product
from wms.models import Stock
from accounts.models import User

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(), source='stock', write_only=True, allow_null=True, required=False
    )
    product = serializers.StringRelatedField(read_only=True)
    stock = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'stock', 'stock_id']

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'amount', 'payment_method', 'status', 'paid_at', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='customer', write_only=True
    )
    items = OrderItemSerializer(many=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'status', 'total_amount', 'created_at', 'updated_at', 'items', 'payments']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = item_data['price']
            stock = item_data.get('stock')
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price, stock=stock)
            total += price * quantity
            if stock:
                stock.quantity -= quantity
                stock.save()
        order.total_amount = total
        order.save()
        return order
