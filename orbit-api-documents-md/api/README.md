# Orbit Web API

**Version:** 5.0.0

**Base URL:** `/api/v0`


The Orbit web API provides access to a variety of resources through RESTful http endpoints.


## How to Use This Documentation

This documentation is organized into separate files by API category. 
Each category file contains all endpoints related to that functionality.


**For AI Agents:** Start here to understand the API structure, then navigate to the 
specific category file for detailed endpoint information. Schema definitions are in `schemas.md`.


## API Categories

| Category | Description | File |
|----------|-------------|------|
| [Anomalies](anomalies.md) | 3 endpoints | `anomalies.md` |
| [Authentication](authentication.md) | 2 endpoints | `authentication.md` |
| [Backup Tasks](backup-tasks.md) | 2 endpoints | `backup-tasks.md` |
| [Backups](backups.md) | 2 endpoints | `backups.md` |
| [Calendar](calendar.md) | 4 endpoints | `calendar.md` |
| [Missions](missions.md) | 3 endpoints | `missions.md` |
| [Robots](robots.md) | 4 endpoints | `robots.md` |
| [Run Archives](run-archives.md) | 1 endpoints | `run-archives.md` |
| [Run Captures](run-captures.md) | 2 endpoints | `run-captures.md` |
| [Run Events](run-events.md) | 2 endpoints | `run-events.md` |
| [Run Facets](run-facets.md) | 3 endpoints | `run-facets.md` |
| [Run Statistics](run-statistics.md) | 2 endpoints | `run-statistics.md` |
| [Runs](runs.md) | 3 endpoints | `runs.md` |
| [SiteDocks](sitedocks.md) | 2 endpoints | `sitedocks.md` |
| [SiteElements](siteelements.md) | 2 endpoints | `siteelements.md` |
| [SiteWalks](sitewalks.md) | 4 endpoints | `sitewalks.md` |
| [Webhooks](webhooks.md) | 5 endpoints | `webhooks.md` |

| [Schemas](schemas.md) | Data model definitions | `schemas.md` |

## Authentication

Most endpoints require authentication. Obtain an API token from the Orbit instance 
and add it to the request header:

```
{"Authorization": "Bearer <API_TOKEN>"}
```


## Quick Reference

| Method | Endpoint | Category | Summary |
|--------|----------|----------|---------|
| POST | ~~`/login`~~ | [Authentication](authentication.md) | Authenticates with username and password. |
| GET | `/api_token/authenticate` | [Authentication](authentication.md) | Authenticates the API token that is provided in th... |
| GET | `/calendar/schedule` | [Calendar](calendar.md) | Returns calendar events on the specified Orbit ins... |
| POST | `/calendar/schedule` | [Calendar](calendar.md) | Create a calendar event to play a mission. |
| DELETE | `/calendar/schedule/{eventid}` | [Calendar](calendar.md) | Removes the specified calendar event. |
| POST | `/calendar/disable-enable` | [Calendar](calendar.md) | Disable/enable mission scheduled on Orbit. |
| GET | `/runs/{runUuid}` | [Runs](runs.md) | Retrieve a run by its uuid. |
| GET | `/runs/{runUuid}/log` | [Runs](runs.md) | Retrieve a run log from its uuid. |
| GET | `/runs/` | [Runs](runs.md) | Query a collection of runs. |
| GET | `/run_events/` | [Run Events](run-events.md) | Retrieve a collection of run events. |
| GET | `/run_events/{runEventUuid}` | [Run Events](run-events.md) | Retrieves a single run event resource by uuid. |
| GET | `/run_captures/` | [Run Captures](run-captures.md) | Retrieve a collection of run captures. |
| GET | `/run_captures/{runCaptureUuid}` | [Run Captures](run-captures.md) | Retrieves a single run capture resource by uuid. |
| GET | `/run_archives/{runId}` | [Run Archives](run-archives.md) | Downloads a zip file containing a run's data. |
| GET | `/runs/facets/actions` | [Run Facets](run-facets.md) | Retrieves a list of action descriptions which matc... |
| GET | `/runs/facets/robots` | [Run Facets](run-facets.md) | Retrieves a list of robot descriptions which match... |
| GET | `/runs/facets/missions` | [Run Facets](run-facets.md) | Retrieves a list of every unique mission which pro... |
| GET | `/run_statistics/sessions` | [Run Statistics](run-statistics.md) | Retrieves a list of session statistics which match... |
| GET | `/run_statistics/sessions_summary` | [Run Statistics](run-statistics.md) | Retrieves a summary of session statistics which ma... |
| GET | `/site_walks/` | [SiteWalks](sitewalks.md) | Retrieve a collection of all SiteWalks on Orbit. |
| GET | `/site_walks/{uuid}` | [SiteWalks](sitewalks.md) | Retrieves a single SiteWalk resource by uuid. |
| DELETE | `/site_walks/{uuid}` | [SiteWalks](sitewalks.md) | Removes the specified SiteWalk. |
| POST | `/site_walks` | [SiteWalks](sitewalks.md) | Adds a new SiteWalk to Orbit. It also updates a pr... |
| GET | `/site_elements/{uuid}` | [SiteElements](siteelements.md) | Retrieves a single SiteElement resource by uuid. |
| POST | `/site_elements` | [SiteElements](siteelements.md) | Adds a new SiteElement to Orbit. It also updates a... |
| GET | `/site_docks/{uuid}` | [SiteDocks](sitedocks.md) | Retrieves a single SiteDock resource by uuid. |
| POST | `/site_docks` | [SiteDocks](sitedocks.md) | Adds a new SiteDock to Orbit. It also updates a pr... |
| GET | `/robots` | [Robots](robots.md) | Retrieves a complete list of robot information on ... |
| POST | `/robots` | [Robots](robots.md) | Adds a new robot to Orbit. |
| GET | `/robots/{robotHostname}` | [Robots](robots.md) | Retrieves information about a single robot. |
| DELETE | `/robots/{robotHostname}` | [Robots](robots.md) | Removes the specified robot. |
| GET | `/webhooks` | [Webhooks](webhooks.md) | Retrieves a complete list of registered webhooks o... |
| POST | `/webhooks` | [Webhooks](webhooks.md) | Adds a new webhook to Orbit. |
| GET | `/webhooks/{uuid}` | [Webhooks](webhooks.md) | Retrieve a webhook by its uuid. |
| POST | `/webhooks/{uuid}` | [Webhooks](webhooks.md) | Updates a specific webhook on Orbit. |
| DELETE | `/webhooks/{uuid}` | [Webhooks](webhooks.md) | Removes the specified webhook. |
| GET | ~~`/missions`~~ | [Missions](missions.md) | Retrieves a complete list of mission information o... |
| GET | ~~`/missions/{missionId}`~~ | [Missions](missions.md) | Retrieves information about a single mission. |
| DELETE | ~~`/missions/{missionId}`~~ | [Missions](missions.md) | Removes the specified mission. |
| GET | `/anomalies` | [Anomalies](anomalies.md) |  |
| PATCH | `/anomalies` | [Anomalies](anomalies.md) |  |
| PATCH | `/anomalies/{anomalyId}` | [Anomalies](anomalies.md) |  |
| GET | `/backup_tasks` | [Backup Tasks](backup-tasks.md) | Retrieves a list of backup tasks. |
| POST | `/backup_tasks` | [Backup Tasks](backup-tasks.md) | Creates a new backup task. |
| GET | `/backups/{taskId}` | [Backups](backups.md) | Retrieves a backup tar file given a task ID. |
| DELETE | `/backups/{taskId}` | [Backups](backups.md) | Deletes a backup tar file from the Orbit instance ... |