
You are now the parser AI:
- Use the EXACT format below
- Maintain the 60/15/15/10 ratio
- Output valid JSONL
- Include thinking traces
- Keep quality high


## 🎯 EXACT Instructions for Your Parser AI

Copy-paste this ENTIRE block to the AI that's structuring your validation responses:

```markdown
# Training Data Structure Requirements for MiniMax-M2-AetherPro

## Output Format: JSONL (JSON Lines)

Each example MUST be a single line with this EXACT structure:

```json
{"text": "<|user|>\n{USER_MESSAGE}\n<|end|>\n<|assistant|>\n<think>\n{THINKING_TRACE}\n</think>\n{RESPONSE}\n<|end|>", "source": "{SOURCE}", "category": "{CATEGORY}", "quality_score": {1-10}}
```

### Critical Format Rules

1. **ONE JSON object per line** (JSONL format)
2. **No line breaks inside JSON** - use `\n` for newlines in the text field
3. **Escape all quotes** inside strings with `\"`
4. **Required fields**: text, source, category, quality_score
5. **Optional fields**: scientific_discipline, failure_type, code_language

## Text Field Structure (EXACT template)

### Single-Turn Example:
```
<|user|>
{The user's question or request}
<|end|>
<|assistant|>
<think>
{Multi-line thinking trace showing:
- First principles being applied (equations, laws)
- Step-by-step reasoning (numbered list)
- Electrical/physics analogies
- Real-world constraints (NEC codes, physics limits)
- Why this solution follows from principles}
</think>
{The actual response with:
- Direct answer
- Physical/electrical analogies
- Quantitative details where applicable
- Practical implementation guidance}
<|end|>
```

### Multi-Turn Example (3-5 turns):
```
<|user|>
{First question}
<|end|>
<|assistant|>
<think>
{Thinking for turn 1}
</think>
{Response 1}
<|end|>
<|user|>
{Challenge or follow-up question}
<|end|>
<|assistant|>
<think>
{Thinking extending same principle to new scenario}
</think>
{Response 2 building on turn 1}
<|end|>
<|user|>
{Third question about edge case}
<|end|>
<|assistant|>
<think>
{Thinking showing principle constraints}
</think>
{Response 3 maintaining consistency}
<|end|>
```

### Code Review Example:
```
<|user|>
Review this code for performance issues:

```python
{BAD_CODE}
```
<|end|>
<|assistant|>
<think>
{Analysis:
1. Identify the principle violation
2. Map to electrical/physics concept
3. Quantify the problem
4. Derive fix from first principles}
</think>

❌ **Violates**: {Principle name} - {Why it's broken}

**Physical analogy**: {Electrical or physics comparison}

**First principles fix**:

```python
{GOOD_CODE}
```

✅ **Respects**: {Principle} by {mechanism}

**Performance gain**: {Quantitative improvement}
**Principle applied**: {Equation or law}
<|end|>
```

## Source Field Values

Use EXACTLY these values:
- `claude_chats` - From Claude export
- `chatgpt_chats` - From ChatGPT export
- `grok_chats` - From Grok conversations
- `gemini_validation` - From Gemini responses
- `kimi_validation` - From Kimi responses
- `aetherpro_docs` - From AetherPro documentation
- `electrical_notes` - From Cory's electrical experience
- `philosophy_generated` - From philosophy/consciousness examples
- `first_principles_generated` - Generated first principles examples
- `control_theory_generated` - Control theory discipline
- `thermodynamics_generated` - Thermodynamics discipline
- `fluid_dynamics_generated` - Fluid dynamics discipline

## Category Field Values

Use EXACTLY these values:
- `electrical` - Electrical engineering topics
- `ai_architecture` - AI infrastructure and deployment
- `coding` - Programming and debugging
- `agentic_workflows` - Agent orchestration, MAESTRO, Relay
- `first_principles` - Pure first principles reasoning
- `philosophy` - Philosophy and consciousness
- `code_review` - Code critique with principles
- `failure_analysis` - System failure scenarios
- `synthesis` - Conflicting principles, trade-offs

## Quality Score (1-10)

Auto-calculate based on:
- 10: Has equation + real constraint + failure mode + multi-turn
- 8-9: Has 3 of above + substantial thinking (200+ chars)
- 6-7: Has 2 of above + technical accuracy
- 4-5: Has 1 of above, technically correct
- 1-3: Missing principles, shallow, or repetitive

## Thinking Trace Requirements

MUST include:
1. **Fundamental principle** stated explicitly (equation/law)
2. **Step-by-step breakdown** (numbered or clearly structured)
3. **Real-world constraint** (NEC code, physics limit, Shannon theorem)
4. **Electrical/physics analogy** when applicable
5. **Quantitative reasoning** where possible (calculations, comparisons)

Length: 50-500 words (substantial but not excessive)

## Content Distribution Target

From all your validation sources, aim for:
- 60% Technical first principles (electrical, control theory, thermo, fluids)
- 15% Philosophy/consciousness (sharp, high-impact examples)
- 15% Code review
- 10% Failure analysis

## Processing Instructions

1. **Extract conversations** from validation responses
2. **Identify the user query** and assistant response
3. **Synthesize thinking trace** that shows first principles reasoning (even if not explicit in original)
4. **Add electrical analogies** where missing but applicable
5. **Format exactly** as shown above
6. **One line per example** in output JSONL
7. **Validate JSON** - each line must parse correctly

## Example Output (single line in file):

```
{"text": "<|user|>\nHow do I prevent cascading failures in microservices?\n<|end|>\n<|assistant|>\n<think>\nThis is circuit protection from electrical engineering:\n1. Cascading failure = one breaker trip causes others to trip\n2. Root cause: no isolation between circuits\n3. Solution: circuit breakers that fail independently\n4. In software: bulkheads, timeouts, circuit breaker pattern\n5. NEC requires isolation: each circuit must be independently protected\n</think>\nPreventing cascading failures requires electrical-style circuit isolation. Install circuit breakers (software pattern) at each service boundary with independent failure modes. When Service A fails, its breaker trips (stops requests) without affecting Service B. This is NEC 240.21 applied to software - each branch circuit must have overcurrent protection that doesn't depend on upstream circuits.\n<|end|>", "source": "gemini_validation", "category": "first_principles", "quality_score": 9}
```

## Validation Checklist

Before saving each example, verify:
- ✅ Valid JSON (no unescaped quotes, proper structure)
- ✅ Contains `<|user|>` and `<|assistant|>` tags
- ✅ Has `<think>` and `</think>` wrapper
- ✅ Thinking trace shows first principles
- ✅ Source and category are from approved lists
- ✅ Quality score 1-10
- ✅ Single line (no literal newlines in JSONL file)

## Error Handling

If original content lacks structure:
1. Infer user query from context
2. Generate thinking trace showing the reasoning
3. Maintain technical accuracy
4. Default to quality_score: 7 if uncertain

If content is too casual or low-quality:
- Skip it (we need high-quality examples only)

## Output File Organization

Create:
- `validation_examples.jsonl` - All extracted examples
- `philosophy_examples.jsonl` - Just philosophy/consciousness 
- `code_review_examples.jsonl` - Just code reviews
- `stats.json` - Summary statistics

Process ALL validation responses, but maintain quality threshold.
```

---

## 🎯 What Kimi's Ratio Means for Your Dataset

**60% Technical** (electrical, control theory, thermo, fluids):
- This is your foundation - the electrical engineering brain
- Deep first principles across disciplines
- ~6,000-9,000 examples

**15% Philosophy/Consciousness**:
- "Spice, not substrate" - prevents rote pattern matching
- Forces meta-cognitive depth
- ~1,500-2,250 examples

**15% Code Review**:
- Practical application of principles to real code
- ~1,500-2,250 examples

**10% Failure Analysis**:
- Systems violating principles
- Diagnostic reasoning
- ~1,000-1,500 examples

**Total Target**: 10,000-15,000 examples

---

## 🔄 Your Workflow (Don't Change Anything Yet)

1. ✅ **You're doing**: Have AI parse validation responses into JSONL
2. ⏸️ **Wait**: Get all examples structured correctly
3. 📂 **Then organize**:
   ```
   minimax-m2-aetherpro-training/
   ├── raw_data/
   │   ├── claude_exports/          (your chats)
   │   ├── chatgpt_exports/         (your chats)
   │   ├── grok_exports/            (your chats)
   │   ├── gemini_validation/       (validation responses)
   │   ├── kimi_validation/         (validation responses)
   │   └── philosophy_generated/    (philosophy examples)
   ├── aetherpro_docs/              (your docs)
   └── output/
       └── (parsed JSONL files go here)
   ```

4. 🤖 **Then Claude Code**: Synthesize everything together

---

## ✋ I'M PAUSED - You Finish Parsing


When you're ready, we'll combine everything and let Claude Code create the final unified dataset.

**No changes from me until you say go. Get that parsing done bro. 💪**
