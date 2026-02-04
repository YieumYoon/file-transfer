# Schemas

[← Back to Index](README.md)


This document contains all data model definitions used by the API.


## Table of Contents

- [Anomaly](#anomaly)
- [BackupParameters](#backupparameters)
- [BackupTask](#backuptask)
- [DashboardBarQuery](#dashboardbarquery)
- [DashboardFooQuery](#dashboardfooquery)
- [DashboardFooSectionBarResults](#dashboardfoosectionbarresults)
- [DashboardQuery](#dashboardquery)
- [DashboardQueryHandles](#dashboardqueryhandles)
- [DashboardResultSet](#dashboardresultset)
- [DashboardSecret](#dashboardsecret)
- [Mission](#mission)
- [Robot](#robot)
- [Run](#run)
- [RunCapture](#runcapture)
- [RunEvent](#runevent)
- [Schedule](#schedule)
- [SiteDock](#sitedock)
- [SiteElement](#siteelement)
- [SiteWalk](#sitewalk)
- [SnowflakeSecrets](#snowflakesecrets)
- [Webhook](#webhook)

---

### Anomaly

An anomaly/alert detected by a Spot mission element

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - The unique identifier for the anomaly.
- **time** (`string`)
  - Format: `date-time`
- **createdAt** (`string`)
  - Format: `date-time`
- **elementId** (`string`)
- **assetId** (`string`)
- **name** (`string`)
- **severity** (`integer`)
- **title** (`string`)
- **source** (`string`)
- **runUuid** (`string`)
- **runEventUuid** (`string`)
- **status** (`string`)
  - Possible values: `open`, `closed`
- **statusModifiedAt** (`string`)
  - Format: `date-time`
- **statusModifiedBy** (`string`)

---

### BackupParameters

Parameters used to define the type of backup task. Determines whether to include missions and/or inspection data captures in the backup.

**Type:** `object`


**Properties:**

- **includeMissions** (`boolean`)
  - Specifies whether to include missions in the backup. When enabled, this will include all mission data, as well as associated robot map data and site maps.
- **includeCaptures** (`boolean`)
  - Specifies whether to include inspection data captures in the backup.

---

### BackupTask

A BackupTask is a data structure representing a backup task of the Orbit instance. It can include mission data and/or inspection data captures based on BackupParameters.

**Type:** `object`


**Properties:**

- **taskId** (`string`)
  - The unique identifier for this backup task.
- **startedAt** (`string`)
  - When this backup task was started.
  - Format: `date-time`
- **status** (`string`)
  - The status of the backup task.
  - Possible values: `Starting`, `Creating database dump`, `Creating zip file`, `Completed`, `Error`, `Cancelled`
- **filename** (`string`)
  - The filename of the backup.
- **size** (`number`)
  - The size of the backup in bytes.
- **error** (`string`)
  - The error message if the backup task failed.
- **params** (`[BackupParameters](schemas.md#backupparameters)`)

---

### DashboardBarQuery

Example dashboard query of specific type

**Type:** `object`


**Properties:**

- **type** (`string`)
- **booleanParam** (`boolean`)
  - Just a demonstration of arbitrary allowable query parameters

---

### DashboardFooQuery

Example dashboard query of specific type

**Type:** `object`


**Properties:**

- **type** (`string`)
- **booleanParam** (`boolean`)
  - Just a demonstration of arbitrary allowable query parameters

---

### DashboardFooSectionBarResults

Example of dashboard section result type

**Type:** `object`


**Properties:**

- **type** (`string`)
  - All ResultSets will define a result type string to allow for Typescript type narrowing
- **results** (`array of array`)
  - All ResultSets will return data as a list of strongly-typed tuples, one for each row of data

---

### DashboardQuery

This oneOf will grow to accomadate each of the supported parameterized dashboards

**Type:** `object`


**One of:**

- [DashboardFooQuery](schemas.md#dashboardfooquery)
- [DashboardBarQuery](schemas.md#dashboardbarquery)

---

### DashboardQueryHandles

Map from dashboard section id to query handle id

**Type:** `object`


**Additional Properties:** `string`

---

### DashboardResultSet

Return from Snowflake query. This oneOf will grow to accommodate each of the supported dashboard section types

**Type:** `object`


**One of:**

- [DashboardFooSectionBarResults](schemas.md#dashboardfoosectionbarresults)

---

### DashboardSecret

This oneOf can grow to accomadate secrets for any of the supported DB backends, although right now it looks a bit like premature abstraction

**Type:** `object`


**One of:**

- [SnowflakeSecrets](schemas.md#snowflakesecrets)

---

### Mission

> **⚠️ DEPRECATED**

Warning: This endpoint is deprecated. Use SiteWalk instead!

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - Orbit's unique id for this mission. Use this as a parameter for operations like scheduling missions.
- **mission_id** (`string`)
  - The mission id from the robot when this mission was uploaded to Orbit.
- **name** (`string`)
  - A descriptive label for the mission.
- **saved_at** (`string`)
  - When this mission was saved.
  - Format: `date-time`

---

### Robot

A Robot is a data structure representing a robot that is used to execute autonomous operations.

**Type:** `object`


**Properties:**

- **robotIndex** (`integer`)
  - The index at which this robot is registered. This is a number between 0 and the max for your Orbit server (typically 32).
- **hostname** (`string`)
  - The hostname where the robot can be reached.
- **nickname** (`string`)
  - A descriptive label for the robot.
- **username** (`string`)
  - The username that Orbit is connected to the robot with.

---

### Run

A Run represents a period of robot operation. Both teleoperation and autonomous operations are represented as Runs.

**Type:** `object`


**Properties:**

- **actionCount** (`integer`)
- **pendingActionCount** (`integer`)
- **uuid** (`string`)
  - A unique identifier for this run.
- **runType** (`string`)
  - Whether the run was of a mission or teleoperation.
  - Possible values: `teleop`, `mission`
- **startTime** (`string`)
  - When this run started.
  - Format: `date-time`
- **endTime** (`string`)
  - When this run completed.
  - Format: `date-time`
- **robotHostname** (`string`)
  - The hostname of the robot being operated.
- **robotSerial** (`string`)
  - The serial of the robot being operated.
- **robotNickname** (`string`)
  - The nickname of the robot being operated.
- **operatorId** (`string`)
  - The username of the driver.
- **missionStatus** (`string`)
  - The status of the mission this run played.
- **missionName** (`string`)
  - The name of the mission this run played.
- **robotSoftwareMajorVersion** (`integer`)
  - The robot software major version during operation.
- **robotSoftwareMinorVersion** (`integer`)
  - The robot software minor version during operation.
- **robotSoftwarePatchVersion** (`integer`)
  - The robot software patch version during operation.
- **robotSoftwareGitHash** (`string`)
  - The version hash of the robot software used during operation.

---

### RunCapture

A RunCapture describes a data point captured during a particular RunEvent.

**Type:** `object`


**Properties:**

- **time** (`string`)
  - The time at which this result was captured.
  - Format: `date-time`
- **uuid** (`string`)
  - A unique identifier for this result.
- **runEventUuid** (`string`)
  - The unique identifier for the run event during which this result was captured.
- **dataUrl** (`string`)
  - The path to the file holding this result's data.
- **createdAt** (`string`)
  - When the result was stored in Orbit.
- **keyResults** (`array of object`)
  - A collection of key value pairs summarizing this result.
- **channelName** (`string`)
  - The name of the action channel which produced this result.
- **actionChannelRunFlagUuid** (`string`)
  - A unique identifier for a flag on this data.

---

### RunEvent

A RunEvent represents the output of an action executed during a Run. It contains all the RunCaptures associated with the action.

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - A unique identifier for this run event.
- **runUuid** (`string`)
  - The unique identifier for the run in which this event took place.
- **time** (`string`)
  - When this event took place on robot.
  - Format: `date-time`
- **createdAt** (`string`)
  - When this event was stored in Orbit.
- **actionName** (`string`)
  - The name of the action which this event represents.
- **actionRunArchiveFileUrl** (`string`)
  - The path to the event's data and metadata archive.
- **error** (`integer`)
  - The error code for an error which occured during this event.
- **actionUuid** (`string`)
  - A unique identifier for the action this event represents.
- **missionName** (`string`)
  - The name of the mission during which this event took place.
- **metadataFileUrl** (`string`)
  - The path to the metadata.json file for this event.
- **eventType** (`string`)
  - The type of run event this is. Could be an action execution (daq) or a user triggered screenshot.
  - Possible values: `daq`, `screenshot`
- **dataCaptures** (`array of [RunCapture](schemas.md#runcapture)`)

---

### Schedule

A schedule describes when and how often a robot should execute an autonomous mission.

**Type:** `object`


**Properties:**

- **eventMetadata** (`object`)
  - Metadata for the calendar event.
- **agent** (`object`)
  - Information about the agent(robot) for the calendar event.
- **task** (`object`)
  - Information about the agent(robot) for the calendar event.
- **schedule** (`object`)
  - Information about the agent(robot) for the calendar event.

---

### SiteDock

A SiteDock is a representation of robot's docking station.

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - Unique identifier for the SiteDock.
- **name** (`string`)
  - The fiducial number of the dock.
- **dockedWaypointId** (`string`)
  - The waypoint where the dock is located.
- **targetPrepPose** (`object`)
  - When it is time for the robot to dock, it will approach this target before issuing docking commands. 
- **createdAt** (`string`)
  - When the SiteDock was stored in Orbit.
- **modifiedAt** (`string`)
  - When the SiteDock was modified in Orbit.

---

### SiteElement

A SiteElement describes what a robot should do and where to do it.

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - Unique identifier for the SiteElement.
- **name** (`string`)
  - The name for the SiteElement.
- **waypointId** (`string`)
  - The location of the element.
- **waypointMaxDistance** (`number`)
  - The maximum distance [meters] that defines when we have reached the element waypoint.
- **waypointMaxYaw** (`number`)
  - The maximum yaw [radians] that defines when we have reached the element waypoint.
- **action** (`object`)
  - Action performed at target destination.
- **targetFailureBehavior** (`object`)
  - Default behavior if a robot fails to navigate to a given position.
- **actionFailureBehavior** (`object`)
  - Default behavior if a robot fails to perform an action.
- **actionDuration** (`object`)
  - The maximum time spent performing the action.
- **relocalize** (`object`)
  - Whether the robot should relocalize at the target.
- **actionWrapper** (`object`)
  - What the robot should do prior to and during an action.
- **createdAt** (`string`)
  - When the SiteElement was stored in Orbit.
- **modifiedAt** (`string`)
  - When the SiteElement was modified in Orbit.

---

### SiteWalk

A SiteWalk describes a series of tasks that define autonomous robot operation. It contains SiteElements and SiteDocks together with other parameters that define autonomous operation.

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - Unique identifier for the SiteWalk.
- **name** (`string`)
  - The name for the SiteWalk.
- **siteElementIds** (`array of string`)
  - References to elements in this walk in the order they will be visited.
- **globalParameters** (`object`)
  - Parameters that apply to the entire mission.
- **siteDockIds** (`object`)
  - References to docks to be used by this walk.
- **createdAt** (`string`)
  - When the SiteWalk was stored in Orbit.
- **modifiedAt** (`string`)
  - When the SiteWalk was modified in Orbit.
- **siteElementMetadata** (`object`)
  - Metadata for each SiteElement references in SiteElement_ids.
- **targetFailureBehavior** (`object`)
  - Default behavior if a robot fails to navigate to a given position.
- **actionFailureBehavior** (`object`)
  - Default behavior if a robot fails to perform an action.
- **preferRecordedRoutes** (`boolean`)
  - Whether or not to take shortcuts.
- **batteryMonitor** (`object`)
  - Default behavior for leaving and returning to dock based on the robot battery charge.
- **travelParams** (`object`)
  - Travel params common to the entire SiteWalk.
- **entityParams** (`object`)
  - Entity params used by all elements.
- **skipDockingAfterCompletion** (`boolean`)
  - Whether or not to dock after executing all actions.

---

### SnowflakeSecrets

**Type:** `object`


**Properties:**

- **backend** (`string`) *(required)*
  - Indicates to the server that this contains the keys necessary to interact with snowflake
- **accountId** (`string`) *(required)*
  - Hyphenated Account Identifier for Snowflake. In the default case, this should be GCRPOWI-BOSDYN
- **username** (`string`) *(required)*
  - LOGIN_NAME of user in Snowflake, visible with `DESCRIBE USER <user>;`
- **privateKey** (`string`) *(required)*
  - Private Key stored as a ,.p8 file. Should look like -----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFHDBOBgkqh...; that is, include the prefix and the newline characters
- **passphrase** (`string`)
  - Optional encryption passphrase for the private key

---

### Webhook

A Webhook is a mechanism by which Orbit sends real-time data from robot operation to any subscribed external systems.

**Type:** `object`


**Properties:**

- **uuid** (`string`)
  - Unique identifier for the webhook instance.
- **url** (`string`)
  - The url of the webhook instance.
- **enabled** (`boolean`)
  - Determines whether or not to send the data to url from the webhook.
- **archived** (`boolean`)
  - Determines whether or not the webhook is archived.
- **events** (`object`)
  - The list that contains what type of events would trigger sending the data to url. These can also be defined as payload types.
- **validateTlsCert** (`boolean`)
  - Whether or not to validate TLS certificate.
- **secret** (`string`)
  - The secret required to update the webhook (32 bit hex string).

---
