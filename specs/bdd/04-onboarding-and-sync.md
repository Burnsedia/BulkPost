# Feature: Onboarding and Sync

Goal: user connects once and the system runs autonomously.

## Scenario 1: Connect X account with OAuth

```gherkin
Given a new authenticated user starts onboarding
When the user completes X OAuth callback
Then access credentials are stored securely
And account connection status is marked connected
```

## Scenario 2: Import tweet history after connect

```gherkin
Given user account is connected to X
When import history action runs
Then ImportedTweet records are created for recent tweets
And duplicate external_tweet_id values are not re-imported
```

## Scenario 3: Build style profile from imported tweets

```gherkin
Given ImportedTweet records exist for a user
When style profile build job runs
Then a StyleProfile is created or updated
And profile version increments on successful rebuild
```

## Scenario 4: Enable autonomous mode after onboarding

```gherkin
Given account is connected and StyleProfile exists
And policy defaults are set
When user toggles autopilot on
Then scheduler is allowed to run autonomous loops
And no manual social actions are required from the user
```
