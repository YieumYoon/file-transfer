# Backups

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Backups endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/backups/{taskId}` | Retrieves a backup tar file given a task ID. |
| DELETE | `/backups/{taskId}` | Deletes a backup tar file from the Orbit instance given a ta... |

---

### **GET** `/backups/{taskId}`

Retrieves a backup tar file given a task ID.


**Parameters:**

- **taskId** (`string`, in path) *(required)*
  - ID of the backup task.

**Responses:**

- **200**: Backup retrieved successfully.
- **500**: Could not retrieve backup.

---

### **DELETE** `/backups/{taskId}`

Deletes a backup tar file from the Orbit instance given a task ID.


**Parameters:**

- **taskId** (`string`, in path) *(required)*
  - ID of the backup task.

**Responses:**

- **200**: Backup deleted successfully.
- **500**: Could not delete backup.

---
