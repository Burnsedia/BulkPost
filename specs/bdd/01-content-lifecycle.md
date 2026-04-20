# Feature: Content Lifecycle

Goal: move content from idea to published post with optional review and safe defaults.

## Scenario 1: Generate draft from campaign context

```gherkin
Given an authenticated user with an active Campaign
And at least one Prompt and SystemPrompt exists
When the user runs the Content Agent for that campaign
Then a ContentDraft is created with status "draft"
And the draft is linked to the campaign and prompt context
And the draft body is not empty
```

## Scenario 2: Approve draft for scheduling

```gherkin
Given an authenticated user owns a ContentDraft with status "in_review"
When the user approves the draft
Then the ContentDraft status becomes "approved"
And approved_by_user is true
And updated_at is changed
```

## Scenario 3: Schedule approved draft

```gherkin
Given an authenticated user owns a ContentDraft with status "approved"
When the user schedules it for a future datetime
Then the ContentDraft status becomes "scheduled"
And scheduled_for is set
And a Post queue item is created with status "pending"
```

## Scenario 4: Publish scheduled post successfully

```gherkin
Given a scheduled Post exists with status "pending"
And the execution service is running
When the scheduler reaches the scheduled time
And the platform API returns success
Then Post status becomes "posted"
And posted_at is set
And twitter_id is stored
And the linked ContentDraft status becomes "published"
```

## Scenario 5: Handle publish failure without data loss

```gherkin
Given a scheduled Post exists with status "pending"
When execution attempts to publish and the platform API fails
Then Post status becomes "failed"
And Post.error contains a failure reason
And no duplicate Post is created
And the linked ContentDraft does not become "published"
```

## Scenario 6: Prevent scheduling unapproved draft

```gherkin
Given an authenticated user owns a ContentDraft with status "draft"
When the user attempts to schedule it
Then the request is rejected
And no Post queue item is created
And the ContentDraft status remains unchanged
```
