# 10 Failure Scenarios Violating Physical Principles

**Scenario**: Queue buildup at API gateway
**Broken Principle**: Conservation of mass (Continuity Equation)  
`∂ρ/∂t + ∇·(ρv) = σ` (Accumulation = Inflow - Outflow + Source)
**Signature**: Queue depth: 10k → 50k → 250k requests (exponential, not linear)  
**Diagnosis**: Arrival rate λ = 15k req/s. Service rate μ = 12k req/s. Net accumulation = +3k req/s. System acts as unstable integrator with pole in right-half plane (τ < 0)
**Fix**: Install rate limiter as negative source term: `σ = -max(0, λ - μ)`. Scale workers to μ = 18k req/s (20% margin). Add TTL-based leak valve for stale requests.

**Scenario**: Cache stampede on cache miss
**Broken Principle**: Conservation of momentum (Impulse-Momentum)  
`FΔt = mΔv` (Synchronized force creates inertial shockwave)
**Signature**: At t=0: 1,000 simultaneous queries hit database. DB connections: 50 → 500 → TIMEOUT  
**Diagnosis**: Synchronized expiration creates Dirac delta: ρ_req(t) = 1000·δ(t). Impulse J = 1000 × query_cost exceeds DB momentum capacity (100 concurrent). Shockwave propagates: slow query → thread pool exhaustion → cascading timeout
**Fix**: Add jitter Δt ~ Uniform(0, 500ms) to spread impulse over time. Use `sync.Once` pattern (elastic collision). Return stale data while repopulating (energy dissipation).

**Scenario**: Cascading failure from service timeout
**Broken Principle**: Positive feedback loop (Control Theory)  
`H(s) = G(s) / (1 - G(s)H(s))` (Unstable when loop gain > 1)
**Signature**: Service B timeout → A retries ×3 → B overload worsens → more timeouts. Failure propagates to 80 services in 3 minutes
**Diagnosis**: Retry creates positive feedback: timeout → retry → increased load → more timeout. Loop gain K = retry_count × timeout_probability > 1. Each iteration amplifies error: `e[n+1] = K·e[n]` (thermal runaway equivalent)
**Fix**: Circuit breaker opens when K > 0.8. Exponential backoff adds negative feedback. Limit retries to 1 (K < 1).

**Scenario**: Memory leak in long-running process
**Broken Principle**: Conservation of mass (Accumulation)  
`dm/dt = ṁ_in - ṁ_out + ṁ_gen`
**Signature**: Memory: 2GB → 4GB → 8GB over 48 hours (doubling every 24h). OOM kills every 2 days
**Diagnosis**: Allocation rate = 500 MB/s, deallocation = 499.99 MB/s. Net generation ṁ_gen = +10 MB/s. No mass sink for persistent allocations. Doubling time τ = (ln 2)/k where k = ṁ_gen/m_current
**Fix**: Fix code to deallocate (remove ṁ_gen). Periodic restart when memory > 6GB. Valgrind/ASan to locate generation source.

**Scenario**: Network congestion collapse
**Broken Principle**: Continuity with finite capacity  
`∂ρ/∂t + ∇·(ρv) = 0` constrained by `v ≤ v_max` and ρ ≤ ρ_max
**Signature**: Bandwidth: 10Gbps → 500Mbps effective throughput. Latency: 1ms → 200ms. Packet loss: 0% → 35%
**Diagnosis**: Flow exceeds shockwave capacity: ρ_in = 12Gbps, ρ_max = 10Gbps. When ρ > ρ_crit, flow becomes supersonic. Shockwave forms: packets compress until ρ_jam (buffer full), causing wave reflection (drops). Throughput collapses to `v = v_max × (ρ_max - ρ)/ρ_max`
**Fix**: TCP window scaling implements backpressure ΔP = ρ_in - ρ_out. Token bucket enforces ρ_in ≤ 0.8 × v_max. ECMP increases cross-sectional area.

**Scenario**: Connection pool exhaustion
**Broken Principle**: Conservation of resources (Discrete constraint)  
`∑_i u_i(t) ≤ C_pool`
**Signature**: 500 threads BLOCKED on `pool.getConnection()`. Active connections: 100 (pool max) all idle. 100% error rate
**Diagnosis**: Connection pool has finite state space C_pool = 100. Each blocked thread consumes slot without progress. Release rate < acquisition rate reaches absorbing state. Missing `finally{conn.close()}` violates detailed balance
**Fix**: Try-with-resources ensures lifetime ∝ request. Pool tracks `time_since_last_use` > 5min: force close (radioactive decay). Set pool size = 2 × typical load.

**Scenario**: Thread starvation in executor pool
**Broken Principle**: Conservation of execution capacity  
`∑ work = N_threads × T_cpu`
**Signature**: Task queue: 10k tasks queued, 0 executing. All 10 threads BLOCKED on `synchronized(lock)`. RejectedExecutionException
**Diagnosis**: Thread pool provides finite concurrency N_threads = 10. Each blocked thread consumes slot with zero progress: `dW/dt = 0`. Equivalent to electrical short: all current bypasses useful work. Pool conductance G = N_threads / blocking_time → 0
**Fix**: Replace `synchronized` with `tryLock(10ms)` (adds series resistance). Separate pools for CPU vs I/O (prevents shorting). `Future.get(5s)` aborts stuck tasks.

**Scenario**: Disk I/O saturation
**Broken Principle**: Bandwidth-delay product + mechanical limits  
`IOPS ≤ 1/(T_seek + T_rotate + T_transfer)`
**Signature**: `iostat`: `%util = 100%`, `await = 850ms` (QD=128). App p99: 10ms → 5s. Effective IOPS: 500 (rated 100k)
**Diagnosis**: Mechanical impedance: seek=4ms, rotation=2ms. At QD=128, service time = 0.85ms. Little's Law predicts W = L/λ = 256ms, but measures 850ms due to NCQ inefficiency and priority inversion (sequential reads blocked by random writes)
**Fix**: `deadline` scheduler: `read_expire=500ms` (express lane). NVMe reduces seek to 20μs. Page cache with 95% hit rate reduces physical IOPS to 5k.

**Scenario**: Stop-the-world GC pause
**Broken Principle**: Second Law of Thermodynamics  
`ΔS ≥ Q/T` (Entropy reduction requires work and time)
**Signature**: GC log: `Pause Young (G1) 5000ms`. 32 threads STOPPED. 15% timeout rate during pause
**Diagnosis**: Heap is disordered system: 8GB objects with random references. GC must do work W = TΔS to organize. Parallel GC scan rate = 25GB/s: predicted time = 0.312s. Actual 5s due to premature promotion (increases Ω exponentially) and fragmentation (reduces scan rate 10×)
**Fix**: `-XX:MaxNewSize=2G` limits young gen (smaller Ω). ZGC organizes concurrently, STW <10ms. Faster CPUs reduce Δt for same ΔS.

**Scenario**: DNS lookup storm
**Broken Principle**: Conservation of request rate + caching  
`λ_effective = λ_actual × (1 - hit_rate)`
**Signature**: DNS server: 100k qps (normal: 500). 10k containers restart simultaneously. External DNS rate-limited at 10k qps → 90% SERVFAIL
**Diagnosis**: Cache normally stores mass: hit_rate=0.995, λ_upstream=500 qps. Cold start: cache_state erased. Each container makes 12 queries/domain. Burst λ = 10k×10×12/60s = 20k qps exceeds capacity C=10k qps. Queue overflow causes drops and retry cascades
**Fix**: Raise TTL to 3600s (increases mass storage). Local `dnsmasq` acts as distributed capacitor. Orchestrator adds startup jitter: `sleep(rand(0,300s))`.

---

# 5 Fundamental Principle Conflicts

**Principle 1**: Little's Law (`L = λW`) suggests high concurrency (large connection pool) reduces wait time  
**Principle 2**: Amdahl's Law (`S = 1/((1-P) + P/N)`) suggests parallel resources have diminishing returns and overhead  
**Conflict**: Large pool increases contention on pool lock (serial fraction), reducing effective parallelism  
**Trade-off Analysis**: Optimal pool size N* occurs where marginal wait reduction = marginal contention increase. Solve `dW/dN = 0` where W(N) = (λ/(μN-λ)) + αN² (contention term). Typically N* ≈ 2×λ/μ + constant  
**Real-world constraint**: Lock acquisition latency (100ns) × thread count creates hyperbolic contention curve. On 32-core, optimum ≈ 50-100 connections before lock convoy dominates

**Principle 1**: CAP Theorem (consistency requires coordination delay) suggests synchronous replication for linearizability  
**Principle 2**: Speed of light (`T_min = distance/c`) imposes absolute latency floor on coordination  
**Conflict**: Can't achieve both low latency and strong consistency across geographic distance  
**Trade-off Analysis**: Relativity: choose reference frame. For local clients (latency <<光速): favor consistency. For global clients: sacrifice consistency (eventual) or accept high latency. Tunable via CRDTs (relaxed consistency) or Raft (strong but slow)  
**Real-world constraint**: NYC-SFO round-trip = 80ms (physical lower bound). Must either: (a) accept 80ms writes, (b) use async replication with 100ms inconsistency window, or (c) partition dataset geographically

**Principle 1**: Shannon-Hartley (`C = B log₂(1+S/N)`) says compression increases effective bandwidth  
**Principle 2**: Landauer Limit (`E = kT ln 2` per bit) says computation has fundamental energy cost  
**Conflict**: Compression reduces network energy but increases CPU energy. Can't minimize both simultaneously  
**Trade-off Analysis**: Total energy E_total = E_network + E_cpu. Network energy ∝ bits sent. CPU energy ∝ compression complexity × bits. Optimal compression ratio r* solves `dE_total/dr = 0`. For typical cloud: network energy dominates >1MB payloads → compress. For <1KB payloads, CPU overhead dominates → send raw  
**Real-world constraint**: 1GB/s compression at 3W/GB vs 10Gbps NIC at 0.5W/GB. Breakeven at ~500KB payload size

**Principle 1**: Parkinson's Law (work expands to fill time) suggests batching increases throughput  
**Principle 2**: Per-request overhead (fixed cost) suggests batching reduces amortized latency  
**Conflict**: Large batch size increases individual request latency (head-of-line blocking) while improving throughput  
**Trade-off Analysis**: Kingman's formula predicts wait in G/G/1: `E[W] ≈ (ρ/(1-ρ)) × (C_a² + C_s²)/2 × E[S]`. Batching increases service variability C_s² ∝ batch_size². Optimal batch size B* balances setup cost S₀ against latency penalty: B* ≈ √(2λS₀/(1-ρ)). Too large: latency spikes. Too small: throughput suffers  
**Real-world constraint**: Kafka batch linger.ms=10ms gives 95% throughput of 100ms but p99 latency improves 10×. Actual optimum requires profiling: measure `dThroughpout/dBatchSize` vs `dLatency/dBatchSize` at knee point

**Principle 1**: Least Recently Used (temporal locality) suggests large caches maximize hit rate  
**Principle 2**: Memory hierarchy (access time ∝ capacity^α) says large caches are slower  
**Conflict**: Can't have both large capacity and fast access. L1 cache is tiny (32KB) but 1ns. DRAM is huge but 100ns  
**Trade-off Analysis**: Optimize for reuse distance. Working set size WSS determines minimum capacity. If WSS < 1MB, L3 cache suffices (10ns). If WSS = 10GB, must accept DRAM latency. Cache hierarchy provides Pareto frontier: `T_avg = Σ h_i × t_i` where h_i = hit rate at level i. Goal: maximize `h₁ + h₂` subject to `C₁ + C₂ ≤ Budget`  
**Real-world constraint**: Redis cache on same host (10μs) vs remote (500μs) vs SSD (100μs). Cache size limited by GC pressure: heap > 32GB causes pointer compression issues. Optimal: cache size = 70% of WSS, measured by LRU age distribution histogram
