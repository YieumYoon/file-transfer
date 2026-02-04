# Orbit API - Actual Response Documentation

[← Back to Index](README.md)

> **Purpose:** This document records **actual API responses** from the Orbit server to validate the assumptions made in `ignition-spot-simple-plan.md`. Paste real responses here to document the true structure.

---

## 🚀 Quick Start (30 minutes)

**Current Status:** 🔴 **ALL VALUES UNVERIFIED** - No real API testing has occurred yet.

### Step 1: Capture Responses (10 min)

**In Terminal:**

```bash
# Capture using Bruno (or curl)
# Option A: Bruno → Send → Save Response → orbit-api-documents-md/api-responses-json/runs.json
# Option B: curl commands:
cd /Users/junsu/Documents/Github/file-transfer

curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-server/api/v0/runs?limit=100" \
  | jq . > orbit-api-documents-md/api-responses-json/runs.json

curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-server/api/v0/robots" \
  | jq . > orbit-api-documents-md/api-responses-json/robots.json

curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-server/api/v0/anomalies?limit=50" \
  | jq . > orbit-api-documents-md/api-responses-json/anomalies.json
```

**Result:**

```
orbit-api-documents-md/
├── actual-responses.md          ← 이 파일 (분석 & 검증)
├── api-responses-json/          ← JSON 응답 파일들
│   ├── runs.json                ← 실제 GET /runs 응답
│   ├── robots.json              ← 실제 GET /robots 응답
│   └── anomalies.json           ← 실제 GET /anomalies 응답
└── (기타 API 문서들...)
```

### Step 2: Extract Status Values (5 min)

```bash
# 모든 status 값 추출 (카운트 포함)
jq -r '.resources[].missionStatus' api-responses/runs.json | sort | uniq -c

# 결과 예시:
  45 success
  30 running
  20 error
   5 pending
```

**이 값들을 아래 [Status Values Observed](#missionstatus-values-observed) 테이블에 기록하세요.**

### Step 3: Document Findings (5 min)

**이 파일(actual-responses.md)에:**

- ✅ 파일 경로 기록: `api-responses/runs.json`
- ✅ 발견된 status 값 테이블 작성
- ✅ Response format 체크: Array vs `{"resources": [...]}`
- ✅ 체크박스 ✅ 표시

### Step 4: Update Plan (10 min)

**File:** `ignition-spot-simple-plan.md` (line ~1270, ~1750)

```python
# ✅ VERIFIED - 2026-02-04 from api-responses/runs.json
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

**Location:** `api-responses/robots.json`

**Captured:** ⬜ Not yet | ✅ Date: \***\*\_\_\_\*\***

**Quick View:**

```bash
# View file
cat api-responses/robots.json | jq .

# Count robots
jq 'length' api-responses/robots.json
```

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

**Location:** `api-responses/runs.json`

**Captured:** ⬜ Not yet | ✅ Date: \***\*\_\_\_\*\***

**Quick View:**

```bash
# View file
cat orbit-api-documents-md/api-responses-json/runs.json | jq .

# Extract all status values with counts
jq -r '.resources[].missionStatus' orbit-api-documents-md/api-responses-json/runs.json | sort | uniq -c

# Check response structure
jq 'keys' orbit-api-documents-md/api-responses-json/runs.json
```

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

**Location:** `orbit-api-documents-md/api-responses-json/anomalies.json`

**Captured:** ⬜ Not yet | ✅ Date: ****\_\_\_****

**Quick View:**

```bash
# View file
cat orbit-api-documents-md/api-responses-json/anomalies.json | jq .

# Extract severity values
jq -r '.resources[].severity' orbit-api-documents-md/api-responses-json/anomalies.json | sort | uniq -c
```

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
├── api-responses-json/          ← JSON 응답 파일들
│   ├── runs.json                ← GET /runs actual response
│   ├── robots.json              ← GET /robots actual response
│   ├── anomalies.json           ← GET /anomalies actual response
│   └── webhook-*.json           ← Webhook payloads (if captured)
└── (기타 API 문서들: runs.md, robots.md, ...)
```

### Why Separate Files?

✅ **Query with jq:** `jq '.resources[] | select(.missionStatus == "error")' orbit-api-documents-md/api-responses-json/runs.json`  
✅ **Git diff:** See what changed between captures  
✅ **Reusable:** Use in tests, scripts, documentation  
✅ **Clean:** actual-responses.md stays small and readable

### Capture Commands (Copy-Paste Ready)

```bash
# Set variables once
export ORBIT_URL="https://your-orbit-server"
export ORBIT_TOKEN="your-api-token"

# From project root directory
cd /Users/junsu/Documents/Github/file-transfer

# Capture all endpoints
curl -H "Authorization: Bearer $ORBIT_TOKEN" \
  "$ORBIT_URL/api/v0/runs?limit=100" \
  | jq . > orbit-api-documents-md/api-responses-json/runs.json

curl -H "Authorization: Bearer $ORBIT_TOKEN" \
  "$ORBIT_URL/api/v0/robots" \
  | jq . > orbit-api-documents-md/api-responses-json/robots.json

curl -H "Authorization: Bearer $ORBIT_TOKEN" \
  "$ORBIT_URL/api/v0/anomalies?limit=50" \
  | jq . > orbit-api-documents-md/api-responses-json/anomalies.json

# Analyze status values
jq -r '.resources[].missionStatus' orbit-api-documents-md/api-responses-json/runs.json | sort | uniq -c
```

---

_Created: 2026-02-04_  
_Purpose: Validate API assumptions in ignition-spot-simple-plan.md_
