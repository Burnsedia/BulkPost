# BulkPost Agent System Specification (SDD)

## Overview

BulkPost is an autonomous social media growth system.

The system operates as an AI-driven loop:

data → decisions → actions → feedback → optimization

The Django layer serves as the **CRM + CMS + system memory**, while agents handle **decision-making and execution planning**.

---

## Goals

* Automate daily content posting
* Automate engagement (replies)
* Identify and qualify leads
* Optimize tone and strategy over time
* Maintain safety and platform compliance

---

## System Architecture

### High-Level Flow

```
Autopilot Agent
    ↓
decides actions
    ↓
subagents generate outputs
    ↓
services execute actions
    ↓
Django stores results
    ↓
metrics collected
    ↓
optimization loop updates system
```

---

## Core Components

### 1. Django Layer (State)

Responsibilities:

* Store posts, replies, and scheduling
* Store CRM data (targets, interactions)
* Store prompt variants and system prompts
* Store performance metrics
* Store growth policy and usage limits

This layer is **stateless in logic**, stateful in data.

---

### 2. Agents (Decision Layer)

Agents determine:

* what to post
* who to engage with
* what to reply
* what is safe
* what works

Agents do NOT:

* write to the database
* call external APIs directly (execution is handled by services)

---

### 3. Tools (Execution Interfaces)

Tools provide:

* Twitter search
* Tweet posting
* Reply posting
* Data retrieval

Tools are:

* stateless
* side-effect free (except API calls)
* reusable

---

### 4. Services (Execution Layer)

Services:

* call tools
* persist results to Django
* enforce scheduling and rate limits

---

## Agent Definitions

---

### Autopilot Agent

#### Role

Primary orchestrator of the system.

#### Responsibilities

* Decide whether to:

  * create posts
  * search and reply
  * skip actions
* Respect growth policy and usage limits

#### Inputs

* recent posts
* daily usage
* growth policy
* pending reply targets

#### Outputs

```
AutopilotAction:
    action: "post" | "engage" | "skip"
    reasoning: str
```

#### Subagents

* Content Agent
* Engagement Agent
* Safety Agent

---

### Content Agent

#### Role

Generate social media posts.

#### Responsibilities

* Generate posts based on prompts
* Apply tone and style
* Use knowledge context if available

#### Inputs

* prompt (topic)
* prompt variant (tone)
* optional knowledge context

#### Outputs

```
PostOutput:
    text: str
    category: str
```

#### Subagents (optional for MVP)

* Hook Generator
* Rewriter

#### Tools

* retrieve_knowledge(query)
* get_top_posts(user)
* get_prompt_variants(user)

---

### Engagement Agent

#### Role

Handle discovery and replies.

#### Responsibilities

* Find relevant tweets
* Identify engagement opportunities
* Generate replies

#### Subagents

1. Discovery Subagent
2. Qualification Subagent
3. Reply Writer Subagent

---

#### Discovery Subagent

Purpose:

* Generate search queries
* Call Twitter search

Tools:

* search_twitter(query)

---

#### Qualification Subagent

Purpose:

* Determine if a tweet is worth replying to
* Identify potential leads

Tools:

* get_user_profile(handle)
* get_past_interactions(handle)

---

#### Reply Writer Subagent

Purpose:

* Generate reply text

Tools:

* retrieve_knowledge(query)

---

#### Output

```
EngagementAction:
    action: "reply" | "ignore"
    target_tweet_id: str
    text: str | None
```

---

### Safety Agent

#### Role

Evaluate risk of content.

#### Responsibilities

* Prevent spammy or risky content
* Enforce platform-safe behavior

#### Inputs

* content text
* recent posts (optional)

#### Output

```
SafetyResult:
    risk_score: float
    should_post: bool
    reason: str
```

---

### Optimization Agent (Phase 2)

#### Role

Improve system performance.

#### Responsibilities

* Analyze post performance
* Identify winning prompt variants
* Suggest improvements

#### Subagents

* Performance Analyzer
* Prompt Evolver

#### Tools

* get_post_metrics(user)
* get_prompt_variants(user)

#### Output

```
OptimizationResult:
    best_variants: list[int]
    suggestions: list[str]
```

---

### Trend Agent (Phase 2)

#### Role

Identify trends in data and external sources.

#### Subagents

* Internal Trend Analyzer
* External Trend Scanner

#### Tools

* get_top_posts(user)
* get_metrics(user)
* search_twitter(query)
* fetch_rss()
* fetch_hackernews()

---

### Strategy Agent (Phase 2)

#### Role

Convert trends into actionable plans.

#### Output

```
StrategyPlan:
    topics: list[str]
    angles: list[str]
    hooks: list[str]
```

---

### Sales Agent (Phase 3)

#### Role

Convert leads into customers.

#### Subagents

* Lead Scorer
* DM Writer
* Follow-up Agent

#### Tools

* get_interactions(user)
* get_contact_history(handle)
* send_dm(handle, text)

---

## Data Models (Core)

### CMS

* Post
* Reply

### CRM

* ReplyTarget
* Interaction

### Prompt System

* Prompt
* PromptVariant
* SystemPrompt

### Metrics

* PostMetricSnapshot

### Policy

* GrowthPolicy
* DailyUsage

---

## Autopilot Flow

```
1. Autopilot Agent runs
2. Decides action

IF post:
    → Content Agent generates post
    → Safety Agent validates
    → Service saves + schedules

IF engage:
    → Engagement Agent finds targets
    → Generates replies
    → Safety Agent validates
    → Service saves + schedules

3. Scheduler executes posts/replies
4. Metrics collected
5. Optimization updates system
```

---

## MVP Scope

### Included

* Autopilot Agent
* Content Agent
* Engagement Agent
* Safety Agent
* Twitter tools (search, post, reply)
* Scheduler (cron-based)
* PromptVariant A/B system
* Metrics tracking

---

### Excluded (Later Phases)

* Trend Agent
* Strategy Agent
* Sales Agent
* Embeddings / vector search
* Multi-agent orchestration
* Advanced optimization (bandits)

---

## Design Rules

1. Agents decide, services execute
2. Tools are stateless
3. Agents return structured data
4. Django is the single source of truth
5. No direct DB writes inside agents
6. No uncontrolled loops or recursive agent calls

---

## Success Criteria

* System posts daily without manual input
* System replies to relevant tweets
* Prompt variants show measurable performance differences
* Engagement increases over time
* No platform violations or bans

---

## Future Extensions

* Multi-armed bandit optimization
* Agent memory refinement
* Semantic search (pgvector)
* Cross-platform posting (LinkedIn, Instagram)
* Fully automated DM sales funnel

---

End of Specification

