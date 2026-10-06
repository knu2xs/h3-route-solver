# Feature 002: Sparse OD and Proximity API

Expose `resolve_location`, `od_cost`, `nearest`, `reachable`, and `matrix`.

## Requirements

- Resolve arbitrary endpoints to solvable cells before OD lookup.
- Keep origin stretch, network cost, and destination stretch in separate fields.
- Provide clearly named combined estimates only when units/policies permit addition.
- Require an explicit/default speed for time-derived stretch.
- Allow asymmetric endpoint policies.
- Support bounded multi-candidate endpoint resolution to avoid a nearest-grid cell with a missing or poor network path.
- Read only required solved-origin partitions and columns.
- Distinguish no nearby solvable cell, missing pair, unreachable pair, and network-cutoff exclusion.
- Never substitute straight-line routing for a missing OD row.
- Return deterministic ordering and dataset/policy provenance.

Changing a stretch policy may change chosen endpoint cells but must not alter stored OD facts.
