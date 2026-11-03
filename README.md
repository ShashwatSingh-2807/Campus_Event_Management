# CampusLoop

A college event discovery, registration, and management platform, starting with a pilot at **NIE Mysuru**.

CampusLoop aims to give students one reliable place to discover campus events and register, while helping clubs and college administrators publish events and manage participation.

## Current status

**Phase:** Product definition and technical planning

The initial product requirements and architecture are documented. Application code has not been implemented yet.

## Documentation

| Document | Purpose |
|---|---|
| [Product Requirements Document](docs/01_PRD.md) | Product vision, users, scope, requirements, business rules, and success metrics |
| [Technical Requirements Document](docs/02_TRD.md) | Architecture, stack, backend modules, APIs, security, and engineering standards |
| [Application Flow](docs/03_APPLICATION_FLOW.md) | Routes, screens, permissions, and user journeys |
| [Database Design](docs/04_DATABASE_DESIGN.md) | Entities, relationships, constraints, indexes, and transaction rules |
| [Documentation Index](docs/README.md) | Documentation map and planned next documents |

## Planned technology

- **Web:** Next.js, TypeScript, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, SQLAlchemy, Alembic
- **API:** REST, versioned under `/api/v1`
- **Infrastructure:** Docker; Redis and background workers when justified

The initial architecture is a modular monolith. A future mobile application is expected to use the same backend APIs.

## Initial pilot

The first deployment is intended for NIE Mysuru. Initial validation targets:

- 3 clubs onboarded
- 10 events published
- 300 student registrations
- 5 active organizers

These are pilot targets, not achieved results.

## Development approach

The project will be built incrementally:

1. Finalize product and technical specifications.
2. Design and validate the database schema.
3. Define API contracts.
4. Implement authentication, authorization, and core event workflows.
5. Build the responsive web application.
6. Test with a small campus pilot and iterate.

## Project principles

- Keep the first release focused on a single-college pilot.
- Enforce authorization on the backend, not only in the UI.
- Treat organizer privileges and trusted-publisher status as separate concepts.
- Protect registration capacity with database transactions and constraints.
- Prefer a maintainable modular monolith over premature microservices.

## Disclaimer

CampusLoop is a working project name and has not been trademark-validated. Product scope and technical decisions may evolve as implementation and pilot feedback provide evidence.
