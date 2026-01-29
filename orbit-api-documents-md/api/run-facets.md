# Run Facets

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Run Facets endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/runs/facets/actions` | Retrieves a list of action descriptions which match query pa... |
| GET | `/runs/facets/robots` | Retrieves a list of robot descriptions which match query par... |
| GET | `/runs/facets/missions` | Retrieves a list of every unique mission which produced a ru... |

---

### **GET** `/runs/facets/actions`

Retrieves a list of action descriptions which match query params.


**Parameters:**

- **missionName** (`string`, in query) *(required)*
  - The name of the mission

**Responses:**

- **200**: Action facets delivered.
- **500**: Something went wrong.

---

### **GET** `/runs/facets/robots`

Retrieves a list of robot descriptions which match query params.


**Responses:**

- **200**: Robot facets delivered.
- **500**: Something went wrong.

---

### **GET** `/runs/facets/missions`

Retrieves a list of every unique mission which produced a run.


**Responses:**

- **200**: Mission facets delivered.
- **500**: Something went wrong.

---
