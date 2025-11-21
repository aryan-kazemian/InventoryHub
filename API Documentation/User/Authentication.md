# InventoryHub API Documentation (User / Authentication)

**Authentication:** JWT Bearer Tokens

---

## 1️⃣ User Signup

**Endpoint:** POST `/api/accounts/signup/`

**Description:** Create a new user account. Returns access and refresh JWT tokens.

**Request Body:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01"
}
```

**Response:**

**201 Created (success)**

```json
{
  "user": {
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-01"
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

**400 Bad Request (invalid JSON or validation error)**

```json
{
  "username": ["This field may not be blank."],
  "password": ["Ensure this field has at least 8 characters."]
}
```

---

## 2️⃣ User Login / Token Obtain

**Endpoint:** POST `/api/accounts/token/`

**Description:** Obtain JWT access and refresh tokens.

**Request Body:**

```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response:**

**200 OK (success)**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

**401 Unauthorized (invalid credentials)**

```json
{
  "detail": "No active account found with the given credentials"
}
```

---

## 3️⃣ Token Refresh

**Endpoint:** POST `/api/accounts/token/refresh/`

**Description:** Refresh the access token using a valid refresh token.

**Request Body:**

```json
{
  "refresh": "<refresh_token>"
}
```

**Response:**

**200 OK**

```json
{
  "access": "<new_access_token>"
}
```

**401 Unauthorized (invalid or expired refresh token)**

```json
{
  "detail": "Token is invalid or expired"
}
```

---

## 4️⃣ User Profile (Retrieve & Update)

**Endpoint:** `/api/accounts/profile/`

**Methods:** GET, PATCH

**Authentication:** JWT access token required in header:

```
Authorization: Bearer <access_token>
```

### 4a. GET Profile

**Description:** Retrieve the current user’s profile.

**Response:**

**200 OK**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01"
}
```

**401 Unauthorized (missing or invalid token)**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 4b. PATCH Profile (Partial Update)

**Description:** Update one or more fields of the user profile.

**Request Body Example:**

```json
{
  "phone": "+1987654321"
}
```

**Response:**

**200 OK (updated)**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+1987654321",
  "date_of_birth": "1990-01-01"
}
```

**400 Bad Request (invalid data)**

```json
{
  "phone": ["Enter a valid phone number."]
}
```

**401 Unauthorized (no token or invalid token)**

```json
{
  "detail": "Given token not valid for any token type"
}
```
