from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Order, OrderItem, Payment
from products.models import Product, Category
from wms.models import Stock, Warehouse, Location

User = get_user_model()

class BaseOMSTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass'
        )
        self.regular_user = User.objects.create_user(
            username='user', email='user@example.com', password='userpass'
        )

        self.client_admin = APIClient()
        response = self.client_admin.post(
            reverse('token_obtain_pair'),
            {'username': 'admin', 'password': 'adminpass'},
            format='json'
        )
        self.admin_token = response.data['access']
        self.client_admin.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        self.client_user = APIClient()
        response = self.client_user.post(
            reverse('token_obtain_pair'),
            {'username': 'user', 'password': 'userpass'},
            format='json'
        )
        self.user_token = response.data['access']
        self.client_user.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            sku="SKU123",
            category=self.category,
            price="999.99"
        )

        self.warehouse = Warehouse.objects.create(name="Main WH", address="123 Street")
        self.location = Location.objects.create(
            warehouse=self.warehouse,
            code="A1",
            description="Shelf A1"
        )

        self.stock = Stock.objects.create(
            product=self.product,
            location=self.location,
            quantity=50
        )

        self.order = Order.objects.create(
            customer=self.regular_user,
            status='pending',
            total_amount=999.99
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=999.99,
            stock=self.stock
        )
        self.payment = Payment.objects.create(
            order=self.order,
            amount=999.99,
            payment_method='Credit Card',
            status='pending'
        )

class OrderAPITestCase(BaseOMSTestCase):

    def test_list_orders_admin(self):
        response = self.client_admin.get(reverse('order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_list_orders_non_admin(self):
        response = self.client_user.get(reverse('order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_admin(self):
        data = {
            "customer_id": self.regular_user.id,
            "status": "pending",
            "items": [
                {"product_id": self.product.id, "quantity": 2, "price": 999.99, "stock_id": self.stock.id}
            ]
        }
        response = self.client_admin.post(reverse('order-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(id=response.data['id']).exists())

    def test_create_order_non_admin(self):
        data = {
            "customer_id": self.regular_user.id,
            "status": "pending",
            "items": [
                {"product_id": self.product.id, "quantity": 1, "price": 999.99, "stock_id": self.stock.id}
            ]
        }
        response = self.client_user.post(reverse('order-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PaymentAPITestCase(BaseOMSTestCase):

    def test_list_payments_admin(self):
        response = self.client_admin.get(reverse('payment-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_list_payments_non_admin(self):
        response = self.client_user.get(reverse('payment-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment_admin(self):
        data = {
            "order_id": self.order.id,
            "amount": 1999.98,
            "payment_method": "PayPal",
            "status": "pending"
        }
        response = self.client_admin.post(reverse('payment-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Payment.objects.filter(id=response.data['id']).exists())

    def test_create_payment_non_admin(self):
        data = {
            "order_id": self.order.id,
            "amount": 999.99,
            "payment_method": "Credit Card",
            "status": "completed"
        }
        response = self.client_user.post(reverse('payment-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_payment_admin(self):
        data = {"status": "completed"}
        response = self.client_admin.patch(
            reverse('payment-detail', kwargs={'pk': self.payment.id}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, "completed")

    def test_delete_payment_admin(self):
        response = self.client_admin.delete(reverse('payment-detail', kwargs={'pk': self.payment.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(pk=self.payment.id).exists())
