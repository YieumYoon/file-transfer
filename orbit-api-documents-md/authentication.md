# Authentication

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Authentication endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| POST | ~~`/login`~~ | Authenticates with username and password. |
| GET | `/api_token/authenticate` | Authenticates the API token that is provided in the request ... |

---

### **POST** `/login`

> **⚠️ DEPRECATED**

Authenticates with username and password.

Warning: This endpoint is deprecated. Use  /api_token/authenticate endpoint instead!


**Request Body:**

Information to post a login request.


**Content-Type:** `application/json`


**Properties:**

- **username** (`string`)
  - The username for the Orbit instance.
- **password** (`string`)
  - The password for the Orbit instance.

**Responses:**

- **200**: Successfully logged into the Orbit instance.
- **401**: Unauthorized Request response.
- **429**: Too Many Requests response.
- **500**: Failed to log into the Orbit instance.

---

### **GET** `/api_token/authenticate`

Authenticates the API token that is provided in the request header. Obtain an API token from the Orbit instance and add it to the request header in the form of {'Authorization': 'Bearer ' + <API TOKEN>}


**Responses:**

- **200**: Successfully authenticated using the provided API Token in the request header.
- **400**: Bad Request response.
- **401**: Unauthorized Request response.

---
