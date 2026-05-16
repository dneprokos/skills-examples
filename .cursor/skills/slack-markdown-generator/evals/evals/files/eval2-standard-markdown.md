# Project Phoenix — Release Notes v3.1

## Overview

This release brings major improvements to the reporting dashboard, a new onboarding flow, and a round of bug fixes.

![Release banner](https://cdn.example.com/images/phoenix-banner.png)

## What's New

### Reporting Dashboard

- Added real-time filtering by date range, team, and status
- Introduced a new **summary widget** showing KPIs at a glance
- Export to CSV and PDF now available

### Onboarding Flow

1. Welcome screen redesigned with guided tooltips
2. Role-selection step added before workspace setup
3. Integration setup moved to step 3 (previously step 5)

## Bug Fixes

| Issue | Severity | Fixed in |
|-------|----------|----------|
| Login loop on SSO timeout | High | v3.1.0 |
| CSV export missing headers | Medium | v3.1.1 |
| Dashboard blank on Safari 16 | Medium | v3.1.1 |

## Code Example

```javascript
// New filter API
const report = await getReport({
  startDate: '2026-01-01',
  endDate: '2026-03-31',
  team: 'engineering'
});
```

## Upgrade Notes

> **Important:** Before upgrading, back up your configuration files. The onboarding flow changes require a database migration — run `npm run migrate` after deploying.

---

For full changelog see [CHANGELOG.md](https://github.com/example/phoenix/blob/main/CHANGELOG.md).
