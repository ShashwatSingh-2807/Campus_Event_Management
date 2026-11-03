# CampusLoop — UI/UX Blueprint

**Document:** 06 — UI/UX Blueprint  
**Version:** 1.0  
**Status:** Draft baseline  
**Initial platform:** Responsive website  
**Primary users:** Visitors, verified students, organizers, and college administrators  
**Design principle:** Clear, approachable, functional, and easy to operate on a campus timetable.

---

## 1. Purpose

This document translates the Product Requirements Document, Application Flow, Database Design, and API Specification into a buildable frontend experience.

It defines:
- Navigation and application shell.
- Page purpose, layout, and primary actions.
- Reusable component inventory.
- Forms and validation expectations.
- Loading, empty, error, and success states.
- Responsive and accessibility behavior.
- The relationship between screens and backend API operations.

This is a UI specification, not a finished Figma design or implemented frontend. The visual values below are a starting design system and may be refined after the first working screens are tested.

## 2. Experience goals

1. **Discovery first:** visitors should understand what is happening on campus without creating an account.
2. **Registration should be obvious:** event details, eligibility, timing, and registration state must be easy to understand.
3. **Role boundaries should be clear:** students, organizers, and college administrators should see relevant workspaces without confusing permissions.
4. **Trustworthy status:** published, pending, rejected, cancelled, and registration-closed states must look and read differently.
5. **Low-friction operations:** organizers should be able to create an event and manage its participants without navigating a complicated admin system.
6. **Responsive by default:** the website should work well on a phone, where many students will discover events.
7. **Accessible interactions:** keyboard navigation, readable contrast, visible focus, and clear form feedback are required.

## 3. Product scope in the UI

### 3.1 Included in the MVP

- Public home and event discovery.
- Public event details.
- Student registration, email verification, login, password reset, profile, and My Events.
- Organizer dashboard, event creation/editing, event management, revision submission, participant list, and CSV export.
- College-admin dashboard, initial event approval/rejection, revision approval/rejection, organizer assignment, and trusted-publisher management.

### 3.2 Excluded from the MVP UI

- Team registration and waitlists.
- Payments, tickets, refunds, or checkout.
- QR attendance/check-in.
- Certificates.
- In-app chat, social feeds, or comments.
- Push-notification inbox.
- Native mobile app.
- Advanced event recommendations.
- Platform-admin operational console beyond separately defined platform operations.

Do not add placeholder navigation for deferred features unless it has a real near-term use.

---

## 4. Visual direction

### 4.1 Overall style

Use a clean campus-product aesthetic:
- Light surfaces with a restrained neutral background.
- Dark, high-contrast text.
- One primary brand accent for links and main actions.
- Small, consistent status colors for lifecycle feedback.
- Clear typography and generous spacing.
- Real event photography or club-provided artwork where available; do not make decorative images mandatory for event creation.
- Avoid excessive gradients, glass effects, animated backgrounds, oversized hero sections, or too many card styles.

The application should feel credible and useful, not like a marketing landing page inside every dashboard.

### 4.2 Suggested design tokens

These are initial design tokens, not final brand guidelines.

| Token | Suggested value | Usage |
|---|---|---|
| `color.primary` | `#4F46E5` | Main CTA, active navigation, links |
| `color.primary.hover` | `#4338CA` | Hover state |
| `color.text` | `#172033` | Main content |
| `color.text.muted` | `#64748B` | Secondary labels |
| `color.surface` | `#FFFFFF` | Cards and panels |
| `color.background` | `#F8FAFC` | Page background |
| `color.border` | `#E2E8F0` | Dividers and field borders |
| `color.success` | `#15803D` | Published/success/confirmed |
| `color.warning` | `#B45309` | Pending/attention |
| `color.danger` | `#B91C1C` | Rejected/cancelled/destructive |
| `radius.control` | `8px` | Inputs and buttons |
| `radius.card` | `12px` | Cards and panels |
| `spacing.unit` | `4px` | Base spacing unit |

Use color together with a text label or icon. Never communicate an event state by color alone.

### 4.3 Typography

- Use a readable sans-serif family such as Inter or the system sans-serif stack.
- Page title: 24–32 px desktop, 22–26 px mobile.
- Section title: 18–20 px.
- Body: 14–16 px.
- Secondary metadata: 12–14 px.
- Use weight and spacing before introducing additional font styles.

### 4.4 Layout and spacing

- Desktop content maximum width: approximately 1200 px.
- Standard page side padding: 24–32 px desktop; 16 px mobile.
- Card padding: 16–20 px.
- Form field vertical gap: 16 px.
- Section gap: 24–32 px.
- Prefer aligned grids and consistent spacing over individually styled cards.

### 4.5 Motion

Motion is optional and should communicate state:
- Short hover and focus transitions.
- Small loading indicators for network actions.
- Subtle drawer or menu transitions.
- No autoplay animation or motion that delays essential actions.
- Respect reduced-motion preferences.

---

## 5. Global application shell

### 5.1 Public shell

Desktop:
- Top navigation with CampusLoop wordmark.
- Primary links: Home, Explore Events.
- Right side: Log in and Create Account.
- Main content in a centered max-width container.
- Footer with About, Contact/Support, and basic policy links when those pages exist.

Mobile:
- Compact header with wordmark and menu button.
- Navigation opens in an accessible drawer or menu.
- Keep Explore Events easy to reach.
- Avoid a crowded row of navigation links.

### 5.2 Authenticated shell

Authenticated pages use a consistent header and role-aware navigation.

Desktop:
- Left sidebar for workspace navigation.
- Top header with page context, current user menu, and optional workspace switcher.
- Main content area with consistent page padding.

Mobile:
- Header with menu button and current page label.
- Navigation opens in a drawer.
- Main content uses a single-column layout.
- Tables convert to stacked rows or provide controlled horizontal scrolling when necessary.

### 5.3 Role-aware workspace switcher

A user can have more than one permission. When the API returns multiple roles, show only the workspaces the current user is allowed to enter:
- Student
- Organizer
- College Admin

The switcher is navigation convenience only. The backend continues to enforce all permissions. Do not show a Platform Admin workspace unless the user's platform role and platform-admin UI are explicitly in scope.

### 5.4 Global user menu

Include:
- Profile / Account
- Current college label, when available
- Switch workspace, when applicable
- Sign out

Do not put trust controls, role grants, or account-security actions in the ordinary student navigation.

---

## 6. Navigation map

| Area | Route | Page |
|---|---|---|
| Public | `/` | Home |
| Public | `/events` | Event discovery |
| Public | `/events/[eventId]` | Event detail |
| Auth | `/register` | Student account registration |
| Auth | `/verify-email` | Verification result |
| Auth | `/login` | Login |
| Auth | `/forgot-password` | Request password reset |
| Auth | `/reset-password` | Set new password |
| Student | `/student/onboarding` | First-time onboarding |
| Student | `/student/dashboard` | Student dashboard |
| Student | `/student/events` | Student event discovery |
| Student | `/student/my-events` | My Events |
| Student | `/student/profile` | Profile and account |
| Organizer | `/organizer/dashboard` | Organizer dashboard |
| Organizer | `/organizer/events` | Managed events |
| Organizer | `/organizer/events/create` | Create event |
| Organizer | `/organizer/events/[eventId]` | Manage event |
| Organizer | `/organizer/events/[eventId]/participants` | Participants |
| College Admin | `/college-admin/dashboard` | College overview |
| College Admin | `/college-admin/approvals` | Initial event approvals and revision queue |
| College Admin | `/college-admin/organizers` | Organizer access and trust |
| College Admin | `/college-admin/settings` | College settings |

Password-reset routes and the college-admin revision queue are added to the route map to support flows already described by the API specification. The revision queue can be a tab within the approvals page rather than a separate page.

---

## 7. Public experience

### 7.1 Home — `/`

**Purpose:** Explain CampusLoop quickly and let visitors discover current events.

Suggested desktop structure:
1. Header navigation.
2. Compact hero: one clear headline, one-sentence explanation, primary "Explore events" action.
3. Upcoming events section with 3–4 event cards.
4. Category shortcuts.
5. Simple footer.

Suggested mobile structure:
1. Compact header.
2. Headline and Explore Events action.
3. One-column upcoming event list.
4. Horizontally scrollable category chips only if they remain keyboard and screen-reader accessible.

Content principles:
- Do not claim event counts or campus adoption statistics unless backed by actual data.
- Show only public events returned by the API.
- If there are no upcoming events, explain that new events will appear here and link to Explore Events.
- Do not place a login wall before event discovery.

Primary actions:
- Explore Events → `/events`
- Open event card → `/events/[eventId]`
- Register / Sign in → `/register` or `/login`

### 7.2 Event discovery — `/events`

**Purpose:** Help visitors find relevant events quickly.

Desktop layout:
- Page title and short helper text.
- Search field at the top.
- Filter row: category, date range, online/in-person, registration open.
- Result count and sort control.
- Responsive event-card grid (2–3 columns depending on width).
- Pagination below results.

Mobile layout:
- Search field full width.
- Filters in a filter button/drawer or compact chips.
- One-column event cards.
- Pagination controls sized for touch.

Event card content:
- Optional event cover image or category visual.
- Category label.
- Event title and short summary.
- Date and time.
- Venue or Online label.
- Club/organizer.
- Registration state: Open, Not open yet, Closed, or Full when known.
- Clear "View details" action.

Filtering behavior:
- Search title and summary.
- Category filter.
- Start date range.
- Online/in-person filter.
- Registration-open filter.
- Sort by start date ascending or descending.
- Preserve active filters in URL query parameters so the page can be shared and refreshed.

API: `GET /event-categories`, `GET /events`.

States:
- Loading: event-card skeletons.
- Empty: "No events match these filters"; provide a Clear filters action.
- No campus events: explain that upcoming events will appear here.
- Error: clear message and Retry action; retain the search/filter state.
- Partial image failure: use a neutral category fallback, not a broken image icon.

### 7.3 Event detail — `/events/[eventId]`

**Purpose:** Provide enough information for a student to decide whether to attend.

Desktop layout:
- Breadcrumb: Explore Events / Event title.
- Main column: title, category, summary, description, date/time, venue/online details, eligibility, club and contact.
- Side panel: registration status, opening/closing time, remaining capacity when limited, and primary registration action.
- On smaller screens, move the action panel below the event summary or use a compact sticky action only if it does not cover content.

Required information hierarchy:
1. Event name and status.
2. Date/time and venue.
3. Registration availability and deadline.
4. Description.
5. Eligibility and contact information.
6. Organizer/club identity.

Actions:
- Visitor: "Log in to register" or "Create account".
- Verified eligible student: "Register".
- Already registered student: "You're registered" plus "Cancel registration" when cancellation is permitted.
- Cancelled registration: "Register again" when registration remains open and capacity is available.
- Closed/full/cancelled event: show a clear non-action state.

The backend decides final eligibility and registration outcome. The UI may display an availability hint but must not guarantee a seat until the API succeeds.

API: `GET /events/{event_id}`, `POST /events/{event_id}/registrations`, `POST /registrations/{registration_id}/cancel`.

### 7.4 Registration confirmation

Use a confirmation dialog or a focused confirmation panel before the initial registration POST:
- Event title and date.
- A clear statement that registration is individual.
- Confirm registration / Go back actions.

After success:
- Show a clear registered state.
- Provide a link to My Events.
- Do not imply that an email or notification was sent unless a notification service has actually confirmed delivery.

For cancellation:
- Ask for confirmation before cancelling.
- Explain that the seat may become available to another student.
- Show the updated Cancelled state only after the API confirms it.

---

## 8. Authentication and onboarding

### 8.1 Student registration — `/register`

Form fields:
- Full name.
- Institutional email.
- Password.
- Confirm password (frontend-only confirmation; never send separately unless required by implementation).
- Terms/privacy acknowledgement when approved policy text exists.

Helper text:
- Explain that only configured institutional email domains can register.
- Explain that college affiliation is assigned after verification.
- Do not present a user-editable college selector.

Behavior:
- Validate required fields and password policy client-side for usability.
- Submit to `POST /auth/register`.
- Show a generic confirmation state after `202 Accepted).
- Do not reveal whether an account already exists.
- Preserve safe form values after recoverable network failure, but clear the password field.

### 8.2 Verification — `/verify-email`

Support token from a verification link or a code-entry flow only if that delivery format is selected for implementation.

States:
- Waiting for token / processing.
- Verification successful.
- Link expired or invalid, with a route to request a new verification message.
- Email already verified.
- Network failure with Retry.

On success:
- Explain that the verified institutional email has assigned the user's college.
- Continue to student onboarding or dashboard.
- Do not ask the user to select their college.

API: `POST /auth/verify-email`.

### 8.3 Login — `/login`

Fields:
- Institutional email.
- Password.
- Show/hide password control.
- Forgot password link.

Behavior:
- Submit to `POST /auth/login`.
- Keep access token in the frontend auth layer's memory.
- Refresh token remains in its HttpOnly cookie.
- Route the user to the intended destination or their default permitted workspace.
- Show one generic invalid-credentials message.
- Provide a distinct unverified-email state with a resend-verification path only once the corresponding API action is specified.

### 8.4 Forgot password — `/forgot-password`

Field:
- Email.

On submit:
- Call `POST /auth/forgot-password`.
- Show a generic "If an eligible account exists, instructions have been sent" state.
- Do not confirm whether the email exists.

### 8.5 Reset password — `/reset-password`

Fields:
- New password.
- Confirm new password.

Token is read from the reset URL and sent to `POST /auth/reset-password`.
States:
- Valid token / form available.
- Successful reset; return to login.
- Invalid or expired token; provide a path to request another reset.
- Server/network error.

### 8.6 Student onboarding — `/student/onboarding`

Keep onboarding short. Collect only profile fields required by the product. The current API baseline permits full name updates and returns the verified college; do not invent additional required profile fields until product and database specifications support them.

---

## 9. Student workspace

### 9.1 Student navigation

- Dashboard
- Discover Events
- My Events
- Profile

### 9.2 Student dashboard — `/student/dashboard`

Suggested layout:
1. Greeting and college label.
2. Upcoming registered events.
3. A small "Explore more events" action.
4. Recently published events.
5. Optional account-verification/profile notice if needed.

Do not add vanity charts or activity metrics to the student dashboard in the MVP.

API:
- `GET /users/me`
- `GET /users/me/registrations`
- `GET /events`

States:
- Loading skeletons.
- Empty upcoming events with an Explore Events action.
- No recent events with a calm empty state.
- Error per section where possible; one failed section should not unnecessarily blank the entire dashboard.

### 9.3 My Events — `/student/my-events`

Use tabs or filters:
- Upcoming (active registrations).
- Past.
- Cancelled.

Each registration item should show:
- Event name.
- Date/time.
- Venue/online label.
- Current registration state.
- View event.
- Cancel registration when allowed.

Re-registration:
- A cancelled registration may show "Register again" when the event is still accepting registrations.
- The UI calls the same registration endpoint; it does not create a new registration resource.
- If full or closed, explain the server response without pretending the action succeeded.

API: `GET /users/me/registrations`, `POST /registrations/{registration_id}/cancel`, `POST /events/{event_id}/registrations`.

### 9.4 Student profile — `/student/profile`

Display:
- Full name.
- Verified email (read-only in v1.0).
- College affiliation (read-only).
- Roles/workspace access as appropriate.
- Account/logout controls.

Only full name is editable under the current API contract. Do not show editable controls for college, role, email verification, or organizer trust.

---

## 10. Organizer workspace

### 10.1 Organizer navigation

- Dashboard
- My Events
- Create Event

Within event management:
- Overview
- Participants
- Revisions (where applicable)

### 10.2 Organizer dashboard — `/organizer/dashboard`

Layout:
- Page title and club/workspace context.
- Small summary cards: Draft, Pending Approval, Published, Completed.
- Upcoming managed events list.
- Recent activity list where the API supplies it.
- Primary "Create event" button.

Do not show metrics for clubs the organizer cannot manage.

API: `GET /organizer/dashboard`.

### 10.3 Managed events — `/organizer/events`

Layout:
- Page title and Create Event action.
- Search.
- Status filters: All, Draft, Pending Approval, Published, Rejected, Cancelled, Completed.
- Optional club filter when organizer belongs to multiple clubs.
- Table on desktop; stacked list/cards on mobile.

Each row/item:
- Event title.
- Club.
- Event date.
- Status badge + text.
- Registration count if returned by API.
- Last updated.
- Manage action.

API: `GET /organizer/events`.

### 10.4 Create event — `/organizer/events/create`

Use one clear form divided into sections rather than a complicated multi-step wizard.

**Section A — Basic information**
- Event title.
- Short summary.
- Full description.
- Category.
- Club (only clubs the organizer can manage).

**Section B — Date and venue**
- Start date/time.
- End date/time.
- Timezone, defaulted from the college.
- In-person / Online selector.
- Venue for in-person events.
- Meeting URL for online events.

**Section C — Registration**
- Registration opening date/time.
- Registration closing date/time.
- Limited capacity toggle.
- Capacity when limited.

**Section D — Eligibility and contact**
- Eligibility notes.
- Contact email.

The last section is required by the PRD but depends on adding `eligibility_notes` and `contact_email` to the database design and API event schemas before implementation. Until that alignment is completed, treat it as a documented schema dependency, not a frontend-only field.

Actions:
- Save Draft.
- Submit for Approval (untrusted organizer).
- Publish Event (trusted publisher).

Show only the action allowed by the user's current organizer permissions and trust state. Do not let the client decide trust status. The backend remains authoritative and can reject a stale or unauthorized action.

Validation:
- Show field-level errors beside the field.
- Validate start/end and registration window relationships.
- Require venue or meeting URL according to event type.
- Explain unlimited capacity when no limit is set.
- Prevent double submission while request is in progress.
- Confirm success with the resulting event status.

API:
- `POST /events`
- `PATCH /events/{event_id}`
- `POST /events/{event_id}/submit`
- `POST /events/{event_id}/publish`

### 10.5 Manage event — `/organizer/events/[eventId]`

Header:
- Event title.
- Status.
- Club name.
- Event date.
- Main actions allowed by current state.

Tabs/sections:
- Overview: approved event details and registration summary.
- Participants: link to participant management.
- Revisions: pending and past material edit proposals.

State-dependent actions:
- DRAFT / REJECTED: Edit, Save Draft, Submit for Approval or Publish if trusted.
- PENDING_APPROVAL: View submitted details and approval status; do not allow a second submission.
- PUBLISHED / REGISTRATION_CLOSED / ONGOING: View current approved version, Submit Material Revision, Cancel Event.
- COMPLETED / CANCELLED: Read-only event history, subject to permitted access.

Approved event content cannot be directly modified through PATCH. Material changes use the revision form and are not reflected publicly until an admin approves them.

### 10.6 Event revision form

Use the same field groups as the event form. Prepopulate all editable fields from the current approved event.

Show:
- Current approved version.
- Proposed version preview or changed-field summary.
- Base content version used by the proposal.
- Notice that the currently published event remains visible until approval.
- Submit Revision action.

Disable resubmission while a revision is already pending. Show the reviewer decision and reason when available.

API: `POST /events/{event_id}/revisions`, `GET /organizer/events/{event_id}/revisions`.

### 10.7 Participants — `/organizer/events/[eventId]/participants`

Layout:
- Event name and event date.
- Active registration count / capacity when supplied.
- Search by participant name or institutional email.
- Status filter: Registered / Cancelled.
- Paginated participant table on desktop.
- Stacked participant cards on mobile.
- Export CSV action.

Participant fields:
- Student name.
- Institutional email.
- Registration status.
- Registration timestamp.

Privacy:
- Show participant data only after the API authorizes the organizer for this event.
- Do not expose participant details in public event pages or general search.
- Require confirmation before exporting if the download includes personal data.
- Explain that downloaded participant data should be used only for event operations.

API: `GET /events/{event_id}/registrations`, `GET /organizer/events/{event_id}/export`.

---

## 11. College administrator workspace

### 11.1 College-admin navigation

- Dashboard
- Approvals
- Organizers
- College Settings

### 11.2 Admin dashboard — `/college-admin/dashboard`

Layout:
- College name and admin workspace label.
- Pending initial event approvals.
- Pending event revisions.
- Published/upcoming event overview.
- Organizer count and trust overview.
- Recent administrative activity where available.

Use simple counts and lists. Avoid elaborate analytics in v1.0.

### 11.3 Approvals — `/college-admin/approvals`

Provide two tabs:
- New Event Submissions.
- Event Revisions.

For each queue, show:
- Event title.
- Club and submitting organizer.
- Submission date.
- Proposed event date.
- Current status.

Review layout:
- Event details in the main panel.
- Organizer/club context in a side panel or top metadata row.
- Approve and Reject actions grouped clearly.
- Require a rejection reason.
- Allow an optional approval comment.
- Show a confirmation step before making a decision.
- On success, remove the item from the pending queue and show a confirmation message.

For revisions, show current approved values beside proposed values for important fields such as date/time, venue, capacity, and description. Do not require an administrator to compare raw JSON.

API:
- `GET /admin/events/pending`
- `POST /admin/events/{event_id}/approve`
- `POST /admin/events/{event_id}/reject`
- `GET /admin/event-revisions/pending`
- `POST /admin/event-revisions/{revision_id}/approve`
- `POST /admin/event-revisions/{revision_id}/reject`

### 11.4 Organizers — `/college-admin/organizers`

Layout:
- Search by name/email.
- Filter by club and trusted status.
- List organizer name, email, club, membership role, and trust status.
- Add Organizer action.

Add Organizer flow:
1. Search/select an existing verified student in the college.
2. Select a club.
3. Select membership role: Owner, Editor, or Viewer.
4. Confirm grant.

Trust management:
- Display trusted status separately from organizer role and club membership.
- Provide a deliberate Grant Trust / Revoke Trust action.
- Ask for confirmation and optional explanatory note.
- Explain that trusted status allows direct initial publishing but does not bypass review for material edits to approved events.

API:
- `GET /admin/organizers`
- `POST /admin/organizers`
- `POST /admin/organizers/{organizer_id}/trust`

### 11.5 College settings — `/college-admin/settings`

Initial view can display read-only college details and configured email domain information if the relevant API is available. The current API baseline does not define college-settings read/update routes. Do not build editable controls that cannot be persisted. Add settings-management APIs only after requirements are agreed.

---

## 12. Reusable component inventory

Build reusable components instead of styling every screen independently.

| Component | Purpose | Key states / variants |
|---|---|---|
| `AppHeader` | Public and authenticated top navigation | Public, signed-in, mobile |
| `WorkspaceSidebar` | Role-aware dashboard navigation | Student, organizer, college admin |
| `WorkspaceSwitcher` | Change between permitted workspaces | Hidden, one role, multiple roles |
| `PageHeader` | Page title, description, main action | With/without action |
| `EventCard` | Public event discovery item | Image/fallback, full/closed/open |
| `EventStatusBadge` | Lifecycle status | Draft, pending, published, rejected, cancelled, completed |
| `RegistrationStatus` | Student registration state | Registered, cancelled |
| `FilterBar` | Search, categories, date, availability | Desktop, mobile drawer |
| `SearchInput` | Search field | Idle, active, loading, clear |
| `FormField` | Label, input, hint, error | Default, focused, invalid, disabled |
| `DateTimeField` | Date/time and timezone entry | Empty, selected, invalid |
| `SelectField` | Category, club, and status selections | Loading, empty, invalid |
| `CapacityField` | Unlimited/limited capacity | Unlimited, limited, full |
| `EmptyState` | No results or no data | Context-specific message/action |
| `ErrorState` | Failed query/action | Retry, recover, contact support |
| `LoadingSkeleton` | Non-blocking loading placeholder | Card, list, table, panel |
| `ConfirmDialog` | Destructive or irreversible action | Cancel event, cancel registration, approve/reject |
| `Toast` / inline feedback | Operation result | Success, warning, error, info |
| `DataTable` | Organizer/admin data | Loading, empty, populated, mobile alternative |
| `Pagination` | Collection navigation | Disabled first/last, current page |
| `ApprovalDecisionPanel` | Review event submission/revision | Pending, processing, decided |
| `RevisionDiff` | Current vs proposed event values | Added, changed, unchanged |
| `StatusTimeline` | Event or registration history | Current state and previous changes |
| `UserMenu` | Profile, workspace, logout | Open, closed |
| `FileDownloadAction` | Participant CSV export | Idle, downloading, error |

Components must have typed props and a single source of truth for status labels and permitted actions.

---

## 13. Forms and validation behavior

### 13.1 General form rules

- Use visible labels; placeholders are examples, not labels.
- Mark required fields clearly.
- Show validation beside the relevant field.
- Validate on submit and, after the first error, revalidate as the user corrects input.
- Keep server validation authoritative.
- Preserve non-sensitive inputs after recoverable failures.
- Clear password fields after submission failures.
- Disable submit buttons while the request is in flight.
- Prevent duplicate form submissions.
- Focus the first invalid field after server or client validation.
- Announce important success and error messages to assistive technology.

### 13.2 Error mapping

Map API error codes to actionable user-facing copy. Examples:

| API error | UI treatment |
|---|---|
| `INVALID_CREDENTIALS` | "Email or password is incorrect." |
| `EMAIL_VERIFICATION_REQUIRED` | Prompt to verify email and show resend path if implemented |
| `REGISTRATION_NOT_OPEN` | "Registration has not opened yet." |
| `REGISTRATION_CLOSED` | "Registration for this event has closed." |
| `EVENT_CAPACITY_REACHED` | "This event is full." |
| `ALREADY_REGISTERED` | Refresh registration state and show "You're already registered." |
| `CANCELLATION_NOT_ALLOWED` | Explain that cancellation is no longer available |
| `REVISION_ALREADY_PENDING` | Link to the existing pending revision |
| `STALE_CONTENT_VERSION` | Ask organizer to reload the latest approved event before creating another revision |
| `CAPACITY_BELOW_REGISTERED_COUNT` | Explain that the proposed capacity is below existing registrations |
| `RATE_LIMITED` | Explain that the user should retry later without exposing throttling internals |
| `RESOURCE_NOT_FOUND` | Show a safe not-found page or return to the list |

Never display raw server exception text.

### 13.3 Success feedback

- Use an inline confirmation for significant workflows such as event submission, event approval, revision approval, and organizer grant.
- Use a small toast for routine saves or status updates.
- Refresh or invalidate affected query data after successful mutations.
- Do not show a successful state until the backend confirms the operation.

---

## 14. Loading, empty, error, and status patterns

Every page that fetches data must define all of these states.

| State | Expected presentation |
|---|---|
| Loading | Skeleton shaped like the expected content; avoid blank screen |
| Empty | Explain why the list is empty and provide one relevant next action |
| Error | Plain-language message, Retry action, preserve filters and form values where safe |
| Success | Updated server-confirmed state |
| Permission denied | Access-denied page or safe navigation; do not render protected data |
| Not found | A simple not-found message and link back to a safe parent page |
| Offline/network failure | Explain that the request did not complete; do not assume a write failed if the outcome is ambiguous |

Status labels should be consistent throughout the application:

| Domain state | Label | Visual treatment |
|---|---|---|
| `DRAFT` | Draft | Neutral |
| `PENDING_APPROVAL` | Pending approval | Warning |
| `PUBLISHED` | Published | Success |
| `REGISTRATION_CLOSED` | Registration closed | Neutral |
| `ONGOING` | Ongoing | Informational |
| `COMPLETED` | Completed | Neutral |
| `REJECTED` | Rejected | Danger |
| `CANCELLED` | Cancelled | Danger |
| `REGISTERED` | Registered | Success |
| `CANCELLED` registration | Registration cancelled | Neutral/danger with clear text |

Do not conflate event status and registration status. They describe different resources.

---

## 15. Responsive behavior

Use three broad layout ranges as starting points; refine with actual content testing.

| Layout | Width | Behavior |
|---|---:|---|
| Mobile | below 640 px | Single column, compact header, drawers, stacked cards |
| Tablet | 640–1023 px | One or two columns, collapsible sidebar, simplified tables |
| Desktop | 1024 px and above | Sidebar workspace, multi-column event grid, full tables |

### 15.1 Mobile-specific requirements

- Touch targets should be at least 44 by 44 CSS pixels where practical.
- Keep main actions visible without requiring precise hover interaction.
- Forms use full-width fields.
- Event cards stack vertically.
- Data tables become stacked rows/cards or use intentional horizontal scrolling with clear affordance.
- Confirmation dialogs should fit within the viewport and be keyboard accessible.
- Avoid sticky bottom actions that cover page content or browser controls.
- Date/time input must remain usable on common mobile browsers.

### 15.2 Tablet and desktop

- Use a collapsible sidebar or drawer at tablet widths.
- Keep form content at a readable maximum width.
- Use side-by-side panels only when each remains wide enough to scan.
- Keep table filters and pagination aligned and predictable.

---

## 16. Accessibility and usability requirements

- Use semantic landmarks: header, nav, main, aside, footer.
- Provide a visible keyboard focus indicator.
- Ensure all actions can be performed without a mouse.
- Use descriptive link and button labels; avoid repeated generic "Click here".
- Associate form labels, hints, and errors programmatically.
- Announce dynamic success/error feedback with suitable live regions.
- Use sufficient color contrast for normal and large text.
- Do not rely on color alone for status or validation.
- Give meaningful alt text to informative event images; decorative images use empty alt text.
- Give accessible names to icon-only buttons.
- Dialogs must manage focus and return it to the triggering element when closed.
- Respect reduced-motion preferences.
- Test zoom to 200% and common mobile viewport sizes without loss of essential functionality.

---

## 17. Frontend architecture and API integration

### 17.1 Suggested frontend structure

The exact implementation structure may evolve, but maintain separation between routes, shared components, and API access.

~~~text
frontend/
  app/
    (public)/
      page.tsx
      events/
      login/
      register/
      verify-email/
      forgot-password/
      reset-password/
    (student)/
      student/
    (organizer)/
      organizer/
    (college-admin)/
      college-admin/
  components/
    layout/
    events/
    forms/
    feedback/
    tables/
  features/
    auth/
    events/
    registrations/
    organizer/
    admin/
  lib/
    api/
    auth/
    validation/
    utils/
  types/
~~~

### 17.2 API client responsibilities

- Keep the base URL in environment configuration.
- Add access-token authorization to protected requests.
- Handle refresh-token flow without exposing the refresh token to JavaScript.
- Normalize API errors into typed frontend errors.
- Apply request cancellation where a component unmounts or search input changes.
- Use a consistent query/cache strategy for list and detail data.
- Invalidate or refresh event, registration, participant, and dashboard data after successful mutations.
- Avoid optimistic updates for high-impact actions such as event approval, event revision approval, and capacity-limited registration unless rollback behavior is fully tested.

### 17.3 Server is authoritative

The frontend may hide actions based on the user's roles and returned resource state for usability. It must still handle `401`, `403`, `404`, and `409` responses because permissions, event status, or capacity can change after the page loads.

---

## 18. Screen-to-API mapping

| Screen / interaction | API operations |
|---|---|
| Home | `GET /events` |
| Event discovery | `GET /event-categories`, `GET /events` |
| Event detail | `GET /events/{event_id}` |
| Student registration | `POST /auth/register` |
| Email verification | `POST /auth/verify-email` |
| Login / logout | `POST /auth/login`, `POST /auth/logout` |
| Refresh session | `POST /auth/refresh` |
| Forgot/reset password | `POST /auth/forgot-password`, `POST /auth/reset-password` |
| Profile | `GET /users/me`, `PATCH /users/me` |
| My Events | `GET /users/me/registrations` |
| Registration / re-registration | `POST /events/{event_id}/registrations` |
| Cancel registration | `POST /registrations/{registration_id}/cancel` |
| Organizer dashboard | `GET /organizer/dashboard` |
| Managed events | `GET /organizer/events` |
| Create/edit event | `POST /events`, `PATCH /events/{event_id}` |
| Submit / direct publish | `POST /events/{event_id}/submit`, `POST /events/{event_id}/publish` |
| Cancel event | `POST /events/{event_id}/cancel` |
| Submit event revision | `POST /events/{event_id}/revisions` |
| Organizer revision history | `GET /organizer/events/{event_id}/revisions` |
| Participants / export | `GET /events/{event_id}/registrations`, `GET /organizer/events/{event_id}/export` |
| Admin approval queue | `GET /admin/events/pending` |
| Initial event approval/rejection | `POST /admin/events/{event_id}/approve`, `POST /admin/events/{event_id}/reject` |
| Revision approval queue | `GET /admin/event-revisions/pending` |
| Revision approval/rejection | `POST /admin/event-revisions/{revision_id}/approve`, `POST /admin/event-revisions/{revision_id}/reject` |
| Organizer management | `GET /admin/organizers`, `POST /admin/organizers` |
| Trust management | `POST /admin/organizers/{organizer_id}/trust` |

---

## 19. Content and product gaps to resolve

Do not silently build UI around fields or policies that are not yet aligned across the product documents.

| Item | Current treatment | Follow-up |
|---|---|---|
| Eligibility and event contact information | Included in the event form design because the PRD requires it | Add `eligibility_notes` and `contact_email` to Database Design and API contracts, or explicitly remove from MVP |
| Event cancellation cutoff | UI follows the backend's returned eligibility/error state | Confirm the proposed "until event start" policy before implementing cancellation controls |
| Organizer membership revocation | Not yet fully specified by the API | Define an admin action and endpoint before building organizer offboarding UI |
| College settings editing | Read-only/omitted because no settings API exists | Define college settings APIs before enabling edit controls |
| Verification resend | UI may offer the action only after an endpoint is added | Specify resend-verification endpoint and rate limit |
| Platform-admin workspace | Not part of the MVP UI | Design only when platform operations are in scope |
| Event imagery | Optional visual in card/detail | Define upload/storage API and image moderation before making uploads a required field |

---

## 20. Implementation sequence

Build the frontend in small vertical slices so every screen can be exercised against a working API.

1. **Foundation:** design tokens, typography, buttons, inputs, status badges, responsive shell, navigation.
2. **Public discovery:** home, event list, filters, event detail, loading/empty/error states.
3. **Authentication:** registration, verification, login, refresh handling, logout, password reset.
4. **Student workspace:** dashboard, My Events, profile, registration and cancellation states.
5. **Organizer workspace:** dashboard, managed events, create/edit form, publish/submit flow.
6. **Participant management:** participant table, mobile layout, CSV export.
7. **College administration:** approval queue, revision comparison, organizer assignment, trust management.
8. **Accessibility and responsive pass:** keyboard, screen readers, contrast, zoom, mobile/tablet testing.
9. **Usability testing:** test the major journeys with a small group of students and organizers; revise based on observed friction.

### 20.1 MVP frontend acceptance checklist

- [ ] Visitors can browse and view published event information without logging in.
- [ ] Search and filters work and survive refresh/share through URL query parameters.
- [ ] Registration directs visitors to authentication and returns them to the intended event where possible.
- [ ] Unverified users are clearly guided through email verification.
- [ ] Student can see their upcoming, past, and cancelled registrations.
- [ ] Re-registration reuses the existing registration and reflects the API-confirmed result.
- [ ] Organizer can create a draft and sees only actions allowed by their current trust state.
- [ ] Untrusted organizer can submit for approval; trusted organizer can directly publish a new event.
- [ ] Published event content is not changed publicly while a material revision is pending.
- [ ] College admin can review new submissions and event revisions.
- [ ] Participant data is visible only to authorized organizers/admins.
- [ ] CSV export has a clear privacy warning and safe download behavior.
- [ ] Every data screen has loading, empty, and error states.
- [ ] Essential actions are keyboard accessible and usable on mobile.
- [ ] Frontend never treats hidden buttons or client-side role checks as security.

---

**Next step:** Review and resolve the remaining product/data contract gaps, then establish the frontend project foundation and implement the public event-discovery vertical slice.
