from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Product, Category

User = get_user_model()


class BaseTestCase(APITestCase):
    """Base class to set up a user and auth token"""
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass'
        )

        # JWT login for admin
        self.client_admin = APIClient()
        response = self.client_admin.post(
            reverse('token_obtain_pair'),
            {'username': 'admin', 'password': 'adminpass'},
            format='json'
        )
        self.admin_token = response.data['access']
        self.client_admin.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # JWT login for regular user
        self.client_user = APIClient()
        response = self.client_user.post(
            reverse('token_obtain_pair'),
            {'username': 'user', 'password': 'userpass'},
            format='json'
        )
        self.user_token = response.data['access']
        self.client_user.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        # Create a sample category
        self.category = Category.objects.create(name="Electronics")

        # Sample product data
        self.product_data = {
            "name": "Laptop",
            "category": self.category.id,
            "sku": "SKU123",
            "price": "999.99"
        }


class ProductAPITestCase(BaseTestCase):

    def test_list_products(self):
        """Test that products can be listed without authentication"""
        Product.objects.create(name="Phone", category=self.category, sku="SKU999", price=199.99)
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)  # Pagination result

    def test_create_product_admin(self):
        """Admin can create product"""
        response = self.client_admin.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_non_admin(self):
        """Non-admin cannot create product"""
        response = self.client_user.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_product(self):
        """Retrieve a single product"""
        product = Product.objects.create(name="Tablet", category=self.category, sku="SKU321", price=299.99)
        response = self.client.get(reverse('product-detail', kwargs={'pk': product.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Tablet")

    def test_update_product_admin(self):
        """Admin can update product"""
        product = Product.objects.create(
            name="Laptop",
            category=self.category,
            sku="SKU123",
            price="999.99"
        )

        update_data = {
            "name": "Gaming Laptop",
            "price": "1299.99",
            "category": self.category.id
        }

        response = self.client_admin.patch(
            reverse('product-detail', kwargs={'pk': product.id}),
            update_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "Gaming Laptop")

    def test_delete_product_admin(self):
        """Admin can delete product"""
        product = Product.objects.create(name="Laptop", category=self.category, sku="SKU123", price="999.99")
        response = self.client_admin.delete(reverse('product-detail', kwargs={'pk': product.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product.id).exists())


class CategoryAPITestCase(BaseTestCase):

    def test_list_categories(self):
        """Categories can be listed without authentication"""
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_create_category_admin(self):
        """Admin can create category"""
        data = {"name": "Appliances"}
        response = self.client_admin.post(reverse('category-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_category_duplicate_name(self):
        """Cannot create category with duplicate name"""
        data = {"name": "Electronics"}
        response = self.client_admin.post(reverse('category-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", str(response.data))

    def test_update_category_admin(self):
        """Admin can update category name and slug auto-updates"""
        data = {"name": "Consumer Electronics"}
        response = self.client_admin.patch(reverse('category-detail', kwargs={'pk': self.category.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Consumer Electronics")
        self.assertTrue("consumer-electronics" in self.category.slug)

    def test_delete_category_admin(self):
        """Admin can delete category"""
        new_cat = Category.objects.create(name="Furniture")
        response = self.client_admin.delete(reverse('category-detail', kwargs={'pk': new_cat.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=new_cat.id).exists())
