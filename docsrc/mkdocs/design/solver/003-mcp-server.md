# Feature 003: MCP Server

Tools: `resolve_location`, `get_od_cost`, `find_nearest`, `get_reachable_h3_cells`, `get_od_matrix`, and `describe_dataset`.

Expose `max_k`, stretch-distance cutoff, stretch-time cutoff, speed, distance method, and endpoint-selection policy. Return requested and solved cells, endpoint `k`, approximate H3 distance, optional exact centroid distance, inferred time, network metrics, combined metrics, warnings, and provenance.

Validate schemas and enforce server limits before expansion or scanning. Prefer configured dataset aliases, suppress stack traces/local paths, and state in tool descriptions that off-network stretch is estimated and distinct from the network solve.
