# Calendar

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Calendar endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/calendar/schedule` | Returns calendar events on the specified Orbit instance. |
| POST | `/calendar/schedule` | Create a calendar event to play a mission. |
| DELETE | `/calendar/schedule/{eventid}` | Removes the specified calendar event. |
| POST | `/calendar/disable-enable` | Disable/enable mission scheduled on Orbit. |

---

### **GET** `/calendar/schedule`

Returns calendar events on the specified Orbit instance.

A list of active calendar events.


**Responses:**

- **200**: Fetched list of active calendar events.
  - `activeEvents`: array of [Schedule](schemas.md#schedule)
- **500**: Failed to get a list of active calendar events.

---

### **POST** `/calendar/schedule`

Create a calendar event to play a mission.


**Request Body:**

Information of a new calendar event to add to Orbit.


**Content-Type:** `application/json`


Schema: [Schedule](schemas.md#schedule)


**Responses:**

- **200**: Successful operation

---

### **DELETE** `/calendar/schedule/{eventid}`

Removes the specified calendar event.


**Parameters:**

- **eventid** (`string`, in path) *(required)*
  - ID of the calendar event

**Responses:**

- **200**: Calendar event deleted successfully.
- **500**: Could not delete calendar event.

---

### **POST** `/calendar/disable-enable`

Disable/enable mission scheduled on Orbit.


**Request Body:**

Information on disable reason and eventId (optional).


**Content-Type:** `application/json`


**Properties:**

- **disableReason** (`string`)
  - The reason for disabling the mission. Enables the mission if left empty.
- **eventId** (`string`)
  - (Optional) The eventId of the specific scheduled mission. Do not use this field if all scheduled missions are targets.

**Responses:**

- **200**: Successfully completed the disable/enable request.
- **500**: Failed to complete the disable/enable request.

---
