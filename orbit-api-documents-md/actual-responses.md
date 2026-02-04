# Orbit API - Actual Response Documentation

[← Back to Index](README.md)

> **Purpose:** This document records **actual API responses** from the Orbit server to validate the assumptions made in `ignition-spot-simple-plan.md`. Paste real responses here to document the true structure.

---

## 🚀 Quick Start (30 minutes)

**Current Status:** 🔴 **ALL VALUES UNVERIFIED** - No real API testing has occurred yet.

### Step 1: Send Requests in Bruno (5 min)

**Bruno Collection:** `orbit-api-documents-md/orbit-api/`

1. **Open Bruno** → Open Collection → `orbit-api-documents-md/orbit-api/`
2. **Configure Auth** (one-time):
   - Collection Settings → Auth → Bearer Token
   - Paste your Orbit API token
3. **Send requests:**
   - Open `runs.bru` → Click Send → Response appears in Bruno
   - Open `robots.bru` → Click Send
   - Open `anomalies.bru` → Click Send (if exists)
4. **Bruno saves responses** in the .bru files automatically

**Result:**

```
orbit-api-documents-md/
├── actual-responses.md          ← 이 파일 (분석 & 검증)
├── orbit-api/                   ← Bruno Collection
│   ├── runs.bru                 ← GET /runs (request + response)
│   ├── robots.bru               ← GET /robots (request + response)
│   └── anomalies.bru            ← GET /anomalies (request + response)
└── (기타 API 문서들...)
```

### Step 2: Extract Status Values (5 min)

**In Bruno:**

1. Open `runs.bru` → View Response tab
2. Scroll through `resources[]` array
3. Note all unique `missionStatus` values

**Or use jq on Bruno response:**

```bash
# Bruno stores response in .bru file - extract it first
# Then parse with jq
grep -A 9999 "^}$" orbit-api-documents-md/orbit-api/runs.bru | \
  jq -r '.resources[].missionStatus' | sort | uniq -c

# 결과 예시:
  45 success
  30 running
  20 error
   5 pending
```

**이 값들을 아래 [Status Values Observed](#missionstatus-values-observed) 테이블에 기록하세요.**

### Step 3: Document Findings (5 min)

**이 파일(actual-responses.md)에:**

- ✅ Bruno 파일 확인: `orbit-api/runs.bru` response 존재
- ✅ 발견된 status 값 테이블 작성
- ✅ Response format 체크: Array vs `{"resources": [...]}`
- ✅ 체크박스 ✅ 표시

### Step 4: Update Plan (10 min)

**File:** `ignition-spot-simple-plan.md` (line ~1270, ~1750)

```python
# ✅ VERIFIED - 2026-02-04 from Bruno orbit-api/runs.bru
status_map = {
    "success": "COMP",    # ✅ Observed: 45 times
    "running": "RUN",     # ✅ Observed: 30 times
    "error": "FAIL",      # ✅ Observed: 20 times
    "pending": "PEND",    # ✅ Observed: 5 times
    # Removed: "completed", "started", etc. (not observed)
}
```

**Done!** ✅ Deployment-ready.

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

### Actual Response File

**Location:** `orbit-api/robots.bru`

**Captured:** ⬜ Not yet | ✅ Date: **\*\*****\_\_****\*\***

**Quick View:**

- Open `robots.bru` in Bruno → View Response tab
- Or extract from .bru file and parse with jq

### Verified Fields

| Field        | Expected Type | Verified? | Notes                    |
| ------------ | ------------- | --------- | ------------------------ |
| `robotIndex` | integer       | ⬜        | Index 0-32               |
| `hostname`   | string        | ⬜        | e.g., "spot-BD-12345678" |
| `nickname`   | string        | ⬜        | Display name             |
| `username`   | string        | ⬜        | Connection username      |

### Response Format

- [ ] Returns array directly: `[ {...}, {...} ]`
- [ ] Returns wrapped: `{ "resources": [...] }`
- [ ] Other format: **\*\***\_\_\_**\*\***

---

## GET /runs

**Endpoint:** `GET /api/v0/runs`

**Documentation Status:** Schema documented, but `missionStatus` possible values NOT specified.

### Actual Response File

**Location:** `orbit-api/runs.bru`

**Captured:** ⬜ Not yet | ✅ Date: **\*\*****\_\_****\*\***

**Quick View:**

- **In Bruno:** Open `runs.bru` → Send → View Response tab
- **Response fields:** Scroll through `resources[]` array in Bruno UI

### Verified Fields

| Field                | Expected Type | Verified? | Actual Value Example | Notes                                      |
| -------------------- | ------------- | --------- | -------------------- | ------------------------------------------ |
| `uuid`               | string        | ⬜        |                      |                                            |
| `missionName`        | string        | ⬜        |                      |                                            |
| `missionStatus`      | string        | ⬜        |                      | **CRITICAL: Document all observed values** |
| `startTime`          | string (ISO)  | ⬜        |                      | Format: `2026-02-04T10:30:00.000Z`         |
| `endTime`            | string (ISO)  | ⬜        |                      | Null when running?                         |
| `robotHostname`      | string        | ⬜        |                      |                                            |
| `robotNickname`      | string        | ⬜        |                      |                                            |
| `robotSerial`        | string        | ⬜        |                      |                                            |
| `runType`            | string        | ⬜        |                      | "mission" or "teleop"                      |
| `actionCount`        | integer       | ⬜        |                      |                                            |
| `pendingActionCount` | integer       | ⬜        |                      |                                            |
| `operatorId`         | string        | ⬜        |                      |                                            |

### missionStatus Values Observed

> **⚠️ CRITICAL LIMITATION:** The OpenAPI spec does NOT document possible values for `missionStatus`.
>
> **This list is INCOMPLETE** - it only shows values we've observed, not all possible values.
> You may encounter other values during:
>
> - Mission failures / aborts / errors
> - Network disconnections / timeouts
> - Low battery scenarios
> - Multi-robot edge cases
> - Different Orbit versions
>
> **Strategy:** Use defensive coding - log unknown values and handle gracefully.

| Status Value          | Description | First Observed | Trigger Scenario | Mapped To (Plan) |
| --------------------- | ----------- | -------------- | ---------------- | ---------------- |
| _(none captured yet)_ | -           | -              | -                | -                |
|                       |             |                |                  |                  |
|                       |             |                |                  |                  |

**Discovery Methods Used:**

- [ ] Normal operations (actual responses)
- [ ] Intentional failure testing (abort, battery, network)
- [ ] Database query (historical data)
- [ ] Orbit source code / enums
- [ ] Boston Dynamics documentation/support
- [ ] Multi-robot deployment testing

**Currently Assumed Values (based on common API patterns - NO VERIFICATION):**

> **⚠️ CRITICAL:** These are AI-generated guesses. The plan document uses defensive coding
> to log unknown values. Update this list as you discover actual values in production.
>
> **EVEN "success" IS UNVERIFIED** - it's an educated guess based on common API conventions.

- [ ] `running` → `RUN` (assumption: in-progress mission)
- [ ] `started` → `RUN` (assumption: synonym for running)
- [ ] `in_progress` → `RUN` (assumption: synonym for running)
- [ ] `completed` → `COMP` (assumption: finished successfully)
- [ ] `success` → `COMP` ⚠️ **AI GUESS** - common pattern but UNVERIFIED
- [ ] `succeeded` → `COMP` (assumption: possible synonym)
- [ ] `failed` → `FAIL` (assumption: mission failure)
- [ ] `error` → `FAIL` (assumption: error during execution)
- [ ] `aborted` → `FAIL` (assumption: user-cancelled mission)
- [ ] `cancelled` → `FAIL` (assumption: synonym for aborted)
- [ ] `pending` → `PEND` (assumption: queued but not started)
- [ ] `paused` → ??? (possible: mission paused mid-execution)
- [ ] `timeout` → ??? (possible: mission exceeded time limit)
- [ ] `battery_low` → ??? (possible: stopped due to low battery)

**How to Test:**

```python
# In Ignition Script Console - monitor for unknown values
import system.util
logger = system.util.getLogger("orbit.status_discovery")

runs = orbit_api.get_runs(limit=100)
for run in runs:
    status = run.get("missionStatus", "")
    logger.info("Observed status: {}".format(status))
```

- [ ] `aborted` → `FAIL`
- [ ] `cancelled` → `FAIL`
- [ ] `pending` → `PEND`

---

## GET /anomalies

**Endpoint:** `GET /api/v0/anomalies`

**Documentation Status:** Schema documented.

### Actual Response File

**Location:** `orbit-api/anomalies.bru`

**Captured:** ⬜ Not yet | ✅ Date: \***\***\_\_**\*\***

**Quick View:**

- **In Bruno:** Open `anomalies.bru` → Send → View Response tab
- **Severity values:** Check `resources[].severity` field in response

### Verified Fields

| Field              | Expected Type | Verified? | Notes              |
| ------------------ | ------------- | --------- | ------------------ |
| `uuid`             | string        | ⬜        |                    |
| `time`             | string (ISO)  | ⬜        |                    |
| `createdAt`        | string (ISO)  | ⬜        |                    |
| `elementId`        | string        | ⬜        |                    |
| `assetId`          | string        | ⬜        |                    |
| `name`             | string        | ⬜        |                    |
| `severity`         | integer       | ⬜        | Range?             |
| `title`            | string        | ⬜        |                    |
| `source`           | string        | ⬜        |                    |
| `runUuid`          | string        | ⬜        |                    |
| `runEventUuid`     | string        | ⬜        |                    |
| `status`           | string        | ⬜        | `open` or `closed` |
| `statusModifiedAt` | string (ISO)  | ⬜        |                    |
| `statusModifiedBy` | string        | ⬜        |                    |

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

| Field          | Expected Type | Verified? | Notes                 |
| -------------- | ------------- | --------- | --------------------- |
| `uuid`         | string        | ⬜        |                       |
| `runUuid`      | string        | ⬜        |                       |
| `time`         | string (ISO)  | ⬜        |                       |
| `createdAt`    | string (ISO)  | ⬜        |                       |
| `actionName`   | string        | ⬜        |                       |
| `missionName`  | string        | ⬜        |                       |
| `error`        | integer       | ⬜        | Error code            |
| `eventType`    | string        | ⬜        | `daq` or `screenshot` |
| `dataCaptures` | array         | ⬜        | Array of RunCapture   |

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

| Field                 | Type   | Present? | Notes                            |
| --------------------- | ------ | -------- | -------------------------------- |
| `type`                | string | ⬜       | Event type (e.g., "run.started") |
| `data`                | object | ⬜       | Event data container             |
| `data.uuid`           | string | ⬜       | Run UUID                         |
| `data.missionName`    | string | ⬜       |                                  |
| `data.status`         | string | ⬜       |                                  |
| `data.startTime`      | string | ⬜       |                                  |
| `data.endTime`        | string | ⬜       |                                  |
| `data.robot`          | object | ⬜       | Robot info container             |
| `data.robot.hostname` | string | ⬜       |                                  |

---

## Status Value Reference

### Mission Status Mapping (Code Reference)

> **⚠️ WARNING:** All mappings below are UNVERIFIED ASSUMPTIONS

This is the current mapping in `ignition-spot-simple-plan.md`:

```python
# runs_polling._process_run_event()
status_to_event = {
    "running": "run.started",
    "started": "run.started",
    "in_progress": "run.started",
    "completed": "run.completed",
    "success": "run.completed",      # ASSUMED - NO verification
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
    "success": "COMP",               # ASSUMED - NO verification
    "failed": "FAIL",
    "pending": "PEND"
}
```

### Update Log

| Date       | Orbit Version   | Discovery                               | Action Taken                           |
| ---------- | --------------- | --------------------------------------- | -------------------------------------- |
| 2026-02-04 | -               | ⚠️ **ALL STATUS VALUES ARE UNVERIFIED** | Marked all values as AI assumptions    |
|            |                 | No real API testing has occurred yet    | Waiting for actual Orbit API responses |
| ------     | --------------- | -----------                             | --------------                         |
| 2026-02-04 | -               | ⚠️ **ALL STATUS VALUES ARE UNVERIFIED** | Marked all values as AI assumptions    |
|            |                 | No real API testing has occurred yet    | Waiting for actual Orbit API responses |
|            |                 |                                         |                                        |
|            |                 |                                         |                                        |

---

## How to Use This Document

### Workflow

1. **Capture responses** → Save as JSON files in `orbit-api-documents-md/api-responses-json/` directory
2. **Use jq commands** (above) to analyze the data
3. **Check the boxes** (⬜ → ✅) for verified fields
4. **Document findings** in the tables
5. **Update the plan** with real values

### Directory Structure

```
orbit-api-documents-md/
├── actual-responses.md          ← 이 파일 (분석 & 검증)
├── orbit-api/                   ← Bruno Collection
│   ├── bruno.json               ← Collection settings (auth, etc.)
│   ├── runs.bru                 ← GET /runs (request + response)
│   ├── robots.bru               ← GET /robots (request + response)
│   └── anomalies.bru            ← GET /anomalies (request + response)
└── (기타 API 문서들: runs.md, robots.md, ...)
```

### Why Bruno Collection?

✅ **Request + Response together:** Everything in one .bru file  
✅ **Git-friendly:** Text format, easy to diff  
✅ **Reusable:** Run requests directly from Bruno GUI  
✅ **No curl hassle:** No need to copy-paste auth tokens  
✅ **Team sharing:** Commit collection to repo, anyone can use

### Using Bruno Collection

**One-time setup:**

1. **Open Bruno** → Open Collection → `orbit-api-documents-md/orbit-api/`
2. **Configure Auth:**
   - Right-click Collection → Settings → Auth
   - Select "Bearer Token"
   - Paste your Orbit API token
   - Auth applies to ALL requests in collection

**Daily workflow:**

1. Open Bruno → Collection already loaded
2. Click `runs.bru` → Click Send → Response appears
3. Click `robots.bru` → Click Send
4. Responses saved automatically in .bru files

**Extract data with jq (optional):**

```bash
# Bruno stores response in .bru file
# Extract JSON portion and analyze
grep -A 9999 "^}$" orbit-api-documents-md/orbit-api/runs.bru | \
  jq -r '.resources[].missionStatus' | sort | uniq -c
```

---

_Created: 2026-02-04_  
_Purpose: Validate API assumptions in ignition-spot-simple-plan.md_
