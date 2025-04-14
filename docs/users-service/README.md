# 🧑‍💼 User Service

The User Service is responsible for authentication, user registration, login, and profile management.

---

## 🔌 API Endpoints

### POST `/api/v1/users/register`

Registers a new user.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "token": "eyJhbGciOiJIUzI1..."
}
```


---


### POST `/api/v1/users/login`

Authenticates a user and returns a token.

**Request Body:**

```json
{
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1..."
}

```


---

### GET `/api/v1/users/me`

Returns the authenticated user's profile.

**Headers:**

```json
Authorization: Bearer <token>
```

**Response:**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com"
}
```


---

## ⚙️ Environment Variables

|Variable|Description|
|---|---|
|`JWT_SECRET_KEY`|Secret key for signing JWTs|
|`JWT_EXPIRE_SECONDS`|Lifetime of tokens (in seconds)|
|`EMAIL_VERIFICATION`|Enable/disable email confirmation|

---

## 🧪 Testing

To run unit tests for this service:

```bash
pytest -v src/user/tests/
```


---

## 📖 Additional Notes

- Passwords are hashed using `PBKDF2` (via Django).

- Authentication is handled via JWT tokens.

- All endpoints are prefixed with `/api/v1/users/`.
