# Run Captures

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Run Captures endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/run_captures/` | Retrieve a collection of run captures. |
| GET | `/run_captures/{runCaptureUuid}` | Retrieves a single run capture resource by uuid. |

---

### **GET** `/run_captures/`

Retrieve a collection of run captures.

Returns a list of run captures which match the provided query parameters. A RunCapture describes a data point captured during a particular RunEvent.


**Parameters:**

- **runEventUuid** (`string`, in query)
  - Include run_captures which occurred during the run event with this uuid.
- **actionUuid** (`string`, in query)
  - Include run_captures from playbacks of an action with this uuid.
- **actionName** (`string`, in query)
  - Include run_captures from playbacks of an action with this name.
- **robotHostname** (`string`, in query)
  - Include run_captures from a robot with this hostname
- **robotNickname** (`string`, in query)
  - Include run_captures from a robot with this nickname.
- **robotSerial** (`string`, in query)
  - Include run_captures from a robot with this serial.
- **missionName** (`string`, in query)
  - Include run_captures which occurred during playback of a mission with this name.
- **startCreatedAt** (`string`, in query)
  - Include run_captures with a created_at greater than or equal to this value. The value should be in isostring format. For e.g: '2023-06-05T19:29:35.066Z' 
- **endCreatedAt** (`string`, in query)
  - Include run_captures with a created_at less than this value. The value should be in isostring format. For e.g: '2023-06-05T19:29:35.066Z' 
- **limit** (`integer`, in query)
  - Only return a number of resources up to this value.
- **orderBy** (`string`, in query)
  - Criteria for ordering results.

**Responses:**

- **200**: Run Captures were fetched.
  - `resources`: array of [RunCapture](schemas.md#runcapture)
- **500**: Something went wrong.

---

### **GET** `/run_captures/{runCaptureUuid}`

Retrieves a single run capture resource by uuid.

A RunCapture describes a data point captured during a particular RunEvent.


**Parameters:**

- **runCaptureUuid** (`string`, in path) *(required)*
  - ID of run capture

**Responses:**

- **200**: Run Capture was fetched.
  - Schema: [RunCapture](schemas.md#runcapture)
- **500**: Something went wrong.

---
