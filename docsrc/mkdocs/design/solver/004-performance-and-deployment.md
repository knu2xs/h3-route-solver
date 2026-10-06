# Feature 004: Performance and Deployment

Cache manifests, solved-cell membership, and hot origin partitions by dataset version. Use lazy scanning, projection, partition pruning, and bounded in-memory results. Abstract filesystem access for later object storage. Provide `describe`, `validate`, `resolve`, `lookup`, `nearest`, and `reachable` CLI commands.

Benchmarks record dataset size, partitions, `k`, candidates evaluated, rows/bytes read, and latency for cold/warm resolution, OD, nearest, reachable, and matrix operations. The package must install and run without ArcPy.
