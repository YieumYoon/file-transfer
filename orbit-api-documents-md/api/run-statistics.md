# Run Statistics

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Run Statistics endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/run_statistics/sessions` | Retrieves a list of session statistics which match query par... |
| GET | `/run_statistics/sessions_summary` | Retrieves a summary of session statistics which match query ... |

---

### **GET** `/run_statistics/sessions`

Retrieves a list of session statistics which match query params.


**Parameters:**

- **start** (`string`, in query)
  - Include sessions with a start time greater than or equal to this value. The value should be in isostring format.
- **end** (`string`, in query)
  - Include sessions with an end time less than this value. The value should be in isostring format.
- **minimumSeverity** (`string`, in query)
  - Include sessions with a minimum severity level.
- **missionNames** (`string`, in query)
  - Include sessions with the specified mission names.
- **includeDispatchFailures** (`boolean`, in query)
  - Include sessions that had dispatch failures.

**Responses:**

- **200**: Session statistics retrieved successfully.
- **500**: Failed to retrieve session statistics.

---

### **GET** `/run_statistics/sessions_summary`

Retrieves a summary of session statistics which match query params.


**Parameters:**

- **start** (`string`, in query) *(required)*
  - Include sessions with a start time greater than or equal to this value. The value should be in isostring format.
- **end** (`string`, in query) *(required)*
  - Include sessions with an end time less than this value. The value should be in isostring format.
- **minimumSeverity** (`string`, in query)
  - Include sessions with a minimum severity level.
- **missionNames** (`string`, in query)
  - Include sessions with the specified mission names.
- **includeDispatchFailures** (`boolean`, in query)
  - Include sessions that had dispatch failures.

**Responses:**

- **200**: Session summary statistics retrieved successfully.
- **500**: Failed to retrieve session summary statistics.

---
