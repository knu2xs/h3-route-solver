# Feature 001: Resolve Inputs to Solvable Cells

## Requirements

1. Accept WGS84 coordinates and H3 integer/hex identifiers.
2. Normalize to canonical resolution.
3. Return a solvable canonical cell immediately with `grid_k=0`.
4. Otherwise expand safe H3 disks/rings until solvable candidates appear or the budget expires.
5. Support `max_k`, metric distance, and speed/time limits.
6. Estimate initial `k` using average edge length and the declared center-spacing factor.
7. Verify candidates against the configured H3-derived or exact centroid metric.
8. Handle pentagon distortion and grid-distance errors explicitly.
9. Retain all minimum-ring ties for deterministic downstream selection.
10. Enforce server maximum `k` and candidate count.
11. Return `grid_k`, estimated distance, optional exact centroid distance, inferred time, cutoff, and approximation metadata.

## Selection

- `nearest_grid`: minimum `k`, then metric distance, then H3 ID.
- `nearest_metric`: minimum metric distance in the bounded candidate set.
- `minimum_combined_cost`: evaluate bounded endpoint candidates and available OD rows to minimize total estimated cost.

No H3-derived metric may be labeled exact physical distance.
