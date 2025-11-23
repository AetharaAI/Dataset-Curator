# HOW MINIMAX AGENT ACTUALLY WORKS
## Reverse-Engineering the Platform Architecture for AetherForge

---

## EXECUTIVE SUMMARY

MiniMax Agent isn't just M2 with a chat interface - it's a **complete multi-agent orchestration platform** that:
1. Decomposes your prompt into subtasks
2. Spawns specialized sub-agents for each task
3. Coordinates execution across multiple tools
4. Generates downloadable artifacts with internal documentation

**Key Insight**: They use **Multi-Agent Collaboration Protocol (MCP)** to orchestrate specialized agents that work like a development team.

---

## THE ARCHITECTURE (Based on Research)

### Level 1: User Interface Layer

```
agent.minimax.io
├── Chat Interface (like ChatGPT)
├── Agent Mode (builds things)
│   ├── Lightning Mode (fast, simple tasks)
│   └── Pro Mode (complex, multi-step projects)
└── Real-time Progress Display
    ├── Shows what M2 is thinking
    ├── Shows subtask breakdown
    └── Shows tool execution
```

**What You See**:
- User uploads prompt
- M2 analyzes and creates internal plan
- Live updates show: "Creating file structure...", "Writing code...", "Testing..."
- Final artifact with download button

### Level 2: Multi-Agent Orchestration (MCP)

This is the SECRET SAUCE - they don't just use one M2 instance, they spawn multiple specialized agents:

```python
# Conceptual Architecture (based on evidence)
class MinimaxAgentOrchestrator:
    """
    Master orchestrator that spawns specialized sub-agents
    """
    
    def process_request(self, user_prompt: str):
        # Step 1: Master planning with M2
        plan = self.master_agent.decompose_task(user_prompt)
        
        # Step 2: Spawn specialized agents
        agents = {
            "coder": CoderAgent(model="minimax-m2"),
            "designer": DesignerAgent(model="lovable"),  # Specialized for UI
            "project_manager": PMAgent(model="manis"),   # Coordination
            "tester": TesterAgent(model="minimax-m2")
        }
        
        # Step 3: Execute in parallel/sequence
        results = self.coordinate_agents(agents, plan)
        
        # Step 4: Integrate and deliver
        final_artifact = self.integrate_results(results)
        
        return final_artifact
```

**Evidence from Research**:
> "The platform uses specialized AI helpers, like 'Lovable' for front-end look and 'Manis' for app behavior"

> "The coder builds functionality... The designer manages visual elements... The project manager keeps everyone on track"

> "MiniMax Agent uses Multi-Agent Collaboration Protocol (MCP), which means it spins up different specialized 'sub-agents' that actually chat with each other"

### Level 3: Tool Execution Layer

Each agent has access to **real tools**:

```python
AVAILABLE_TOOLS = {
    # Code execution
    "shell": ShellExecutor(),          # Run bash commands
    "python": PythonInterpreter(),     # Execute Python code
    "browser": BrowserAutomation(),    # Web scraping, testing
    
    # File operations
    "file_create": FileCreator(),
    "file_edit": FileEditor(),
    "file_read": FileReader(),
    
    # Testing
    "test_runner": TestRunner(),       # Run unit tests
    "linter": CodeLinter(),            # Check code quality
    
    # Deployment
    "build": BuildSystem(),            # Compile/bundle
    "preview": LivePreview(),          # Generate preview URL
    
    # MCP Marketplace
    "external_apis": MCPConnector(),   # Connect to external services
    
    # Multimodal (MiniMax Suite)
    "image_gen": ImageGenerator(),
    "video_gen": VideoGenerator(),
    "audio_gen": AudioGenerator(),
    "voice_clone": VoiceCloner()
}
```

**How They Use Tools** (from evidence):
> "It can independently execute code, identify errors, and suggest or implement test-validated fixes"

> "Native support for Shell, Browser, Python interpreter, and MCP tools"

> "The AI even finds missing functions during testing and fixes them"

### Level 4: Artifact Generation System

This is how they create downloadable projects:

```python
class ArtifactGenerator:
    """
    Generates complete project with documentation
    """
    
    def create_artifact(self, execution_results):
        artifact = ProjectArtifact()
        
        # 1. Source code files
        artifact.add_source_files(execution_results.code_files)
        
        # 2. Internal documentation (the "thoughts" and "notes")
        artifact.add_docs({
            "ANALYSIS.md": execution_results.initial_analysis,
            "ARCHITECTURE.md": execution_results.system_design,
            "TODO.md": execution_results.future_improvements,
            "IMPLEMENTATION_NOTES.md": execution_results.decisions_made
        })
        
        # 3. Test files
        artifact.add_tests(execution_results.test_files)
        
        # 4. Config files
        artifact.add_configs({
            "package.json": execution_results.dependencies,
            "README.md": execution_results.usage_guide,
            ".env.example": execution_results.env_template
        })
        
        # 5. Generated assets (if multimodal)
        if execution_results.has_media:
            artifact.add_assets(execution_results.images, 
                               execution_results.audio,
                               execution_results.videos)
        
        # 6. Zip everything
        return artifact.to_zip()
```

**What You Get** (based on user reports):
> "Everything comes with instructions and a to-do list for future updates"

> "Download full code, then tweak colors or features as your business grows"

> "I can download his 'thoughts' and 'notes' with the finished project"

---

## THE WORKFLOW (Step-by-Step)

### User Submits Prompt

```
"Build a Netflix clone with user authentication, video streaming, 
and recommendation engine"
```

### M2 Master Agent: Planning Phase

```markdown
<think>
This requires:
1. Frontend (React/Next.js)
   - Landing page
   - Auth pages (login/signup)
   - Video player
   - Browse interface
   - User profile
   
2. Backend (Node.js/Express or Python/FastAPI)
   - User auth (JWT)
   - Video streaming API
   - Recommendation algorithm
   - Database (PostgreSQL)
   
3. Assets
   - Logo and branding
   - Sample video content
   - UI components
   
4. Testing
   - Unit tests for auth
   - Integration tests for streaming
   - E2E tests for user flow

I'll spawn:
- Coder Agent (for main implementation)
- Designer Agent (for UI/UX)
- Test Agent (for quality assurance)
- PM Agent (for coordination)
</think>

Breaking down into 12 subtasks:
1. Initialize project structure ✓
2. Set up authentication system ⏳
3. Implement video player...
```

### Agent Coordination: Execution Phase

**Parallel Execution**:

```
Coder Agent:
  ├─ Creates file structure
  ├─ Implements auth logic
  ├─ Builds video streaming API
  └─ Integrates recommendation engine

Designer Agent (Lovable):
  ├─ Designs landing page
  ├─ Creates component library
  ├─ Generates logo/branding
  └─ Ensures responsive design

Test Agent:
  ├─ Writes unit tests
  ├─ Runs integration tests
  ├─ Identifies bugs
  └─ Validates fixes

PM Agent (Manis):
  ├─ Coordinates agent communication
  ├─ Tracks progress
  ├─ Resolves conflicts
  └─ Ensures completeness
```

### Tool Execution: Real Work

```bash
# Coder Agent using Shell tool
$ npm create vite@latest netflix-clone --template react-ts
$ cd netflix-clone
$ npm install express jsonwebtoken bcrypt prisma

# Coder Agent using File Create tool
[Creating: src/components/VideoPlayer.tsx]
[Creating: src/pages/Browse.tsx]
[Creating: backend/server.ts]

# Coder Agent using Python tool (for recommendation engine)
[Running: recommendation_model.py]
[Output: Model trained, accuracy: 87%]

# Test Agent using Test Runner
$ npm run test
[Output: 47 tests passed, 2 failed]

# Test Agent analyzes failures and calls Coder Agent
[Requesting: Fix authentication edge case]

# Coder Agent fixes and re-tests
[Fixed: Auth now handles expired tokens]
$ npm run test
[Output: 49 tests passed]

# Designer Agent uses Image Generation
[Generating: Netflix-style logo with custom colors]
[Generating: Hero banner images]

# PM Agent checks progress
[Status: 92% complete, 1 subtask remaining]
```

### Integration Phase

```python
# PM Agent coordinates final integration
integration_status = {
    "frontend": "✓ Complete",
    "backend": "✓ Complete",
    "database": "✓ Seeded with sample data",
    "tests": "✓ All passing",
    "documentation": "✓ Generated",
    "deployment": "⏳ Creating preview"
}

# Generate preview URL
preview_url = deploy_to_vercel(project)
# Returns: https://netflix-clone-abc123.vercel.app
```

### Artifact Packaging

```
netflix-clone/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── docs/
│   ├── ANALYSIS.md          ← M2's initial analysis of prompt
│   ├── ARCHITECTURE.md      ← System design decisions
│   ├── TODO.md              ← Future improvements
│   └── NOTES.md             ← Implementation notes
├── assets/
│   ├── logo.png
│   └── screenshots/
├── .env.example
└── DEPLOYMENT_GUIDE.md
```

---

## THE KEY INNOVATIONS

### 1. Multi-Agent Orchestration (MCP)

**Traditional Approach** (like ChatGPT Code Interpreter):
```
User → Single LLM → Tool → Single LLM → Output
```

**MiniMax Agent Approach**:
```
User → Master Agent (M2) → Task Decomposition
                ↓
        ┌───────┴───────┬───────────┬─────────┐
        ↓               ↓           ↓         ↓
    Coder Agent    Designer     Tester    PM Agent
        ↓               ↓           ↓         ↓
     [Tools]        [Tools]     [Tools]   [Coordination]
        ↓               ↓           ↓         ↓
        └───────┬───────┴───────────┴─────────┘
                ↓
         Integration Layer
                ↓
          Final Artifact
```

**Why This Works Better**:
- Parallel execution (faster)
- Specialized expertise per agent
- Better quality through division of labor
- Graceful error recovery (agents can retry independently)

### 2. Interleaved Thinking Preservation

M2's `<think>` blocks are KEPT throughout the process:

```
Agent Communication Example:

Coder Agent: <think>
User wants Netflix clone. I'll use Next.js for frontend.
Need to implement:
- Auth with JWT
- Video streaming with HLS
- Recommendation with collaborative filtering
</think>
Let me start with the project structure...

Designer Agent: <think>
Coder is using Next.js. I'll create Tailwind components
that match Netflix's dark theme with red accents.
</think>
Creating landing page with hero section...

PM Agent: <think>
Coder is 60% done, Designer is 40% done.
Need to sync on component naming conventions.
</think>
@Coder, @Designer: Let's align on button component names...
```

**This is why M2 works so well** - the thinking context is preserved across ALL agents in the orchestration!

### 3. Compile-Run-Fix Loops

```python
class AutoFixLoop:
    """
    Automated testing and fixing
    """
    
    def execute(self, code_files):
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            # Run tests
            test_results = self.test_runner.run(code_files)
            
            if test_results.all_passed:
                break
            
            # Analyze failures
            failures = test_results.get_failures()
            
            # Ask Coder Agent to fix
            fixes = self.coder_agent.fix_issues(
                code_files, 
                failures,
                context=test_results.full_output
            )
            
            # Apply fixes
            code_files = self.apply_fixes(code_files, fixes)
            
            iteration += 1
        
        return code_files, test_results
```

**Evidence**:
> "A standout feature is its ability to independently execute code, identify errors, and suggest or implement test-validated fixes"

> "The AI even finds missing functions during testing and fixes them"

### 4. Real-Time Progress Streaming

```typescript
// WebSocket connection to show live progress
socket.on('agent_update', (data) => {
  switch (data.type) {
    case 'thinking':
      showThinking(data.content);  // Show <think> block
      break;
    case 'subtask_start':
      updateProgress(data.subtask, 'in_progress');
      break;
    case 'subtask_complete':
      updateProgress(data.subtask, 'complete');
      break;
    case 'tool_execution':
      showToolOutput(data.tool, data.output);
      break;
    case 'agent_communication':
      showAgentChat(data.from_agent, data.to_agent, data.message);
      break;
  }
});
```

**User Experience**:
```
✓ Analyzed requirements
⏳ Creating project structure...
  ├─ ✓ Frontend scaffolding
  ├─ ✓ Backend setup
  └─ ⏳ Database schema
✓ Implementing authentication
⏳ Building video player...
  Tool: file_create (VideoPlayer.tsx)
  Tool: npm install (video-react)
  Tool: test (VideoPlayer.test.tsx)
    Failed: Missing prop validation
    Fixing...
    ✓ Fixed
⏳ Testing complete application...
✓ All tests passing
✓ Generating documentation
✓ Creating deployment preview
Done! Download your project below.
```

---

## HOW TO REPLICATE THIS FOR AETHERFORGE

### Architecture Blueprint

```python
# backend/app/core/orchestration/conductor.py
class AgentConductor:
    """
    Orchestrates multiple agents for complex tasks
    """
    
    def __init__(self):
        self.master_agent = MiniMaxM2Client()
        self.agent_pool = {
            "coder": AgentWorker("minimax-m2", "coding"),
            "designer": AgentWorker("minimax-m2", "ui/ux"),
            "tester": AgentWorker("minimax-m2", "testing"),
            "researcher": AgentWorker("claude-sonnet-4.5", "research"),
            "pm": AgentWorker("minimax-m2", "coordination")
        }
        self.tool_registry = ToolRegistry.get_all_tools()
    
    async def execute_complex_task(
        self,
        user_prompt: str,
        user_id: str
    ) -> Artifact:
        """
        Main orchestration method
        """
        
        # Phase 1: Planning
        plan = await self.master_agent.create_plan(user_prompt)
        
        # Phase 2: Agent Assignment
        agent_assignments = self.assign_agents_to_subtasks(
            plan.subtasks
        )
        
        # Phase 3: Parallel Execution
        results = await self.execute_agents_in_parallel(
            agent_assignments
        )
        
        # Phase 4: Integration
        artifact = self.create_artifact(
            results,
            user_id,
            include_documentation=True
        )
        
        # Phase 5: Testing & Validation
        validated_artifact = await self.validate_and_fix(artifact)
        
        return validated_artifact
    
    async def execute_agents_in_parallel(
        self,
        assignments: List[AgentAssignment]
    ):
        """
        Run multiple agents concurrently
        """
        tasks = []
        
        for assignment in assignments:
            agent = self.agent_pool[assignment.agent_type]
            task = asyncio.create_task(
                agent.execute(
                    assignment.subtask,
                    tools=assignment.required_tools,
                    context=assignment.context
                )
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
```

### Agent Communication Protocol

```python
# backend/app/core/orchestration/communication.py
class AgentMessage:
    """
    Message format for inter-agent communication
    """
    from_agent: str
    to_agent: str
    message_type: str  # "request", "response", "status", "error"
    content: str
    thinking: Optional[str]  # Preserve <think> blocks
    attachments: Optional[List[File]]

class AgentBus:
    """
    Message bus for agent communication
    """
    
    def __init__(self):
        self.subscribers = {}
        self.message_history = []
    
    async def publish(self, message: AgentMessage):
        """
        Broadcast message to relevant agents
        """
        self.message_history.append(message)
        
        # Deliver to recipient
        if message.to_agent in self.subscribers:
            await self.subscribers[message.to_agent].receive(message)
        
        # Also notify PM agent for coordination
        if message.to_agent != "pm":
            await self.subscribers["pm"].receive(message)
    
    def subscribe(self, agent_id: str, handler: callable):
        """
        Agent registers to receive messages
        """
        self.subscribers[agent_id] = handler
```

### Real-Time Progress Streaming

```python
# backend/app/api/v1/orchestration.py
@router.post("/complex-task")
async def execute_complex_task(request: ComplexTaskRequest):
    """
    Execute multi-agent orchestrated task with real-time updates
    """
    
    async def generate_updates():
        # Create conductor
        conductor = AgentConductor()
        
        # Subscribe to conductor events
        async for event in conductor.execute_with_updates(
            request.prompt,
            request.user_id
        ):
            # Stream each event to client
            yield f"data: {json.dumps(event.dict())}\n\n"
        
        # Final artifact
        artifact = await conductor.get_artifact()
        yield f"data: {json.dumps({
            'type': 'complete',
            'artifact_url': artifact.download_url
        })}\n\n"
    
    return StreamingResponse(
        generate_updates(),
        media_type="text/event-stream"
    )
```

### Artifact Documentation Generator

```python
# backend/app/core/orchestration/documentation.py
class DocumentationGenerator:
    """
    Generates internal documentation from agent execution
    """
    
    def create_analysis_doc(self, planning_phase: PlanningResult):
        """
        ANALYSIS.md - What M2 understood from the prompt
        """
        return f"""# Project Analysis

## User Request
{planning_phase.original_prompt}

## Understanding
{planning_phase.interpretation}

## Scope
{planning_phase.scope}

## Assumptions Made
{planning_phase.assumptions}

## Key Requirements Identified
{planning_phase.requirements}
"""
    
    def create_architecture_doc(self, execution_results: List[AgentResult]):
        """
        ARCHITECTURE.md - System design decisions
        """
        return f"""# System Architecture

## Tech Stack Chosen
{execution_results.tech_stack}

## Component Structure
{execution_results.component_tree}

## Design Patterns Used
{execution_results.patterns}

## Data Flow
{execution_results.data_flow_diagram}

## Rationale
{execution_results.design_decisions}
"""
    
    def create_todo_doc(self, validation_results: ValidationResult):
        """
        TODO.md - Future improvements
        """
        return f"""# Future Improvements

## Known Limitations
{validation_results.limitations}

## Suggested Enhancements
{validation_results.enhancements}

## Scalability Considerations
{validation_results.scalability_notes}

## Security Hardening
{validation_results.security_todos}
"""
```

---

## IMPLEMENTATION ROADMAP FOR AETHERFORGE

### Phase 1: Basic Agent Orchestration
- [ ] Build AgentConductor class
- [ ] Implement agent assignment logic
- [ ] Create agent communication bus
- [ ] Test with 2-3 simple agents

### Phase 2: Tool Integration
- [ ] Connect all computer use tools
- [ ] Add MiniMax multimodal tools
- [ ] Implement tool result parsing
- [ ] Add error recovery logic

### Phase 3: Real-Time Streaming
- [ ] WebSocket/SSE implementation
- [ ] Progress tracking system
- [ ] Live log streaming
- [ ] Agent communication display

### Phase 4: Artifact Generation
- [ ] Project packaging system
- [ ] Documentation generator
- [ ] Download link creation
- [ ] Version control integration

### Phase 5: Testing & Validation
- [ ] Auto-test generation
- [ ] Compile-run-fix loops
- [ ] Quality assurance agent
- [ ] Performance validation

---

## KEY LESSONS FOR AETHERFORGE

### 1. Don't Try to Do Everything in One Prompt
MiniMax Agent's power comes from **decomposition** - break complex tasks into subtasks and assign to specialized agents.

### 2. Preserve Thinking Context
Keep M2's `<think>` blocks throughout the entire orchestration - this maintains reasoning continuity.

### 3. Real Tools Are Essential
Don't just generate code - RUN IT, TEST IT, FIX IT. Users trust systems that deliver working artifacts.

### 4. Documentation Is a Feature
Including M2's analysis, architecture decisions, and TODOs makes the artifacts actually useful.

### 5. Parallel Execution Scales
Running multiple agents concurrently is how they deliver complex projects in <5 minutes.

---

## WHAT MAKES MINIMAX AGENT SPECIAL

1. **Multi-Agent Orchestration**: Not just one M2, but a team of specialized agents
2. **Real Tool Execution**: Actually runs code, tests, and fixes
3. **MCP Integration**: Connects to external services seamlessly
4. **Thinking Preservation**: Maintains reasoning context across agents
5. **Production Artifacts**: Delivers complete, documented, working projects

**Bottom Line**: MiniMax Agent is basically **GitHub Copilot Workspace + Bolt.ai + Claude Projects combined**, but with M2's speed and cost efficiency.

---

## FINAL RECOMMENDATIONS FOR YOUR BUILDER

### For AetherInterface "App Builder"

**Core Features to Add**:
1. Multi-agent orchestration (master + worker agents)
2. Real-time progress streaming
3. Automated testing & fixing loops
4. Documentation generation
5. Downloadable artifacts with project structure

**Architecture**:
```
User Prompt → Master Agent (Planning)
                    ↓
        ┌───────────┼───────────┐
    Coder       Designer      Tester
        ↓           ↓           ↓
    [Tools]     [Tools]     [Tools]
        ↓           ↓           ↓
        └───────────┼───────────┘
                    ↓
          Integration Layer
                    ↓
    Complete Project + Docs
```

### For AetherStudio (Future)

**Positioning**: "MiniMax Agent for AetherPro Ecosystem"
- Built on AetherForge foundation
- Multi-agent orchestration native
- Integration with AetherAgent Forge marketplace
- Custom agent specializations for different industries

**Differentiators**:
- Your ecosystem integration
- Customizable agent specializations
- On-premise deployment option
- White-label capabilities

---

**You're building something BETTER than MiniMax Agent because you'll have:**
1. ✅ AetherForge as the foundation (Dual-LLM already)
2. ✅ Computer use built-in (like Claude)
3. ✅ Multimodal generation (like MiniMax)
4. ✅ Multi-agent orchestration (this document shows you how)
5. ✅ Your own brand ecosystem

**This is HUGE. You're combining the best of all worlds.** 🚀
