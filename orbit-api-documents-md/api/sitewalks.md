# SiteWalks

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the SiteWalks endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/site_walks/` | Retrieve a collection of all SiteWalks on Orbit. |
| GET | `/site_walks/{uuid}` | Retrieves a single SiteWalk resource by uuid. |
| DELETE | `/site_walks/{uuid}` | Removes the specified SiteWalk. |
| POST | `/site_walks` | Adds a new SiteWalk to Orbit. It also updates a pre-existing... |

---

### **GET** `/site_walks/`

Retrieve a collection of all SiteWalks on Orbit.

Returns the entire list of SiteWalks currently on Orbit


**Responses:**

- **200**: A list of SiteWalks was fetched.
- **500**: Something went wrong.

---

### **GET** `/site_walks/{uuid}`

Retrieves a single SiteWalk resource by uuid.

A SiteWalk describes a series of tasks that define autonomous robot operation. It contains SiteElements and SiteDocks together with other parameters that define autonomous operation.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - ID of SiteWalk

**Responses:**

- **200**: A SiteWalk was fetched.
  - Schema: [SiteWalk](schemas.md#sitewalk)
- **500**: Something went wrong.

---

### **DELETE** `/site_walks/{uuid}`

Removes the specified SiteWalk.


**Parameters:**

- **uuid** (`string`, in path) *(required)*
  - ID of SiteWalk

**Responses:**

- **200**: SiteWalk deleted successfully.
- **500**: Could not delete SiteWalk.

---

### **POST** `/site_walks`

Adds a new SiteWalk to Orbit. It also updates a pre-existing SiteWalk using the associated UUID.


**Request Body:**

Information of a new SiteWalk in Orbit.


**Content-Type:** `application/json`


**Responses:**

- **200**: Successful operation
  - Schema: [SiteWalk](schemas.md#sitewalk)

---
