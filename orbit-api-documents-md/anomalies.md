# Anomalies

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Anomalies endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/anomalies` |  |
| PATCH | `/anomalies` |  |
| PATCH | `/anomalies/{anomalyId}` |  |

---

### **GET** `/anomalies`

Get a paginated array of Anomalies.


**Parameters:**

- **uuid** (`string`, in query)
  - Include Anomalies with this uuid.
- **runEventUuid** (`string`, in query)
- **runEventUuids** (`string`, in query)
- **status** (`string`, in query)
- **startTime** (`string`, in query)
- **endTime** (`string`, in query)
- **limit** (`integer`, in query)
  - Only return a number of resources up to this value.
- **orderBy** (`string`, in query)
  - Criteria for ordering results.

**Responses:**

- **200**: Anomalies retrieved successfully.
  - `resources`: array of [Anomaly](schemas.md#anomaly)

---

### **PATCH** `/anomalies`

Bulk close Anomalies by Element ID.


**Request Body:**

Bulk updates to apply to multiple Anomalies.


**Content-Type:** `application/json`


**Properties:**

- **command** (`string`)
  - Possible values: `close`
- **elementIds** (`array of string`)

**Responses:**

- **200**: Anomalies updated successfully.

---

### **PATCH** `/anomalies/{anomalyId}`

Update an Anomaly.


**Parameters:**

- **anomalyId** (`string`, in path) *(required)*
  - ID of the Anomaly.

**Request Body:**

Updates to apply to the Anomaly.


**Content-Type:** `application/json`


**Properties:**

- **status** (`string`)
  - Possible values: `open`, `closed`

**Responses:**

- **200**: Anomaly updated successfully.
  - Schema: [Anomaly](schemas.md#anomaly)

---
