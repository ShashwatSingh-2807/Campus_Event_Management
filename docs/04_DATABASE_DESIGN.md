# CampusLoop Database Design

**Document:** 04 — Database Design  
**Version:** 1.2  
**Status:** Draft baseline  
**Database:** PostgreSQL  
**Scope:** Single-college MVP pilot at NIE Mysuru; schema designed so additional colleges can be onboarded later.

---

## 1. Purpose

This document defines the initial relational data model for CampusLoop. It translates the PRD, TRD, and Application Flow into database entities, relationships, constraints, and transaction rules.

The schema is intentionally designed for the MVP. It supports verified students, club-based organizers, trusted publishing, event approval, individual registrations, and college-level administration. Team registration, payments, attendance scanning, certificates, and waitlists are outside this version.

The following product decisions have been confirmed for this baseline:
- A student may register again after cancelling, provided registration is open and capacity is available. The same registration row is reactivated.
- One account has at most one college affiliation in the MVP.
- Material edits to an approved event must be reviewed before they replace the currently approved event details, including when the organizer is a trusted publisher.

A documented schema is a design proposal. It becomes authoritative only after review and implementation testing.

## 2. Design principles

1. **College-scoped data:** college-owned records carry a `college_id` directly or through a parent relationship. Every read and write must be scoped and authorized by the backend.
2. **Separate identity from permissions:** a user account, verified college affiliation, organizer membership, and trusted-publisher status are distinct concepts.
3. **Database-enforced integrity:** use foreign keys, unique constraints, check constraints, and transactions rather than relying only on frontend validation.
4. **No premature denormalization:** calculate registration counts from registration rows in the MVP. Introduce cached counters only if measured performance requires them.
5. **Auditable administration:** record approvals, trust changes, and other important administrative actions.
6. **UTC storage:** store timestamps as PostgreSQL `timestamptz`; render them in the event's configured timezone.

## 3. Entity overview

| Module | Tables | Responsibility |
|---|---|---|
| Institution | `colleges`, `college_email_domains` | College identity and permitted institutional email domains |
| Identity | `users`, `email_verification_tokens`, `refresh_sessions` | Accounts, verification, and refresh-session lifecycle |
| Authorization | `user_role_assignments` | College-scoped and platform-level roles |
| Clubs | `clubs`, `club_memberships`, `organizer_profiles` | Clubs, organizer membership, and trusted-publisher status |
| Events | `event_categories`, `events`, `event_revisions`, `event_approval_history` | Approved event content, proposed edits, lifecycle, and approval trail |
| Participation | `registrations`, `registration_status_history` | Individual registrations and their activation/cancellation history |
| Governance | `audit_logs` | Security-sensitive and administrative activity |

Primary keys will use UUIDs. Table and column names use `snake_case`. SQLAlchemy models and Alembic migrations will implement this design.

## 4. Entity relationships

```mermaid
erDiagram
    COLLEGES ||--o{ COLLEGE_EMAIL_DOMAINS : allows
    COLLEGES ||--o{ USERS : affiliates
    USERS ||--o{ EMAIL_VERIFICATION_TOKENS : verifies
    USERS ||--o{ REFRESH_SESSIONS : owns
    USERS ||--o{ USER_ROLE_ASSIGNMENTS : receives
    COLLEGES ||--o{ USER_ROLE_ASSIGNMENTS : scopes
    COLLEGES ||--o{ CLUBS : contains
    USERS ||--o{ ORGANIZER_PROFILES : has
    COLLEGES ||--o{ ORGANIZER_PROFILES : scopes
    CLUBS ||--o{ CLUB_MEMBERSHIPS : has
    USERS ||--o{ CLUB_MEMBERSHIPS : joins
    ORGANIZER_PROFILES ||--o{ CLUB_MEMBERSHIPS : authorizes
    EVENT_CATEGORIES ||--o{ EVENTS : classifies
    COLLEGES ||--o{ EVENTS : hosts
    CLUBS ||--o{ EVENTS : organizes
    USERS ||--o{ EVENTS : creates
    EVENTS ||--o{ EVENT_REVISIONS : receives
    USERS ||--o{ EVENT_REVISIONS : proposes
    EVENTS ||--o{ EVENT_APPROVAL_HISTORY : records
    EVENT_REVISIONS o|--o{ EVENT_APPROVAL_HISTORY : reviewed_in
    USERS ||--o{ EVENT_APPROVAL_HISTORY : reviews
    EVENTS ||--o{ REGISTRATIONS : receives
    USERS ||--o{ REGISTRATIONS : makes
    REGISTRATIONS ||--o{ REGISTRATION_STATUS_HISTORY : tracks
    USERS o|--o{ REGISTRATION_STATUS_HISTORY : changes
    USERS ||--o{ AUDIT_LOGS : performs
    COLLEGES ||--o{ AUDIT_LOGS : scopes
```

The diagram shows the principal relationships. Some relationships are optional at the row level; for example, an event may not yet have an approver while it is a draft.

## 5. Table specifications

### 5.1 `colleges`

Stores each participating institution.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `name` | VARCHAR(180) | Required |
| `slug` | VARCHAR(100) | Required, unique |
| `city` | VARCHAR(100) | Required |
| `state` | VARCHAR(100) | Required |
| `country_code` | CHAR(2) | Required; ISO 3166-1 alpha-2 |
| `timezone` | VARCHAR(64) | Required; default `Asia/Kolkata` for the pilot |
| `is_active` | BOOLEAN | Required; default true |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

### 5.2 `college_email_domains`

Defines the institutional domains accepted for student verification.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `college_id` | UUID | FK → `colleges.id`, required |
| `domain` | VARCHAR(255) | Required; normalized lowercase, unique |
| `is_active` | BOOLEAN | Required; default true |
| `created_at` | TIMESTAMPTZ | Required |

A domain must be explicitly configured by an administrator. Do not accept arbitrary email suffixes supplied by a client. Domain ownership and institutional affiliation still require a verification process; a matching domain alone is not proof that an email address is controlled by the user.

### 5.3 `users`

Stores the account and basic profile. A user has at most one college affiliation in the MVP. `college_id` is assigned by the backend after institutional email verification and is not user-editable.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `college_id` | UUID | FK → `colleges.id`, nullable until verified |
| `email` | VARCHAR(320) | Required; normalized lowercase |
| `password_hash` | VARCHAR(255) | Required; Argon2id hash, never plaintext |
| `full_name` | VARCHAR(160) | Required |
| `email_verified_at` | TIMESTAMPTZ | Nullable until verified |
| `account_status` | VARCHAR(20) | Required; `ACTIVE`, `SUSPENDED`, or `DELETED` |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

Constraints:
- Unique index on normalized `email`.
- A verified student must have a college affiliation; enforce this in the verification transaction. The database should prevent a verified account from existing without its college affiliation.
- Do not allow a client to set `college_id` directly during signup. The backend derives it from the verified, configured domain and the verification workflow.
- After verification, the account remains affiliated with that one college in the MVP. Do not silently move an account to another college. A future transfer process would require an explicit, audited account-reaffiliation workflow.
- Account deletion should be a controlled deactivation/anonymization workflow, not an unrestricted cascading delete that destroys audit history.

### 5.4 `email_verification_tokens`

Stores one-time email verification challenges.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK → `users.id`, required |
| `token_hash` | VARCHAR(255) | Required; unique |
| `expires_at` | TIMESTAMPTZ | Required |
| `consumed_at` | TIMESTAMPTZ | Nullable |
| `created_at` | TIMESTAMPTZ | Required |

Store only a cryptographic hash of the verification token. A token is valid only when it has not expired and `consumed_at IS NULL`. Consume it atomically so it cannot be reused. When a replacement verification message is issued, mark prior unexpired tokens for the same user as consumed in the same transaction that creates the new token. Expired and consumed tokens can be periodically purged according to the retention policy.

### 5.5 `refresh_sessions`

Tracks refresh-token sessions to support rotation and logout.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK → `users.id`, required |
| `token_hash` | VARCHAR(255) | Required; unique |
| `expires_at` | TIMESTAMPTZ | Required |
| `revoked_at` | TIMESTAMPTZ | Nullable |
| `replaced_by_session_id` | UUID | Self-FK → `refresh_sessions.id`, nullable |
| `created_at` | TIMESTAMPTZ | Required |
| `user_agent` | TEXT | Optional |
| `ip_address` | INET | Optional; apply privacy and retention controls |

Refresh tokens are rotated on use. Reuse of an already-rotated token should trigger session-family revocation and security logging. Store token hashes, not raw refresh tokens.

### 5.6 `user_role_assignments`

Stores roles separately from the user account so one user can be a student and also hold organizer or college-admin privileges.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK → `users.id`, required |
| `college_id` | UUID | FK → `colleges.id`, nullable only for platform-wide roles |
| `role` | VARCHAR(30) | `STUDENT`, `ORGANIZER`, `COLLEGE_ADMIN`, `PLATFORM_ADMIN` |
| `granted_by_user_id` | UUID | FK → `users.id`, nullable for controlled system bootstrap |
| `revoked_by_user_id` | UUID | FK → `users.id`, nullable until revoked |
| `revoked_at` | TIMESTAMPTZ | Nullable; null means the role assignment is active |
| `created_at` | TIMESTAMPTZ | Required |

Constraints:
- Enforce uniqueness only for active assignments using partial unique indexes where `revoked_at IS NULL`; handle platform-wide rows separately because `college_id` is null.
- Revocation is soft: set `revoked_at` and `revoked_by_user_id`, and append an audit log. Do not delete the historical role assignment.
- `PLATFORM_ADMIN` must have `college_id IS NULL`; college-scoped roles must have a college.
- Only an authorized administrator or controlled bootstrap process can grant privileged roles.
- `STUDENT` is assigned after successful institutional email verification.
- Organizer access is additionally tied to club membership; a role assignment alone does not grant access to every club.

### 5.7 `clubs`

Represents a recognized student club or organizing body within a college.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `college_id` | UUID | FK → `colleges.id`, required |
| `name` | VARCHAR(160) | Required |
| `slug` | VARCHAR(120) | Required; unique within a college |
| `description` | TEXT | Optional |
| `contact_email` | VARCHAR(320) | Optional |
| `is_active` | BOOLEAN | Required; default true |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

Unique constraint: `(college_id, slug)`.

### 5.8 `organizer_profiles`

Represents a user's organizer standing within a college. This is where trusted-publisher status is stored, separately from student verification and club membership.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK → `users.id`, required |
| `college_id` | UUID | FK → `colleges.id`, required |
| `is_trusted_publisher` | BOOLEAN | Required; default false |
| `trusted_by_user_id` | UUID | FK → `users.id`, nullable |
| `trusted_at` | TIMESTAMPTZ | Nullable |
| `trust_note` | TEXT | Optional |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

Unique constraint: `(user_id, college_id)`.

Trust can be granted or revoked only by an authorized college administrator. The change must also create an audit-log record. A trusted publisher may publish eligible events directly; trust does not bypass validation, cancellation rules, or moderation.

### 5.9 `club_memberships`

Links organizer profiles to clubs and defines what they can do within each club.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `club_id` | UUID | FK → `clubs.id`, required |
| `organizer_profile_id` | UUID | FK → `organizer_profiles.id`, required |
| `membership_role` | VARCHAR(20) | `OWNER`, `EDITOR`, or `VIEWER` |
| `is_active` | BOOLEAN | Required; default true |
| `granted_by_user_id` | UUID | FK → `users.id`, nullable |
| `revoked_by_user_id` | UUID | FK → `users.id`, nullable until revoked |
| `revoked_at` | TIMESTAMPTZ | Nullable; records soft revocation time |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

Use a partial unique index on `(club_id, organizer_profile_id)` where `is_active = true`, so only one active membership exists for a club/organizer pair while revoked history rows remain. The application must verify that the club and organizer profile belong to the same college. A composite foreign key can enforce this if the implementation adds matching unique keys on the parent tables.

Revocation is performed by setting `is_active = false`, `revoked_at`, and `revoked_by_user_id`, and appending an audit log. Do not delete the membership row. A later re-grant creates a new active membership row; the revoked row remains for history. When the organizer has no remaining active club memberships in that college, revoke the college-scoped `ORGANIZER` role assignment using its `revoked_at` and `revoked_by_user_id` fields, and clear `is_trusted_publisher` so a later re-grant does not silently restore old publishing privileges. If the organizer still has another active club membership in the same college, the college-scoped organizer role and trust attribute remain; access is still limited to the active memberships.

### 5.10 `event_categories`

A small lookup table for consistent event classification.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `name` | VARCHAR(80) | Required; unique |
| `slug` | VARCHAR(90) | Required; unique |
| `is_active` | BOOLEAN | Required; default true |

Initial categories may include Technical, Cultural, Sports, Workshop, Seminar, and Other. Administrators can manage this list.

### 5.11 `events`

Stores the event itself and its current lifecycle state.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `college_id` | UUID | FK → `colleges.id`, required |
| `club_id` | UUID | FK → `clubs.id`, required |
| `category_id` | UUID | FK → `event_categories.id`, required |
| `created_by_user_id` | UUID | FK → `users.id`, required |
| `title` | VARCHAR(180) | Required |
| `summary` | VARCHAR(300) | Required |
| `description` | TEXT | Required |
| `venue` | VARCHAR(240) | Required for in-person events |
| `is_online` | BOOLEAN | Required; default false |
| `meeting_url` | TEXT | Optional; do not expose before permitted |
| `starts_at`, `ends_at` | TIMESTAMPTZ | Required; ends after starts |
| `registration_opens_at` | TIMESTAMPTZ | Required |
| `registration_closes_at` | TIMESTAMPTZ | Required |
| `timezone` | VARCHAR(64) | Required; default from college |
| `capacity` | INTEGER | Nullable for unlimited; if set, must be greater than zero |
| `eligibility_notes` | TEXT | Nullable; human-readable eligibility requirements |
| `contact_email` | VARCHAR(320) | Nullable; validated and normalized email address for event enquiries |
| `status` | VARCHAR(30) | Required; lifecycle state |
| `rejection_reason` | TEXT | Nullable |
| `cancellation_reason` | TEXT | Nullable |
| `published_at` | TIMESTAMPTZ | Nullable |
| `content_version` | INTEGER | Required; default 1; increments whenever approved event content is changed |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

Allowed statuses:
- `DRAFT`
- `PENDING_APPROVAL`
- `PUBLISHED`
- `REGISTRATION_CLOSED`
- `ONGOING`
- `COMPLETED`
- `CANCELLED`
- `REJECTED`

The backend validates allowed transitions. For example, a normal draft is submitted for approval; a trusted publisher can publish directly on initial publication; an approved event moves through registration closed, ongoing, and completed. Cancellation is available only to authorized users and must be recorded.

For an already-approved event, material edits are submitted as a separate event revision for college-admin review. The approved row in `events` remains unchanged and continues to power public event details while the proposed revision is pending. On approval, the proposed content is copied into `events` atomically and `content_version` is incremented. On rejection, the approved event remains unchanged. This approval requirement also applies to trusted publishers; trusted status bypasses initial publication review, not review of material edits to an approved event.

Material edits include changes to the title, summary, description, category, venue or online details, event schedule, registration window, or capacity. Until a narrower non-material-edit policy is defined, changes to approved event content should use the revision workflow rather than being written directly to the published row.

The `college_id` on an event must match the college of its club. The creator must be an active member of that club with sufficient membership permissions. Event data includes optional `eligibility_notes` and `contact_email`; these fields are copied into event revision snapshots and are published only as part of approved event content. Enforce these cross-table rules in the service layer and, where practical, with composite foreign keys.

### 5.12 `event_revisions`

Stores proposed material changes to an event that has already been approved or published. This keeps unapproved edits separate from the public, approved event record.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `event_id` | UUID | FK → `events.id`, required |
| `version` | INTEGER | Required; revision number for this event |
| `base_content_version` | INTEGER | Required; `events.content_version` when this revision was submitted |
| `proposed_by_user_id` | UUID | FK → `users.id`, required |
| `proposed_data` | JSONB | Required; complete validated snapshot of editable event fields |
| `status` | VARCHAR(24) | `PENDING_APPROVAL`, `APPROVED`, `REJECTED`, or `SUPERSEDED` |
| `created_at` | TIMESTAMPTZ | Required |
| `reviewed_at` | TIMESTAMPTZ | Nullable |

Constraints and behavior:
- Unique on `(event_id, version)`.
- A partial unique index allows at most one row per event with `status = 'PENDING_APPROVAL'`.
- Once submitted, `proposed_data` is immutable. A change to the proposal requires a new revision or replacement of the still-pending proposal under a controlled service operation.
- Validate the JSON structure against the event schema in the backend before inserting it. Do not accept arbitrary JSON fields from clients.
- `base_content_version` prevents a stale proposal from overwriting newer approved content. Before approval, lock the event row and verify that its current `content_version` still matches the revision's base version.
- Approval applies the proposed fields to `events`, increments `events.content_version`, marks the revision approved, and inserts the approval-history record in one transaction.
- Rejection marks the revision rejected and records the review decision; the approved event row is not changed.
- Only authorized organizers for the event's club may submit revisions. Only a college admin for the event's college may approve or reject them.

When a revision is pending, the public event remains the last approved version. This avoids showing students unreviewed schedule, venue, capacity, or description changes.

### 5.13 `event_approval_history`

Keeps a history of initial event approval decisions and later revision decisions.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `event_id` | UUID | FK → `events.id`, required |
| `revision_id` | UUID | FK → `event_revisions.id`, nullable for initial publication review |
| `reviewed_by_user_id` | UUID | FK → `users.id`, required |
| `decision` | VARCHAR(20) | `APPROVED` or `REJECTED` |
| `comment` | TEXT | Optional |
| `created_at` | TIMESTAMPTZ | Required |

For initial publication, `revision_id` is null and the decision applies to the event submission itself. For a material edit, `revision_id` identifies the exact proposed revision reviewed. The current event content remains on `events`; this table explains how initial publication and later changes were reviewed.

### 5.14 `registrations`

Stores individual student registrations. Team registration and waitlists are not part of this MVP.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `event_id` | UUID | FK → `events.id`, required |
| `student_user_id` | UUID | FK → `users.id`, required |
| `status` | VARCHAR(20) | `REGISTERED` or `CANCELLED` |
| `registered_at` | TIMESTAMPTZ | Required |
| `cancelled_at` | TIMESTAMPTZ | Nullable |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required |

Constraints:
- Unique on `(event_id, student_user_id)` for the MVP. A student/event pair has one registration row, whether currently registered or cancelled.
- Student must be verified and affiliated with the same college as the event.
- Only published events within their registration window accept registrations.
- On cancellation, set status to `CANCELLED` and populate `cancelled_at`. On re-registration, reactivate the same row by setting status to `REGISTERED`, updating `registered_at` to the latest successful registration time, and clearing `cancelled_at`.
- Re-registration is allowed only while the registration window is open and capacity is available. The reactivated row counts as one active seat; it does not create a second registration.
- Record every initial registration, cancellation, and reactivation in `registration_status_history` so the sequence is retained even though the current state is stored on one row.

### 5.15 `registration_status_history`

Records every change in a registration's lifecycle, including repeated cancellations and reactivations.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `registration_id` | UUID | FK → `registrations.id`, required |
| `previous_status` | VARCHAR(20) | Nullable for the initial registration event |
| `new_status` | VARCHAR(20) | `REGISTERED` or `CANCELLED` |
| `changed_by_user_id` | UUID | FK → `users.id`, nullable only for controlled system actions |
| `reason` | TEXT | Optional |
| `created_at` | TIMESTAMPTZ | Required |

Insert the registration row and its initial history row in one transaction. Cancellation and reactivation each update the current registration and append a history row in the same transaction. Application roles should not be able to update or delete historical rows.

## 6. Audit logging

### 6.1 `audit_logs`

Records important actions such as organizer trust changes, role grants/revocations, event approvals/rejections, and event cancellation.

| Column | Type | Rules |
|---|---|---|
| `id` | UUID | Primary key |
| `college_id` | UUID | FK → `colleges.id`, nullable for platform-wide actions |
| `actor_user_id` | UUID | FK → `users.id`, nullable only for controlled system actions |
| `action` | VARCHAR(100) | Required |
| `entity_type` | VARCHAR(80) | Required |
| `entity_id` | UUID | Required |
| `metadata` | JSONB | Optional; exclude passwords, tokens, and sensitive personal data |
| `created_at` | TIMESTAMPTZ | Required |

Audit rows should be append-only for application users. Restrict access to administrators and never log raw authentication tokens or passwords.

## 7. Important constraints and indexes

Create indexes for common filters and joins:

| Table | Index / constraint | Reason |
|---|---|---|
| `users` | Unique on normalized `email` | Login and duplicate-account prevention |
| `college_email_domains` | Unique on `domain`; index on `college_id` | Domain lookup and administration |
| `user_role_assignments` | Partial unique indexes for active role assignments; index on `(college_id, role, revoked_at)` | Authorization checks and role history |
| `clubs` | Unique on `(college_id, slug)` | College-scoped club identity |
| `club_memberships` | Partial unique index on `(club_id, organizer_profile_id)` where active; index on `organizer_profile_id` | Active membership uniqueness and history lookup |
| `events` | Index on `(college_id, status, starts_at)` | Public event discovery |
| `events` | Index on `(club_id, created_at)` | Organizer event dashboard |
| `events` | Check `ends_at > starts_at`; positive capacity when not null | Valid event data |
| `events` | Index on `(college_id, contact_email)` only if contact lookup is needed; otherwise no dedicated contact index | Avoid unnecessary indexes on low-selectivity profile fields |
| `registrations` | Unique on `(event_id, student_user_id)` | Prevent duplicate registration |
| `registrations` | Index on `(student_user_id, status, registered_at)` | Student's registered events |
| `registrations` | Index on `(event_id, status)` | Participant lists and capacity checks |
| `event_revisions` | Unique on `(event_id, version)` and partial unique on `event_id` for pending revisions | Prevent duplicate revision numbers and simultaneous pending edits |
| `event_approval_history` | Index on `(event_id, created_at)` and optional `revision_id` | Initial and revision approval history |
| `registration_status_history` | Index on `(registration_id, created_at)` | Registration lifecycle history |
| `audit_logs` | Index on `(college_id, created_at)` and `(entity_type, entity_id)` | Audit investigation |

For frequently queried event lists, use pagination and stable ordering (for example, `starts_at, id`). Add partial indexes only after query patterns are measured.

## 8. Registration capacity: transaction rule

A simple count-then-insert without locking can oversubscribe an event when two requests arrive simultaneously. The registration service must perform the capacity check and registration write in one database transaction.

Recommended MVP approach:

1. Begin a transaction.
2. Lock the event row using `SELECT ... FOR UPDATE`.
3. Confirm the event is published and the current time is within the registration window.
4. Confirm the student is verified and belongs to the event's college.
5. Check whether the student already has a registration row.
6. Count rows with `status = 'REGISTERED'` for that event.
7. If capacity is set and the count has reached it, reject the request.
8. If no row exists, insert it; if a cancelled row exists, reactivate that same row and update its latest registration timestamp.
9. Append a `registration_status_history` row for the registration or reactivation.
10. Commit.

All registration creation paths must use this service/locking rule. The unique constraint remains a final defense against duplicate requests. If throughput later requires a counter-based approach, introduce it with a carefully tested atomic update and reconciliation job.

## 9. Authorization rules represented by the model

| Action | Required authorization |
|---|---|
| Browse published events | Public; college filter applies |
| Register for an event | Verified student in the same college |
| Create/edit a draft event | Active club member with OWNER or EDITOR permission |
| Submit material edits to an approved event | Active club member with OWNER or EDITOR permission; revision review required |
| Publish a new event directly | Eligible active organizer with trusted-publisher status |
| Approve/reject material event revisions | College admin for the event's college |
| Submit for approval | Eligible active organizer without trusted-publisher status |
| Approve/reject an event | College admin for that college |
| Grant/revoke organizer trust | College admin for that college |
| Manage college settings/domains | Authorized college admin |
| Platform-wide administration | Platform admin |

The frontend may hide unavailable actions, but the backend must independently enforce every rule. Never trust a role, college ID, organizer ID, or trust flag supplied by the client.

## 10. Deletion and retention policy

- Prefer soft deactivation for colleges, clubs, users, and categories where historical records depend on them.
- Do not cascade-delete events, registrations, approval history, or audit history when a user account is deactivated.
- Restrict deletion of parent records referenced by historical records.
- Define a retention and privacy policy before production deployment, especially for IP addresses, session metadata, and account deletion requests.
- Avoid collecting personal data that is not needed for the MVP.

## 11. Migration and implementation plan

1. Create SQLAlchemy models matching the approved schema.
2. Generate and review the initial Alembic migration.
3. Add foreign keys, unique constraints, check constraints, and indexes in migrations.
4. Seed the initial college, its verified email domain(s), and event categories through a controlled seed process.
5. Create the first college-admin account through a secure bootstrap command; never hardcode production credentials.
6. Add model and migration tests.
7. Add service tests for verification, role checks, approval transitions, and concurrent registration capacity.
8. Use test data to validate that one college cannot access another college's private organizer or administrative data.

## 12. Confirmed decisions and remaining policy choices

The following database-level product decisions are confirmed for this version:

| Decision | Confirmed rule | Database consequence |
|---|---|---|
| Re-registration after cancellation | Allowed while registration is open and capacity is available | Reactivate the existing unique `(event_id, student_user_id)` row; append a status-history record |
| Student cancellation cutoff | A student may cancel their active registration until strictly before the event start time | Service checks current UTC time against `events.starts_at`; no per-event cutoff column in v1.0 |
| College affiliation | One college per account in the MVP | Store one `users.college_id`; assign after verification and do not allow client-side changes |
| Editing an approved event | Material edits require approval again | Store proposed edits in `event_revisions`; keep the public approved event unchanged until approval |
| Event eligibility/contact details | Store optional eligibility notes and an event contact email | Add `eligibility_notes` and `contact_email` to `events`; include them in revision snapshots |

Additional policy choices still need to be settled before implementation:

| Decision | Proposed MVP default | Why it matters |
|---|---|---|
| Can clubs have multiple owners? | Yes | Avoids a single-person bottleneck |
| Are external guests allowed to register? | No in MVP | Keeps the first release college-scoped |
| Are waitlists supported? | No in MVP | Avoids extra capacity and promotion workflows |
| What qualifies as a non-material correction? | Until defined, route edits to approved event content through revision approval | Avoids accidentally exposing unreviewed changes |
| What happens when an approved revision changes date or venue? | Keep existing registrations; require organizer/admin communication policy | Schedule and venue changes can materially affect attendees |
| Can an approved revision reduce capacity below the current active registration count? | No | Prevents an approved change from making the event oversubscribed |

These defaults and policy choices should be checked against the PRD before creating migrations. In particular, the API must implement reactivation, revision submission/review, college-scoped authorization, organizer membership revocation, and active-role history as explicit workflows.

## 13. Out of scope for v1.0

- Team registration and team-member tables
- Waitlists and automatic waitlist promotion
- Payments, refunds, and invoices
- Attendance/check-in QR codes
- Certificates
- Event feedback and ratings
- Notifications and notification-delivery logs
- Sponsorships and monetization records
- Multi-college memberships for one user

These can be added through later migrations without building them prematurely into the MVP.

---

**Next document:** API Specification — define endpoint contracts, request/response schemas, validation rules, authorization requirements, and error responses against this data model.
