# Orbit API - Actual Response Documentation

[← Back to Index](README.md)

> **Purpose:** This document records **actual API responses** from the Orbit server to validate the assumptions made in `ignition-spot-simple-plan.md`. Paste real responses here to document the true structure.

---

## Table of Contents

- [GET /robots](#get-robots)
- [GET /runs](#get-runs)
- [GET /anomalies](#get-anomalies)
- [GET /run_events](#get-run_events)
- [Webhook Payloads](#webhook-payloads)
- [Status Value Reference](#status-value-reference)

---

## GET /robots

**Endpoint:** `GET /api/v0/robots`

**Documentation Status:** Response structure not fully documented in OpenAPI spec.

### Actual Response

```json
// TODO: Paste actual response here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### Verified Fields

| Field | Expected Type | Verified? | Notes |
|-------|---------------|-----------|-------|
| `robotIndex` | integer | ⬜ | Index 0-32 |
| `hostname` | string | ⬜ | e.g., "spot-BD-12345678" |
| `nickname` | string | ⬜ | Display name |
| `username` | string | ⬜ | Connection username |

### Response Format

- [ ] Returns array directly: `[ {...}, {...} ]`
- [ ] Returns wrapped: `{ "resources": [...] }`
- [ ] Other format: _______________

---

## GET /runs

**Endpoint:** `GET /api/v0/runs`

**Documentation Status:** Schema documented, but `missionStatus` possible values NOT specified.

### Actual Response

```json
// TODO: Paste actual response here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### Verified Fields

| Field | Expected Type | Verified? | Actual Value Example | Notes |
|-------|---------------|-----------|---------------------|-------|
| `uuid` | string | ⬜ | | |
| `missionName` | string | ⬜ | | |
| `missionStatus` | string | ⬜ | | **CRITICAL: Document all observed values** |
| `startTime` | string (ISO) | ⬜ | | Format: `2026-02-04T10:30:00.000Z` |
| `endTime` | string (ISO) | ⬜ | | Null when running? |
| `robotHostname` | string | ⬜ | | |
| `robotNickname` | string | ⬜ | | |
| `robotSerial` | string | ⬜ | | |
| `runType` | string | ⬜ | | "mission" or "teleop" |
| `actionCount` | integer | ⬜ | | |
| `pendingActionCount` | integer | ⬜ | | |
| `operatorId` | string | ⬜ | | |

### missionStatus Values Observed

> **IMPORTANT:** The OpenAPI spec does NOT document the possible values for `missionStatus`. 
> Document ALL values observed in production here.

| Status Value | Description | First Observed | Mapped To (Plan) |
|--------------|-------------|----------------|------------------|
| `success` | Run completed successfully | v2.9 discovery | `COMP` |
| | | | |
| | | | |
| | | | |

**Currently Assumed Values (unverified):**
- [ ] `running` → `RUN`
- [ ] `started` → `RUN`
- [ ] `in_progress` → `RUN`
- [ ] `completed` → `COMP` (Note: API uses `success` instead)
- [x] `success` → `COMP` ✅ Verified in v2.9
- [ ] `succeeded` → `COMP`
- [ ] `failed` → `FAIL`
- [ ] `error` → `FAIL`
- [ ] `aborted` → `FAIL`
- [ ] `cancelled` → `FAIL`
- [ ] `pending` → `PEND`

---

## GET /anomalies

**Endpoint:** `GET /api/v0/anomalies`

**Documentation Status:** Schema documented.

### Actual Response

```json
// TODO: Paste actual response here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### Verified Fields

| Field | Expected Type | Verified? | Notes |
|-------|---------------|-----------|-------|
| `uuid` | string | ⬜ | |
| `time` | string (ISO) | ⬜ | |
| `createdAt` | string (ISO) | ⬜ | |
| `elementId` | string | ⬜ | |
| `assetId` | string | ⬜ | |
| `name` | string | ⬜ | |
| `severity` | integer | ⬜ | Range? |
| `title` | string | ⬜ | |
| `source` | string | ⬜ | |
| `runUuid` | string | ⬜ | |
| `runEventUuid` | string | ⬜ | |
| `status` | string | ⬜ | `open` or `closed` |
| `statusModifiedAt` | string (ISO) | ⬜ | |
| `statusModifiedBy` | string | ⬜ | |

---

## GET /run_events

**Endpoint:** `GET /api/v0/run_events`

**Documentation Status:** Schema documented.

### Actual Response

```json
// TODO: Paste actual response here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### Verified Fields

| Field | Expected Type | Verified? | Notes |
|-------|---------------|-----------|-------|
| `uuid` | string | ⬜ | |
| `runUuid` | string | ⬜ | |
| `time` | string (ISO) | ⬜ | |
| `createdAt` | string (ISO) | ⬜ | |
| `actionName` | string | ⬜ | |
| `missionName` | string | ⬜ | |
| `error` | integer | ⬜ | Error code |
| `eventType` | string | ⬜ | `daq` or `screenshot` |
| `dataCaptures` | array | ⬜ | Array of RunCapture |

---

## Webhook Payloads

**Note:** The Orbit API documentation describes how to configure webhooks, but does NOT document the payload format sent to webhook endpoints.

> If using webhooks (Web Dev module), capture and document actual payloads here.

### run.started Payload

```json
// TODO: Paste actual webhook payload here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### run.completed Payload

```json
// TODO: Paste actual webhook payload here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### run.failed Payload

```json
// TODO: Paste actual webhook payload here
// Date captured: YYYY-MM-DD
// Orbit version: X.X.X

```

### Webhook Payload Structure (Verified)

| Field | Type | Present? | Notes |
|-------|------|----------|-------|
| `type` | string | ⬜ | Event type (e.g., "run.started") |
| `data` | object | ⬜ | Event data container |
| `data.uuid` | string | ⬜ | Run UUID |
| `data.missionName` | string | ⬜ | |
| `data.status` | string | ⬜ | |
| `data.startTime` | string | ⬜ | |
| `data.endTime` | string | ⬜ | |
| `data.robot` | object | ⬜ | Robot info container |
| `data.robot.hostname` | string | ⬜ | |

---

## Status Value Reference

### Mission Status Mapping (Code Reference)

This is the current mapping in `ignition-spot-simple-plan.md`:

```python
# runs_polling._process_run_event()
status_to_event = {
    "running": "run.started",
    "started": "run.started",
    "in_progress": "run.started",
    "completed": "run.completed",
    "success": "run.completed",      # ✅ Verified
    "succeeded": "run.completed",
    "failed": "run.failed",
    "error": "run.failed",
    "aborted": "run.failed",
    "cancelled": "run.failed",
}

# run_event_handlers.handle_run_event()
status_map = {
    "started": "RUN",
    "completed": "COMP",
    "success": "COMP",               # ✅ Verified
    "failed": "FAIL",
    "pending": "PEND"
}
```

### Update Log

| Date | Orbit Version | Discovery | Action Taken |
|------|---------------|-----------|--------------|
| 2026-02-03 | - | API returns `"success"` not `"completed"` for finished runs | Added to status_map (v2.9) |
| | | | |
| | | | |

---

## How to Use This Document

1. **Capture responses** using curl, Postman, or browser dev tools
2. **Paste the JSON** in the appropriate section
3. **Check the boxes** (change `⬜` to `✅`) for verified fields
4. **Update the plan document** if any assumptions were wrong
5. **Log discoveries** in the Update Log section

### Example curl commands:

```bash
# Get robots
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-orbit-server/api/v0/robots | jq .

# Get runs
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-orbit-server/api/v0/runs?limit=5" | jq .

# Get anomalies
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-orbit-server/api/v0/anomalies?limit=5" | jq .

# Get run events
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-orbit-server/api/v0/run_events?limit=5" | jq .
```

---

*Created: 2026-02-04*  
*Purpose: Validate API assumptions in ignition-spot-simple-plan.md*
