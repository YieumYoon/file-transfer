# Run Events

[← Back to Index](README.md) | [Schemas](schemas.md)


This document describes the Run Events endpoints.


## Endpoints

| Method | Endpoint | Summary |
|--------|----------|---------|
| GET | `/run_events/` | Retrieve a collection of run events. |
| GET | `/run_events/{runEventUuid}` | Retrieves a single run event resource by uuid. |

---

### **GET** `/run_events/`

Retrieve a collection of run events.

Returns a list of run events which match the provided query parameters. A RunEvent represents the output of an action executed during a Run. It contains all the RunCaptures associated with the action.


**Parameters:**

- **runUuid** (`string`, in query)
  - Include run_events which occurred during the run with this uuid.
- **actionUuid** (`string`, in query)
  - Include run_events which represent playback of actions with this uuid.
- **elementId** (`string`, in query)
  - Include run_events which represent playback of a SiteElement with this uuid.
- **robotHostname** (`string`, in query)
  - Include run_events performed by a robot with this hostname
- **robotNickname** (`string`, in query)
  - Include run_events performed by a robot with this nickname.
- **robotSerial** (`string`, in query)
  - Include run_events performed by a robot with this serial.
- **missionName** (`string`, in query)
  - Include run_events which occurred during playback of a mission with this name.
- **excludeNonAlerts** (`boolean`, in query)
  - If true, only include run_events that generated an alert.
- **startTime** (`string`, in query)
  - Include run_events with a time greater than or equal to this value. The value should be in isostring format. For e.g: '2023-06-05T19:29:35.066Z' 
- **endTime** (`string`, in query)
  - Include run_events with a time less than this value. The value should be in isostring format. For e.g: '2023-06-05T19:29:35.066Z' 
- **startCreatedAt** (`string`, in query)
  - Include run_events with a created_at greater than or equal to this value. The value should be in isostring format. For e.g: '2023-06-05T19:29:35.066Z' 
- **endCreatedAt** (`string`, in query)
  - Include run_events with a created_at less than this value. The value should be in isostring format. For e.g: '2023-06-05T19:29:35.066Z' 
- **limit** (`integer`, in query)
  - Only return a number of resources up to this value.
- **orderBy** (`string`, in query)
  - Criteria for ordering results.

**Responses:**

- **200**: Run Events were fetched.
  - `resources`: array of [RunEvent](schemas.md#runevent)
- **500**: Something went wrong.

---

### **GET** `/run_events/{runEventUuid}`

Retrieves a single run event resource by uuid.

A RunEvent represents the output of an action executed during a Run. It contains all the RunCaptures associated with the action.


**Parameters:**

- **runEventUuid** (`string`, in path) *(required)*
  - ID of run

**Responses:**

- **200**: Run Event was fetched.
  - Schema: [RunEvent](schemas.md#runevent)
- **500**: Something went wrong.

---
