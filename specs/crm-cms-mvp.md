# BulkPost CRM + CMS MVP Specification

## 1) Purpose

Build a focused MVP that combines:
- CMS for social content operations (draft -> schedule -> publish -> measure)
- CRM for social lead operations (discover -> qualify -> engage -> offer -> track)

Primary channel for MVP: **X/Twitter only**.

---

## 2) Product Goals

- Automate daily social posting with policy controls.
- Automate engagement replies to relevant targets.
- Capture and track leads generated from social interactions.
- Measure performance and improve prompts/strategy over time.
- Operate in setup-and-go mode with autonomous posting, replies, and qualified DM offers.

### Non-Goals (MVP)
- Multi-platform publishing (LinkedIn/Instagram/etc.)
- Advanced optimization (bandits, autonomous strategy loops)
- Team roles/permissions beyond single owner/admin

---

## 3) MVP Scope

### Included
- Authenticated single-user workspace
- Content pipeline:
  - Draft generation
  - Scheduling queue
  - Publish and error handling
- CRM pipeline:
  - Lead capture from reply/mention/follow interactions
  - Lead qualification and scoring
  - Contact + activity timeline + offer funnel tracking
- Agent loop:
  - Autopilot, Content, Engagement, Safety, Sales
- Basic analytics:
  - Post/reply counts
  - Engagement metrics snapshots
  - Lead and offer funnel counts
- Policy controls:
  - Daily limits, min intervals, kill switch, DM cooldown/suppression

### Excluded
- Multi-tenant organization support
- Complex role-based access control
- Multi-platform adapters

---

## 4) Architecture

### High-level flow

Autopilot Agent
-> decides action (post | engage | dm_offer | skip)
-> subagent output (content/reply/offer + safety result)
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
- status (idea | draft | scheduled | published | rejected)
- risk_score (float)
- scheduled_for (datetime nullable)
- linked_post (FK Post nullable)
- created_at, updated_at

#### Lead
- id
- user (FK)
- source_channel (default: x)
- source_handle
- source_tweet_id (nullable, origin inbound post/tweet)
- status (new | qualified | engaged | converted | disqualified)
- score (0-100)
- owner (FK user)
- notes (text)
- last_dm_at (datetime nullable)
- cooldown_until (datetime nullable)
- do_not_contact (bool default false)
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
- type (reply_sent | dm_sent | note | status_change | offer_sent | offer_outcome)
- content (text)
- source_post_id (FK Post nullable)
- source_reply_id (FK Reply nullable)
- happened_at (datetime)
- created_at

#### Offer
- id
- user (FK)
- lead (FK)
- channel (x_dm)
- template_name
- message_text
- lead_magnet_link
- app_link
- status (queued | sent | replied | interested | won | lost | suppressed)
- sent_at (datetime nullable)
- created_at, updated_at

#### OfferEvent
- id
- user (FK)
- offer (FK)
- event_type (sent | replied | clicked | interested | won | lost | suppressed)
- detail (text nullable)
- happened_at (datetime)

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
- action: post | engage | dm_offer | skip
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

Qualification policy:
- Only `reply`, `mention`, and `follow` interactions count for DM qualification.
- Likes are tracked for analytics but excluded from DM qualification.

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
- DM suppression and cooldown constraints

Output:
- risk_score
- should_post (bool)
- reason

### Sales Agent
Role:
- DM qualified leads with a lead magnet and app link, then track offer outcomes.

Qualification policy:
- DM only when lead score threshold is met (recommended default: `>= 70`).
- Enforce cooldown and suppression before queueing any DM.

Output:
- action: send_offer_dm | follow_up | skip
- lead_id
- message_text
- offer metadata

---

## 7) Services (non-LLM)

### Execution Service
- Publishes posts/replies and sends DMs via X API.
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
- offers
- offer-events

### Action endpoints
- `POST /api/agents/autopilot/run-once`
- `POST /api/agents/content/generate-draft`
- `POST /api/agents/engagement/discover`
- `POST /api/agents/safety/check`
- `POST /api/agents/sales/process-qualified`
- `POST /api/offers/send-qualified`
- `POST /api/offers/{id}/follow-up`
- `POST /api/leads/{id}/suppress`
- `POST /api/queue/posts/{id}/cancel`
- `POST /api/queue/replies/{id}/cancel`

### Analytics endpoint
- `GET /api/dashboard/summary`
  - posts_today
  - replies_today
  - dms_sent_today
  - queued_count
  - lead_counts_by_status
  - offer_counts_by_status
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
  - columns: draft/scheduled/published/rejected
- Queue View
  - pending posts/replies/offers + cancel/retry
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
- Queue transitions (cancel/post success/failure + DM send/follow-up/suppression).
- GrowthPolicy limits enforcement.
- Safety block behavior.

### Integration tests
- Autopilot run-once -> expected queue side effects.
- Execution service publishes, sends DMs, and updates status.
- Metrics snapshot job writes snapshots.

### Smoke tests
- End-to-end happy path:
  - generate draft -> schedule -> publish -> lead qualifies -> DM offer sent -> metrics visible

---

## 12) Acceptance Criteria (Definition of Done)

1. System can run daily without manual prompting.
2. At least one post and one reply can be published from queue.
3. Leads are created and visible in CRM workflow.
4. Dashboard shows post/reply/lead/offer KPIs from real stored data.
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
- implement 5 agents + scheduler + execution
- metrics collector + dashboard summary
- reliability hardening

### Phase D (Post-MVP)
- optimization/trend/strategy agents
- multi-platform adapters
- advanced analytics and experiments
