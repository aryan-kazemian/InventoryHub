from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Warehouse, Location, Stock
from products.models import Product, Category

User = get_user_model()


class BaseWMSTestCase(APITestCase):

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
            quantity=10
        )


class WarehouseAPITestCase(BaseWMSTestCase):

    def test_list_warehouses_admin(self):
        response = self.client_admin.get(reverse('warehouse-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_list_warehouses_non_admin(self):
        response = self.client_user.get(reverse('warehouse-list-create'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_warehouse_admin(self):
        data = {"name": "Second WH", "address": "456 Street"}
        response = self.client_admin.post(reverse('warehouse-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Warehouse.objects.filter(name="Second WH").exists())

    def test_create_warehouse_non_admin(self):
        data = {"name": "Invalid WH"}
        response = self.client_user.post(reverse('warehouse-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LocationAPITestCase(BaseWMSTestCase):

    def test_list_locations_admin(self):
        response = self.client_admin.get(reverse('location-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_location_admin(self):
        data = {"code": "B1", "warehouse_id": self.warehouse.id, "description": "Shelf B1"}
        response = self.client_admin.post(reverse('location-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Location.objects.filter(code="B1").exists())

    def test_create_location_non_admin(self):
        data = {"code": "B2", "warehouse_id": self.warehouse.id}
        response = self.client_user.post(reverse('location-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StockAPITestCase(BaseWMSTestCase):

    def test_list_stocks_admin(self):
        response = self.client_admin.get(reverse('stock-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_stock_admin(self):
        new_location = Location.objects.create(warehouse=self.warehouse, code="B2", description="Shelf B2")
        data = {"product_id": self.product.id, "location_id": new_location.id, "quantity": 50}
        response = self.client_admin.post(reverse('stock-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Stock.objects.filter(quantity=50).exists())

    def test_create_stock_non_admin(self):
        data = {"product_id": self.product.id, "location_id": self.location.id, "quantity": 20}
        response = self.client_user.post(reverse('stock-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_stock_admin(self):
        data = {"quantity": 99}
        response = self.client_admin.patch(
            reverse('stock-detail', kwargs={'pk': self.stock.id}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 99)

    def test_delete_stock_admin(self):
        response = self.client_admin.delete(reverse('stock-detail', kwargs={'pk': self.stock.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Stock.objects.filter(pk=self.stock.id).exists())
