# InventoryHub API Documentation (Products & Categories)

**Authentication:** JWT Bearer Tokens

---

## 1️⃣ Products

### 1a. GET Product List / POST Create Product

**Endpoint:** `/api/products/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST (admin only)

**Filtering:** You can filter products using `id`, `category`, `sku`, or `name`.

**Query Parameters Example:** `/api/products/?category=2&name=iPhone`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "name": "iPhone 13",
    "slug": "iphone-13",
    "category": 2,
    "sku": "IP13-001",
    "price": "799.99",
    "created_by": 1,
    "created_at": "2025-11-21T12:00:00Z",
    "updated_at": "2025-11-21T12:00:00Z"
  }
]
```

**POST Request Body Example:**

```json
{
  "name": "MacBook Pro",
  "category": 3,
  "sku": "MBP-2025",
  "price": "1999.99"
}
```

**201 Created Response:**

```json
{
  "id": 2,
  "name": "MacBook Pro",
  "slug": "macbook-pro",
  "category": 3,
  "sku": "MBP-2025",
  "price": "1999.99",
  "created_by": 1,
  "created_at": "2025-11-21T12:05:00Z",
  "updated_at": "2025-11-21T12:05:00Z"
}
```

### 1b. GET / PATCH / DELETE Product Detail

**Endpoint:** `/api/products/<int:pk>/`

**Description:** Retrieve, update, or delete a product by ID.

**PATCH Request Example:**

```json
{
  "price": "749.99"
}
```

**Response:**

**200 OK**

```json
{
  "id": 1,
  "name": "iPhone 13",
  "slug": "iphone-13",
  "category": 2,
  "sku": "IP13-001",
  "price": "749.99",
  "created_by": 1,
  "created_at": "2025-11-21T12:00:00Z",
  "updated_at": "2025-11-21T12:10:00Z"
}
```

**204 No Content**

**401 Unauthorized**

```json
{
  "detail": "Authentication credentials were not provided or permission denied."
}
```

---

## 2️⃣ Categories

### 2a. GET Category List / POST Create Category

**Endpoint:** `/api/products/categories/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST (admin only)

**Filtering:** You can filter categories using `id`, `name`, `slug`, or `parent`.

**Query Parameters Example:** `/api/products/categories/?name=Electronics`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics",
    "parent": null,
    "children": [
      {
        "id": 2,
        "name": "Mobile Phones",
        "slug": "mobile-phones",
        "parent": 1,
        "children": []
      }
    ]
  }
]
```

**POST Request Body Example:**

```json
{
  "name": "Laptops",
  "parent": 1
}
```

**201 Created Response:**

```json
{
  "id": 3,
  "name": "Laptops",
  "slug": "laptops",
  "parent": 1,
  "children": []
}
```

### 2b. GET / PATCH / DELETE Category Detail

**Endpoint:** `/api/products/categories/<int:pk>/`

**Description:** Retrieve, update, or delete a category by ID.

**PATCH Request Example:**

```json
{
  "name": "Consumer Electronics"
}
```

**200 OK Response:**

```json
{
  "id": 1,
  "name": "Consumer Electronics",
  "slug": "consumer-electronics",
  "parent": null,
  "children": []
}
```

**204 No Content**

**401 Unauthorized**

```json
{
  "detail": "Authentication credentials were not provided or permission denied."
}
```
