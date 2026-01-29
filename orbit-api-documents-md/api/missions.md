# Missions

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Missions endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | ~~`/missions`~~ | Retrieves a complete list of mission information on Orbit. |
| GET | ~~`/missions/{missionId}`~~ | Retrieves information about a single mission. |
| DELETE | ~~`/missions/{missionId}`~~ | Removes the specified mission. |

---

### **GET** `/missions`

> **⚠️ DEPRECATED**

Retrieves a complete list of mission information on Orbit.

Warning: This endpoint is deprecated. Use SiteWalk instead!


**Responses:**

- **200**: Successfully retrieved missions.
- **500**: Could not fetch missions.

---

### **GET** `/missions/{missionId}`

> **⚠️ DEPRECATED**

Retrieves information about a single mission.

Warning: This endpoint is deprecated. Use SiteWalk instead!


**Parameters:**

- **missionId** (`string`, in path) *(required)*
  - ID of the mission. This should match the uuid field of the mission resource.

**Responses:**

- **200**: Mission retrieved successfully.
  - Schema: [Mission](schemas.md#mission)
- **500**: Could not fetch mission.

---

### **DELETE** `/missions/{missionId}`

> **⚠️ DEPRECATED**

Removes the specified mission.

Warning: This endpoint is deprecated. Use SiteWalk instead!


**Parameters:**

- **missionId** (`string`, in path) *(required)*
  - ID of the mission. This should match the uuid field of the mission resource.

**Responses:**

- **200**: Mission deleted successfully.
- **500**: Could not delete mission.

---
