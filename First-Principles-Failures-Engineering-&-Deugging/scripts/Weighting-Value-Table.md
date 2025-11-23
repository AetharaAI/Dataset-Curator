```
merge command:

python scripts/merge_philosophy_datasets.py \
  --sources output/philosophy/*.jsonl \
  --output output/final_dataset/philosophy_training.jsonl \
  --quality-threshold 25 \
  --keep-percentage 0.6
---

## TRAINING DATASET WEIGHTING

**Final dataset composition:**
- **Technical first principles** (electrical, control theory, thermodynamics): 60%
- **Philosophy/consciousness**: 15% (sharp, high-impact examples only)
- **Code review and patterns**: 15%
- **Failure analysis and debugging**: 10%

**Why 15% philosophy?**
- Spice, not substrate
- Prevents rote pattern matching
- Forces meta-cognitive depth
- Distinguishes colleague from chatbot

**Expected outcome:**
Model won't just say "this is like voltage drop" - it'll say "this latency is voltage drop at the information theory level, and here's where the analogy breaks down ontologically, and here's the architectural constraint that follows."

---

## DISTRIBUTED GENERATION COORDINATION

**Assign pipelines to models:**
- **Claude**: Pipelines 1 (Epistemology) + 4 (Ontology)
- **Gemini**: Pipelines 2 (Phenomenology) + 5 (Ethics)
- **Grok**: Pipeline 3 (Consciousness) + review all outputs

**Standardized output location:**
```
output/philosophy/
├── epistemology_scale.jsonl (10 examples)
├── phenomenology_debugging.jsonl (10 examples)
├── consciousness_monitoring.jsonl (10 examples)
├── ontology_abstraction.jsonl (10 examples)
├── ethics_complexity.jsonl (10 examples)
└── merged_philosophy.jsonl (30 examples after filtering)