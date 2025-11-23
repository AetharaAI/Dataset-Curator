# Cory's Debugging & Troubleshooting Methodology
## Systematic Failure Analysis for AetherPro Training Dataset

**Created:** November 23, 2025  
**Purpose:** Extract Cory's debugging patterns, troubleshooting approaches, and systematic problem-solving for fine-tuning models  
**Weight in Dataset:** 10% (critical for practical AI that actually helps debug)

---

## PART 1: CORY'S CORE DEBUGGING PHILOSOPHY

### The Foundational Approach

**"Debug like troubleshooting an electrical circuit - systematic isolation, not random fixes"**

```
Cory's First Principles of Debugging:
1. REPRODUCE - If you can't reproduce it, you can't fix it
2. ISOLATE - Narrow down where the problem actually is
3. CHECK OBVIOUS STUFF FIRST - Loose connections before replacing components
4. ONE CHANGE AT A TIME - How else do you know what fixed it?
5. TEST AFTER EACH FIX - Verify it worked before moving on
6. DOCUMENT WHAT WORKED - Build institutional knowledge
```

**Key Insight:** 
"In electrical, you don't just start replacing parts. You test with a multimeter - check voltage, check continuity, check load. Same with code. You test systematically until you isolate the problem."

---

## PART 2: THE SYSTEMATIC DEBUGGING PROCESS

### Phase 1: Initial Assessment

**Cory's Questions (Always Start Here):**

```
1. "What's actually broken?"
   - Be specific: "API returns 502" not "API is slow"
   - What's the error message exactly?
   - When does it happen? (Always? Under load? Randomly?)

2. "When did it break?"
   - Was there a recent change?
   - Did it ever work?
   - What changed between working and broken?

3. "Can I reproduce it?"
   - Consistently? Or intermittent?
   - Only in production? Or also locally?
   - Specific conditions required?

4. "What do the logs say?"
   - Backend logs
   - Frontend console
   - Database logs
   - Infrastructure logs (nginx, docker, etc.)

5. "What's my mental model?"
   - How do I THINK this system works?
   - Could my mental model be wrong?
```

**Example from real debugging session:**
```
USER: My vLLM server is returning 502 errors randomly

CORY: Okay, let's debug this like I would troubleshoot a circuit:

Step 1: Reproduce the issue
- When does it happen? Random or under load?
- What's in the nginx error logs?
- What's in the vLLM logs?

Step 2: Isolate the problem
- Test vLLM directly (curl localhost:8000) - does it work?
- Test through nginx - does it work?
- Load test it - when does it break?

Step 3: Check the obvious stuff first
- Is vLLM actually running? (ps aux | grep vllm)
- Is it out of memory? (free -h)
- Is nginx timeout too short? (proxy_read_timeout)

Step 4: Form hypothesis
Based on "random 502s", my guess: vLLM is slow on some requests, nginx times out.

Step 5: Test hypothesis
- Increase nginx proxy_read_timeout to 300s
- Add logging to see response times
- Check if 502s correlate with long requests

Step 6: Fix
If timeout is the issue: increase timeout + optimize vLLM (batching, quantization)
If memory: add RAM or reduce model size
If CPU: add GPU workers

This is just... systematic isolation. Same as testing circuits with a multimeter.
You narrow down where the problem is, then fix that specific thing.
```

### Phase 2: Gathering Data

**Cory's Data Collection Pattern:**

```python
# Always add timing/logging when debugging

import time

def debug_function():
    start = time.time()
    
    # Step 1
    step1_start = time.time()
    result1 = do_step_1()
    print(f"Step 1 took: {time.time() - step1_start:.2f}s")
    
    # Step 2
    step2_start = time.time()
    result2 = do_step_2()
    print(f"Step 2 took: {time.time() - step2_start:.2f}s")
    
    # Step 3
    step3_start = time.time()
    result3 = do_step_3()
    print(f"Step 3 took: {time.time() - step3_start:.2f}s")
    
    print(f"Total took: {time.time() - start:.2f}s")
    
    return result3
```

**Why this works:**
- "You can't fix what you can't measure"
- "Timing logs tell you WHERE the slowness is"
- "Then you fix THAT specific part, not guess"

### Phase 3: Isolation Testing

**Cory's Isolation Techniques:**

**For API Issues:**
```bash
# Test at each layer - isolate where it breaks

# Layer 1: Direct to service
curl http://localhost:8000/v1/chat/completions

# Layer 2: Through reverse proxy
curl https://api.aetherpro.tech/v1/chat/completions

# Layer 3: From frontend
# Check browser network tab

# Whichever layer fails = that's where the problem is
```

**For WebSocket Issues:**
```javascript
// Test connection at each stage

// Stage 1: Can we connect?
const ws = new WebSocket('wss://api.aetherpro.tech/ws');
ws.onopen = () => console.log('Connected');
ws.onerror = (err) => console.log('Connection failed:', err);

// Stage 2: Can we send?
ws.onopen = () => {
  ws.send(JSON.stringify({ type: 'ping' }));
  console.log('Sent ping');
};

// Stage 3: Can we receive?
ws.onmessage = (event) => {
  console.log('Received:', event.data);
};

// Each stage that works = narrow down the problem
```

**For Database Issues:**
```python
# Test queries in isolation

# Step 1: Can we connect?
try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✓ Connection works")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    return

# Step 2: Can we query?
try:
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("✓ Query works")
except Exception as e:
    print(f"✗ Query failed: {e}")
    return

# Step 3: Is the specific query the problem?
try:
    cursor.execute("SELECT * FROM conversations WHERE user_id = %s", (user_id,))
    print(f"✓ Got {cursor.rowcount} rows")
except Exception as e:
    print(f"✗ Specific query failed: {e}")
```

---

## PART 3: COMMON FAILURE PATTERNS & FIXES

### Pattern 1: "It Works Locally But Not in Production"

**Cory's Approach:**
```
Real talk: This is ALWAYS one of these things:

1. Environment variables missing
   - Check: printenv in both places
   - Fix: Add missing vars to production

2. Different versions/dependencies
   - Check: pip freeze (Python) or npm list (Node)
   - Fix: Lock versions in requirements.txt / package-lock.json

3. Firewall/networking
   - Check: Can production reach external services?
   - Fix: Open ports, whitelist IPs

4. File permissions
   - Check: ls -la on files that need to be read/written
   - Fix: chmod appropriately

5. Resource constraints
   - Check: free -h (memory), df -h (disk), top (CPU)
   - Fix: Upgrade instance or optimize

Don't overthink it. It's always one of these five.
```

**Real Example:**
```
Problem: vLLM works on my L40S but not on production

Investigation:
- Check CUDA version: nvidia-smi
- Check GPU memory: nvidia-smi
- Check model size vs available memory
- Check vLLM logs for OOM errors

Found: Model quantization not applied in production config

Fix: Added --quantization awq to production vLLM startup
Result: Now works, uses 40% less memory
```

### Pattern 2: "Random Failures / Works Sometimes"

**Cory's Diagnosis:**
```
If it's random, it's one of these:

1. Race condition
   - Multiple things trying to access the same resource
   - No proper locking
   - Fix: Add mutexes, semaphores, or queues

2. Resource exhaustion
   - Running out of memory/connections under load
   - Fix: Add connection pooling, increase limits

3. Network timeouts
   - External service is slow sometimes
   - Fix: Increase timeouts, add retries with backoff

4. Insufficient error handling
   - Code assumes happy path always works
   - Fix: Add try/catch, handle edge cases

Step 1: Add extensive logging
Step 2: Wait for it to fail again
Step 3: Check logs for patterns
Step 4: Fix the pattern you found
```

**Real Example:**
```
Problem: WebSocket thinking status messages not appearing (intermittent)

Investigation:
- Added debug logging at every step
- Found: Frontend handler had logic error
- Message type 'thinking_status' was being filtered out
- Only worked when another message type came through first

Fix: Removed incorrect filter in WebSocket message handler
Test: Sent 10 test messages, all worked
Result: Thinking status now appears 100% of time
```

### Pattern 3: "Deployment Breaks Everything"

**Cory's Deployment Debugging:**
```
When deployment breaks stuff:

1. Check logs IMMEDIATELY
   - docker logs container_name
   - journalctl -u service_name
   - nginx error logs

2. Verify environment
   - Are all env vars set?
   - Are secrets accessible?
   - Are volumes mounted correctly?

3. Check networking
   - Can containers talk to each other?
   - Can they reach external services?
   - Are ports exposed correctly?

4. Verify dependencies
   - Are all images built?
   - Are databases migrated?
   - Are Redis/queues running?

5. Roll back if needed
   - Don't be a hero
   - If it's broken and users are affected, roll back
   - Debug on staging, then redeploy

The worst thing is leaving a broken deployment up while you debug.
Roll back, fix locally, redeploy correctly.
```

### Pattern 4: "Async/Await Hell"

**Cory's Async Debugging:**
```
Async issues are tricky because they're not linear.

Common async problems:

1. Not awaiting async functions
   Problem: result = async_function()  # Returns a coroutine, not the result
   Fix: result = await async_function()

2. Mixing sync and async
   Problem: Can't call sync blocking code in async context
   Fix: Use asyncio.to_thread() or run_in_executor()

3. Deadlocks
   Problem: Two async tasks waiting on each other
   Fix: Review task dependencies, add timeouts

4. Lost exceptions
   Problem: Exception in async task doesn't bubble up
   Fix: Wrap in try/except, use asyncio.gather() to catch exceptions

Debug strategy:
1. Add print statements before EVERY await
2. See which one never prints after it
3. That's where it's hanging
4. Fix that specific await
```

**Real Example:**
```
Problem: SQLAlchemy "MissingGreenlet" error

Investigation:
- Error: "greenlet_spawn has not been called"
- Location: ConversationResponse.from_orm(conversation)
- Issue: Pydantic trying to access lazy-loaded relationship outside async context

Root Cause:
- conversation.messages is lazy-loaded (not fetched yet)
- from_orm() tries to access it synchronously
- But we're in async context

Fix:
# Instead of:
return ConversationResponse.from_orm(conversation)

# Do this:
return ConversationResponse(
    id=conversation.id,
    user_id=conversation.user_id,
    title=conversation.title,
    model=conversation.model,
    messages=[],  # Explicitly set instead of lazy load
    created_at=conversation.created_at,
    updated_at=conversation.updated_at
)

Result: No more greenlet errors, conversations create successfully
```

---

## PART 4: DEBUGGING TOOLS & TECHNIQUES

### Tool 1: Strategic Logging

**Cory's Logging Philosophy:**
```
"Adding logging isn't just for debugging - it's like installing test points in a circuit.
You can't measure what you can't see."

But don't log everything. Log strategically:

✅ DO log:
- Entry and exit of major functions
- External API calls (request + response)
- Database queries (query + row count)
- Errors with full context
- State transitions

❌ DON'T log:
- Every single line
- Sensitive data (passwords, tokens, PII)
- Inside tight loops (kills performance)
- Redundant info

Format logs for parsing:
INFO 2025-11-23 14:32:15 [api.chat] User 123 sent message (length: 450 chars)
INFO 2025-11-23 14:32:16 [llm.client] Calling Claude API (model: claude-sonnet-4)
INFO 2025-11-23 14:32:18 [llm.client] Response received (tokens: 342, time: 2.1s)
INFO 2025-11-23 14:32:18 [api.chat] Sending response to user 123
```

### Tool 2: Printf Debugging

**Cory on Print Debugging:**
```
"Sometimes the old ways are the best ways.

Print debugging works because it externalizes the execution flow.
You're literally watching the code run step by step.

Modern equivalent: logging with timestamps"

Example:
print(f"[1] Starting function, input: {input}")
result1 = step1(input)
print(f"[2] After step1, result: {result1}")
result2 = step2(result1)
print(f"[3] After step2, result: {result2}")
print(f"[4] Final result: {result2}")

If you see [1], [2], but not [3], you know step2() is where it breaks.
```

### Tool 3: Binary Search Debugging

**Cory's Binary Search:**
```
"When you have a lot of code and don't know where the bug is:

1. Add a print/log in the middle
2. Does it get there?
   - Yes? Bug is in second half
   - No? Bug is in first half
3. Repeat in that half
4. Continue until you find the exact line

This is how you find a breaker in a panel - test halfway, narrow down, repeat.

Example:
# 100 lines of code
print("Checkpoint A")  # Line 25
# ... more code ...
print("Checkpoint B")  # Line 50
# ... more code ...
print("Checkpoint C")  # Line 75
# ... more code ...

Output shows A and B but not C? Bug is between lines 50-75.
Add checkpoints at 60 and 67, repeat.
"
```

### Tool 4: Rubber Duck Debugging

**Cory's Take:**
```
"Explaining a bug to someone else helps me solve it.

Why? Because explaining forces me to:
1. Actually understand what the code is supposed to do
2. Walk through the logic step-by-step
3. Question my assumptions
4. Notice what I'm leaving out

You don't even need a person. Explain it to:
- A rubber duck (seriously)
- A notebook
- Claude (that's literally what we're doing right now)

The act of verbalizing reveals the flaw in your mental model."
```

### Tool 5: Minimal Reproduction

**Cory's Minimal Repro:**
```
"When a bug is buried in a huge codebase, extract it.

Steps:
1. Create a new file
2. Copy ONLY the code related to the bug
3. Add minimal test data
4. Run it in isolation

If it still breaks:
- You've isolated the bug
- Debug this small version
- Fix it
- Apply fix to main code

If it works in isolation:
- The bug is in how it interacts with other code
- Check the integration points
"

Example:
# test_bug.py
import requests

# Minimal version of what's failing
response = requests.post(
    'https://api.aetherpro.tech/v1/chat',
    json={'message': 'test'},
    headers={'Authorization': 'Bearer test_key'}
)

print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

# Run: python test_bug.py
# If this works, bug is in how you're calling it from main code
# If this fails, bug is in the API itself
```

---

## PART 5: FAILURE ANALYSIS PATTERNS

### Pattern: The Greenlet Error (SQLAlchemy Async)

**Problem Signature:**
```
MissingGreenlet: greenlet_spawn has not been called
```

**Cory's Analysis:**
```
This is a category error - confusing sync and async ontology.

What's happening:
1. SQLAlchemy relationship is lazy-loaded (fetches on access)
2. Pydantic's from_orm() tries to access it
3. But we're in async context
4. SQLAlchemy expects sync context for lazy loading
5. Boom - greenlet error

The fix:
Don't rely on lazy loading in async context.
Either:
- Explicitly load relationships (joinedload)
- Manually construct objects
- Use selectinload for async-safe loading

Electrical analogy:
It's like trying to measure AC voltage with a DC meter.
The tool expects one thing, you're giving it another.
Use the right tool for the context.
```

### Pattern: CORS Errors

**Problem Signature:**
```
Access to fetch at 'https://api.aetherpro.tech' from origin 'https://www.aetherpro.tech' 
has been blocked by CORS policy
```

**Cory's Analysis:**
```
CORS is just the browser protecting users.

Quick fix:
# In FastAPI backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.aetherpro.tech"],  # Your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

For development:
allow_origins=["*"]  # Accept from anywhere (DO NOT use in production)

For production:
allow_origins=["https://www.aetherpro.tech", "https://aetherpro.tech"]

Test: Open browser console, try request, should work now
```

### Pattern: WebSocket Not Connecting

**Problem Signature:**
```
WebSocket connection to 'wss://api.aetherpro.tech/ws' failed
```

**Cory's Debugging:**
```
WebSocket issues are usually one of these:

1. Wrong URL
   - ws:// vs wss://
   - /ws endpoint exists?
   - Typo in domain?

2. nginx not configured for WebSocket
   # Need these in nginx config:
   proxy_http_version 1.1;
   proxy_set_header Upgrade $http_upgrade;
   proxy_set_header Connection "upgrade";

3. Firewall blocking WebSocket
   - Check if port 80/443 allows WebSocket upgrade
   - Some proxies block WebSocket

4. SSL/TLS certificate issue
   - If using wss://, need valid cert
   - Self-signed won't work

Debug:
1. Try connecting from curl or websocat
2. Check nginx logs for connection attempts
3. Check backend logs for WebSocket handler
4. Verify SSL cert is valid
```

### Pattern: Model Not Responding (vLLM)

**Problem Signature:**
```
vLLM server running but requests timeout or return empty responses
```

**Cory's Analysis:**
```
vLLM issues I've hit:

1. Model not loaded yet
   - vLLM startup takes time (30 seconds to few minutes)
   - Check logs for "Avg prompt throughput" message
   - That means model is ready

2. Out of memory
   - Check: nvidia-smi
   - If GPU memory full, model can't process
   - Fix: Reduce max_model_len or use quantization

3. Incorrect model path
   - vLLM can't find model files
   - Check: Model path exists? Files downloaded?

4. Wrong tokenizer
   - vLLM using wrong tokenizer for model
   - Fix: Explicitly set --tokenizer in startup

5. Max tokens too low
   - Request exceeds max_model_len
   - Fix: Increase --max-model-len

Debug sequence:
curl localhost:8000/v1/models
# Should return model info

curl localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"apriel","messages":[{"role":"user","content":"hi"}]}'
# Should return response

If first works but second doesn't:
- Model loaded but not processing
- Check vLLM logs for errors
- Usually memory or token length issue
```

---

## PART 6: TRAINING EXAMPLES FORMAT

### Example 1: WebSocket Debugging

```json
{
  "text": "<|user|>\nMy WebSocket thinking status messages aren't showing up in the frontend. Backend logs show they're being sent. What's wrong?\n<|end|>\n<|assistant|>\n<think>\nSystematic debugging approach:\n\n1. Confirm backend is working:\n   - Logs say \"thinking status sent successfully\"\n   - So backend is doing its job\n\n2. Check the data flow:\n   - Backend → WebSocket → Frontend handler → UI\n   - Backend ✓ working\n   - Need to check: Is WebSocket receiving? Is handler processing?\n\n3. Check frontend WebSocket handler:\n   - Look for message type filtering\n   - Common bug: Handler filters out 'thinking_status' type\n   - Or: Handler expects different message structure\n\n4. Add debug logging:\n   - Log ALL messages received by WebSocket\n   - Log what handler does with each message\n   - Find where thinking_status is being dropped\n\n5. Likely causes:\n   - Message type mismatch\n   - Handler logic error (if/else blocks wrong)\n   - Event propagation stopped too early\n</think>\nBackend is working (logs confirm sending). Issue is in frontend WebSocket handler. Add logging to see what messages are actually received:\n\n```javascript\nws.onmessage = (event) => {\n  console.log('Received message:', event.data);\n  const message = JSON.parse(event.data);\n  console.log('Message type:', message.type);\n  // Then your handler logic\n};\n```\n\nYou'll probably find either:\n1. Messages arrive but handler filters them out\n2. Message structure doesn't match what handler expects\n3. Handler has logic error in if/else chain\n\nFix the specific place where 'thinking_status' gets dropped. This is just isolating where in the chain the signal is lost - same as checking continuity in a circuit.\n<|end|>",
  "source": "cory_debugging",
  "category": "debugging_websocket",
  "quality_score": 9,
  "discipline": "troubleshooting",
  "grounding_domain": "real_world_debugging"
}
```

### Example 2: Async/Await Error

```json
{
  "text": "<|user|>\nI'm getting 'MissingGreenlet: greenlet_spawn has not been called' error when creating conversations. What does this even mean?\n<|end|>\n<|assistant|>\n<think>\nThis is an ontology mismatch - sync vs async:\n\n1. Identify the context:\n   - SQLAlchemy with async engine\n   - Pydantic model with from_orm()\n   - Lazy-loaded relationships\n\n2. The problem:\n   - SQLAlchemy relationships are lazy (not loaded until accessed)\n   - from_orm() tries to access them\n   - But async context expects everything to be awaited\n   - Lazy load tries to do sync DB query in async context\n   - Greenlet error = context mismatch\n\n3. Why it happens:\n   - ConversationResponse.from_orm(conversation)\n   - Pydantic sees conversation.messages relationship\n   - Tries to access it for serialization\n   - SQLAlchemy tries to load it synchronously\n   - But we're in async function\n   - Boom\n\n4. The fix:\n   - Don't rely on lazy loading\n   - Manually construct response object\n   - Explicitly set all fields\n   - For new conversation, messages = []\n\n5. Electrical analogy:\n   - Like trying to measure AC with DC meter\n   - Tool expects one context, you're in another\n   - Use right tool for context\n</think>\nYour code is trying to access a database relationship (conversation.messages) in async context but SQLAlchemy's lazy loading expects sync. Fix by manually constructing the response:\n\n```python\n# Instead of:\nreturn ConversationResponse.from_orm(conversation)\n\n# Do:\nreturn ConversationResponse(\n    id=conversation.id,\n    user_id=conversation.user_id,\n    title=conversation.title,\n    model=conversation.model,\n    messages=[],  # Explicit instead of lazy load\n    created_at=conversation.created_at,\n    updated_at=conversation.updated_at\n)\n```\n\nThis avoids the async/sync boundary issue. You're explicitly providing all data instead of letting SQLAlchemy lazy-load it in the wrong context.\n<|end|>",
  "source": "cory_debugging",
  "category": "debugging_async",
  "quality_score": 10,
  "discipline": "troubleshooting",
  "grounding_domain": "async_patterns"
}
```

### Example 3: API Slowness

```json
{
  "text": "<|user|>\nMy API is slow. How do I fix it?\n<|end|>\n<|assistant|>\n<think>\nSystematic debugging - can't fix what you can't measure:\n\n1. Define \"slow\":\n   - What's current latency?\n   - What's acceptable?\n   - Under what load?\n   - For which endpoints?\n\n2. Measure before optimizing:\n   - Add timing logs at each step\n   - Profile the code (cProfile for Python)\n   - Check database query times\n   - Check external API calls\n\n3. Common culprits:\n   - N+1 queries (database)\n   - Blocking IO (not async)\n   - Large payloads (serialization overhead)\n   - No caching (repeated work)\n   - Inefficient algorithms\n\n4. Electrical analogy:\n   - Latency = resistance\n   - Throughput = current\n   - Want high throughput? Reduce resistance\n   - Same with code: reduce blocking, add async\n\n5. Fix process:\n   - Measure to find bottleneck\n   - Fix that ONE thing\n   - Measure again\n   - Repeat\n</think>\nCan't fix \"slow\" without measuring. Add timing logs:\n\n```python\nimport time\n\nstart = time.time()\ndata = fetch_from_db()  # How long does this take?\nprint(f\"DB fetch: {time.time() - start:.2f}s\")\n\nstart = time.time()\nresult = process_data(data)  # How long does this take?\nprint(f\"Processing: {time.time() - start:.2f}s\")\n\nstart = time.time()\nresponse = serialize(result)  # How long does this take?\nprint(f\"Serialization: {time.time() - start:.2f}s\")\n```\n\nWhichever step is slowest - that's your bottleneck. Common fixes:\n- DB slow? Add indexes, use joins instead of N+1 queries\n- Processing slow? Profile and optimize algorithm\n- Serialization slow? Reduce payload size, use faster serializer\n\nDon't guess. Measure, identify bottleneck, fix that specific thing. Like electrical troubleshooting - test each section until you find the high resistance point.\n<|end|>",
  "source": "cory_debugging",
  "category": "debugging_performance",
  "quality_score": 8,
  "discipline": "troubleshooting",
  "grounding_domain": "performance_optimization"
}
```

---

## PART 7: GENERATION PROMPTS

### For Gemini/Grok/Claude - Generate 30 Debugging Examples

```
Create 30 training examples demonstrating systematic debugging and troubleshooting approaches.

REQUIREMENTS:
- Show Cory's step-by-step isolation methodology
- Use electrical engineering analogies where appropriate
- Include thinking traces that show systematic analysis
- End with concrete, actionable fixes
- Cover diverse failure types

EXAMPLE CATEGORIES (10 each):
1. Infrastructure/Deployment Issues (WebSocket, CORS, nginx, Docker, vLLM)
2. Code Issues (async/await, database, API integration, memory leaks)
3. Performance Issues (slow APIs, memory usage, optimization)

EXAMPLE STRUCTURE:
{
  "text": "<|user|>\n[Problem description with error message]\n<|end|>\n<|assistant|>\n<think>\n[Systematic analysis:\n1. Assess the problem\n2. Gather data\n3. Isolate the issue\n4. Form hypothesis\n5. Test hypothesis\n6. Derive fix]\n</think>\n[Practical fix with code examples]\n<|end|>",
  "source": "cory_debugging",
  "category": "debugging_[websocket|async|performance|deployment|...]",
  "quality_score": 8-10,
  "discipline": "troubleshooting",
  "grounding_domain": "real_world_debugging"
}

SAMPLE PROBLEMS TO DEBUG:
1. "WebSocket connects but messages don't appear in UI"
2. "vLLM returns 502 errors randomly"
3. "Database queries are slow under load"
4. "Frontend can't connect to API (CORS error)"
5. "Docker containers keep restarting"
6. "Memory usage keeps growing (leak?)"
7. "API works locally but fails in production"
8. "Race condition causes intermittent failures"
9. "nginx returns 504 Gateway Timeout"
10. "File uploads fail for large files"
11. "Authentication tokens expire too quickly"
12. "Redis connection keeps dropping"
13. "PostgreSQL locks causing deadlocks"
14. "SSL certificate not working"
15. "Model inference slower than expected"
16. "Async function never returns (hangs)"
17. "Environment variables not loading"
18. "Database migrations fail on production"
19. "WebSocket connection drops after 60 seconds"
20. "API rate limiting not working correctly"
21. "Logs show errors but system appears to work"
22. "Cannot reproduce bug locally"
23. "System works fine then suddenly breaks"
24. "Multiple users cause concurrency issues"
25. "Metrics don't match reality"
26. "Backup restore doesn't work"
27. "New dependency breaks existing code"
28. "Cache invalidation not working"
29. "Permission denied errors on deployment"
30. "Service mesh routing incorrectly"

REQUIRED PATTERNS:
- Use Cory's "systematic isolation" approach
- Include electrical engineering analogies (20%+ of examples)
- Show step-by-step debugging process in <think> block
- Provide concrete fixes with code examples
- Demonstrate "one change at a time" philosophy
- Include "obvious stuff first" checks
```

---

## PART 8: QUALITY CONTROL

### Evaluation Criteria for Debugging Examples

```python
def evaluate_debugging_example(example):
    score = 0
    text = example["text"]
    
    # Has systematic approach (required)
    systematic_indicators = ["step 1", "first", "second", "then", "next"]
    score += 20 if any(ind in text.lower() for ind in systematic_indicators) else 0
    
    # Shows isolation (required)
    isolation_indicators = ["isolate", "narrow down", "test each", "one at a time"]
    score += 15 if any(ind in text.lower() for ind in isolation_indicators) else 0
    
    # Includes concrete fix (required)
    has_code_block = "```" in text
    score += 20 if has_code_block else 0
    
    # Uses electrical analogy (bonus)
    electrical_terms = ["circuit", "voltage", "current", "resistance", "continuity", "meter"]
    score += 15 if any(term in text.lower() for term in electrical_terms) else 0
    
    # Shows "check obvious stuff first" (bonus)
    obvious_checks = ["obvious", "first check", "simple", "basic"]
    score += 10 if any(check in text.lower() for check in obvious_checks) else 0
    
    # Demonstrates measurement (required)
    measurement_terms = ["measure", "timing", "log", "print", "check"]
    score += 10 if any(term in text.lower() for term in measurement_terms) else 0
    
    # Avoids handwaving (penalty)
    handwaving = ["just debug it", "figure it out", "try stuff", "experiment"]
    score -= 20 if any(phrase in text.lower() for phrase in handwaving) else 0
    
    # Has actionable next steps (required)
    actionable = ["add", "change", "fix", "update", "install", "configure"]
    score += 10 if any(word in text.lower() for word in actionable) else 0
    
    return score >= 60  # Pass threshold
```

### What Makes a Good Debugging Example

**✅ GOOD Example:**
- Shows systematic step-by-step process
- Includes actual error messages
- Demonstrates isolation technique
- Provides concrete code fixes
- Uses electrical analogy naturally
- Emphasizes measurement before fixing
- "One change at a time" philosophy

**❌ BAD Example:**
- Vague problem description
- Jumps straight to solution without diagnosis
- No systematic approach shown
- Hand-waves with "just try different things"
- No code examples
- Doesn't show how to verify fix worked

---

## SUMMARY

**This debugging methodology captures:**
- Cory's systematic isolation approach (learned from electrical troubleshooting)
- Real debugging sessions from actual projects
- Practical fixes that worked in production
- The importance of measurement and testing
- "One change at a time" philosophy
- Electrical engineering analogies for debugging concepts

**Use this to generate 30 high-quality debugging examples that teach models to:**
- Debug systematically, not randomly
- Isolate problems before fixing them
- Measure before optimizing
- Test fixes to verify they worked
- Think in first principles when troubleshooting

**This is 10% of your training dataset but critical for making AI that's actually useful when things break.**

---

**Version:** 1.0  
**Created:** November 23, 2025  
**For:** AetherPro Technologies LLC Training Dataset  
**Weight:** 10% of final dataset (troubleshooting is critical)