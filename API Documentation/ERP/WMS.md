# InventoryHub API Documentation (WMS)

**Authentication:** JWT Bearer Tokens

---

## 1️⃣ Warehouses

### 1a. GET Warehouse List / POST Create Warehouse

**Endpoint:** `/api/erp/wms/warehouses/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST (admin only)

**Filtering:** You can filter warehouses using `id` or `name`.

**Query Parameters Example:** `/api/erp/wms/warehouses/?name=Main WH`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "name": "Main WH",
    "address": "123 Street",
    "created_at": "2025-11-21T12:00:00Z",
    "updated_at": "2025-11-21T12:00:00Z"
  }
]
```

**POST Request Body Example:**

```json
{
  "name": "Second WH",
  "address": "456 Street"
}
```

**201 Created Response:**

```json
{
  "id": 2,
  "name": "Second WH",
  "address": "456 Street",
  "created_at": "2025-11-21T12:05:00Z",
  "updated_at": "2025-11-21T12:05:00Z"
}
```

### 1b. GET / PATCH / DELETE Warehouse Detail

**Endpoint:** `/api/erp/wms/warehouses/<int:pk>/`

**PATCH Request Example:**

```json
{
  "address": "789 Avenue"
}
```

**Response:**

**200 OK**

```json
{
  "id": 1,
  "name": "Main WH",
  "address": "789 Avenue",
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

## 2️⃣ Locations

### 2a. GET Location List / POST Create Location

**Endpoint:** `/api/erp/wms/locations/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST (admin only)

**Filtering:** You can filter locations using `id`, `code`, or `warehouse`.

**Query Parameters Example:** `/api/erp/wms/locations/?warehouse=1`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "code": "A1",
    "description": "Shelf A1",
    "warehouse": {
      "id": 1,
      "name": "Main WH",
      "address": "123 Street",
      "created_at": "2025-11-21T12:00:00Z",
      "updated_at": "2025-11-21T12:00:00Z"
    }
  }
]
```

**POST Request Body Example:**

```json
{
  "code": "B1",
  "warehouse_id": 1,
  "description": "Shelf B1"
}
```

**201 Created Response:**

```json
{
  "id": 2,
  "code": "B1",
  "description": "Shelf B1",
  "warehouse": {
    "id": 1,
    "name": "Main WH",
    "address": "123 Street",
    "created_at": "2025-11-21T12:00:00Z",
    "updated_at": "2025-11-21T12:00:00Z"
  }
}
```

### 2b. GET / PATCH / DELETE Location Detail

**Endpoint:** `/api/erp/wms/locations/<int:pk>/`

**PATCH Request Example:**

```json
{
  "description": "Updated Shelf A1"
}
```

**200 OK Response:**

```json
{
  "id": 1,
  "code": "A1",
  "description": "Updated Shelf A1",
  "warehouse": {
    "id": 1,
    "name": "Main WH",
    "address": "123 Street",
    "created_at": "2025-11-21T12:00:00Z",
    "updated_at": "2025-11-21T12:10:00Z"
  }
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

## 3️⃣ Stocks

### 3a. GET Stock List / POST Create Stock

**Endpoint:** `/api/erp/wms/stocks/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST (admin only)

**Filtering:** You can filter stocks using `id`, `product`, or `location`.

**Query Parameters Example:** `/api/erp/wms/stocks/?product=1&location=2`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "product": "Laptop",
    "product_id": 1,
    "location": {
      "id": 1,
      "code": "A1",
      "description": "Shelf A1",
      "warehouse": {...}
    },
    "location_id": 1,
    "quantity": 10,
    "updated_at": "2025-11-21T12:00:00Z"
  }
]
```

**POST Request Body Example:**

```json
{
  "product_id": 1,
  "location_id": 2,
  "quantity": 50
}
```

**201 Created Response:**

```json
{
  "id": 2,
  "product": "Laptop",
  "product_id": 1,
  "location": {
    "id": 2,
    "code": "B1",
    "description": "Shelf B1",
    "warehouse": {...}
  },
  "location_id": 2,
  "quantity": 50,
  "updated_at": "2025-11-21T12:05:00Z"
}
```

### 3b. GET / PATCH / DELETE Stock Detail

**Endpoint:** `/api/erp/wms/stocks/<int:pk>/`

**PATCH Request Example:**

```json
{
  "quantity": 99
}
```

**200 OK Response:**

```json
{
  "id": 1,
  "product": "Laptop",
  "product_id": 1,
  "location": {...},
  "location_id": 1,
  "quantity": 99,
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
