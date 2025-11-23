### PART 1: 5 Examples of Fundamental Principle Conflicts in System Design

1. **Latency vs Consistency (CAP theorem interpreted through physics)**
   - **Principle 1**: Speed-of-light delay (c ≈ 300,000 km/s) and Shannon’s channel capacity suggest minimizing round-trip distance and using low-latency links to achieve near-instantaneous response.
   - **Principle 2**: Second law of thermodynamics (entropy never decreases) + Brewer’s CAP theorem interpreted physically: perfect consistency requires global ordering of events, which demands information propagation across all nodes → bounded by light-speed latency.
   - **Conflict**: You cannot have both zero-latency reads and perfect linearizability across geographically distributed nodes; information cannot travel faster than light.
   - **Trade-off Analysis**: Choose two of {C, A, P} because the third is bounded by physics. In practice: accept eventual consistency (relax C) for low latency, or accept higher latency (relax low-L) for strong consistency, or partition the system (relax A).
   - **Real-world constraint**: Earth’s circumference and undersea cable routes (minimum ~100–200 ms coast-to-coast light-speed RTT).

2. **Caching vs Memory Pressure**
   - **Principle 1**: Amdahl’s law and locality of reference suggest aggressive caching of hot data to maximize hit rate and throughput.
   - **Principle 2**: Conservation of memory (finite DRAM particles) → total cached objects ≤ physical RAM / average object size.
   - **Conflict**: Infinite cache size is impossible; evicting too aggressively destroys hit rate, keeping everything causes OOM.
   - **Trade-off Analysis**: Apply least-frequently-used or least-recently-used eviction (information-theory optimal under Zipf-like workloads) and size cache to working set bounded by available memory minus OS/resident set overhead.
   - **Real-world constraint**: DRAM density and cost; you cannot buy infinite RAM at finite price and power.

3. **Connection Pooling vs Response Time**
   - **Principle 1**: Little’s Law (L = λ × W) suggests large pool size to keep queueing delay low under bursty traffic.
   - **Principle 2**: Database/server has finite thread/CPU resources; each open connection consumes non-trivial memory and file descriptors on both client and server (conservation of resources).
   - **Conflict**: Pool too small → queueing delay explodes; pool too large → server resource exhaustion → per-connection latency explodes.
   - **Trade-off Analysis**: Set pool size ≈ (target latency × peak request rate) / average DB service time, with circuit breakers and back-pressure to protect server.
   - **Real-world constraint**: OS file-descriptor limits (ulimit), database max_connections, and per-connection memory (~10–30 MB for PostgreSQL/MySQL).

4. **Batching vs Latency**
   - **Principle 1**: Throughput scales with batch size (amortize fixed costs: network headers, disk seek, CPU pipeline flush).
   - **Principle 2**: Little’s Law again: average latency = batch interval / 2 + processing time per batch.
   - **Conflict**: Larger batches → higher throughput but linearly higher p99 latency.
   - **Trade-off Analysis**: Use coalescing with dynamic timeout + size trigger (e.g., flush when 1 MB or 5 ms elapsed, whichever comes first) to bound worst-case latency while retaining most throughput gains.
   - **Real-world constraint**: Tail-latency-sensitive workloads (human-facing services need p99 < 100 ms).

5. **Compression vs CPU Utilization**
   - **Principle 1**: Shannon entropy says compressible data can be reduced dramatically → lower network I/O and storage.
   - **Principle 2**: Data processing inequality + thermodynamics of computation (Landauer limit ~kT ln 2 joules per irreversible bit operation) → decompression costs real CPU cycles and energy.
   - **Conflict**: Higher compression ratio needs more complex algorithm → more CPU per byte.
   - **Trade-off Analysis**: Choose compression level where marginal network savings = marginal CPU cost (often zstd level 3–5 or Brotli 4–6 for web).
   - **Real-world constraint**: Battery life on mobile devices and thermal throttling on densely packed servers.

### PART 2: 10 Distributed System Failure Scenarios Violating Physical/Mathematical Principles

1. **Scenario**: Message queue backlog growing without bound  
   **Broken Principle**: Conservation of mass (messages in − messages out > 0)  
   **Signature**: Lag increasing ~linearly over hours/days (10k → 100k → 1M messages)  
   **Diagnosis**: Producer rate (5,000 msg/s) > consumer processing capacity (3,000 msg/s) → accumulation rate 2,000 msg/s  
   **Physics-based fix**: Rate-limit producers or horizontally scale consumers until total consumption ≥ production + headroom

2. **Scenario**: Cache stampede / thundering herd on key expiration  
   **Broken Principle**: Conservation of work (N concurrent misses → N times original computation instead of 1)  
   **Signature**: Single cache miss causes 10k+ simultaneous backend requests, latency spikes from 5 ms → 10 s  
   **Diagnosis**: All clients retry exactly when TTL expires → amplification factor = concurrency  
   **Physics-based fix**: Probabilistic early refresh, jittered TTL, or single-flight deduplication (mutex per key)

3. **Scenario**: Cascading failures across microservices  
   **Broken Principle**: Conservation of energy (retry storms amplify load exponentially)  
   **Signature**: One slow service → retries → more threads blocked → entire cluster latency → 503s everywhere  
   **Diagnosis**: Retry amplifier + timeout too high turns one overloaded node into total outage  
   **Physics-based fix**: Exponential backoff + jitter, circuit breakers, and bulkheads so failure energy stays contained

4. **Scenario**: Java application slowly OOMs over weeks  
   **Broken Principle**: Conservation of memory (objects allocated but never freed)  
   **Signature**: Heap usage 2 GB → 4 GB → 8 GB over weeks, GC time increasing  
   **Diagnosis**: Unbounded cache, off-heap leak, or finalized objects holding native references  
   **Physics-based fix**: Enforce hard bounds on all collections (you cannot store more bytes than physical RAM exists)

5. **Scenario**: Network congestion collapse (bufferbloat)  
   **Broken Principle**: Shannon-Hartley theorem + queueing theory (bandwidth-delay product limit)  
   **Signature**: Latency jumps from 20 ms → 5 s while throughput drops  
   **Diagnosis**: Deep packet buffers + TCP sawtooth fills queues → standing queue delay  
   **Physics-based fix**: Active Queue Management (FQ-CoDel, PIE) to keep buffers shallow; cannot send more bits than pipe can drain

6. **Scenario**: Connection pool exhaustion under load  
   **Broken Principle**: Conservation of file descriptors / server threads  
   **Signature**: “Connection pool timeout after 30s” errors while DB CPU < 20%  
   **Diagnosis**: Leaked/slow connections → pool size 200 exhausted → new requests wait forever  
   **Physics-based fix**: Enforce per-connection timeout + max lifetime; you cannot have more open sockets than OS allows

7. **Scenario**: Thread starvation / priority inversion in thread-per-request model  
   **Broken Principle**: Conservation of CPU time slices  
   **Signature**: Latency p99 explodes while CPU < 50%  
   **Diagnosis**: Thousands of threads stuck in blocking I/O → context-switch overhead eats all cycles  
   **Physics-based fix**: Async/non-blocking I/O or bounded thread pools (e.g., work-stealing with virtual threads sized to CPU cores)

8. **Scenario**: Disk I/O saturation → everything slows down  
   **Broken Principle**: Seek time + rotational latency are physical (cannot read two tracks at once)  
   **Signature**: iostat shows 100% util, queue length 50+, read latency 500 ms  
   **Diagnosis**: Random 4K writes exceeding ~200–300 IOPS of single HDD or saturation of SSD write units  
   **Physics-based fix**: Sequentialize writes (log-structured), add more spindles/SSDs, or shard data

9. **Scenario**: Long GC pauses in large-heap Java services  
   **Broken Principle**: Conservation of memory + data processing inequality (must visit all live objects)  
   **Signature**: 5–30 second stop-the-world pauses every few hours  
   **Diagnosis**: Live set > 50–70% of heap → full GC must scan almost everything  
   **Physics-based fix**: Keep heap small (G1/ZGC target < 4–6 GB) or use Shenandoah/ZGC with bounded pause targets; you cannot avoid touching live memory

10. **Scenario**: DNS lookup storm after redeploy  
    **Broken Principle**: Conservation of work + amplification (one request triggers thousands of identical DNS queries)  
    **Signature**: DNS server errors, latency spike right after deploy  
    **Diagnosis**: New code removes DNS caching → every connection does fresh lookup → 10k req/s → 10k DNS/s  
    **Physics-based fix**: Local DNS cache with reasonable TTL (at least 1–5 s); you cannot resolve the same name millions of times without doing the work millions of times

These examples and failures all trace back to unbreakable physical or mathematical laws: conservation laws, speed of light, entropy, information theory bounds, and queueing theory. Great engineering is just disciplined trade-off reasoning in the face of those immutable constraints.
