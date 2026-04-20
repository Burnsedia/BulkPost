# BulkPost MVP BDD Scenarios

This folder contains behavior-driven scenarios for the CRM + CMS MVP.

Scope:
- Content lifecycle (draft to published)
- Engagement lifecycle (discovery to posted reply)
- Policy and safety controls
- API authentication and user scoping

How to use:
- Use each scenario during implementation as a behavior contract.
- Convert scenarios to automated tests (pytest + Django REST Framework test client).
- Keep examples small and deterministic.

Files:
- `01-content-lifecycle.md`
- `02-engagement-lifecycle.md`
- `03-policy-and-safety.md`
- `04-api-auth-and-scoping.md`
