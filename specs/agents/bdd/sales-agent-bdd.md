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
Given qualified leads exist and suppression rules allow contact
When Sales Agent proposes DM actions
Then actions include send_offer_dm for eligible leads
And each DM includes lead magnet and app link payload
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

## Scenario 5: Respect suppression and cooldown
```gherkin
Given a lead is marked do_not_contact or is within cooldown window
When Sales Agent evaluates DM actions
Then no send_offer_dm action is created for that lead
And output may include suppress or skip action
```

## Scenario 6: Follow-up after no response
```gherkin
Given an offer DM was sent and no reply was received within follow-up window
When Sales Agent evaluates follow-up actions
Then one follow_up action is generated if follow-up cap is not exceeded
And follow-up respects per-lead cadence limits
```
