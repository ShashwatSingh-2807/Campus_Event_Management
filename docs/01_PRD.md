# CampusLoop — Product Requirements Document

**Version:** 1.2  
**Status:** Draft baseline  
**Initial pilot:** NIE Mysuru  
**Product type:** Responsive web platform; mobile application considered for a later phase

---

## 1. Product overview

CampusLoop is a college event discovery, registration, and management platform. It brings student-facing event discovery and registration together with organizer-facing publishing and participant management.

The initial release will focus on one institution, NIE Mysuru. The product should be designed so that additional colleges can be supported later without rebuilding the core domain model.

## 2. Problem statement

College event information is often scattered across social media posts, messaging groups, posters, forms, and club-specific channels. Students can miss relevant events or struggle to find reliable details and registration links. Organizers may have to manage registrations and participant lists manually across separate tools.

CampusLoop aims to provide:

- A central, searchable catalogue of college events.
- Consistent event details and registration status.
- A clear registration experience for students.
- A workspace for organizers to publish events and manage participants.
- Administrative controls for event approval and organizer trust.

## 3. Product vision

Make campus events easier to discover, easier to join, and easier to manage.

## 4. Target users and personas

### 4.1 Student

A verified student who wants to discover events, understand eligibility and event details, register, and track their registrations.

### 4.2 Organizer

A club or event-team member who creates and manages events, reviews participant information, and communicates event changes through the platform.

### 4.3 College administrator

An authorized institutional administrator who manages organizer trust, reviews events from untrusted organizers, and oversees college-level platform activity.

### 4.4 Platform administrator

An operator responsible for platform-wide configuration and support. This role is distinct from a college administrator.

## 5. Goals

### 5.1 MVP goals

- Provide a reliable event discovery experience for students.
- Verify student affiliation using an official institutional email address.
- Allow authorized organizers to create and manage events.
- Apply approval rules to event publishing.
- Support individual event registration and cancellation.
- Give organizers access to participant lists and basic exports.
- Provide college administrators with approval and trust-management controls.

### 5.2 Pilot success targets

The initial pilot targets are:

| Metric | Target |
|---|---:|
| Clubs onboarded | 3 |
| Events published | 10 |
| Student registrations | 300 |
| Active organizers | 5 |

These are targets for validating adoption, not current achievements.

## 6. Non-goals for the MVP

The first release will not attempt to provide:

- Multi-college federation or cross-college discovery at launch.
- Team or group registration.
- Native Android or iOS applications.
- Payments, ticket sales, or refunds.
- Complex attendance scanning or QR-based check-in.
- In-app chat or social networking.
- Automated certificate generation.
- Advanced recommendation algorithms.
- A public organizer self-service marketplace.

These may be considered after the core workflow is validated.

## 7. Scope and functional requirements

### 7.1 Public event discovery

- Visitors can browse published events without logging in.
- Visitors can view event details.
- Event listings should support basic filtering and search.
- Draft, pending, rejected, and cancelled events must not appear as normally available public events.
- Registration requires an authenticated, verified student account.

### 7.2 Student registration and verification

- A student can register using an email address from an institution-approved domain.
- Email ownership must be verified through a verification link or one-time code.
- An unverified user can request a replacement verification message; the response must not reveal whether an account exists, and requests must be rate-limited.
- The backend determines the student's college affiliation from the verified email/domain configuration; users must not be able to assign themselves an arbitrary college.
- Students can log in and view their profile.
- Students can view their current and past registrations.
- Students can register individually for an eligible event.
- Students can cancel their own active registration strictly before the event start time. At or after the event start time, self-cancellation is not allowed.
- The system must prevent duplicate active registrations for the same student and event.

### 7.3 Organizer access

- Organizer access is granted separately from student verification.
- A student account does not automatically become an organizer account.
- Authorized administrators assign organizer privileges and can revoke individual club memberships. Revoking the final active club membership in a college also revokes the college-scoped organizer role and trusted-publisher status; a later organizer grant does not automatically restore trust.
- Organizers can create event drafts and edit events they are permitted to manage.
- Organizers can submit events for approval when required.
- Organizers can view registrations for their own events.
- Organizers can export participant data for operational use, subject to access controls.

### 7.4 Event publishing and trust

Organizer role and trusted-publisher status are separate attributes.

- A trusted organizer may publish directly, subject to validation and policy.
- An untrusted organizer must submit an event for college-admin approval.
- A college administrator can approve or reject a pending event.
- A college administrator can grant or revoke trusted status.
- Revoking trusted status affects future publishing decisions; it must not silently grant broader permissions.
- Every administrative approval, rejection, and trust change should be auditable.

### 7.5 Event management

An event should include, at minimum:

- Title and description
- Organizer/club association
- Event category
- Start and end date/time
- Venue or online-event details
- Registration opening and closing times
- Capacity, if limited
- Eligibility information
- Contact or support information
- Publication and lifecycle status

Organizers can update or cancel events they are authorized to manage. Material changes to an approved/published event must be submitted as a separate revision and approved by a college administrator before replacing the currently published content. Trusted-publisher status does not bypass revision approval.

### 7.6 Registration management

- Registration is individual in the MVP.
- Capacity-limited registration must not exceed the configured capacity.
- Registration creation must be atomic under concurrent requests.
- Registration records must retain their status and timestamps.
- Organizers can view the participant list for their events.
- A student can view their own registrations.
- Team registration and waitlists are deferred.

## 8. Roles and permissions

| Capability | Student | Organizer | College Admin | Platform Admin |
|---|---:|---:|---:|---:|
| Browse public events | Yes | Yes | Yes | Yes |
| Register for events | Yes | Policy-based | Policy-based | Policy-based |
| Manage own profile | Yes | Yes | Yes | Yes |
| Create/manage assigned events | No | Yes | Policy-based | Support/override |
| View event participants | No | Own events | College scope | Support/override |
| Approve pending college events | No | No | Yes | Platform policy |
| Grant/revoke organizer trust | No | No | Yes | Platform policy |
| Manage platform configuration | No | No | No | Yes |

The table is a high-level permission summary. Detailed resource-level authorization must be enforced by the backend.

## 9. Business rules

1. Only verified institutional accounts can use student registration features.
2. College affiliation is assigned by the backend based on verified institutional email configuration.
3. Organizer privileges are explicitly granted and are not implied by student verification.
4. Trusted status is separate from the organizer role.
5. Untrusted organizers require approval before an event becomes public.
6. Trusted organizers can publish directly, provided event validation succeeds.
7. Students can register only when registration is open and the event is eligible for registration.
8. Duplicate active registrations are not allowed.
9. Event capacity must never be exceeded, including during concurrent registrations.
10. A student can cancel only their own active registration and only strictly before the event start time. The cutoff is evaluated by the backend using server time.
11. Organizers can manage only events assigned to them or their authorized club.
12. College administrators operate within their college scope.
13. Platform administrators have platform-level responsibilities and should use elevated access only when necessary.

## 10. Event lifecycle

Proposed event states:

`DRAFT → PENDING_APPROVAL → PUBLISHED → REGISTRATION_CLOSED → ONGOING → COMPLETED`

Additional terminal or exception states:

- `REJECTED`
- `CANCELLED`

The backend must validate permitted transitions. A client must not be able to set arbitrary lifecycle states directly.

## 11. Registration lifecycle

Initial MVP statuses:

- `REGISTERED`
- `CANCELLED`

Waitlisted, checked-in, attended, and no-show states are not part of the initial registration lifecycle and may be introduced in later iterations.

## 12. Non-functional requirements

### Security and privacy

- Enforce authentication and authorization on the server.
- Store passwords using a modern password-hashing algorithm.
- Protect session and refresh-token handling.
- Validate and normalize user input.
- Apply college-level data access boundaries.
- Avoid exposing participant information to unauthorized users.
- Keep secrets and credentials out of source control.
- Record security-sensitive administrative actions.

### Reliability and correctness

- Use database transactions for registration and capacity enforcement.
- Use database uniqueness constraints to prevent duplicate registrations.
- Handle concurrent registration requests safely.
- Return consistent API errors.
- Preserve data integrity across event lifecycle changes.

### Usability and accessibility

- Provide a responsive experience for common mobile and desktop screen sizes.
- Keep event discovery and registration flows simple.
- Communicate event status, capacity, and registration outcomes clearly.
- Use accessible labels, keyboard navigation, and sufficient contrast.

### Maintainability

- Keep backend modules separated by domain responsibility.
- Use schema migrations for database changes.
- Document API behavior.
- Add automated tests for authorization and critical workflows.

## 13. Product metrics

Initial metrics to monitor:

- Verified student sign-ups
- Weekly and monthly active students
- Events published
- Event detail views
- Registration conversion rate
- Registration cancellation rate
- Organizer activation and retention
- Approval turnaround time
- Registration failures and capacity conflicts

Metrics should be interpreted in context; raw registrations alone do not prove sustained adoption.

## 14. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Students continue using existing channels | Start with a small set of active clubs and make event information reliable |
| Fake or unauthorized organizers | Explicit organizer grants, trust controls, and audit logs |
| Incorrect college affiliation | Verify institutional email and manage domain configuration carefully |
| Overbooking | Transactional registration and database constraints |
| Poor event data quality | Required fields and validation before publishing |
| Low organizer adoption | Keep event creation and participant management straightforward |
| Sensitive participant data exposure | Least-privilege access and college-scoped authorization |

## 15. Assumptions and open decisions

- The first pilot is limited to NIE Mysuru.
- The institution can provide or confirm an approved email-domain policy.
- College administrators can identify authorized clubs and organizers.
- Individual registration is sufficient for the MVP.
- Material edits to approved events require a reviewed revision, as defined in the confirmed business rules.
- Event categories, eligibility rules, and required organizer verification evidence may be refined during pilot planning.
- Legal, privacy, and institutional policy requirements must be reviewed before real student data is collected.

## 16. Future opportunities

After the MVP is validated, possible extensions include:

- Multi-college support
- Team registration and waitlists
- QR-based attendance
- Notifications and reminders
- Certificates
- Native mobile applications
- Event analytics for clubs and administrators
- Payments where institutionally appropriate

## 17. MVP acceptance criteria

The MVP can be considered ready for a controlled pilot when:

- A student can register, request a replacement verification message, and verify an approved institutional email.
- Unverified users cannot access student registration actions.
- A verified student can browse published events and register individually.
- Duplicate active registrations are rejected.
- Capacity cannot be exceeded under concurrent registration attempts.
- An organizer can create and manage an authorized event.
- An untrusted organizer's event requires approval.
- A trusted organizer can publish a valid event directly.
- College administrators can approve/reject pending events and revisions, grant/revoke organizer access, and manage trusted status.
- Students and organizers can see only the data permitted to their roles.
- Critical workflows have automated tests and documented failure behavior.
- The deployment has appropriate logging, secret management, and backup practices.

---

**Document note:** This is a product baseline for planning. It does not claim that any listed feature has been implemented.
