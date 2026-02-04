# SiteElements

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the SiteElements endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/site_elements/{uuid}` | Retrieves a single SiteElement resource by uuid. |
| POST | `/site_elements` | Adds a new SiteElement to Orbit. It also updates a pre-exist... |

---

### **GET** `/site_elements/{uuid}`

Retrieves a single SiteElement resource by uuid.

A SiteElement describes what a robot should do and where to do it.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - ID of SiteElement

**Responses:**

- **200**: A SiteElement was fetched.
  - Schema: [SiteElement](schemas.md#siteelement)
- **500**: Something went wrong.

---

### **POST** `/site_elements`

Adds a new SiteElement to Orbit. It also updates a pre-existing SiteElement using the associated UUID.


**Request Body:**

Information of a new SiteElement in Orbit.


**Content-Type:** `application/json`


**Responses:**

- **200**: Successful operation

---
