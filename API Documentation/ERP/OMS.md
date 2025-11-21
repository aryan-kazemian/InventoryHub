# InventoryHub API Documentation (Order Management System - OMS)

**Authentication:** JWT Bearer Tokens

---

## 1️⃣ Orders

### 1a. GET Order List / POST Create Order

**Endpoint:** `/api/erp/oms/orders/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST

**Filtering:** You can filter orders using `id`, `status`, or `customer`.

**Query Parameters Example:** `/api/erp/oms/orders/?status=pending&customer=2`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "customer": "user",
    "status": "pending",
    "total_amount": "999.99",
    "created_at": "2025-11-21T12:00:00Z",
    "updated_at": "2025-11-21T12:05:00Z",
    "items": [
      {
        "id": 1,
        "product": "Laptop",
        "quantity": 1,
        "price": "999.99",
        "stock": "Main WH - A1"
      }
    ],
    "payments": [
      {
        "id": 1,
        "amount": "999.99",
        "payment_method": "Credit Card",
        "status": "pending",
        "paid_at": null,
        "created_at": "2025-11-21T12:01:00Z"
      }
    ]
  }
]
```

**POST Request Body Example:**

```json
{
  "customer_id": 2,
  "status": "pending",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 999.99,
      "stock_id": 1
    }
  ]
}
```

**201 Created Response:**

```json
{
  "id": 2,
  "customer": "user",
  "status": "pending",
  "total_amount": "1999.98",
  "created_at": "2025-11-21T12:10:00Z",
  "updated_at": "2025-11-21T12:10:00Z",
  "items": [
    {
      "id": 2,
      "product": "Laptop",
      "quantity": 2,
      "price": "999.99",
      "stock": "Main WH - A1"
    }
  ],
  "payments": []
}
```

### 1b. GET / PATCH / DELETE Order Detail

**Endpoint:** `/api/erp/oms/orders/<int:pk>/`

**Description:** Retrieve, update, or delete an order by ID.

**PATCH Request Example:**

```json
{
  "status": "confirmed"
}
```

**200 OK Response:**

```json
{
  "id": 1,
  "customer": "user",
  "status": "confirmed",
  "total_amount": "999.99",
  "created_at": "2025-11-21T12:00:00Z",
  "updated_at": "2025-11-21T12:15:00Z",
  "items": [
    {
      "id": 1,
      "product": "Laptop",
      "quantity": 1,
      "price": "999.99",
      "stock": "Main WH - A1"
    }
  ],
  "payments": [
    {
      "id": 1,
      "amount": "999.99",
      "payment_method": "Credit Card",
      "status": "pending",
      "paid_at": null,
      "created_at": "2025-11-21T12:01:00Z"
    }
  ]
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

## 2️⃣ Payments

### 2a. GET Payment List / POST Create Payment

**Endpoint:** `/api/erp/oms/payments/`

**Methods:** GET, POST

**Authentication:** JWT access token required for POST

**Filtering:** You can filter payments using `id`, `order`, or `status`.

**Query Parameters Example:** `/api/erp/oms/payments/?status=pending&order=1`

**Response:**

**200 OK**

```json
[
  {
    "id": 1,
    "order": "Order #1 - user",
    "amount": "999.99",
    "payment_method": "Credit Card",
    "status": "pending",
    "paid_at": null,
    "created_at": "2025-11-21T12:01:00Z"
  }
]
```

**POST Request Body Example:**

```json
{
  "order_id": 1,
  "amount": 999.99,
  "payment_method": "PayPal",
  "status": "pending"
}
```

**201 Created Response:**

```json
{
  "id": 2,
  "order": "Order #1 - user",
  "amount": "999.99",
  "payment_method": "PayPal",
  "status": "pending",
  "paid_at": null,
  "created_at": "2025-11-21T12:10:00Z"
}
```

### 2b. GET / PATCH / DELETE Payment Detail

**Endpoint:** `/api/erp/oms/payments/<int:pk>/`

**Description:** Retrieve, update, or delete a payment by ID.

**PATCH Request Example:**

```json
{
  "status": "completed"
}
```

**200 OK Response:**

```json
{
  "id": 1,
  "order": "Order #1 - user",
  "amount": "999.99",
  "payment_method": "Credit Card",
  "status": "completed",
  "paid_at": "2025-11-21T12:20:00Z",
  "created_at": "2025-11-21T12:01:00Z"
}
```

**204 No Content**

**401 Unauthorized**

```json
{
  "detail": "Authentication credentials were not provided or permission denied."
}
```
