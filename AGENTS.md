# Agent Behavior Guidelines

## Project Context

This repository contains Ignition SCADA integration plans for Boston Dynamics Spot robots via the Orbit API. The primary document is `ignition-spot-simple-plan.md`.

---

## Critical Rules for Architecture Planning

### 0. **NEVER Assume Unknown Information - Request Real Data First**

**CRITICAL:** When working with external APIs, databases, or any system you haven't tested:

- ❌ **DON'T:** Assume API response values based on "common patterns"
- ❌ **DON'T:** Invent field values, status codes, or response formats
- ❌ **DON'T:** Present assumptions as verified facts
- ❌ **DON'T:** Write code based on unverified assumptions
- ✅ **DO:** Explicitly request real API responses from the user
- ✅ **DO:** Mark ALL assumptions with "⚠️ ASSUMPTION - NOT VERIFIED"
- ✅ **DO:** Ask user to verify foundations before proceeding with implementation
- ✅ **DO:** Provide validation workflow (like API-RESPONSE-VALIDATION-GUIDE.md)

**Why This Matters:**

- Wrong API assumptions → Missed critical events (e.g., mission failures)
- Wrong status values → Notifications don't fire
- Wrong response formats → Code crashes in production
- User discovers errors only after deployment

**Example - BAD (What Happened in v2.9):**

```python
# Claimed "Verified" but was actually AI assumption:
status_map = {
    "success": "COMP",  # ✅ Verified - Orbit uses "success"
}
# Reality: NEVER tested with real Orbit API
```

**Example - GOOD (Honest Approach):**

```python
# ⚠️ ASSUMPTION - Common API pattern, NOT verified with real Orbit API
# Before deployment: Capture actual responses using:
#   curl -H "Authorization: Bearer TOKEN" .../api/v0/runs | jq .
status_map = {
    "success": "COMP",    # ASSUMED - verify first
    "completed": "COMP",  # ASSUMED - verify first
}
```

**Required Workflow Before Implementation:**

1. **Check for existing real data:**
   - Check `orbit-api-documents-md/actual-responses.md` for verified values
   - Check `orbit-api-documents-md/orbit-api/` for Bruno collection responses
   - If none exist → **STOP and request from user**

2. **Request user to capture real API responses:**

   ```
   Before I implement this, I need to verify the actual API responses.

   Can you send the API request in Bruno?

   1. Open Bruno → orbit-api-documents-md/orbit-api/ collection
   2. Open runs.bru → Click Send
   3. View the Response tab
   4. Note the missionStatus values you see

   Then I can use the REAL field values from the response.
   ```

3. **Mark assumptions clearly:**
   - Use `⚠️ ASSUMPTION` in code comments
   - Use `🔴 UNVERIFIED` in documentation
   - Never use "✅ Verified" unless documented in actual-responses.md

4. **Get user approval before proceeding:**

   ```
   I've marked these values as ASSUMPTIONS. We have two options:

   A) You capture real API responses now (30 min) → I use verified values
   B) I proceed with assumptions → You MUST verify before production

   Which approach do you prefer?
   ```

**Red Flags to Avoid:**

- "Based on common API patterns..." without verification
- "Typically APIs return..." without checking THIS API
- Version history claiming "Fixed" or "Verified" when no testing occurred
- Status value lists without source data
- Claiming verification in code comments when it's fictional

**When Documentation is Incomplete:**

If official API docs don't specify possible values (e.g., `missionStatus` field exists but values not listed):

```
⚠️ The API documentation shows the `missionStatus` field exists (type: string)
but does NOT list the possible values.

Before I can implement status handling correctly, we need actual responses.

Please:
  1. Open Bruno → orbit-api-documents-md/orbit-api/ collection
  2. Open runs.bru → Click Send
  3. In Response tab, scroll through resources[] array
  4. Note all unique missionStatus values you see

Or extract from Bruno response:
  grep -A 9999 "^}$" orbit-api-documents-md/orbit-api/runs.bru | \
    jq -r '.resources[].missionStatus' | sort | uniq -c

This will show ALL status values currently in your system.
```

**Prevention Checklist:**

- [ ] Have I checked `orbit-api-documents-md/actual-responses.md` for verified data?
- [ ] Have I explicitly marked assumptions as unverified?
- [ ] Have I asked user to verify before implementation?
- [ ] Have I provided exact commands to capture real data?
- [ ] Have I avoided claiming "verified" without proof?

---

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
| Requirement | Option A   | Option B    |
| ----------- | ---------- | ----------- |
| Cost        | Free       | $X extra    |
| Latency     | 60 seconds | < 5 seconds |
| Complexity  | Low        | Medium      |
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

| Module                                 | Purpose                   | Free?                       |
| -------------------------------------- | ------------------------- | --------------------------- |
| Perspective                            | Modern HMI                | ✅ Included (most editions) |
| Vision                                 | Legacy HMI                | ✅ Included (some editions) |
| **Web Dev**                            | HTTP endpoints, REST APIs | ❌ **Separate purchase**    |
| Tag Historian                          | Time-series data storage  | ❌ Separate purchase        |
| Alarm Notification                     | Advanced alarming         | ✅ Included                 |
| Enterprise Administration Module (EAM) | Multi-gateway management  | ❌ Separate purchase        |

### Common Cost-Free Alternatives

| Need                | Paid Option    | Free Alternative             |
| ------------------- | -------------- | ---------------------------- |
| Receive webhooks    | Web Dev module | Gateway Timer polling        |
| Historical data     | Tag Historian  | Database + Named Queries     |
| Custom REST API     | Web Dev module | Not available (polling only) |
| Email notifications | (Built-in)     | ✅ system.net.sendEmail()    |

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

| Operation                | ❌ Don't Use                  | ✅ Use Instead                                                         |
| ------------------------ | ----------------------------- | ---------------------------------------------------------------------- |
| Row count                | `len(dataset)`                | `dataset.getRowCount()`                                                |
| Column count             | N/A                           | `dataset.getColumnCount()`                                             |
| Column names             | N/A                           | `dataset.getColumnName(index)`                                         |
| Get value                | `dataset[row][col]`           | `dataset.getValueAt(row, col)` or `dataset.getValueAt(row, "ColName")` |
| Get value (with default) | `row.get("ColName", default)` | `row["ColName"] if "ColName" in row else default`                      |
| Iterate rows             | `for row in dataset:`         | Works, but `row` is not a dict!                                        |
| Convert to dict          | `dict(row)`                   | Manual loop with `getValueAt()`                                        |

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

**Pattern 4: Access Optional Fields with Default Values**

```python
result = system.db.runNamedQuery("GetNotificationRules", params)
for rule in result:
    rule_id = rule["NotificationRuleId"]

    # ❌ WRONG - .get() method doesn't exist
    rule_name = rule.get("RuleName", "Rule #{}".format(rule_id))

    # ✅ CORRECT - use bracket notation with conditional
    rule_name = rule["RuleName"] if "RuleName" in rule else "Rule #{}".format(rule_id)
```

**Pattern 5: Check for Results**

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
5. **`.get()` doesn't exist** - PyDataset rows are Java objects, not Python dicts; they don't have `.get()`, `.keys()`, `.values()` methods

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

This mistake appeared in `ignition-spot-simple-plan.md` multiple times:

- **v2.7:** `get_site_config()` used `dict(result[0])` - failed to convert (fixed in v2.11)
- **v2.7:** `evaluate_and_send()` used `getValueAt(0, 1)` instead of `getValueAt(0, i)` - copied wrong column (fixed in v2.11)
- **v2.11:** Test verification functions used `len(ds)` instead of `ds.getRowCount()` (fixed in v2.11)
- **v2.11:** `evaluate_and_send()` used `rule.get("RuleName", ...)` - `.get()` method doesn't exist on PyDataset row objects (fixed in v2.12)

**Root Cause:** PyDataset rows are Java objects that implement a subset of Python dict-like behavior (bracket notation `[]`, `in` operator) but do NOT support Python dict methods (`.get()`, `.keys()`, `.values()`, etc.)

**Prevention:**

- Always use PyDataset methods (`getRowCount()`, `getValueAt()`, etc.) when working with Named Query results
- Use bracket notation `row["ColName"]` instead of `row.get("ColName", default)`
- For optional fields, use: `row["ColName"] if "ColName" in row else default`

---

## Document Update Protocol

When updating architecture documents:

1. **Version History:** Always add version entry with clear change summary
2. **Deprecation:** Don't delete old approaches - move to Appendix for reference
3. **Migration Path:** If changing architecture, document what changed and why
4. **Consistency:** Update ALL references (code, tests, deployment checklist)

### Version History Format

```markdown
| Version | Date       | Changes                                                                                              |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------- |
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

When working on Orbit API integration tasks, **ALWAYS search the local API documentation first**:

**Documentation Location:** `orbit-api-documents-md/`

**Priority Order:**

1. **Check `actual-responses.md` FIRST** - Contains verified real API responses
2. **Check `orbit-api/*.bru`** - Bruno collection with real request/response examples
3. **Check endpoint docs** - `runs.md`, `robots.md`, etc. for API structure
4. **Check `schemas.md`** - For data model definitions

**When to Search:**

- ✅ User asks about any Orbit API endpoint, parameter, or response
- ✅ Need to verify API capabilities or response formats
- ✅ Planning implementations or data structures
- ✅ Debugging API-related issues

**Available Documentation:**

- `actual-responses.md` - **Verified API responses (check first!)**
- `orbit-api/` - **Bruno collection** with real API requests/responses
- `README.md` - API overview and AI agent guidelines
- `authentication.md`, `runs.md`, `robots.md`, `webhooks.md`, etc.
- `schemas.md` - Data model definitions

**Benefits:**

- ✅ Accurate, up-to-date API information
- ✅ Prevents false assumptions
- ✅ Ensures correct endpoint usage

---

## Lessons Learned from This Project

### What Went Wrong

1. Proposed Web Dev module without mentioning license requirement
2. Built entire architecture around webhooks before discussing costs
3. **Assumed API response values without verification** (v2.9 false "verified" claims)
4. Had to refactor mid-project (v2.7 → v2.8)

### What Should Have Happened

1. **Check actual-responses.md first** - Would have discovered no verified values
2. **Request real API data** - 30 minutes to capture responses
3. **Present cost options upfront:**
   ```
   Data Collection Options:
   A) Polling (free, 60s delay)
   B) Webhooks (requires Web Dev license purchase, real-time)
   Which do you prefer?
   ```
4. Build architecture based on verified data and chosen option

### Key Takeaways

- ✅ **Verify before implementing** - Save hours of rework
- ✅ **Disclose costs upfront** - Let user decide
- ✅ **Mark assumptions clearly** - Never claim "verified" without proof
- ✅ **30 minutes of verification** > days of fixing wrong assumptions

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

_Created: 2026-02-03_  
_Last Updated: 2026-02-04_  
_Context: After v2.7 → v2.8 architecture refactor (webhook → polling) + PyDataset conversion fixes (v2.11) + API verification lessons (v2.12) + Documentation consolidation (v2.13)_  
_Purpose: Prevent similar issues in future agent interactions_

**v2.13 Updates (2026-02-04):**

- ✅ Consolidated validation docs → single `actual-responses.md` file
- ✅ Set up Bruno collection in `orbit-api-documents-md/orbit-api/`
- ✅ Updated all file paths to reflect Bruno collection structure
- ✅ Enhanced `orbit-api-documents-md/README.md` with AI agent guidelines
- ✅ Simplified this document - removed redundant sections
