# Enterprise Naming Convention — **Compact Guide**

*Version 1.1 — Owner: AME | Applies to: MSSQL, Ignition (Tags & Scripting)*

***

## 0) Principles

*   **Consistency > preference** · **Clarity > brevity** · **Hierarchy first** (Ignition).
*   **No spaces or special chars**; use alphanumerics.
    *   **Tag paths** use `/`. **Avoid `_`** in tag/folder names unless vendor‑forced.
*   **Separation of concerns**: SQL / Tags / Python each have their own casing rules.

***

## 1) SQL (MSSQL) — **PascalCase**

**Objects**

*   **Schemas**: `Robotics`, `Production`, `Quality`
*   **Tables (plural)**: `SpotMissions`, `RobotUnits`
*   **Views (singular)**: `vwMissionEvent`, `vwRobotUnit`
*   **Stored Procedures**: `usp_GetMissionStatus`, `usp_UpsertRobotUnit`
*   **UDFs**: Scalar `ufn_IsMissionComplete`; TVF `utfn_SplitCsv`

**Schema vs. Prefix (important)**

*   **Preferred (standard MSSQL)**: Use schemas, reference objects as `Robotics.<TableName>` (e.g., `Robotics.RobotUnits`).
*   **If schemas cannot be used in your environment**: Use a **schema-like prefix** in `dbo` and reference objects as `Robotics<TableName>` (e.g., `RoboticsRobotUnits`).  
    *This is an approved exception for this project when `Robotics.<tablename>` is not available.*

**Keys & Columns**

*   **PK**: `TableNameId` *(enforced)*; **FK**: `<ReferencedTable>Id`
*   **Columns**: `BatteryLevel`, `EventTimestampUtc`, `IsActive`
*   **Booleans**: `Is/Has/Can…` → `IsConnected`, `HasError`, `CanDock`
*   **Timestamps (UTC)**: `…AtUtc` → `CreatedAtUtc`, `UpdatedAtUtc`
*   **Enums**: `…Code` + lookup table → `MissionStateCode`
*   **Units (only if ambiguous)**: `DistanceMm`, `PayloadKg`, `TemperatureC`
*   **Auditing**: `CreatedAtUtc`, `CreatedBy`, `UpdatedAtUtc`, `UpdatedBy`

**Indexes & Constraints**

*   Constraint and index naming is **mandatory**, not optional.
*   Use these exact patterns:
    *   `PK_<Table>`
    *   `FK_<From>_<To>`
    *   `UQ_<Table>_<Columns>`
    *   `IX_<Table>_<Columns>`
*   **Why enforce**: deterministic names speed up debugging (constraint violations), enable repeatable migrations, and keep scripts/queries/docs consistent across environments.

**SQL Example**

```sql
CREATE SCHEMA Robotics;

CREATE TABLE Robotics.RobotUnits (
  RobotUnitId INT IDENTITY(1,1) PRIMARY KEY,
  Name NVARCHAR(100) NOT NULL,
  SerialNumber NVARCHAR(50) NOT NULL,
  IsActive BIT NOT NULL DEFAULT 1,
  CreatedAtUtc DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedAtUtc DATETIME2(3) NULL
);

CREATE PROCEDURE Robotics.usp_GetMissionStatus @MissionId NVARCHAR(50)
AS
BEGIN
  SET NOCOUNT ON;
  SELECT TOP 1 MissionStateCode, StartedAtUtc, CompletedAtUtc
  FROM Robotics.SpotMissions
  WHERE MissionId = @MissionId
  ORDER BY SpotMissionId DESC;
END;
```

**SQL Example (schema-less alternative)**

```sql
-- If schemas are not available, keep objects in dbo and prefix the table name.
CREATE TABLE RoboticsRobotUnits (
  RobotUnitId INT IDENTITY(1,1) PRIMARY KEY,
  Name NVARCHAR(100) NOT NULL,
  SerialNumber NVARCHAR(50) NOT NULL,
  IsActive BIT NOT NULL DEFAULT 1,
  CreatedAtUtc DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedAtUtc DATETIME2(3) NULL
);
```

***

## 2) Ignition Tags & UDTs — **PascalCase + ISA‑95**

**Namespace / Folder Hierarchy**

    <Enterprise>/<Site>/<Area>/<Line>/<Cell>/<Device>/<Tag>

*   **Names**: PascalCase; numeric suffix with leading zeros → `Line001`, `Spot002`
*   **Examples**

<!---->

    ClevelandPlant/Avon/Assembly/Line001/Spot001/BatteryLevel
    ClevelandPlant/Avon/Assembly/Line001/Spot001/MissionId
    ClevelandPlant/Avon/Inspection/Line002/Spot002/IsConnected

**Tag Names (under Device)**

*   **PascalCase**: `BatteryLevel`, `IsCharging`, `PoseX`, `PoseY`, `PoseTheta`, `MissionId`
*   **Booleans**: `Is/Has/Can…`
*   **Units (if needed)**: `DistanceMm`, `SpeedMps`
*   **Status/Timestamps**: `QualityCode`, `CommStatus`, `SampledAtUtc`, `ReceivedAtUtc`

**UDT (Template)**

    SpotRobot
      BatteryLevel (Float)
      IsConnected (Boolean)
      MissionId (String)
      PoseX (Float), PoseY (Float), PoseTheta (Float)
      RobotStateCode (String)
      SampledAtUtc (DateTime)

**Historian**

*   Store **full tag path**; use engineering deadbands; clear alarm names (`BatteryLow`, `CommLost`).

**Don’ts**

*   Don’t mix cases or formats: `Spot1` / `Spot001` / `spot001` / `Spot_001`
*   Don’t flatten devices outside **Site/Area/Line** hierarchy.
*   **Don’t include the device name inside the tag name** — the path provides context.  
    *Bad*: `Line001/Spot001/Spot001BatteryLevel`  
    *Good*: `Line001/Spot001/BatteryLevel`
***

## 3) Ignition Scripting (Python/Jython) — **PEP 8**

*   **Variables & Functions**: `snake_case` → `battery_level`, `start_mission()`
*   **Constants**: `UPPER_SNAKE_CASE` → `DEFAULT_TIMEOUT_S`
*   **Classes**: `PascalCase` → `SpotController`
*   **Modules/Files**: `snake_case.py` → `robot_service.py`

**Build Tag Paths via Helpers**

```python
ENTERPRISE = "ClevelandPlant"
SITE = "Avon"
AREA = "Assembly"
LINE = "Line001"

def device_path(device_name):
    return f"{ENTERPRISE}/{SITE}/{AREA}/{LINE}/{device_name}"

SPOT001 = device_path("Spot001")
BATTERY_TAG = f"{SPOT001}/BatteryLevel"
```

**Named Queries**

*   Names: PascalCase → `GetMissionStatus`, `UpsertRobotUnit`
*   Parameters: `snake_case` → `mission_id`, `robot_unit_id`

**Python Read**

```python
def get_battery_level(device="Spot001"):
    base = f"ClevelandPlant/Avon/Assembly/Line001/{device}"
    return system.tag.readBlocking([f"{base}/BatteryLevel"])[0].value
```

**Multi‑tag reads to dictionaries (pattern)**

*Recommendation*: For multi‑tag reads, map tag paths to **snake\_case** keys and return a dictionary for clarity and parity with your naming rules.

```python
def read_device_snapshot(device="Spot001"):
    base = f"ClevelandPlant/Avon/Assembly/Line001/{device}"
    tags = {
        "battery_level": f"{base}/BatteryLevel",
        "is_connected": f"{base}/IsConnected",
        "robot_state_code": f"{base}/RobotStateCode",
        "sampled_at_utc": f"{base}/SampledAtUtc",
    }
    values = system.tag.readBlocking(list(tags.values()))
    return {k: v.value for k, v in zip(tags.keys(), values)}
```

***

## 4) Cross‑Layer Mapping (Case Rules)

*   **SQL & Tags**: **PascalCase**
*   **Python**: **snake\_case**
*   **Enums**: `…Code` across all layers

| Concept         | SQL                   | Ignition Tag       | Python var              |
| --------------- | --------------------- | ------------------ | ----------------------- |
| Device          | `Robotics.RobotUnits` | `…/Spot001/`        | `device_path("Spot001")` |
| Mission ID      | `MissionId`           | `…/MissionId`      | `mission_id`            |
| Battery         | `BatteryLevel`        | `…/BatteryLevel`   | `battery_level`         |
| Connectivity    | `IsActive/IsOnline`   | `…/IsConnected`    | `is_connected`          |
| State (enum)    | `RobotStateCode`      | `…/RobotStateCode` | `robot_state_code`      |
| Timestamp (UTC) | `…AtUtc`              | `SampledAtUtc`     | `sampled_at_utc`        |

***

## 5) Reserved Prefix/Suffix Conventions

*   **Booleans**: `Is/Has/Can` → `IsConnected`, `HasFault`, `CanDock`
*   **Units**: `Mm`, `M`, `Kg`, `C`, `Deg`, `Mps`
*   **Timestamps**: `…AtUtc` → `StartedAtUtc`, `CompletedAtUtc`
*   **IDs/Keys**: SQL/Tags `…Id`; Python `…_id`
*   **Enums**: `…Code` + lookup table

***

## 6) Alarms & Events

*   **Alarm names**: short, actionable → `BatteryLow`, `CommLost`, `Overtemp`, `EstopEngaged`
*   **Events**
    *   SQL: `MissionEvents` with `EventTypeCode`, `EventTimestampUtc`
    *   Tags: optional `LastAlarmCode`, `LastAlarmAtUtc`

***

## 7) MQTT / UNS (Future‑Proof)

*   Keep **folder levels stable** for publish/subscribe.
*   Avoid `_` in topic segments; use `Spot001`, `Line001`.
*   Tag names remain **PascalCase** for parity across systems.

***

## 8) Mini Examples

**Full Tag Paths**

    ClevelandPlant/Avon/Assembly/Line001/Spot001/BatteryLevel
    ClevelandPlant/Avon/Assembly/Line001/Spot001/RobotStateCode
    ClevelandPlant/Avon/Assembly/Line001/Spot001/SampledAtUtc

**Python Read**

```python
def get_battery_level(device="Spot001"):
    base = f"ClevelandPlant/Avon/Assembly/Line001/{device}"
    return system.tag.readBlocking([f"{base}/BatteryLevel"])[0].value
```

***

### Optional Quick Checks (Regex)

*   **PascalCase**: `^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*$`
*   **snake\_case**: `^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$`
*   **Tag path (segments)**: `^(?:[A-Z][A-Za-z0-9]*?(?:\d{2,})?)(?:\/[A-Z][A-Za-z0-9]*?(?:\d{2,})?)+$`

***
