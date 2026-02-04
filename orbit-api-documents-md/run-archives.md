# Run Archives

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Run Archives endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/run_archives/{runId}` | Downloads a zip file containing a run's data. |

---

### **GET** `/run_archives/{runId}`

Downloads a zip file containing a run's data.

All run events, images, and metadata for the given run are packaged into a zip file and downloaded upon this request. The result is similar to what can be downloaded from the tablet after mission execution.


**Parameters:**

- **runId** (`string`, in path) *(required)*
  - ID of run

**Responses:**

- **200**: File generated.
- **500**: Could not generate file.

---
