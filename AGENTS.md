# Agent Behavior Guidelines

## Project Context
This repository contains Ignition SCADA integration plans for Boston Dynamics Spot robots via the Orbit API. The primary document is `ignition-spot-simple-plan.md`.

---



## Critical Rules for Architecture Planning

### 1. **ALWAYS Disclose License Costs Upfront**

When proposing any solution involving Ignition modules or third-party components:

- ✅ **DO:** Clearly state if additional licenses are required
- ✅ **DO:** Provide cost-free alternatives first
- ✅ **DO:** Let the user make informed decisions at design stage
- ❌ **DON'T:** Assume the user has or will purchase additional modules
- ❌ **DON'T:** Build plans around optional modules without explicit user approval

**Example - Bad:**
```
We'll use the Web Dev module to receive webhooks...
(User discovers later it requires separate purchase)
```

**Example - Good:**
```
Option A (No extra cost): Polling every 60s using Gateway Timer
Option B (Requires Web Dev license): Real-time webhooks
Which approach do you prefer?
```

### 2. **Present Alternatives at Decision Points**

For ANY architectural decision with trade-offs, present options with pros/cons:

```markdown
| Requirement | Option A | Option B |
|-------------|----------|----------|
| Cost | Free | $X extra |
| Latency | 60 seconds | < 5 seconds |
| Complexity | Low | Medium |
```

### 3. **Avoid Mid-Project Architecture Changes**

Changing architecture after code is written is painful:
- Multiple modules need updates
- Testing needs revalidation
- Documentation becomes inconsistent
- User frustration increases

**Prevention:** Spend extra time on initial design review before coding.

---

## Ignition-Specific Guidelines

### Modules Requiring Additional Licenses

Always check and inform the user about these modules:

| Module | Purpose | Free? |
|--------|---------|-------|
| Perspective | Modern HMI | ✅ Included (most editions) |
| Vision | Legacy HMI | ✅ Included (some editions) |
| **Web Dev** | HTTP endpoints, REST APIs | ❌ **Separate purchase** |
| Tag Historian | Time-series data storage | ❌ Separate purchase |
| Alarm Notification | Advanced alarming | ✅ Included |
| Enterprise Administration Module (EAM) | Multi-gateway management | ❌ Separate purchase |

### Common Cost-Free Alternatives

| Need | Paid Option | Free Alternative |
|------|-------------|------------------|
| Receive webhooks | Web Dev module | Gateway Timer polling |
| Historical data | Tag Historian | Database + Named Queries |
| Custom REST API | Web Dev module | Not available (polling only) |
| Email notifications | (Built-in) | ✅ system.net.sendEmail() |

### PyDataset Handling with Named Queries

**CRITICAL:** Ignition Named Queries return **PyDataset** objects, NOT standard Python lists/dicts. You cannot use normal Python operations on them.

#### Common Mistakes

❌ **WRONG:**
```python
result = system.db.runNamedQuery("GetSiteConfig", {"site_id": 1})
if result and len(result) > 0:
    return dict(result[0])  # ERROR: dict() doesn't work on PyDataset rows
```

✅ **CORRECT:**
```python
result = system.db.runNamedQuery("GetSiteConfig", {"site_id": 1})
if result and result.getRowCount() > 0:
    # Convert PyDataset row to dictionary manually
    config = {}
    for i in range(result.getColumnCount()):
        col_name = result.getColumnName(i)
        config[col_name] = result.getValueAt(0, i)
    return config
```

#### PyDataset API Reference

| Operation | ❌ Don't Use | ✅ Use Instead |
|-----------|--------------|----------------|
| Row count | `len(dataset)` | `dataset.getRowCount()` |
| Column count | N/A | `dataset.getColumnCount()` |
| Column names | N/A | `dataset.getColumnName(index)` |
| Get value | `dataset[row][col]` | `dataset.getValueAt(row, col)` or `dataset.getValueAt(row, "ColName")` |
| Iterate rows | `for row in dataset:` | Works, but `row` is not a dict! |
| Convert to dict | `dict(row)` | Manual loop with `getValueAt()` |

#### Correct Patterns for Common Operations

**Pattern 1: Single Row to Dictionary**
```python
result = system.db.runNamedQuery("GetRobotByHostname", {"hostname": "spot-01"})
if result and result.getRowCount() > 0:
    robot = {}
    for i in range(result.getColumnCount()):
        robot[result.getColumnName(i)] = result.getValueAt(0, i)
    return robot
return None
```

**Pattern 2: Multiple Rows to List of Dictionaries**
```python
result = system.db.runNamedQuery("GetAllRobots", {"site_id": 1})
robots = []
for row_idx in range(result.getRowCount()):
    robot = {}
    for col_idx in range(result.getColumnCount()):
        col_name = result.getColumnName(col_idx)
        robot[col_name] = result.getValueAt(row_idx, col_idx)
    robots.append(robot)
return robots
```

**Pattern 3: Iterate with PyDataset Row Objects**
```python
result = system.db.runNamedQuery("GetNotificationRules", params)
for rule in result:  # rule is a PyDataset row object
    # Access by column name (recommended)
    rule_id = rule["NotificationRuleId"]
    pattern = rule["MissionNamePattern"]
    
    # Note: rule is NOT a dict, but supports [] access
```

**Pattern 4: Check for Results**
```python
result = system.db.runNamedQuery("GetRecipients", {"rule_id": 5})

# ❌ WRONG
if not result or len(result) == 0:
    return

# ✅ CORRECT
if not result or result.getRowCount() == 0:
    return
```

#### Why This Matters

1. **`dict(row)` fails silently** - doesn't convert PyDataset rows properly
2. **`len()` may not work** - PyDataset doesn't always support Python's `len()`
3. **`getValueAt(0, 1)` bug** - using wrong index in comprehensions copies same column repeatedly
4. **Loop variable confusion** - `for row in dataset:` gives PyDataset row, not dict

#### Testing PyDataset Code

Always test Named Query code with real queries. Dictionary conversion bugs won't show up until runtime.

```python
# Test in Script Console
result = system.db.runNamedQuery("GetSiteConfig", {"site_id": 1})
print "Row count:", result.getRowCount()
print "Column count:", result.getColumnCount()
print "Columns:", [result.getColumnName(i) for i in range(result.getColumnCount())]
print "First row:", result.getValueAt(0, 0), result.getValueAt(0, 1)
```

#### Historical Context

This mistake appeared in `ignition-spot-simple-plan.md` v2.7 and was fixed in v2.11:
- `get_site_config()`: Used `dict(result[0])` - failed to convert
- `evaluate_and_send()`: Used `getValueAt(0, 1)` instead of `getValueAt(0, i)` - copied wrong column
- Test verification functions: Used `len(ds)` instead of `ds.getRowCount()`

**Prevention:** Always use PyDataset methods (`getRowCount()`, `getValueAt()`, etc.) when working with Named Query results.

---

## Document Update Protocol

When updating architecture documents:

1. **Version History:** Always add version entry with clear change summary
2. **Deprecation:** Don't delete old approaches - move to Appendix for reference
3. **Migration Path:** If changing architecture, document what changed and why
4. **Consistency:** Update ALL references (code, tests, deployment checklist)

### Version History Format

```markdown
| Version | Date | Changes |
|---------|------|---------|
| **X.X** | YYYY-MM-DD | **Brief Title**<br>• Bullet point changes<br>• Why the change was made<br>• Impact on implementation |
```

---

## Communication Style with User

### When User is Frustrated

- ✅ **Acknowledge mistake directly:** "You're absolutely right, I should have..."
- ✅ **Apologize sincerely:** Don't minimize or deflect
- ✅ **Offer concrete solutions:** "Here's what we can do now..."
- ❌ **Don't over-explain:** Keep it brief and actionable

### When Presenting Technical Choices

- ✅ Use comparison tables for clarity
- ✅ Highlight cost implications prominently
- ✅ Recommend an option with reasoning
- ✅ Support user's final decision even if different from recommendation

---

## Project-Specific Context

### Technology Stack
- **Platform:** Ignition 8.1+
- **Language:** Python 2.7 (Jython) in Ignition
- **Database:** Microsoft SQL Server
- **External API:** Boston Dynamics Orbit REST API

### Key Design Decisions (v2.8)
- **Data Collection:** Polling-based (every 60s) - no Web Dev module
- **Module Name:** `run_event_handlers` (handles DB/tags/notifications)
- **Logger Prefix:** `orbit.*` for all log messages
- **Architecture:** Gateway Timer → Polling → Change Detection → Event Handler

### If User Wants Real-Time (< 5 sec latency)
- See Appendix A in `ignition-spot-simple-plan.md`
- Requires Web Dev module license
- Only recommend if user explicitly needs sub-5-second updates

---

## Orbit API Documentation Reference

### Automatic Documentation Search

When working on Orbit API integration tasks, **ALWAYS search the local API documentation first** before making assumptions or asking the user:

**Documentation Location:** `orbit-api-documents-md/api/`

**When to Search:**
- ✅ User asks about any Orbit API endpoint, parameter, or response
- ✅ Implementing new API integration features
- ✅ Debugging API-related issues
- ✅ Uncertain about API capabilities or limitations
- ✅ Need to verify authentication requirements
- ✅ Planning webhook implementations or data structures

**How to Search:**

1. **Use Grep** for specific terms:
   ```
   Pattern: "endpoint_name" or "field_name" or "authentication"
   Path: orbit-api-documents-md/api/
   ```

2. **Use Glob** to find relevant files:
   ```
   Pattern: "*.md" in orbit-api-documents-md/api/
   ```

3. **Read the relevant documentation** before responding to user

**Available Documentation Files:**
- `authentication.md` - API authentication methods
- `webhooks.md` - Webhook configuration and events
- `runs.md` - Run data and operations
- `run-events.md` - Run event types and structure
- `run-captures.md` - Media capture data
- `missions.md` - Mission management
- `robots.md` - Robot information and status
- `anomalies.md` - Anomaly detection data
- `backup-tasks.md` - Backup task management
- And more... (see `orbit-api-documents-md/api/` directory)

**Example Workflow:**

```
User: "How do I get the run events from Orbit API?"

Agent Actions:
1. Grep for "run-events" or "events" in orbit-api-documents-md/api/
2. Read orbit-api-documents-md/api/run-events.md
3. Provide accurate answer based on documentation
4. Reference the documentation file in response
```

**Benefits:**
- ✅ Provides accurate, up-to-date API information
- ✅ Reduces back-and-forth with user
- ✅ Ensures correct endpoint usage
- ✅ Prevents API integration errors
- ❌ **DON'T:** Make assumptions about API structure
- ❌ **DON'T:** Ask user for API details that exist in documentation

---

## Lessons Learned from This Project

### What Went Wrong
1. Proposed Web Dev module without mentioning license requirement
2. Built entire architecture around webhooks before discussing costs
3. Had to refactor mid-project (v2.7 → v2.8)
4. Caused user frustration and extra work

### What Should Have Happened
1. Initial proposal should have been:
   ```
   Data Collection Options:
   A) Polling (free, 60s delay) 
   B) Webhooks (requires Web Dev license purchase, real-time)
   Which do you prefer?
   ```
2. User makes informed choice upfront
3. Build architecture based on chosen option
4. No mid-project refactoring needed

---

## Summary Checklist

Before proposing any Ignition architecture:

- [ ] Listed all required modules
- [ ] Identified which modules require additional licenses
- [ ] Presented cost-free alternatives
- [ ] Provided comparison table with trade-offs
- [ ] Got user approval before detailed design
- [ ] Double-checked no hidden costs in dependencies

---

*Created: 2026-02-03*  
*Last Updated: 2026-02-03*  
*Context: After v2.7 → v2.8 architecture refactor (webhook → polling) + PyDataset conversion fixes (v2.11)*  
*Purpose: Prevent similar issues in future agent interactions*
