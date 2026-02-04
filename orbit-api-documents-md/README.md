# Orbit Web API

**Version:** 5.0.0

**Base URL:** `/api/v0`

The Orbit web API provides access to a variety of resources through RESTful http endpoints.

---

## 🤖 For AI Agents: START HERE

**CRITICAL:** Before making ANY assumptions about API response values:

1. ✅ **Check [actual-responses.md](actual-responses.md) FIRST** - Contains verified real API responses
2. ✅ **Check `orbit-api/` directory** - Contains Bruno collection with real API responses
3. ❌ **DO NOT assume** response values based on "common API patterns"
4. ❌ **DO NOT claim "verified"** unless documented in actual-responses.md

### Quick Verification Workflow for AI Agents

```
User asks about API integration
  ↓
Check actual-responses.md for verified values
  ↓
If verified → Use real values
If not verified → Request user to capture real API responses
  ↓
NEVER proceed with assumptions - always mark as "⚠️ UNVERIFIED"
```

**Example - What NOT to do:**

```python
# ❌ WRONG - Assuming values without verification
status_map = {
    "success": "COMP",  # Claimed "verified" but never tested
}
```

**Example - What TO do:**

```python
# ✅ CORRECT - Mark assumptions clearly
status_map = {
    "success": "COMP",  # ⚠️ ASSUMPTION - verify with actual-responses.md first
}
# OR request user to capture real responses before proceeding
```

**See:** [AGENTS.md](../AGENTS.md) Rule #0 for detailed guidelines.

---

## How to Use This Documentation

This documentation is organized into separate files by API category.
Each category file contains all endpoints related to that functionality.

### For Developers

- **Browse by category** - Navigate to specific endpoint documentation
- **Check schemas** - See data models in [schemas.md](schemas.md)
- **Verify assumptions** - Always check [actual-responses.md](actual-responses.md) for real API behavior

### For AI Agents

**CRITICAL WORKFLOW:**

1. **Read API structure** from category files (runs.md, robots.md, etc.)
2. **Check [actual-responses.md](actual-responses.md)** for verified response values
3. **If no verified data exists** → Request user to capture real API responses
4. **Mark assumptions** with `⚠️ UNVERIFIED` - never claim "verified" without proof

**Directory Structure:**

```
orbit-api-documents-md/
├── README.md                    ← Start here
├── actual-responses.md          ← **VERIFIED API responses** (check first!)
├── orbit-api/                   ← **Bruno Collection** (real API requests/responses)
│   ├── bruno.json              ← Collection settings (auth, etc.)
│   ├── runs.bru                ← GET /runs (request + response)
│   ├── robots.bru              ← GET /robots (request + response)
│   └── anomalies.bru           ← GET /anomalies (request + response)
├── runs.md                      ← Endpoint documentation
├── robots.md                    ← Endpoint documentation
├── schemas.md                   ← Data model definitions
└── (other endpoint docs...)
```

## API Categories

| Category                                       | Description                                | File                  |
| ---------------------------------------------- | ------------------------------------------ | --------------------- |
| [**🔴 Actual Responses**](actual-responses.md) | **⚠️ START HERE - Verified API responses** | `actual-responses.md` |
| [Schemas](schemas.md)                          | Data model definitions                     | `schemas.md`          |
|                                                |                                            |                       |
| [Anomalies](anomalies.md)                      | 3 endpoints                                | `anomalies.md`        |
| [Authentication](authentication.md)            | 2 endpoints                                | `authentication.md`   |
| [Backup Tasks](backup-tasks.md)                | 2 endpoints                                | `backup-tasks.md`     |
| [Backups](backups.md)                          | 2 endpoints                                | `backups.md`          |
| [Calendar](calendar.md)                        | 4 endpoints                                | `calendar.md`         |
| [Missions](missions.md)                        | 3 endpoints                                | `missions.md`         |
| [Robots](robots.md)                            | 4 endpoints                                | `robots.md`           |
| [Run Archives](run-archives.md)                | 1 endpoints                                | `run-archives.md`     |
| [Run Captures](run-captures.md)                | 2 endpoints                                | `run-captures.md`     |
| [Run Events](run-events.md)                    | 2 endpoints                                | `run-events.md`       |
| [Run Facets](run-facets.md)                    | 3 endpoints                                | `run-facets.md`       |
| [Run Statistics](run-statistics.md)            | 2 endpoints                                | `run-statistics.md`   |
| [Runs](runs.md)                                | 3 endpoints                                | `runs.md`             |
| [SiteDocks](sitedocks.md)                      | 2 endpoints                                | `sitedocks.md`        |
| [SiteElements](siteelements.md)                | 2 endpoints                                | `siteelements.md`     |
| [SiteWalks](sitewalks.md)                      | 4 endpoints                                | `sitewalks.md`        |
| [Webhooks](webhooks.md)                        | 5 endpoints                                | `webhooks.md`         |

---

## 🚨 Important Files

| File                                           | Purpose                               | When to Use                        |
| ---------------------------------------------- | ------------------------------------- | ---------------------------------- |
| [**actual-responses.md**](actual-responses.md) | **Verified real API responses**       | **Check FIRST before coding**      |
| `orbit-api/*.bru`                              | Bruno collection (requests/responses) | Send requests, view real responses |
| [schemas.md](schemas.md)                       | Data model definitions                | Understand field types             |
| [AGENTS.md](../AGENTS.md)                      | AI Agent guidelines                   | Prevent false assumptions          |

## Authentication

Most endpoints require authentication. Obtain an API token from the Orbit instance
and add it to the request header:

```
{"Authorization": "Bearer <API_TOKEN>"}
```

**Testing Authentication:**

```bash
# Verify your token works
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-orbit-server/api/v0/api_token/authenticate"

# Expected response: 200 OK
```

See [authentication.md](authentication.md) for details.

---

## Common Pitfalls (For AI Agents)

### ❌ WRONG: Assuming Response Values

```python
# This code LOOKS correct but may be completely wrong:
status_map = {
    "success": "COMP",     # Is "success" the real value?
    "completed": "COMP",   # Or is it "completed"? Or "SUCCEEDED"?
    "failed": "FAIL",      # Nobody knows - never tested!
}
```

**Problem:** OpenAPI schema shows `missionStatus: string` but doesn't list possible values.

### ✅ CORRECT: Verify First, Code Second

```python
# Step 1: Check actual-responses.md
# Step 2a: If verified → use real values
status_map = {
    "success": "COMP",     # ✅ Verified in actual-responses.md (observed 45 times)
    "error": "FAIL",       # ✅ Verified in actual-responses.md (observed 20 times)
}

# Step 2b: If NOT verified → request user to send requests in Bruno
# "Before implementing, please:
#  1. Open Bruno → orbit-api collection
#  2. Send runs.bru request
#  3. Check response → note missionStatus values
#  Then I'll use the REAL values instead of assumptions."
```

**See:** [actual-responses.md](actual-responses.md) for verification workflow.

---

## Quick Reference

| Method | Endpoint                           | Category                            | Summary                                               |
| ------ | ---------------------------------- | ----------------------------------- | ----------------------------------------------------- |
| POST   | ~~`/login`~~                       | [Authentication](authentication.md) | Authenticates with username and password.             |
| GET    | `/api_token/authenticate`          | [Authentication](authentication.md) | Authenticates the API token that is provided in th... |
| GET    | `/calendar/schedule`               | [Calendar](calendar.md)             | Returns calendar events on the specified Orbit ins... |
| POST   | `/calendar/schedule`               | [Calendar](calendar.md)             | Create a calendar event to play a mission.            |
| DELETE | `/calendar/schedule/{eventid}`     | [Calendar](calendar.md)             | Removes the specified calendar event.                 |
| POST   | `/calendar/disable-enable`         | [Calendar](calendar.md)             | Disable/enable mission scheduled on Orbit.            |
| GET    | `/runs/{runUuid}`                  | [Runs](runs.md)                     | Retrieve a run by its uuid.                           |
| GET    | `/runs/{runUuid}/log`              | [Runs](runs.md)                     | Retrieve a run log from its uuid.                     |
| GET    | `/runs/`                           | [Runs](runs.md)                     | Query a collection of runs.                           |
| GET    | `/run_events/`                     | [Run Events](run-events.md)         | Retrieve a collection of run events.                  |
| GET    | `/run_events/{runEventUuid}`       | [Run Events](run-events.md)         | Retrieves a single run event resource by uuid.        |
| GET    | `/run_captures/`                   | [Run Captures](run-captures.md)     | Retrieve a collection of run captures.                |
| GET    | `/run_captures/{runCaptureUuid}`   | [Run Captures](run-captures.md)     | Retrieves a single run capture resource by uuid.      |
| GET    | `/run_archives/{runId}`            | [Run Archives](run-archives.md)     | Downloads a zip file containing a run's data.         |
| GET    | `/runs/facets/actions`             | [Run Facets](run-facets.md)         | Retrieves a list of action descriptions which matc... |
| GET    | `/runs/facets/robots`              | [Run Facets](run-facets.md)         | Retrieves a list of robot descriptions which match... |
| GET    | `/runs/facets/missions`            | [Run Facets](run-facets.md)         | Retrieves a list of every unique mission which pro... |
| GET    | `/run_statistics/sessions`         | [Run Statistics](run-statistics.md) | Retrieves a list of session statistics which match... |
| GET    | `/run_statistics/sessions_summary` | [Run Statistics](run-statistics.md) | Retrieves a summary of session statistics which ma... |
| GET    | `/site_walks/`                     | [SiteWalks](sitewalks.md)           | Retrieve a collection of all SiteWalks on Orbit.      |
| GET    | `/site_walks/{uuid}`               | [SiteWalks](sitewalks.md)           | Retrieves a single SiteWalk resource by uuid.         |
| DELETE | `/site_walks/{uuid}`               | [SiteWalks](sitewalks.md)           | Removes the specified SiteWalk.                       |
| POST   | `/site_walks`                      | [SiteWalks](sitewalks.md)           | Adds a new SiteWalk to Orbit. It also updates a pr... |
| GET    | `/site_elements/{uuid}`            | [SiteElements](siteelements.md)     | Retrieves a single SiteElement resource by uuid.      |
| POST   | `/site_elements`                   | [SiteElements](siteelements.md)     | Adds a new SiteElement to Orbit. It also updates a... |
| GET    | `/site_docks/{uuid}`               | [SiteDocks](sitedocks.md)           | Retrieves a single SiteDock resource by uuid.         |
| POST   | `/site_docks`                      | [SiteDocks](sitedocks.md)           | Adds a new SiteDock to Orbit. It also updates a pr... |
| GET    | `/robots`                          | [Robots](robots.md)                 | Retrieves a complete list of robot information on ... |
| POST   | `/robots`                          | [Robots](robots.md)                 | Adds a new robot to Orbit.                            |
| GET    | `/robots/{robotHostname}`          | [Robots](robots.md)                 | Retrieves information about a single robot.           |
| DELETE | `/robots/{robotHostname}`          | [Robots](robots.md)                 | Removes the specified robot.                          |
| GET    | `/webhooks`                        | [Webhooks](webhooks.md)             | Retrieves a complete list of registered webhooks o... |
| POST   | `/webhooks`                        | [Webhooks](webhooks.md)             | Adds a new webhook to Orbit.                          |
| GET    | `/webhooks/{uuid}`                 | [Webhooks](webhooks.md)             | Retrieve a webhook by its uuid.                       |
| POST   | `/webhooks/{uuid}`                 | [Webhooks](webhooks.md)             | Updates a specific webhook on Orbit.                  |
| DELETE | `/webhooks/{uuid}`                 | [Webhooks](webhooks.md)             | Removes the specified webhook.                        |
| GET    | ~~`/missions`~~                    | [Missions](missions.md)             | Retrieves a complete list of mission information o... |
| GET    | ~~`/missions/{missionId}`~~        | [Missions](missions.md)             | Retrieves information about a single mission.         |
| DELETE | ~~`/missions/{missionId}`~~        | [Missions](missions.md)             | Removes the specified mission.                        |
| GET    | `/anomalies`                       | [Anomalies](anomalies.md)           |                                                       |
| PATCH  | `/anomalies`                       | [Anomalies](anomalies.md)           |                                                       |
| PATCH  | `/anomalies/{anomalyId}`           | [Anomalies](anomalies.md)           |                                                       |
| GET    | `/backup_tasks`                    | [Backup Tasks](backup-tasks.md)     | Retrieves a list of backup tasks.                     |
| POST   | `/backup_tasks`                    | [Backup Tasks](backup-tasks.md)     | Creates a new backup task.                            |
| GET    | `/backups/{taskId}`                | [Backups](backups.md)               | Retrieves a backup tar file given a task ID.          |
| DELETE | `/backups/{taskId}`                | [Backups](backups.md)               | Deletes a backup tar file from the Orbit instance ... |
