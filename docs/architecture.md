# Architecture and trust model

The factory separates evidence ingestion, deterministic analysis and authorized execution.

1. Read-only connectors import governed deal-room, CMDB, cloud, identity and contract evidence.
2. Normalization maps assets to legal entities, business capabilities, owners and dependencies.
3. Deterministic engines calculate readiness, TSA exposure, identity risk and economics.
4. Agents may summarize gaps and propose plans but cannot approve their own conclusions.
5. Legal, finance, security and asset owners approve the transaction perimeter and execution wave.
6. Scoped automation performs changes with idempotency, rollback and protected audit evidence.

Production deployments require data-room access controls, encryption, residency enforcement, legal holds, separation of duties and an authenticated evidence chain.

