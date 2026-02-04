# Robots

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Robots endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/robots` | Retrieves a complete list of robot information on Orbit. Thi... |
| POST | `/robots` | Adds a new robot to Orbit. |
| GET | `/robots/{robotHostname}` | Retrieves information about a single robot. |
| DELETE | `/robots/{robotHostname}` | Removes the specified robot. |

---

### **GET** `/robots`

Retrieves a complete list of robot information on Orbit. This includes which robot is assigned to each slot.


**Responses:**

- **200**: Successfully retrieved robots.

---

### **POST** `/robots`

Adds a new robot to Orbit.


**Request Body:**

Information of a robot in Orbit.


**Content-Type:** `application/json`


**Properties:**

- **hostname** (`string`)
  - The hostname where the robot can be reached.
- **nickname** (`string`)
  - A descriptive label for the robot.
- **username** (`string`)
  - The username that Orbit is connected to the robot with.
- **password** (`string`)
  - The password of the account Orbit will use to connect to the robot.

**Responses:**

- **200**: Successful operation

---

### **GET** `/robots/{robotHostname}`

Retrieves information about a single robot.


**Parameters:**

- **robotHostname** (`string`, in path) *(required)*
  - Hostname of the robot. This should match the hostname field of the robot resource.

**Responses:**

- **200**: Robot retrieved successfully.
  - Schema: [Robot](schemas.md#robot)
- **404**: Could not find robot
- **500**: Could not fetch robot due to server error.

---

### **DELETE** `/robots/{robotHostname}`

Removes the specified robot.


**Parameters:**

- **robotHostname** (`string`, in path) *(required)*
  - Hostname of the robot. This should match the hostname field of the robot resource.

**Responses:**

- **200**: Robot deleted successfully.
- **500**: Could not delete robot.

---
