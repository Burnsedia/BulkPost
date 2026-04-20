# BulkPost CRM + CMS MVP Specification

## 1) Purpose

Build a focused MVP that combines:
- CMS for social content operations (draft -> review -> schedule -> publish -> measure)
- CRM for social lead operations (discover -> qualify -> engage -> track)

Primary channel for MVP: **X/Twitter only**.

---

## 2) Product Goals

- Automate daily social posting with policy controls.
- Automate engagement replies to relevant targets.
- Capture and track leads generated from social interactions.
- Measure performance and improve prompts/strategy over time.
- Keep humans in control with optional review gates and kill switch.

### Non-Goals (MVP)
- Multi-platform publishing (LinkedIn/Instagram/etc.)
- Advanced optimization (bandits, autonomous strategy loops)
- Full sales automation/DM funnel
- Team roles/permissions beyond single owner/admin

---

## 3) MVP Scope

### Included
- Authenticated single-user workspace
- Content pipeline:
  - Draft generation
  - Optional review/approval
  - Scheduling queue
  - Publish and error handling
- CRM pipeline:
  - Lead capture from engagement discovery
  - Lead qualification and scoring
  - Contact + activity timeline
- Agent loop:
  - Autopilot, Content, Engagement, Safety
- Basic analytics:
  - Post/reply counts
  - Engagement metrics snapshots
  - Lead funnel counts
- Policy controls:
  - Daily limits, min intervals, kill switch

### Excluded
- Multi-tenant organization support
- Complex role-based access control
- Multi-platform adapters
- AI-driven sales DM automation

---

## 4) Architecture

### High-level flow

Autopilot Agent
-> decides action (post | engage | skip)
-> subagent output (content/reply + safety result)
-> Execution services perform API calls + persistence
-> Django stores state + metrics
-> Dashboard reads analytics

### Design rules
1. Agents decide, services execute.
2. Agents do not write to DB directly.
3. Tools are stateless.
4. Django models are system-of-record.
5. Every external action is logged with run_id and status.
6. Fail-safe defaults: skip on uncertainty/high risk.

---

## 5) Domain Model

### 5.1 Existing models retained
- SystemPrompt
- Prompt
- GrowthPolicy
- DailyUsage
- Post
- ReplyTarget
- Reply
- PostMetricSnapshot
- AgentRunLog

### 5.2 New MVP models to add

#### Campaign
- id
- user (FK)
- name
- goal (awareness | engagement | lead_gen)
- audience
- is_active (bool)
- created_at, updated_at

#### ContentDraft
- id
- user (FK)
- campaign (FK nullable)
- source_prompt (FK Prompt nullable)
- title (optional)
- body
- status (idea | draft | in_review | approved | scheduled | published | rejected)
- risk_score (float)
- approved_by_user (bool)
- scheduled_for (datetime nullable)
- linked_post (FK Post nullable)
- created_at, updated_at

#### Lead
- id
- user (FK)
- source_channel (default: x)
- source_handle
- source_tweet_id (nullable)
- status (new | qualified | engaged | converted | disqualified)
- score (0-100)
- owner (FK user)
- notes (text)
- created_at, updated_at

#### Contact
- id
- user (FK)
- lead (OneToOne or FK)
- handle
- display_name
- bio
- follower_count (int nullable)
- website (nullable)
- created_at, updated_at

#### Activity
- id
- user (FK)
- lead (FK)
- type (reply_sent | dm_sent | note | status_change)
- content (text)
- source_post_id (FK Post nullable)
- source_reply_id (FK Reply nullable)
- happened_at (datetime)
- created_at

---

## 6) Agent Definitions (MVP)

### Autopilot Agent
Role:
- Orchestrator; decides one action per run.

Input:
- GrowthPolicy
- DailyUsage
- Pending queue state
- Recent performance
- Pending reply targets

Output:
- action: post | engage | skip
- reason: str

### Content Agent
Role:
- Generate content drafts aligned to campaign/prompt variant.

Input:
- Prompt/SystemPrompt variant
- Campaign context
- Recent content constraints

Output:
- text/body
- category/tag
- optional hooks

### Engagement Agent
Role:
- Find targets, qualify lead opportunities, draft replies.

Sub-steps:
1. Discovery (search queries + candidate tweets)
2. Qualification (relevance/lead fit)
3. Reply writing

Output:
- action: reply | ignore
- target_tweet_id
- draft_reply
- lead_candidate fields

### Safety Agent
Role:
- Guardrails and compliance checks.

Checks:
- Spam risk
- Policy violations
- Unsafe claims/phrasing
- Frequency/duplicate constraints

Output:
- risk_score
- should_post (bool)
- reason

---

## 7) Services (non-LLM)

### Execution Service
- Publishes posts/replies to X API.
- Applies retries/backoff/rate controls.
- Updates queue status and errors.

### Scheduler Service
- Triggers autopilot and execution jobs on interval.
- Honors min intervals and daily caps.
- Stops all actions if kill_switch=true.

### Metrics Collector Service
- Pulls post-level metrics snapshots.
- Stores engagement trend points.
- Feeds dashboard and optimization phase later.

---

## 8) API Contract (MVP)

Base: `/api/`

### Existing resources
- system-prompts
- prompts
- posts
- growth-policies
- reply-targets
- replies
- daily-usage

### New resources
- campaigns
- content-drafts
- leads
- contacts
- activities

### Action endpoints
- `POST /api/agents/autopilot/run-once`
- `POST /api/agents/content/generate-draft`
- `POST /api/agents/engagement/discover`
- `POST /api/agents/safety/check`
- `POST /api/queue/posts/{id}/approve`
- `POST /api/queue/replies/{id}/approve`
- `POST /api/queue/posts/{id}/cancel`
- `POST /api/queue/replies/{id}/cancel`

### Analytics endpoint
- `GET /api/dashboard/summary`
  - posts_today
  - replies_today
  - queued_count
  - lead_counts_by_status
  - top_posts_recent

### Security rules
- All endpoints require auth.
- Querysets always filtered by `request.user`.
- `perform_create` always injects `user=request.user`.

---

## 9) Frontend MVP Screens

- Dashboard
  - KPI cards, recent agent runs, recent failures
- Content Board
  - columns: draft/in_review/approved/scheduled/published
- Queue View
  - pending posts/replies + approve/reject
- CRM View
  - leads table + contact detail + activity timeline
- Settings
  - GrowthPolicy editor, kill switch, limits, intervals

---

## 10) Reliability, Safety, and Observability

- Provider HTTP retries with exponential backoff + Retry-After support.
- Idempotent publish jobs (prevent duplicates).
- Kill switch hard-stop in scheduler + executor.
- Structured run logs for each agent action.
- Capture model/tool errors and retry count.
- Instrumentation for:
  - token usage
  - latency
  - tool calls
  - API failures

---

## 11) Testing Strategy (MVP)

### Backend tests
- Auth required on all endpoints.
- User scoping for list/retrieve/update/delete.
- Queue transitions (approve/cancel/post success/failure).
- GrowthPolicy limits enforcement.
- Safety block behavior.

### Integration tests
- Autopilot run-once -> expected queue side effects.
- Execution service publishes and updates status.
- Metrics snapshot job writes snapshots.

### Smoke tests
- End-to-end happy path:
  - generate draft -> approve -> schedule -> publish -> metrics visible

---

## 12) Acceptance Criteria (Definition of Done)

1. System can run daily without manual prompting.
2. At least one post and one reply can be published from queue.
3. Leads are created and visible in CRM workflow.
4. Dashboard shows post/reply/lead KPIs from real stored data.
5. Safety agent can block risky content and record reason.
6. Policy limits and kill switch are enforced.
7. Critical tests pass in CI.

---

## 13) Delivery Phases

### Phase A (Foundation)
- Fix startup/model issues
- auth + scoped APIs
- baseline tests

### Phase B (Core CRM+CMS)
- add new models + CRUD endpoints
- content board + CRM screens
- queue actions

### Phase C (Agentic MVP)
- implement 4 agents + scheduler + execution
- metrics collector + dashboard summary
- reliability hardening

### Phase D (Post-MVP)
- optimization/trend/strategy agents
- multi-platform adapters
- advanced analytics and experiments
