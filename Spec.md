# Software Design Document (SDD)

# BulkPost AI Marketing Copilot

**Version:** 0.1 MVP
**Architecture:** Django + PydanticAI + FastMCP
**Status:** Design Specification

---

# 1. Introduction

## 1.1 Purpose

BulkPost is an AI-powered marketing copilot that transforms a user's knowledge, expertise, and business information into social media content and customer conversations.

The system enables users to:

* Build a personal/business knowledge base.
* Generate authentic social content.
* Publish content automatically.
* Analyze engagement.
* Assist with customer conversations.
* Identify qualified leads.

BulkPost is designed as an AI-native platform that can be controlled by humans and external AI agents.

---

# 2. System Goals

## Primary Goals

* Create a persistent AI knowledge base for users.
* Generate content based on user-specific knowledge.
* Maintain user's writing style and brand voice.
* Automate social media workflows.
* Convert engagement into business opportunities.

## Secondary Goals

* Support external AI agents through MCP.
* Enable custom agent workflows.
* Provide reusable AI marketing infrastructure.

---

# 3. Architecture Overview

## High-Level Architecture

```
                         AI Clients

      OpenCode   Claude Code   Gemini CLI   Hermes   OpenClaw
              \       |          |          |        /
                       MCP Protocol
                            |
                            |
                    FastMCP Server
                            |
                            |
                  PydanticAI Agent Layer
                            |
                            |
                    Django Application
                            |
        ------------------------------------------------
        |                    |                         |
    PostgreSQL          Vector Database          Redis/Celery
        |
        |
  User Data / Knowledge / Content / Leads
```

---

# 4. Technology Stack

## Backend

* Python
* Django
* Django REST Framework

## Database

* PostgreSQL
* pgvector for embeddings

## AI Framework

* PydanticAI

Responsibilities:

* Agent creation
* Tool calling
* Structured responses
* Agent workflows

## MCP

FastMCP

Responsibilities:

* Expose BulkPost capabilities
* Allow external AI agents to interact with BulkPost

## Background Processing

* Celery
* Redis

Used for:

* Content generation
* Scheduled posts
* Reply processing
* Agent tasks

---

# 5. Django Application Structure

```
bulkpost/

├── accounts/
│   └── users, teams, billing

├── knowledge/
│   └── business knowledge and embeddings

├── content/
│   └── generated posts and campaigns

├── social/
│   └── platform integrations

├── conversations/
│   └── replies and leads

├── agents/
│   └── PydanticAI agents

├── mcp/
│   └── FastMCP server

└── analytics/
    └── engagement metrics
```

---

# 6. Core Data Models

## User

Represents a BulkPost user.

Fields:

```
id
email
username
created_at
```

---

## Workspace

Represents a business or creator account.

Fields:

```
id
owner
name
description
brand_voice
created_at
```

---

## Knowledge Base

Stores user information.

Sources:

* Documents
* URLs
* Notes
* Voice transcripts
* Previous posts

Model:

```
KnowledgeItem

id
workspace
source_type
content
embedding
metadata
created_at
```

---

## Generated Content

Stores AI-generated content.

Model:

```
Post

id
workspace
platform
content
status
source
scheduled_time
published_time
```

Status:

```
draft
approved
scheduled
published
```

---

## Conversation

Stores social interactions.

Model:

```
Conversation

id
workspace
contact
message
classification
ai_response
status
created_at
```

Classification:

```
lead
customer
question
spam
community
```

---

## Agent Execution Log

Tracks AI activity.

Model:

```
AgentRun

id
workspace
agent_name
input
output
tokens_used
created_at
```

---

# 7. AI Agent Architecture

## Agent System

Agents are implemented using PydanticAI.

---

# Knowledge Agent

Purpose:

Maintain understanding of the user.

Capabilities:

* Search knowledge
* Extract business information
* Maintain brand voice

Tools:

```
search_knowledge()
get_brand_voice()
get_business_profile()
```

---

# Content Agent

Purpose:

Create marketing content.

Input:

```
Topic
Goal
Audience
Platform
```

Output:

```
SocialPost

content
hook
call_to_action
hashtags
```

---

# Engagement Agent

Purpose:

Process replies.

Responsibilities:

* Analyze messages
* Draft responses
* Identify opportunities

Output:

```
ReplyDecision

category
confidence
response
requires_review
```

---

# Lead Agent

Purpose:

Find potential customers.

Responsibilities:

* Score conversations
* Detect buying intent
* Recommend action

Output:

```
LeadScore

score
intent
next_action
```

---

# 8. MCP Interface Design

BulkPost exposes MCP tools.

## Knowledge Tools

```
search_knowledge()
get_brand_voice()
```

---

## Content Tools

```
generate_post()
create_thread()
create_campaign()
```

---

## Publishing Tools

```
schedule_post()
publish_post()
```

---

## Sales Tools

```
analyze_reply()
classify_lead()
draft_response()
```

---

# 9. Main User Workflow

## New User

```
Create Account
      |
Create Workspace
      |
Upload Knowledge
      |
AI Creates Brand Profile
      |
Generate Content
      |
Approve
      |
Publish
      |
Monitor Engagement
      |
Convert Leads
```

---

# 10. Security Design

## Requirements

* User data isolation
* Workspace permissions
* Encrypted tokens
* API authentication
* Audit logging

---

# 11. Future Expansion

## Agent Marketplace

Users create:

* Sales agents
* Launch agents
* Support agents
* Newsletter agents

---

## Additional Knowledge Sources

Integrations:

* GitHub
* Notion
* Google Drive
* Slack
* CRM systems
* Email

---

## Autonomous Marketing

Future workflow:

```
Business Goal

     ↓

Marketing Agent

     ↓

Creates Campaign

     ↓

Publishes Content

     ↓

Engages Audience

     ↓

Generates Leads
```

---

# 12. MVP Definition

The first production version must support:

## Required

✅ Django SaaS backend
✅ User accounts
✅ Knowledge base
✅ RAG search
✅ PydanticAI agents
✅ Content generation
✅ X/Twitter publishing
✅ Reply analysis
✅ FastMCP server

---

# 13. Success Criteria

The MVP is successful when:

A user can:

1. Add their knowledge.
2. Generate authentic content.
3. Publish consistently.
4. Receive engagement.
5. Convert conversations into leads.

---

# End of Document

