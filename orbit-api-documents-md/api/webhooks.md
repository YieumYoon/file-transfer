# Webhooks

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Webhooks endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/webhooks` | Retrieves a complete list of registered webhooks on Orbit. |
| POST | `/webhooks` | Adds a new webhook to Orbit. |
| GET | `/webhooks/{uuid}` | Retrieve a webhook by its uuid. |
| POST | `/webhooks/{uuid}` | Updates a specific webhook on Orbit. |
| DELETE | `/webhooks/{uuid}` | Removes the specified webhook. |

---

### **GET** `/webhooks`

Retrieves a complete list of registered webhooks on Orbit.


**Responses:**

- **200**: Successfully retrieved list of webhooks.
- **500**: Could not fetch webhooks.

---

### **POST** `/webhooks`

Adds a new webhook to Orbit.


**Request Body:**

Information of a new webhook on Orbit.


**Content-Type:** `application/json`


**Properties:**

- **url** (`string`)
  - The url of the webhook.
- **enabled** (`boolean`)
  - Determines whether or not to send the data to url from the webhook.
- **events** (`object`)
  - The list that contains what type of events would trigger sending the data to url. These can also be defined as payload types.
- **validateTlsCert** (`boolean`)
  - Whether or not to validate TLS certificate.
- **secret** (`string`)
  - The secret required to update the webhook (32 bit hex string).

**Responses:**

- **200**: Successfully created a webhook.

---

### **GET** `/webhooks/{uuid}`

Retrieve a webhook by its uuid.

A single webhook registered webhook identified by the unique id.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - A webhook's uuid

**Responses:**

- **200**: Fetched webhook details.
  - Schema: [Webhook](schemas.md#webhook)
- **500**: Failed to get webhook details.

---

### **POST** `/webhooks/{uuid}`

Updates a specific webhook on Orbit.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - A webhook's uuid

**Request Body:**

Information to update for a specific webhook on Orbit.


**Content-Type:** `application/json`


**Properties:**

- **url** (`string`)
  - The url of the webhook.
- **enabled** (`boolean`)
  - Determines whether or not to send the data to url from the webhook.
- **events** (`object`)
  - The list that contains what type of events would trigger sending the data to url. These can also be defined as payload types.
- **validateTlsCert** (`boolean`)
  - Whether or not to validate TLS certificate.
- **secret** (`string`)
  - The secret required to update the webhook (32 bit hex string).

**Responses:**

- **200**: Successfully updated a specific webhook.

---

### **DELETE** `/webhooks/{uuid}`

Removes the specified webhook.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - A webhook's uuid

**Responses:**

- **200**: Webhook deleted successfully.
- **500**: Could not delete a webhook.

---
