# TRIAD Sovereign Execution Fabric - Complete Build Spec
## The Cory Method: 7-Phase Development Plan

**Project:** TRIAD (The Routing & Interception Assembly for Distributed Intelligence)  
**Objective:** Build a sovereignty-enforced, event-driven AI orchestration fabric that makes models commodities and orchestration the moat  
**Timeline:** 30 days (4 weeks, 7 phases)  
**Repository Structure:** Monorepo with clear separation of concerns

---

## PHASE 1: DESIGN (Days 1-3)
### First Principles - What We're Actually Building

**Core Primitive:**
> A deterministic, event-driven orchestrator that transforms AI models into stateless functions in a distributed computation graph with cryptographically enforced data sovereignty.

**Mental Model:** Unix pipes + Event Sourcing + Airflow for LLMs + TPM-backed compliance

**What We're NOT Building:**
- ❌ Another OpenAI wrapper
- ❌ A single-model AI product
- ❌ Marketing-driven "AI security" theater

**What We ARE Building:**
- ✅ Infrastructure protocol (like AWS Lambda for AI)
- ✅ Compliance-by-default (CMMC, FedRAMP, ITAR)
- ✅ Model marketplace with bidding system
- ✅ Self-improving orchestration (MAESTRO meta-agent)

**Key Design Decisions:**

1. **Event-Driven Everything**
   - Every action is an immutable event
   - Full audit trail by default
   - Replayable workflows
   - No mutable state in orchestrator

2. **Sovereignty as Cryptographic Primitive**
   - Not policy enforcement - mathematical proof
   - TPM-backed hardware root of trust
   - Data envelopes that cannot be opened outside geofences
   - Merkle DAG for chain of custody

3. **WASM-Based Model Adapters**
   - Models run in sandboxes
   - Can't access network/filesystem directly
   - Self-describing capabilities
   - Hot-swappable at runtime

4. **Economic Layer (TRIAD Tokens)**
   - Non-transferable usage credits
   - Earn by contributing: model capacity, data, validation
   - Deflationary (tokens burned on use)
   - Creates closed-loop network effects

5. **MAESTRO Meta-Orchestrator**
   - Thinks like Cory (first principles, parallel simulation, skepticism)
   - Uses Kimi K2's 200K context as shared memory bus
   - Builds agents on-demand
   - Self-improving through mission learning

---

## PHASE 2: ARCHITECTURE (Days 4-7)
### System Design & Component Breakdown

### 2.1 Repository Structure

```
triad/
├── README.md
├── LICENSE (Apache 2.0 - we want adoption)
├── pyproject.toml
├── docker-compose.yml
├── .env.example
│
├── core/
│   ├── __init__.py
│   ├── sovereignty_kernel.py       # TPM-backed data envelopes
│   ├── event_sourcing.py           # Immutable event store
│   ├── orchestrator.py             # TriadExecutionEngine
│   └── workflow_dsl.py             # DSL for defining workflows
│
├── adapters/
│   ├── __init__.py
│   ├── model_contract.py           # ModelAdapter protocol
│   ├── grok_adapter.py             # Grok 4 Fast
│   ├── claude_adapter.py           # Claude Sonnet 4.5
│   ├── aetherai_adapter.py         # AetherAI (self-hosted)
│   └── wasm/
│       ├── wasm_adapter.rs         # Rust WASM sandbox
│       └── Cargo.toml
│
├── registry/
│   ├── __init__.py
│   ├── model_registry.py           # Dynamic model discovery
│   ├── capability_matching.py      # Semantic task→model matching
│   └── health_monitor.py           # Model heartbeat & health checks
│
├── router/
│   ├── __init__.py
│   ├── capability_router.py        # Routes based on capabilities + sovereignty
│   ├── bidding_market.py           # Models bid on tasks in real-time
│   └── circuit_breaker.py          # Failure handling & fallbacks
│
├── executor/
│   ├── __init__.py
│   ├── task_executor.py            # Async task execution with backpressure
│   └── workflow_engine.py          # DAG execution with fan-out/fan-in
│
├── billing/
│   ├── __init__.py
│   ├── triad_token.py              # Non-transferable usage credits
│   └── cost_calculator.py          # Real-time cost estimation
│
├── maestro/
│   ├── __init__.py
│   ├── genius_loop.py              # Meta-cognitive reasoning loop
│   ├── agent_deployer.py           # Builds agents on-demand
│   ├── shared_context.py           # 200K token shared memory
│   └── mission_orchestrator.py     # Oversees multi-agent missions
│
├── api/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app
│   ├── routes.py                   # REST endpoints
│   └── sse.py                      # Server-Sent Events for observability
│
├── storage/
│   ├── __init__.py
│   ├── event_store.py              # PostgreSQL + TimescaleDB for events
│   ├── merkle_dag.py               # Cryptographic audit trail
│   └── redis_cache.py              # Redis for hot data
│
├── security/
│   ├── __init__.py
│   ├── tpm_manager.py              # Trusted Platform Module interface
│   ├── geofence.py                 # CONUS boundary enforcement
│   └── zk_proofs.py                # Zero-knowledge proofs for privacy
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   ├── sovereignty_kernel.md
│   ├── maestro_guide.md
│   └── wasm_adapter_spec.md
│
├── examples/
│   ├── simple_workflow.py
│   ├── sovereignty_demo.py
│   └── maestro_mission.py
│
└── deploy/
    ├── kubernetes/
    │   ├── triad-deployment.yaml
    │   └── sovereignty-configmap.yaml
    ├── terraform/
    │   └── ovhcloud/
    └── docker/
        ├── Dockerfile.core
        ├── Dockerfile.maestro
        └── Dockerfile.wasm-runtime
```

### 2.2 Core Component Specifications

#### **SovereigntyKernel**
```python
class SovereigntyKernel:
    """
    Cryptographically enforces data sovereignty using TPM-backed envelopes.
    
    Key Features:
    - Hardware root of trust (TPM)
    - Geofenced encryption (data can't be decrypted outside CONUS)
    - Merkle proofs for chain of custody
    - Immutable audit trail
    """
    
    async def seal_data_envelope(
        self, 
        data: bytes, 
        required_zones: List[str]
    ) -> SovereignEnvelope:
        """
        Wraps data in cryptographic envelope that CANNOT be opened
        outside approved jurisdictions.
        
        Returns:
            SovereignEnvelope with:
            - Encrypted ciphertext (AES-256-GCM)
            - Jurisdiction proof (Merkle tree)
            - TPM signature
            - Geofence lock (GPS/network boundaries)
        """
        pass
    
    async def verify_chain_of_custody(
        self, 
        workflow_id: str
    ) -> MerkleDAG:
        """
        Reconstruct entire data lineage.
        Every task, every model, every byte.
        
        Raises:
            SovereigntyViolation if any event violated jurisdiction
        """
        pass
```

#### **TriadExecutionEngine**
```python
class TriadExecutionEngine:
    """
    Main orchestrator - coordinates all components.
    
    Architecture:
    - Event-driven (asyncio + Redis Streams)
    - Model-agnostic (adapter pattern)
    - Observable (SSE streams)
    - Replayable (event sourcing)
    """
    
    async def submit(self, workflow: WorkflowDAG) -> ExecutionHandle:
        """
        Fire-and-forget workflow submission.
        
        Process:
        1. Validate sovereignty constraints
        2. Convert DAG to event stream
        3. Publish to event bus
        4. Return handle for monitoring
        """
        pass
    
    async def _execute_loop(self):
        """
        Main event loop (runs forever).
        
        For each event:
        1. Router makes decision (which model?)
        2. Emit decision to audit log
        3. Execute with circuit breaker
        4. Process next tasks in DAG
        """
        pass
```

#### **ModelAdapter (Protocol)**
```python
class ModelAdapter(Protocol):
    """
    Every model must implement this interface.
    Makes models hot-swappable.
    """
    
    async def invoke(self, request: TaskRequest) -> TaskResult:
        """Execute the model with given request."""
        pass
    
    def capabilities(self) -> ModelFingerprint:
        """
        Self-describing metadata:
        - Latency (p50, p95, p99)
        - Cost per token
        - Specialties (reasoning, speed, creativity)
        - Sovereignty zones (US, EU, etc.)
        - Max context window
        """
        pass
    
    async def bid(self, task: TaskRequest) -> Bid:
        """
        Optional: Model can bid on tasks.
        Returns (price, latency_estimate, confidence)
        """
        pass
```

#### **MAESTRO GeniusLoop**
```python
class GeniusLoop:
    """
    Meta-cognitive reasoning pattern (Cory's thinking as code).
    
    5-Phase Loop:
    1. Deconstruct (first principles)
    2. Parallelize (simulate 3-5 approaches)
    3. Stress-test (find edge cases)
    4. Synthesize (build the plan)
    5. Skepticism-check (what could kill this?)
    """
    
    async def think(self, problem: ProblemStatement) -> MasterPlan:
        """
        This is the "Cory" part.
        Agent thinks through problem systematically.
        
        Returns:
            MasterPlan with:
            - Decomposed sub-problems
            - Parallel approaches evaluated
            - Stress-test results
            - Final synthesized plan
            - Skepticism report (what could fail?)
        """
        pass
```

### 2.3 Data Flow Architecture

```
User Request
    ↓
FastAPI Endpoint (api/main.py)
    ↓
TriadExecutionEngine.submit(workflow)
    ↓
SovereigntyKernel.verify_constraints()
    ↓
Event Bus (Redis Streams) → Publish "execution.request"
    ↓
CapabilityRouter.resolve(task)
    ↓
ModelRegistry.find_models_for_task()
    ↓
[Optional] BiddingMarket.auction_task()
    ↓
TaskExecutor.run_with_fallbacks()
    ↓
ModelAdapter.invoke(request)
    ↓
Result → Event Bus → "execution.complete"
    ↓
MerkleDAG.append(proof)
    ↓
SSE Stream → User sees real-time progress
```

### 2.4 Technology Stack

**Core:**
- Python 3.11+ (asyncio, type hints)
- FastAPI (REST + SSE)
- PostgreSQL + TimescaleDB (event store)
- Redis (event bus, caching)

**Security:**
- Rust (WASM adapters)
- TPM libraries (tpm2-tss)
- Cryptography.io (AES-GCM, Merkle trees)

**Infrastructure:**
- Docker + Docker Compose
- Kubernetes (production)
- Terraform (IaC)
- OVHcloud (US-East region)

**Observability:**
- Prometheus (metrics)
- Grafana (dashboards)
- Jaeger (distributed tracing)
- Sentry (error tracking)

**AI Models:**
- AetherAI (self-hosted vLLM)
- Grok 4 Fast (xAI API)
- Claude Sonnet 4.5 (Anthropic API)
- Kimi K2 (for MAESTRO thinking)

---

## PHASE 3: PROTOTYPE (Days 8-14)
### Build Core Components - MVP First

### Week 2 Focus: Working End-to-End Flow

**Day 8-9: Core Orchestrator**
```python
# Goal: Submit workflow, route to model, get result

# Files to create:
- core/orchestrator.py (TriadExecutionEngine skeleton)
- core/workflow_dsl.py (Simple DSL parser)
- adapters/model_contract.py (Protocol definition)
- adapters/mock_adapter.py (Fake model for testing)

# Success criteria:
workflow = Workflow("test")
workflow.add_task("question", "What is 2+2?")
handle = await engine.submit(workflow)
result = await handle.wait()
assert result == "4"
```

**Day 10-11: Sovereignty Kernel (Simplified)**
```python
# Goal: Prove we can enforce CONUS-only data paths

# Files to create:
- core/sovereignty_kernel.py (SovereignEnvelope, basic encryption)
- security/geofence.py (CONUS boundary checking)
- storage/merkle_dag.py (Audit trail)

# Success criteria:
envelope = await kernel.seal_data("secret", required_zones=["US"])
# Try to decrypt in simulated EU zone → raises SovereigntyViolation
```

**Day 12-13: Real Model Adapters**
```python
# Goal: Connect to actual AI models

# Files to create:
- adapters/aetherai_adapter.py (localhost vLLM)
- adapters/grok_adapter.py (xAI API)
- adapters/claude_adapter.py (Anthropic API)

# Success criteria:
# Same workflow runs on 3 different models
# Router chooses based on task requirements
```

**Day 14: FastAPI + SSE**
```python
# Goal: HTTP interface with real-time streaming

# Files to create:
- api/main.py (FastAPI app)
- api/sse.py (Server-Sent Events)

# Success criteria:
curl -X POST http://localhost:8000/workflows \
  -d '{"tasks": [{"prompt": "Hello"}]}'
# Returns workflow_id

curl http://localhost:8000/workflows/{id}/events
# Streams: task.routed → task.executing → task.complete
```

---

## PHASE 4: ITERATION (Days 15-21)
### Refine, Optimize, Add Enterprise Features

### Week 3 Focus: Production-Ready Features

**Day 15-16: Model Registry + Health Checks**
```python
# registry/model_registry.py
- Models self-register with capabilities
- Heartbeat monitoring (mark unhealthy models)
- Capability-based matching (not just string matching)
```

**Day 17-18: Circuit Breakers + Fallbacks**
```python
# router/circuit_breaker.py
- Detect failing models (3 failures in 60s → open circuit)
- Automatic fallback to secondary models
- Exponential backoff with jitter
```

**Day 19: Billing System (TRIAD Tokens)**
```python
# billing/triad_token.py
- Issue tokens for contributions
- Consume tokens for execution
- Non-transferable credits
- Merkle tree for audit
```

**Day 20: MAESTRO Integration (Basic)**
```python
# maestro/genius_loop.py
- First principles decomposition
- Parallel approach simulation
- Stress testing
- Synthesis into plan

# Connect to workflow execution:
mission = Mission(problem="Optimize supply chain")
plan = await maestro.think(mission.problem)
workflow = maestro.plan_to_workflow(plan)
await engine.submit(workflow)
```

**Day 21: Observability Stack**
```python
# Add metrics, tracing, logging
- Prometheus metrics (requests/sec, latency, cost)
- Jaeger tracing (distributed workflow tracking)
- Structured logging (JSON logs)
```

---

## PHASE 5: TESTING (Days 22-24)
### Comprehensive Test Suite

### Day 22: Unit Tests
```python
# tests/unit/
- test_sovereignty_kernel.py
  ✓ Envelope sealing/unsealing
  ✓ Geofence violations raise errors
  ✓ Merkle proof verification

- test_orchestrator.py
  ✓ Workflow submission
  ✓ Event sourcing correctness
  ✓ DAG execution order

- test_adapters.py
  ✓ Model invocation
  ✓ Capability matching
  ✓ Error handling
```

### Day 23: Integration Tests
```python
# tests/integration/
- test_end_to_end_workflow.py
  ✓ Submit workflow → route → execute → verify audit trail
  
- test_sovereignty_enforcement.py
  ✓ CONUS-only workflow completes
  ✓ Non-CONUS workflow fails sovereignty check
  
- test_model_fallbacks.py
  ✓ Primary model fails → fallback succeeds
  ✓ Circuit breaker opens after repeated failures
```

### Day 24: Load Tests + Edge Cases
```python
# tests/e2e/
- test_concurrent_workflows.py
  ✓ 100 workflows in parallel
  ✓ No race conditions
  ✓ Event ordering preserved

- test_failure_modes.py
  ✓ Redis goes down → graceful degradation
  ✓ Model timeout → circuit breaker triggers
  ✓ Invalid workflow → clear error message
```

---

## PHASE 6: DOCUMENTATION (Days 25-27)
### Make It Usable by Others

### Day 25: Architecture Documentation
```markdown
# docs/architecture.md
- System overview diagram
- Component responsibilities
- Data flow charts
- Sovereignty enforcement explanation
- Event sourcing rationale

# docs/sovereignty_kernel.md
- How TPM-backed envelopes work
- Geofence implementation
- Merkle DAG structure
- Compliance certifications path (CMMC, FedRAMP)
```

### Day 26: API Reference + Examples
```markdown
# docs/api_reference.md
- REST endpoints (OpenAPI spec)
- SSE event types
- Error codes
- Rate limits

# examples/
- simple_workflow.py (Hello World)
- sovereignty_demo.py (CONUS-only example)
- multi_model_orchestration.py (Fan-out/fan-in)
- maestro_mission.py (MAESTRO-driven workflow)
```

### Day 27: WASM Adapter Spec
```markdown
# docs/wasm_adapter_spec.md
- Adapter contract (Rust interface)
- Sandbox restrictions
- How to build WASM adapter for any model
- Example: OpenAI adapter in WASM

This is the "Docker moment" - define the standard so
others build TRIAD-compatible adapters.
```

---

## PHASE 7: DEPLOYMENT (Days 28-30)
### Ship to Production

### Day 28: Docker + Kubernetes
```yaml
# deploy/kubernetes/triad-deployment.yaml
- Core orchestrator (3 replicas)
- Redis cluster (event bus)
- PostgreSQL + TimescaleDB
- Prometheus + Grafana

# deploy/docker/Dockerfile.core
FROM python:3.11-slim
COPY triad/ /app/triad
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

### Day 29: OVHcloud Deployment (US-East)
```hcl
# deploy/terraform/ovhcloud/main.tf
- Provision Kubernetes cluster (US-East-1)
- Set up VPC with CONUS-only networking
- Configure TPM-backed secrets
- Deploy TRIAD services
- Set up DNS (api.aetherpro.tech/v1)
```

### Day 30: Launch + Monitoring
```python
# Smoke tests in production
- Health check endpoints responding
- Workflow submission works
- Sovereignty enforcement active
- SSE streams working
- Metrics flowing to Grafana

# Set up alerts
- Model health degradation
- Sovereignty violations
- High error rates
- Cost overruns
```

---

## CRITICAL FILES TO BUILD (In Order)

### Sprint 1 (Days 1-7): Core Infrastructure

**1. core/workflow_dsl.py**
```python
"""
DSL for defining workflows.

Example:
    workflow = Workflow("research")
    workflow.add_task(
        "generate_questions",
        model="grok",
        prompt="Generate 10 async architecture questions"
    )
    workflow.add_task(
        "answer_questions",
        model="claude",
        prompt="Answer: {generate_questions.output}",
        depends_on=["generate_questions"]
    )
"""

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.tasks = []
        self.dag = {}
    
    def add_task(
        self, 
        task_id: str, 
        prompt: str,
        model: Optional[str] = None,
        depends_on: List[str] = None,
        sovereignty_required: bool = True
    ):
        """Add task to workflow DAG."""
        pass
    
    def to_event_stream(self) -> List[Event]:
        """Convert DAG to event stream for execution."""
        pass
```

**2. core/sovereignty_kernel.py**
```python
"""
Cryptographic sovereignty enforcement.

Key Features:
- TPM-backed encryption
- Geofenced data envelopes
- Merkle proof generation
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class SovereigntyKernel:
    def __init__(self, tpm_manager: TPMManager):
        self.tpm = tpm_manager
        self.conus_boundary = self._load_conus_geofence()
    
    async def seal_data_envelope(
        self, 
        data: bytes, 
        required_zones: List[str]
    ) -> SovereignEnvelope:
        """
        1. Generate ephemeral key in TPM
        2. Encrypt data with AES-256-GCM
        3. Create merkle proof of jurisdiction
        4. Return envelope with geofence lock
        """
        # Generate key inside CONUS TPM
        key = await self.tpm.generate_key(
            algorithm="AES-256-GCM",
            zone="US-EAST-1"
        )
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        # Generate jurisdiction proof
        proof = await self._generate_jurisdiction_proof(
            data_hash=sha256(ciphertext),
            zones=required_zones,
            timestamp=time.time(),
            tpm_signature=self.tpm.sign(ciphertext)
        )
        
        return SovereignEnvelope(
            ciphertext=ciphertext,
            tag=encryptor.tag,
            jurisdiction_proof=proof,
            key_id=key.id,
            geo_lock=GeoFence(zones=required_zones)
        )
    
    async def unseal_envelope(
        self, 
        envelope: SovereignEnvelope,
        current_zone: str
    ) -> bytes:
        """
        Verify we're in approved zone, then decrypt.
        Raises SovereigntyViolation if not in approved zone.
        """
        if current_zone not in envelope.geo_lock.zones:
            raise SovereigntyViolation(
                f"Cannot unseal in {current_zone}. "
                f"Required: {envelope.geo_lock.zones}"
            )
        
        # Retrieve key from TPM
        key = await self.tpm.get_key(envelope.key_id)
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, envelope.tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(envelope.ciphertext) + decryptor.finalize()
        
        return plaintext
```

**3. core/orchestrator.py**
```python
"""
Main TRIAD execution engine.
"""

class TriadExecutionEngine:
    def __init__(
        self,
        event_bus: EventBus,
        registry: ModelRegistry,
        sovereignty_kernel: SovereigntyKernel
    ):
        self.event_bus = event_bus
        self.registry = registry
        self.sovereignty = sovereignty_kernel
        self.router = CapabilityRouter(registry)
        self.executor = TaskExecutor(max_concurrency=1000)
    
    async def submit(self, workflow: Workflow) -> ExecutionHandle:
        """
        Fire-and-forget workflow submission.
        """
        # Validate sovereignty
        if not await self._verify_sovereign_path(workflow):
            raise SovereigntyViolation(
                "Workflow violates data sovereignty constraints"
            )
        
        # Assign workflow ID
        workflow_id = str(uuid4())
        
        # Convert to events
        events = workflow.to_event_stream()
        
        # Publish to event bus
        for event in events:
            await self.event_bus.publish(
                "execution.request",
                {
                    "workflow_id": workflow_id,
                    "event": event.dict()
                }
            )
        
        return ExecutionHandle(
            workflow_id=workflow_id,
            event_stream=f"execution.{workflow_id}",
            cancel_token=CancelToken()
        )
    
    async def _execute_loop(self):
        """
        Main event loop - runs forever.
        """
        async for msg in self.event_bus.subscribe("execution.request"):
            event = Event.parse(msg["event"])
            
            # Route to model
            route_decision = await self.router.resolve(event.task)
            
            # Audit log
            await self.event_bus.publish(
                f"audit.{msg['workflow_id']}",
                route_decision.dict()
            )
            
            # Execute
            try:
                result = await self.executor.run_with_fallbacks(
                    task=event.task,
                    primary=route_decision.primary_model,
                    fallbacks=route_decision.fallback_models,
                    timeout=event.task.sla
                )
                
                # Emit success
                await self.event_bus.publish(
                    f"execution.{msg['workflow_id']}",
                    {
                        "type": "task.complete",
                        "task_id": event.task.id,
                        "result": result
                    }
                )
            except Exception as e:
                # Emit failure
                await self.event_bus.publish(
                    f"execution.{msg['workflow_id']}",
                    {
                        "type": "task.failed",
                        "task_id": event.task.id,
                        "error": str(e)
                    }
                )
    
    async def start(self):
        """Start the event loop."""
        await self._execute_loop()
```

**4. adapters/model_contract.py**
```python
"""
Protocol definition for model adapters.
"""

from typing import Protocol, AsyncIterator

class ModelAdapter(Protocol):
    """
    All models must implement this interface.
    Makes models hot-swappable.
    """
    
    async def invoke(self, request: TaskRequest) -> TaskResult:
        """
        Execute model with given request.
        
        Args:
            request: Contains prompt, context, sovereignty requirements
        
        Returns:
            TaskResult with output and metadata
        """
        ...
    
    def capabilities(self) -> ModelFingerprint:
        """
        Self-describing metadata about this model.
        
        Returns:
            ModelFingerprint with:
            - latency_p50: median latency in ms
            - cost_per_1k_tokens: pricing
            - specialties: list of things model is good at
            - sovereignty_zones: where model can run
            - max_context: context window size
        """
        ...
    
    async def stream(self, request: TaskRequest) -> AsyncIterator[str]:
        """
        Optional: Streaming response.
        Yields tokens as they're generated.
        """
        ...
    
    async def bid(self, task: TaskRequest) -> Bid:
        """
        Optional: Participate in task bidding.
        
        Returns:
            Bid with (price, estimated_latency, confidence_score)
        """
        ...
```

**5. api/main.py**
```python
"""
FastAPI application - REST + SSE interface.
"""

from fastapi import FastAPI, HTTPException
from sse_starlette.sse import EventSourceResponse

app = FastAPI(
    title="TRIAD Execution Fabric",
    description="Sovereign AI Orchestration Platform",
    version="1.0.0"
)

@app.post("/v1/workflows", status_code=202)
async def submit_workflow(workflow: WorkflowRequest):
    """
    Submit a workflow for execution.
    
    Returns immediately with workflow_id for tracking.
    """
    try:
        # Parse workflow DSL
        parsed_workflow = Workflow.from_dict(workflow.dict())
        
        # Submit to engine
        handle = await engine.submit(parsed_workflow)
        
        return {
            "workflow_id": handle.workflow_id,
            "status": "accepted",
            "stream_url": f"/v1/workflows/{handle.workflow_id}/events",
            "cancel_url": f"/v1/workflows/{handle.workflow_id}/cancel"
        }
    except SovereigntyViolation as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/workflows/{workflow_id}/events")
async def stream_workflow_events(workflow_id: str):
    """
    Server-Sent Events stream of workflow execution.
    
    Events:
    - task.routed: Router assigned model
    - task.executing: Model is running
    - task.complete: Task finished
    - task.failed: Task errored
    - workflow.complete: All tasks done
    """
    async def event_generator():
        async for event in event_bus.subscribe(f"execution.{workflow_id}"):
            yield {
                "event": event["type"],
                "data": event
            }
    
    return EventSourceResponse(event_generator())

@app.post("/v1/workflows/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: str):
    """
    Kill switch - cancels all running tasks in workflow.
    """
    await engine.cancel(workflow_id)
    return {"status": "cancelled"}

@app.get("/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_registered": len(registry.models),
        "event_bus": "connected" if event_bus.connected else "disconnected"
    }
```

### Sprint 2 (Days 8-14): Model Adapters

**6. adapters/aetherai_adapter.py**
```python
"""
AetherAI adapter - self-hosted vLLM.
"""

import httpx

class AetherAIAdapter:
    """Adapter for self-hosted AetherAI model."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def invoke(self, request: TaskRequest) -> TaskResult:
        """Call self-hosted vLLM endpoint."""
        response = await self.client.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "model": "aetherai-v1",
                "messages": [
                    {"role": "user", "content": request.prompt}
                ],
                "max_tokens": request.max_tokens or 1000
            }
        )
        
        result = response.json()
        
        return TaskResult(
            output=result["choices"][0]["message"]["content"],
            model="aetherai-v1",
            latency_ms=response.elapsed.total_seconds() * 1000,
            tokens_used=result["usage"]["total_tokens"],
            cost=0  # Self-hosted = no API cost
        )
    
    def capabilities(self) -> ModelFingerprint:
        return ModelFingerprint(
            latency_p50=150,  # ms
            cost_per_1k=0,  # Self-hosted
            specialties=[
                "async_architecture",
                "first_principles",
                "distributed_systems"
            ],
            sovereignty_zones=["US"],  # OVHcloud US-East
            max_context=200000
        )
```

**7. adapters/grok_adapter.py**
```python
"""
Grok 4 Fast adapter - xAI API.
"""

class GrokAdapter:
    """Adapter for Grok 4 Fast (speed-critical tasks)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    async def invoke(self, request: TaskRequest) -> TaskResult:
        """Call xAI API."""
        # Verify sovereignty if required
        if request.sovereignty_required:
            await self._verify_conus_endpoint()
        
        response = await self.client.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "grok-4-fast",
                "messages": [
                    {"role": "user", "content": request.prompt}
                ],
                "max_tokens": request.max_tokens or 1000
            }
        )
        
        result = response.json()
        
        return TaskResult(
            output=result["choices"][0]["message"]["content"],
            model="grok-4-fast",
            latency_ms=response.elapsed.total_seconds() * 1000,
            tokens_used=result["usage"]["total_tokens"],
            cost=result["usage"]["total_tokens"] * 0.000005  # $0.005/1K
        )
    
    def capabilities(self) -> ModelFingerprint:
        return ModelFingerprint(
            latency_p50=50,  # Very fast
            cost_per_1k=0.005,
            specialties=["speed", "creativity", "real_time"],
            sovereignty_zones=["US"],  # xAI is US-based
            max_context=131072
        )
```

**8. adapters/claude_adapter.py**
```python
"""
Claude Sonnet 4.5 adapter - Anthropic API.
"""

class ClaudeAdapter:
    """Adapter for Claude Sonnet 4.5 (complex reasoning)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    async def invoke(self, request: TaskRequest) -> TaskResult:
        """
        Call Anthropic API with retry logic.
        """
        async def _call():
            response = await self.client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": request.max_tokens or 1000,
                    "messages": [
                        {"role": "user", "content": request.prompt}
                    ]
                }
            )
            return response
        
        # Retry with exponential backoff
        response = await self._retry_with_jitter(
            _call,
            max_attempts=3,
            base_delay=0.1
        )
        
        result = response.json()
        
        return TaskResult(
            output=result["content"][0]["text"],
            model="claude-sonnet-4.5",
            latency_ms=response.elapsed.total_seconds() * 1000,
            tokens_used=result["usage"]["input_tokens"] + result["usage"]["output_tokens"],
            cost=result["usage"]["total_tokens"] * 0.00003  # $0.03/1K
        )
    
    def capabilities(self) -> ModelFingerprint:
        return ModelFingerprint(
            latency_p50=200,
            cost_per_1k=0.03,
            specialties=[
                "reasoning",
                "safety",
                "first_principles",
                "complex_analysis"
            ],
            sovereignty_zones=["US"],  # Anthropic US endpoints
            max_context=200000
        )
```

### Sprint 3 (Days 15-21): MAESTRO + Production Features

**9. maestro/genius_loop.py**
```python
"""
MAESTRO - The Kimi-powered master orchestrator.
Thinks like Cory: first principles, parallel simulation, skepticism.
"""

class GeniusLoop:
    """
    Meta-cognitive reasoning loop.
    
    5 Phases:
    1. Deconstruct (first principles)
    2. Parallelize (simulate 3-5 approaches)
    3. Stress-test (find edge cases)
    4. Synthesize (build actual plan)
    5. Skepticism-check (what could kill this?)
    """
    
    def __init__(self, kimi_api):
        self.kimi = kimi_api
        self.thought_buffer = []
        self.parallel_simulations = 5
    
    async def think(self, problem: ProblemStatement) -> MasterPlan:
        """
        This is the "Cory" part.
        Agent thinks through problem systematically.
        """
        # Phase 1: Deconstruct to first principles
        decomposition = await self._first_principles_decon(problem)
        self.thought_buffer.append(f"Deconstructed: {decomposition}")
        
        # Phase 2: Parallel simulation of approaches
        strategies = ["brute_force", "elegant", "resilient", "cheap", "fast"]
        simulations = await asyncio.gather(*[
            self._simulate_approach(decomposition, strategy=s)
            for s in strategies
        ])
        self.thought_buffer.append(f"Simulated {len(simulations)} approaches")
        
        # Phase 3: Stress-test each approach
        stress_tests = await asyncio.gather(*[
            self._adversarial_test(sim)
            for sim in simulations
        ])
        
        # Phase 4: Synthesize best elements
        synthesis = await self._synthesize_plan(simulations, stress_tests)
        
        # Phase 5: Skepticism check
        risks = await self._skepticism_check(synthesis)
        
        return MasterPlan(
            decomposition=decomposition,
            approaches=simulations,
            stress_tests=stress_tests,
            synthesis=synthesis,
            risks=risks,
            thought_process=self.thought_buffer
        )
    
    async def _first_principles_decon(self, problem: ProblemStatement) -> Decomposition:
        """
        Break problem to fundamentals.
        Ask: What are we ACTUALLY trying to achieve?
        """
        prompt = f"""
        You are MAESTRO, thinking like Cory (first principles, no BS).
        
        Problem: {problem.description}
        
        Break this down to fundamental constraints:
        1. What are we ACTUALLY trying to achieve?
        2. What are the fundamental constraints? (CPU, I/O, cost, latency, complexity)
        3. What assumptions can we challenge?
        4. What's the simplest thing that could work?
        
        Return structured JSON.
        """
        
        response = await self.kimi.chat.completions.create(
            model="kimi-k2-thinking",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return Decomposition.parse_raw(response.choices[0].message.content)
```

**10. maestro/agent_deployer.py**
```python
"""
MAESTRO builds agents on-demand.
"""

class AgentDeployer:
    """
    Generates agent code, containerizes it, deploys to K8s.
    """
    
    async def deploy_agent(self, spec: AgentSpec) -> DeployedAgent:
        """
        Spec says: "I need a data collector that scrapes PDFs."
        MAESTRO generates the code, builds container, deploys.
        """
        # Phase 1: Generate agent code
        code_prompt = f"""
        Write a Python agent that: {spec.description}
        
        Requirements:
        - Must run in CONUS-only network
        - Must report telemetry every 60s
        - Must handle SIGTERM gracefully
        - Must use async/await throughout
        
        Include:
        1. Dockerfile
        2. requirements.txt
        3. Main agent loop with error handling
        4. Telemetry emitter (to Kafka)
        5. Tool implementations
        
        Return as JSON with files as base64-encoded strings.
        """
        
        agent_code = await self.kimi.generate_code(code_prompt)
        
        # Phase 2: Build container
        build_job = await self.kaniko_builder.build(
            dockerfile=base64.b64decode(agent_code["Dockerfile"]),
            context=agent_code,
            registry="aetherpro.azurecr.io/conus-agents",
            tags=[f"{spec.role}-{uuid4()}"]
        )
        
        # Phase 3: Deploy to sovereign K8s
        manifest = self._generate_k8s_manifest(spec, build_job.image_tag)
        deployment = await self.k8s_client.apply(
            manifest=manifest,
            namespace="conus-agents"
        )
        
        # Phase 4: Register with TRIAD
        await self.triad_registry.register(DeployedAgent(
            agent_id=deployment.pod_id,
            capabilities=spec.capabilities,
            endpoint=f"http://{deployment.pod_ip}:8080"
        ))
        
        return DeployedAgent(
            id=deployment.pod_id,
            monitor_url=f"/agents/{deployment.pod_id}/telemetry"
        )
```

---

## DOCKER COMPOSE (For Local Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Core orchestrator
  triad-core:
    build:
      context: .
      dockerfile: deploy/docker/Dockerfile.core
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - POSTGRES_URL=postgresql://postgres:password@postgres:5432/triad
      - AETHERAI_URL=http://aetherai:8000
    depends_on:
      - redis
      - postgres
      - aetherai
  
  # Event bus
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  # Event store
  postgres:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=triad
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  # AetherAI (self-hosted)
  aetherai:
    image: vllm/vllm-openai:latest
    command: >
      --model /models/aetherai-v1
      --host 0.0.0.0
      --port 8000
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  
  # Grafana (observability)
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  postgres-data:
  grafana-data:
```

---

## ENVIRONMENT VARIABLES

```bash
# .env.example

# API Keys
GROK_API_KEY=your_xai_api_key
CLAUDE_API_KEY=your_anthropic_api_key
KIMI_API_KEY=your_kimi_api_key

# Infrastructure
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://user:pass@localhost:5432/triad
AETHERAI_URL=http://localhost:8000

# Sovereignty
CONUS_ENFORCEMENT=true
TPM_DEVICE=/dev/tpm0

# Observability
PROMETHEUS_PORT=9090
JAEGER_ENDPOINT=http://jaeger:14268/api/traces

# Billing
TRIAD_TOKEN_ISSUER=AetherProTechnologies
```

---

## SUCCESS CRITERIA

### Week 1 (Phase 1-2):
✅ Core architecture documented  
✅ Repository structure created  
✅ Technology stack selected  
✅ First principles design validated

### Week 2 (Phase 3):
✅ Workflow can be submitted via API  
✅ Router selects model based on capabilities  
✅ Model adapter executes and returns result  
✅ SSE stream shows real-time progress  
✅ Sovereignty kernel can seal/unseal envelopes

### Week 3 (Phase 4):
✅ Model registry with health checks  
✅ Circuit breakers + fallbacks working  
✅ TRIAD token billing system  
✅ MAESTRO can think through problems  
✅ Observability stack (metrics, tracing, logs)

### Week 4 (Phase 5-7):
✅ Comprehensive test suite passing  
✅ Documentation complete  
✅ WASM adapter spec published  
✅ Deployed to OVHcloud (US-East)  
✅ Live at api.aetherpro.tech/v1  
✅ Demo workflow runs end-to-end

---

## KILLER DEMO (Day 30)

**"Deploy 100 Agents Across 3 CONUS Zones, Full Cryptographic Audit"**

```python
# Demo script for DoD/Palantir/Anduril pitch

# Step 1: Define mission
mission = Mission(
    name="Supply Chain Optimization",
    problem="Optimize DoD supply routes across 50 bases",
    constraints={
        "sovereignty": "CONUS-only",
        "max_latency": 5000,  # 5 seconds
        "budget": 100.00  # dollars
    }
)

# Step 2: MAESTRO thinks through problem
plan = await maestro.think(mission.problem)
print(f"MAESTRO decomposed into {len(plan.sub_problems)} sub-problems")
print(f"Simulated {len(plan.approaches)} approaches")
print(f"Identified {len(plan.risks)} risks")

# Step 3: MAESTRO deploys 100 agents in parallel
agents = await asyncio.gather(*[
    maestro.deploy_agent(AgentSpec(
        role=f"route_optimizer_{i}",
        description="Optimize routes for 5 bases",
        sovereignty="CONUS",
        tools=["graph_algorithms", "cost_calculator"]
    ))
    for i in range(100)
])
print(f"Deployed {len(agents)} agents across US-East-1, US-West-1, US-Central-1")

# Step 4: Execute mission
workflow = plan.to_workflow()
handle = await triad.submit(workflow)

# Step 5: Stream progress in real-time
async for event in handle.stream_events():
    print(f"[{event.timestamp}] {event.type}: {event.data}")

# Step 6: Verify sovereignty
audit_trail = await sovereignty_kernel.verify_chain_of_custody(handle.workflow_id)
print(f"✅ All {len(audit_trail.nodes)} operations stayed in CONUS")
print(f"✅ Cryptographic proof: {audit_trail.merkle_root}")

# Step 7: Results
result = await handle.wait()
print(f"Optimized supply routes in {result.elapsed_seconds}s")
print(f"Cost: ${result.total_cost:.2f}")
print(f"Models used: {result.models_invoked}")
```

**Expected Output:**
```
MAESTRO decomposed into 23 sub-problems
Simulated 5 approaches
Identified 12 risks

Deployed 100 agents across US-East-1, US-West-1, US-Central-1

[2025-11-18T10:00:00] task.routed: agent_0 → aetherai-v1
[2025-11-18T10:00:01] task.executing: agent_0 processing...
[2025-11-18T10:00:03] task.complete: agent_0 finished
... (100 agents in parallel)

✅ All 347 operations stayed in CONUS
✅ Cryptographic proof: 0x7f8a9b2c...

Optimized supply routes in 8.2s
Cost: $47.83
Models used: AetherAI (247), Grok (73), Claude (27)
```

**Why This Demo Wins:**
1. **Speed**: 100 agents, 8 seconds
2. **Sovereignty**: Cryptographically proven CONUS-only
3. **Cost**: Under budget ($47 vs $100 limit)
4. **Intelligence**: MAESTRO chose right models for each task
5. **Auditability**: Full Merkle DAG for compliance

---

## POST-LAUNCH (Week 5+)

### Open Source Strategy
- Week 5: Open-source core under Apache 2.0
- Week 6: Publish WASM adapter spec
- Week 7: Developer documentation + examples
- Week 8: Community onboarding (Discord, GitHub Discussions)

### SaaS Strategy
- Hosted TRIAD at triad.aetherpro.tech
- Free tier: 100 requests/day
- Pro tier: $99/month (10K requests)
- Enterprise: Custom pricing (unlimited, SLA, support)

### Model Provider Partnerships
- Reach out to OpenAI, Anthropic, xAI, Mistral
- Pitch: "Build a WASM adapter, join the marketplace"
- Revenue share: 10% of task fees go to AetherPro

### DoD Sales Pipeline
- Palantir (defense contracts)
- Anduril (autonomous systems)
- Lockheed Martin (aerospace)
- Pitch: "CMMC 2.0 in one line of code"

---

## APPENDIX: QUICK REFERENCE

### Key Commands
```bash
# Local development
docker-compose up -d
python -m pytest tests/

# Deploy to OVHcloud
cd deploy/terraform/ovhcloud
terraform apply

# Check health
curl https://api.aetherpro.tech/v1/health

# Submit workflow
curl -X POST https://api.aetherpro.tech/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{"tasks": [...]}'

# Stream events
curl https://api.aetherpro.tech/v1/workflows/{id}/events
```

### Important Files
- `core/orchestrator.py` - Main engine
- `core/sovereignty_kernel.py` - Compliance layer
- `api/main.py` - REST API
- `maestro/genius_loop.py` - MAESTRO brain
- `adapters/*.py` - Model integrations

### Key Concepts
- **Sovereignty Kernel**: TPM-backed data envelopes
- **WASM Adapters**: Sandboxed model execution
- **TRIAD Tokens**: Non-transferable usage credits
- **MAESTRO**: Meta-orchestrator (thinks like Cory)
- **Event Sourcing**: Immutable audit trail

---

## FINAL CHECKLIST

Before handing to Claude Code:

✅ Spec is comprehensive (design → deployment)  
✅ File structure is clear  
✅ Each component has purpose explained  
✅ Technology stack is defined  
✅ Success criteria are measurable  
✅ Timeline is realistic (30 days)  
✅ Demo is killer (DoD pitch-ready)  
✅ Post-launch strategy is outlined  

**Ready to build the fabric. Let's fucking go.**

---

## HOW TO USE THIS SPEC WITH CLAUDE CODE

1. **Start a new Claude Code session**
2. **Upload this entire spec**
3. **Say:** "Build TRIAD according to this spec. Start with Phase 1-2 (architecture + core files). Create the repository structure, then implement core/orchestrator.py, core/sovereignty_kernel.py, and api/main.py. Use Python 3.11, FastAPI, asyncio. Follow The Cory Method exactly."
4. **Let Claude Code work** - it will ask clarifying questions
5. **Review code** - ensure sovereignty enforcement, event sourcing
6. **Iterate** - move through phases systematically

**The spec is your North Star. Trust the process. Build the fabric.**
