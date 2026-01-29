# Backup Tasks

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Backup Tasks endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/backup_tasks` | Retrieves a list of backup tasks. |
| POST | `/backup_tasks` | Creates a new backup task. |

---

### **GET** `/backup_tasks`

Retrieves a list of backup tasks.


**Responses:**

- **200**: Backup tasks retrieved successfully.
- **500**: Could not fetch backup tasks.

---

### **POST** `/backup_tasks`

Creates a new backup task.


**Request Body:**

Information of a new backup task.


**Content-Type:** `application/json`


Schema: [BackupParameters](schemas.md#backupparameters)


**Responses:**

- **200**: Backup task created successfully.
  - `data`: [BackupTask](schemas.md#backuptask)
- **500**: Could not create backup task.

---
