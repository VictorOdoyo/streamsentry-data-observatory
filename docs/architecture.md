# Architecture

## Boundaries

StreamSentry uses explicit dependency direction:

```text
React console -> versioned HTTP API -> application services -> store protocol
                                      -> policy evaluators
```

Domain records do not import FastAPI, SQLAlchemy, or frontend concepts. Services own workflows and state transitions. Routes translate HTTP requests into service calls and expose domain records as JSON.

## Application State

The API factory creates a service container around a store, clock, and identifier factory. Production defaults use a system clock and random identifiers. Tests inject a frozen clock and sequential identifiers, keeping state transitions deterministic.

The seeded Northstar workspace is fictional and loaded on process start. This keeps local startup immediate while still presenting connected datasets, checks, runs, incidents, lineage, SLOs, and costs.

## Quality Execution

Each check delegates to a small evaluator selected by check type. Evaluators are pure: the same policy, observation, and evaluation time produce the same result. The run service records the outcome and updates dataset health only for executed checks; disabled checks remain skipped and do not alter dataset state.

## Incident State Machine

Incidents follow guarded transitions:

```text
open -> investigating -> monitoring -> resolved
  |           |             |
  +-----------+-------------+-> resolved
```

Resolved incidents cannot be reopened through the current contract. This makes accidental state regression visible instead of silently accepting it.

## Storage

`MemoryStore` is the runnable default and implements the complete store protocol with workspace isolation, deterministic ordering, and lock-protected mutations. `SessionFactory` provides a transaction-scoped SQLAlchemy boundary, and `migrations/001_initial.sql` documents the normalized relational model and operational indexes.

A production persistence adapter can implement the existing protocol without changing evaluators, services, or route contracts.

## Frontend

The console fetches independent workspace resources concurrently after discovering the active workspace. It models loading, ready, and failure as an explicit state union. Views consume one typed observatory snapshot and keep local interaction state such as filters, selected incidents, lineage focus, and dataset details.
