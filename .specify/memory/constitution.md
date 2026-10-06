<!--
Sync Impact Report
- Version change: (template) -> 1.0.0
- Ratified from: h3-route-solver-specs/01-shared-constitution.md (shared principles I-X)
  plus solver-specific principles XI-XV.
- Added sections: Core Principles, Solver Principles, Technology Constraints,
  Development Workflow & Quality Gates, Governance.
- Templates reviewed: .specify/templates/plan-template.md (Constitution Check gate applies),
  spec-template.md, tasks-template.md - no structural changes required.
- Follow-up TODOs: resolve open clarifications listed in docsrc/mkdocs/design/10-roadmap.md
  via /speckit-clarify before the first /speckit-plan.
-->

# H3 Route Solver Constitution

The H3 Route Solver is the ArcPy-free half of a two-project system. It is a pip-installable Python
library, CLI, and MCP server that answers origin-destination (OD) and proximity queries against
the sparse H3 dataset published by
[h3-route-data-builder](https://github.com/knu2xs/h3-route-data-builder). Principles I-X are
shared in intent with the builder; principles XI-XV apply to this project only.

## Core Principles (Shared)

### I. Explicit Semantics

Every behavior-affecting choice MUST be an explicit parameter or documented default, never an
implicit constant: H3 resolution, network cutoff, stretch cutoffs (`max_k`,
`max_stretch_distance_m`, `max_stretch_time_s`), `stretch_speed_mps`, distance method,
endpoint-selection policy, units, and tie-breaking.

- Defaults MUST be echoed back in every response's policy/provenance fields.
- Units MUST be explicit in field and parameter names (`_m`, `_s`, `_mps`).

*Rationale:* callers, including LLM agents, must see exactly which assumptions produced a result.

### II. ArcPy Isolation (NON-NEGOTIABLE)

The solver MUST NOT require ArcPy. Importing `h3_route_solver` or any of its submodules MUST NOT
load `arcpy`, enforced by a test that checks `sys.modules`. Template utilities with guarded
optional ArcPy imports are tolerated but MUST NOT be used by solver features.

*Rationale:* the solver must run anywhere Python runs: servers, containers, notebooks, CI.

### III. Sparse Correctness

Only cells with `eligibility_status=solvable` in the dataset are endpoints for OD lookup.
Unsolved inputs MUST be resolved to solvable cells before lookup; the solver MUST NOT fabricate
OD facts for non-solvable cells.

*Rationale:* the dataset is sparse by design; pretending otherwise produces fictitious costs.

### IV. Immutable Reproducibility

The solver reads published datasets and never writes to them. Every response MUST carry the
dataset version and build fingerprint from the manifest, and identical inputs against the same
dataset MUST return identical results.

*Rationale:* answers must be traceable to the exact data and policy that produced them.

### V. Idempotent, Side-Effect-Free Queries

Queries are pure functions of (dataset, inputs, policy). Caches MUST be keyed by dataset
fingerprint and MUST NOT change results. Changing a stretch policy may change chosen endpoint
cells but MUST NOT alter stored OD facts.

*Rationale:* safe to retry, cache, and parallelize.

### VI. Approximation Transparency (NON-NEGOTIABLE)

Origin stretch, network cost, and destination stretch MUST be returned as separate fields.
H3-derived stretch distance and speed-derived stretch time are always labeled estimates.
Combined totals are provided only when units and policies permit addition and are clearly named.
Stretch time is null unless a speed is supplied or configured. The solver MUST NEVER substitute
straight-line distance for a missing OD row.

*Rationale:* the core value of the system is honest separation of solved and estimated cost.

### VII. Bounded Execution

All ring expansion, candidate evaluation, partition reads, and outputs (matrix size, reachable
set size, candidate count) have enforced limits. The strictest supplied bound wins. Exceeding a
server limit returns a structured error, never a truncated silent result.

*Rationale:* protects latency, memory, and MCP clients from runaway queries.

### VIII. Interoperability

The solver MUST read datasets that validate against the shared data contract and selected
GeoParquet specification, using PyArrow/DuckDB, and MUST reject datasets with an incompatible
contract version with a `dataset_error` status.

*Rationale:* the builder and solver evolve in separate repos; the contract is the boundary.

### IX. Observable Operation

Structured logs (via `get_logger`) record query type, policy, dataset fingerprint, partitions
read, and timing. Responses distinguish `invalid_input`, `no_solvable_cell_within_cutoff`,
`not_built`, `unreachable`, `outside_network_cutoff`, and `dataset_error`.

*Rationale:* every non-answer must say why.

### X. Testable Contracts

Every requirement has acceptance coverage. The public Python API, CLI, and MCP tool schemas are
contracts with tests; the shared data contract (`docsrc/mkdocs/design/03-data-contract.md`)
MUST be exercised by fixture datasets.

*Rationale:* the two projects evolve independently; tests are the only enforceable boundary.

## Solver Principles

### XI. Library-First, Pip-Installable

All functionality lives in the `h3_route_solver` package and is installable with
`pip install h3-route-solver` (or from git). The CLI and MCP server are thin adapters over the
same library API. Optional integrations (MCP, GeoPandas) are pip extras, not core requirements.

### XII. Stable Public API

The public surface (`resolve_location`, `od_cost`, `nearest`, `reachable`, `matrix`, CLI
commands, MCP tools) follows semantic versioning. Breaking changes require a MAJOR version bump
and a migration note.

### XIII. Bounded, Deterministic Stretch Resolution

Input normalization and stretch resolution use safe H3 grid traversal with pentagon handling,
estimate initial `k` from average edge length, verify candidates against the configured stretch
metric, retain minimum-ring ties, and order results deterministically.

### XIV. Read Only What Is Needed

Queries MUST use manifest-driven partition pruning and column projection, reading only the
solved-origin partitions and columns required. Storage access goes through a filesystem
abstraction so local and object storage behave identically.

### XV. Safe MCP Surface

MCP tools validate input schemas, enforce server-side limits, return separated metrics with
provenance, suppress stack traces and filesystem paths, and label off-network stretch as
estimated.

## Technology Constraints

- Python `>=3.10`; no ArcPy dependency at install or import time.
- Core runtime dependencies: `h3` (v4 API), `pyarrow`, `duckdb`, `pandas`, `pyyaml`.
- Optional extras: `mcp` (MCP server), `geo` (GeoPandas output), `dev` (testing).
- `src/` layout; package `h3_route_solver`; build backend setuptools via `pyproject.toml`.
- Adding a core dependency MUST be flagged in the plan and justified; prefer extras.

## Development Workflow & Quality Gates

- Features follow spec-kit: `/speckit-specify` -> `/speckit-clarify` -> `/speckit-plan` ->
  `/speckit-tasks` -> `/speckit-analyze` -> `/speckit-implement`.
- Feature order follows `docsrc/mkdocs/design/10-roadmap.md` phases 5-7.
- Every plan MUST pass a Constitution Check against principles I-XV before research and again
  after design; violations require a recorded justification in the plan's Complexity Tracking.
- Tests are written with or before implementation; `make test` MUST pass before merge, and the
  package MUST install and import in a clean virtual environment without ArcGIS.
- Performance-sensitive features include benchmarks (latency/throughput) per
  `docsrc/mkdocs/design/solver/004-performance-and-deployment.md`.
- Code follows `AGENTS.md` conventions (black, type hints, Google docstrings, `pathlib`,
  module-level loggers).

## Governance

- This constitution supersedes other practice documents; `AGENTS.md` provides runtime coding
  guidance subordinate to it.
- Principles I-X are shared with `h3-route-data-builder`. Amending a shared principle MUST be
  mirrored in the builder constitution in the same release cycle.
- Amendments require a pull request describing the change, rationale, and migration impact, and
  updating dependent templates and docs.
- Versioning: MAJOR for removed/redefined principles, MINOR for added principles or materially
  expanded guidance, PATCH for clarifications.
- Reviews MUST verify compliance; unjustified complexity is rejected.

**Version**: 1.0.0 | **Ratified**: 2026-10-06 | **Last Amended**: 2026-10-06
