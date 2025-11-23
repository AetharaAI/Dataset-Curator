# scripts/merge_philosophy_datasets.py

def philosophical_quality_check(example):
    """Stricter than technical examples"""
    score = 0
    
    # Named philosopher/theory (required)
    philosophers = ["Husserl", "Jonas", "Polanyi", "Gödel", "Münchhausen", 
                   "Kant", "Rawls", "IIT", "GWT", "Φ"]
    score += 15 if any(p in example["text"] for p in philosophers) else 0
    
    # Concrete grounding
    concrete_terms = ["architectural constraint", "debugging technique", 
                     "design principle", "observability pattern"]
    score += 10 if any(term in example["text"].lower() for term in concrete_terms) else 0
    
    # Dual ontology (uses both abstract and concrete)
    score += 10 if ("abstract" in example["text"] or "philosophical" in example["text"]) and \
                    ("concrete" in example["text"] or "practical" in example["text"]) else 0
    
    # Hand-waving penalty
    hand_waving = ["in conclusion", "basically", "simply put", "just remember"]
    score -= 20 if any(phrase in example["text"].lower() for phrase in hand_waving) else 0
    
    # Must have actionable outcome
    actionable = ["use ", "implement", "apply", "deploy", "measure", "test"]
    score += 10 if any(word in example["text"].lower() for word in actionable) else 0
    
    return score >= 25

def merge_philosophy_datasets(sources):
    """Keep only exceptional philosophy examples"""
    all_examples = []
    
    for source_file in sources:
        with open(source_file) as f:
            examples = [json.loads(line) for line in f]
            # Strict filtering: keep only 60% of philosophy examples
            quality_sorted = sorted(examples, 
                                   key=philosophical_quality_check, 
                                   reverse=True)
            keep_count = int(len(quality_sorted) * 0.6)
            all_examples.extend(quality_sorted[:keep_count])
    
    # Deduplicate by similar thinking patterns
    unique_examples = deduplicate_by_reasoning(all_examples)
    
    return unique_examples

def deduplicate_by_reasoning(examples):
    """Remove examples with similar philosophical arguments"""
    # Use embedding similarity on <think> blocks
    # Keep only one example per philosophical pattern
    # Implementation left as exercise (use sentence transformers)
    pass
