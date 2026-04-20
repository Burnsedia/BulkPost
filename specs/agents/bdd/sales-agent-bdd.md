# Feature: Sales Agent

## Scenario 1: Create actions from qualified leads
```gherkin
Given qualified leads with interaction history exist
When Sales Agent evaluates pipeline actions
Then output.actions contains score, dm_draft, or follow_up actions
And each action references a lead_id
```

## Scenario 2: Respect outbound policy guardrails
```gherkin
Given outbound DM requires human approval
When Sales Agent proposes DM actions
Then actions are drafts only
And no direct send action is executed by the agent
```

## Scenario 3: Prioritize high-intent leads
```gherkin
Given leads have different qualification scores and intent signals
When Sales Agent ranks follow-up actions
Then higher intent leads receive higher priority actions
```

## Scenario 4: Return traceable action summary
```gherkin
Given Sales Agent completes a run
When output is returned
Then output.summary is present
And each action includes rationale in content or context
```
