# Product Spec: BulkPost MVP

## 1. Goal

Define the smallest system that can:

- AI generate posts
- Automatically publish
- Track engagements
- store leads

Non-goals:

- Multi-platform postings
- Advanced AI fine-tuning
- Complex analytics dashboards

---

## 2. Core Entgities

### Post

- id
- title (string)
- slug (string)
- content (string)
- category(enum: value, engagements, authority, contrast, transfermation )
- status (enum)

### PostStatus

- id
- StatusName/Ttile(string)

### SchedlutleObject

- schedulted_time (datetime)
  
<!-- TODO:make something like this per platfrom -->
### TwitterPost

- twitterID
- post(FK post)

### LinkedInPost

- linkedinID
- post(FK post)

### ThreadsPost

- ThreedsID
- post(FK post)

### contact

- id
- username
- platfrom()
- bio

### interaction

- id
- post(FK)
- contact(FK)
this should be a django taggit tag
- type (enum: reply, like, retweet)

### LeadStatus

- id
- title(String)

### Lead

- id
- platform (enum of platfoms names maybe a choice class)
- status (FK LeadStatus)
- status (enum new, contacted, qulified, converted)
- contact (one2many contact)
