# SiteDocks

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the SiteDocks endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/site_docks/{uuid}` | Retrieves a single SiteDock resource by uuid. |
| POST | `/site_docks` | Adds a new SiteDock to Orbit. It also updates a pre-existing... |

---

### **GET** `/site_docks/{uuid}`

Retrieves a single SiteDock resource by uuid.

A SiteDock is a representation of robot's docking station.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - ID of SiteDock

**Responses:**

- **200**: A SiteDock was fetched.
  - Schema: [SiteDock](schemas.md#sitedock)
- **500**: Something went wrong.

---

### **POST** `/site_docks`

Adds a new SiteDock to Orbit. It also updates a pre-existing SiteDock using the associated UUID.


**Request Body:**

Information of a new SiteDock in Orbit.


**Content-Type:** `application/json`


**Responses:**

- **200**: Successful operation

---
