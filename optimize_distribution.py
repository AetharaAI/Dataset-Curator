#!/usr/bin/env python3
"""
Optimize dataset distribution to match 60/15/15/10 target
Reclassifies examples based on content analysis
"""

import json
import re
from pathlib import Path

def analyze_example_for_reclassification(example):
    """Analyze example content to determine best category"""
    text = example['text']
    current_category = example['category']

    # Extract content for analysis
    has_equation = bool(re.search(r'\$\$.*?\$\$|\$.*?\$|=\s*[A-Za-z]|→|∝|≈|∫|∆|Σ', text))
    has_code = bool(re.search(r'```(?:python|go|java|rust|javascript)', text, re.IGNORECASE))
    has_review_markers = bool(re.search(r'❌.*?Violates|✅.*?Respects|BEFORE|AFTER', text))
    has_physical_law = bool(re.search(
        r'Ohm|Kirchhoff|Carnot|Reynolds|Bernoulli|Shannon|Nyquist|conservation of|thermodynamic|CAP theorem|Little.*Law',
        text, re.IGNORECASE
    ))
    has_philosophy = bool(re.search(
        r'epistemology|phenomenology|ontology|consciousness|Husserl|Popper|Gödel|intentionality|epoché',
        text, re.IGNORECASE
    ))
    has_failure_keywords = bool(re.search(
        r'failure|fail|error|bug|crash|fault|debug|broke',
        text, re.IGNORECASE
    ))
    has_principle_explanation = bool(re.search(
        r'principle|fundamental|governing equation|first principles|physical law|theorem',
        text, re.IGNORECASE
    ))

    # Reclassification logic
    # Philosophy: highest priority for philosophy keywords
    if has_philosophy:
        return 'philosophy'

    # Code review: has code + review markers
    if has_code and has_review_markers:
        return 'code_review'

    # First principles: has equation/physical law and explains principles
    # Even if it mentions failures, if it explains via principles, it's first_principles
    if (has_equation or has_physical_law) and has_principle_explanation:
        return 'first_principles'

    # Electrical: specific electrical terms
    if re.search(r'voltage|current|circuit|NEC|AWG|ampacity|breaker|resistance', text, re.IGNORECASE):
        if has_physical_law or has_equation:
            return 'electrical'

    # Failure analysis: debug/error focused without strong principle explanation
    if has_failure_keywords and not (has_equation and has_principle_explanation):
        return 'failure_analysis'

    # Default: keep current category
    return current_category

def optimize_distribution():
    """Reclassify examples to match target distribution"""

    input_path = Path("/home/user/Dataset-Curator/minimax-m2-aetherpro-training/output/training_dataset.jsonl")
    output_path = Path("/home/user/Dataset-Curator/minimax-m2-aetherpro-training/output/optimized_dataset.jsonl")

    # Load examples
    examples = []
    with open(input_path) as f:
        for line in f:
            examples.append(json.loads(line))

    print(f"Loaded {len(examples)} examples")
    print("\nOriginal distribution:")

    # Show original distribution
    orig_dist = {}
    for ex in examples:
        orig_dist[ex['category']] = orig_dist.get(ex['category'], 0) + 1

    for cat, count in sorted(orig_dist.items()):
        pct = (count / len(examples)) * 100
        print(f"  {cat:20s}: {count:3d} ({pct:5.1f}%)")

    # Reclassify
    reclassified_count = 0
    for example in examples:
        old_category = example['category']
        new_category = analyze_example_for_reclassification(example)

        if old_category != new_category:
            example['category'] = new_category
            reclassified_count += 1

    print(f"\nReclassified {reclassified_count} examples")
    print("\nNew distribution:")

    # Show new distribution
    new_dist = {}
    for ex in examples:
        new_dist[ex['category']] = new_dist.get(ex['category'], 0) + 1

    total = len(examples)
    for cat, count in sorted(new_dist.items()):
        pct = (count / total) * 100
        print(f"  {cat:20s}: {count:3d} ({pct:5.1f}%)")

    # Calculate vs target
    print("\nComparison to target:")
    targets = {
        'first_principles': 0.60,
        'electrical': 0.60,  # Part of technical 60%
        'philosophy': 0.15,
        'code_review': 0.15,
        'failure_analysis': 0.10
    }

    # Combine technical categories
    technical_count = new_dist.get('first_principles', 0) + new_dist.get('electrical', 0)
    technical_pct = (technical_count / total) * 100

    print(f"  Technical (first_principles + electrical): {technical_count:3d} ({technical_pct:5.1f}%) - Target: 60%")
    print(f"  Philosophy:                                {new_dist.get('philosophy', 0):3d} ({(new_dist.get('philosophy', 0)/total)*100:5.1f}%) - Target: 15%")
    print(f"  Code review:                               {new_dist.get('code_review', 0):3d} ({(new_dist.get('code_review', 0)/total)*100:5.1f}%) - Target: 15%")
    print(f"  Failure analysis:                          {new_dist.get('failure_analysis', 0):3d} ({(new_dist.get('failure_analysis', 0)/total)*100:5.1f}%) - Target: 10%")

    # Write optimized dataset
    with open(output_path, 'w', encoding='utf-8') as f:
        for example in examples:
            json_line = json.dumps(example, ensure_ascii=False)
            f.write(json_line + '\n')

    print(f"\n✅ Optimized dataset saved to: {output_path}")

    # Also update the main training_dataset.jsonl
    with open(input_path, 'w', encoding='utf-8') as f:
        for example in examples:
            json_line = json.dumps(example, ensure_ascii=False)
            f.write(json_line + '\n')

    # Write category-specific files
    output_dir = input_path.parent

    categories = {
        'technical': ['first_principles', 'electrical'],
        'philosophy': ['philosophy'],
        'code_review': ['code_review'],
        'failure_analysis': ['failure_analysis']
    }

    for name, cats in categories.items():
        cat_examples = [ex for ex in examples if ex['category'] in cats]
        if cat_examples:
            cat_path = output_dir / f"{name}_examples.jsonl"
            with open(cat_path, 'w', encoding='utf-8') as f:
                for ex in cat_examples:
                    json_line = json.dumps(ex, ensure_ascii=False)
                    f.write(json_line + '\n')
            print(f"✅ Updated {cat_path.name}: {len(cat_examples)} examples")

    # Update stats
    stats = {
        "total_examples": len(examples),
        "reclassified_count": reclassified_count,
        "category_distribution": new_dist,
        "category_percentages": {
            cat: f"{(count/total)*100:.1f}%"
            for cat, count in new_dist.items()
        },
        "target_distribution": {
            "technical": "60%",
            "philosophy": "15%",
            "code_review": "15%",
            "failure_analysis": "10%"
        }
    }

    stats_path = output_dir / "optimized_stats.json"
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"✅ Stats saved to: {stats_path}")

if __name__ == "__main__":
    optimize_distribution()
