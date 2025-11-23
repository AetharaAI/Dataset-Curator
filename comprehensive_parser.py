#!/usr/bin/env python3
"""
Comprehensive Parser - Extracts and converts ALL content types to training format
Handles: pre-formatted conversations, technical mappings, code reviews, raw principles
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

class ComprehensiveParser:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.examples = []

    def extract_numbered_principles(self, content: str, section_title: str) -> list:
        """Extract numbered principle lists (1. Principle, 2. Principle, etc.)"""
        examples = []

        # Find numbered sections (1. **Title** or **1. Title**)
        pattern = r'(?:^|\n)\s*(?:\*?\*?(\d+)\.\s*\*?\*?(.+?)\*?\*?|\*?\*?(\d+)\.\s+(.+?)\n)'
        matches = re.finditer(pattern, content, re.MULTILINE)

        current_num = None
        current_title = None
        current_content = []

        for match in matches:
            num = match.group(1) or match.group(3)
            title = match.group(2) or match.group(4)

            if num:
                # Save previous principle
                if current_title and current_content:
                    example_text = self._create_principle_example(
                        current_title, '\n'.join(current_content), section_title
                    )
                    if example_text:
                        examples.append(example_text)

                # Start new principle
                current_num = num
                current_title = title.strip().rstrip('*')
                current_content = []

                # Get content after this match
                pos = match.end()
                next_match = re.search(r'\n\s*(?:\*?\*?\d+\.|\#\#)', content[pos:])
                if next_match:
                    chunk = content[pos:pos+next_match.start()]
                else:
                    chunk = content[pos:pos+1500]  # Limit size

                current_content.append(chunk)

        # Save last principle
        if current_title and current_content:
            example_text = self._create_principle_example(
                current_title, '\n'.join(current_content), section_title
            )
            if example_text:
                examples.append(example_text)

        return examples

    def _create_principle_example(self, title: str, content: str, context: str) -> str:
        """Convert a principle description into Q&A format"""
        # Extract components
        principle_match = re.search(r'(?:principle|equation|law)[:：]?\s*(.*?)(?=\n|$)', content, re.IGNORECASE)
        principle = principle_match.group(1).strip() if principle_match else ""

        # Extract variable mapping
        var_match = re.search(r'[Vv]ariable mapping:?\s*(.*?)(?=\n\s*[-\*]|\n[A-Z]|\Z)', content, re.DOTALL)
        variables = var_match.group(1).strip() if var_match else ""

        # Extract failure scenario
        failure_match = re.search(r'[Ff]ailure.*?:?\s*(.*?)(?=\n\s*[-\*]|\n[A-Z]|\Z)', content, re.DOTALL)
        failure = failure_match.group(1).strip() if failure_match else ""

        # Extract constraint
        constraint_match = re.search(r'(?:[Rr]eal|[Cc]onstraint).*?:?\s*(.*?)(?=\n\s*[-\*]|\n[A-Z]|\Z)', content, re.DOTALL)
        constraint = constraint_match.group(1).strip() if constraint_match else ""

        # Extract EE analogy
        ee_match = re.search(r'EE analogy:?\s*(.*?)(?=\n\n|\Z)', content, re.DOTALL)
        ee_analogy = ee_match.group(1).strip() if ee_match else ""

        # Must have some substance
        if not (principle or failure or variables):
            return None

        # Create user question
        user_msg = f"Explain how {title} applies to software systems"

        # Build thinking trace
        thinking_parts = []
        if principle:
            thinking_parts.append(f"Starting from first principles:")
            thinking_parts.append(principle[:300])

        if variables:
            thinking_parts.append(f"\nMapping variables to software:")
            var_lines = [line.strip() for line in variables.split('\n') if line.strip()]
            thinking_parts.extend(var_lines[:5])

        if failure:
            thinking_parts.append(f"\nFailure mode:")
            thinking_parts.append(failure[:200])

        if constraint:
            thinking_parts.append(f"\nPhysical constraint:")
            thinking_parts.append(constraint[:150])

        thinking = "\n".join(thinking_parts)

        # Build response
        response_parts = []
        if principle:
            response_parts.append(f"The governing principle: {principle[:200]}")

        if variables:
            response_parts.append(f"\nIn software terms:\n{variables[:300]}")

        if failure:
            response_parts.append(f"\n**Critical failure mode**: {failure[:300]}")

        if ee_analogy:
            response_parts.append(f"\n**Electrical analogy**: {ee_analogy[:250]}")

        if constraint:
            response_parts.append(f"\n**Constraint**: {constraint[:200]}")

        response = "\n".join(response_parts)

        return f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"

    def extract_code_reviews(self, content: str) -> list:
        """Extract code review examples"""
        examples = []

        # Find code blocks with before/after patterns
        code_pattern = r'```python\n(.*?)```.*?(?:❌|#\s*❌).*?(?:Violates|violates):?\s*(.*?)(?:\n.*?)?```python\n(.*?)```.*?(?:✅|#\s*✅).*?(?:Respects|respects):?\s*(.*?)(?:\n|$)'
        matches = re.findall(code_pattern, content, re.DOTALL)

        for bad_code, violation, good_code, principle in matches:
            # Create Q&A
            user_msg = f"Review this code for issues:\n\n```python\n{bad_code.strip()[:500]}\n```"

            # Build thinking
            thinking = f"Analyzing code against first principles:\n\n1. Identify violation: {violation.strip()[:200]}\n2. Map to physical/electrical analogy\n3. Derive correct implementation\n4. Verify principle compliance"

            # Build response
            response = f"❌ **Violates**: {violation.strip()[:300]}\n\n**Fixed code**:\n\n```python\n{good_code.strip()[:500]}\n```\n\n✅ **Respects**: {principle.strip()[:200]}"

            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"
            examples.append(text)

        return examples

    def extract_pre_formatted_conversations(self, content: str) -> list:
        """Extract already-formatted conversations"""
        pattern = r'```\s*\n(<\|user\|>.*?<\|end\|>)\s*\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

    def extract_dialogue_sections(self, content: str) -> list:
        """Extract multi-turn dialogues"""
        examples = []

        # Find dialogue blocks
        dialogue_pattern = r'####?\s+Dialogue\s+\d+:.*?\n(.*?)(?=####?\s+Dialogue|\Z)'
        dialogues = re.findall(dialogue_pattern, content, re.DOTALL)

        for dialogue_content in dialogues:
            # Extract turns
            turn_pattern = r'\*\s+\*\*Turn\s+\d+.*?\*\*User:\*\*\s*["\u201c]?(.*?)["\u201d]?\s*\*\*AI:\*\*\s*["\u201c]?(.*?)["\u201d]?(?=\n\s*\*\s+\*\*Turn|\n\*\*Rating|\Z)'
            turns = re.findall(turn_pattern, dialogue_content, re.DOTALL)

            if not turns:
                continue

            conversation_parts = []
            for user_text, ai_text in turns:
                user_text = user_text.strip()
                ai_text = ai_text.strip()

                # Extract or generate thinking
                thinking_match = re.search(
                    r'((?:We should|This is|Starting from|Applying|model).*?(?:equation|principle|theorem).*?\.)',
                    ai_text, re.DOTALL
                )
                if thinking_match:
                    thinking = thinking_match.group(1)
                    response = ai_text.replace(thinking, '').strip()
                else:
                    thinking = "Applying first principles to derive the solution"
                    response = ai_text

                conversation_parts.append(f"<|user|>\n{user_text}\n<|end|>")
                conversation_parts.append(f"<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>")

            if conversation_parts:
                examples.append("\n".join(conversation_parts))

        return examples

    def calculate_quality_score(self, text: str) -> int:
        """Calculate quality score"""
        score = 6

        # Has equation/formula
        if re.search(r'\$\$.*?\$\$|\$.*?\$|=.*?[A-Za-z]|→|∝|≈', text):
            score += 1

        # Has principle/constraint reference
        if re.search(r'NEC|IEEE|Shannon|Nyquist|Ohm|Kirchhoff|Carnot|Reynolds|Bernoulli|theorem|principle|law|constraint', text, re.IGNORECASE):
            score += 1

        # Has failure mode
        if re.search(r'failure|fail|error|fault|violate|break|cascade', text, re.IGNORECASE):
            score += 1

        # Has substantial thinking
        thinking_match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
        if thinking_match and len(thinking_match.group(1)) > 200:
            score += 1

        # Multi-turn
        if text.count('<|user|>') >= 3:
            score += 1

        # Has code
        if '```python' in text or '```go' in text or '```' in text:
            score += 1

        return min(score, 10)

    def determine_category(self, text: str, filepath: Path) -> str:
        """Determine category"""
        text_lower = text.lower()
        filepath_str = str(filepath).lower()

        if 'philosophy' in filepath_str or any(term in text_lower for term in ['epistemology', 'phenomenology', 'ontology', 'consciousness']):
            return 'philosophy'
        elif '```python' in text or '```go' in text:
            if 'review' in text_lower or '❌' in text or 'violates' in text_lower:
                return 'code_review'
        elif 'failure' in text_lower or 'error' in text_lower or 'fault' in text_lower:
            return 'failure_analysis'
        elif 'electrical' in text_lower or 'voltage' in text_lower or 'circuit' in text_lower or 'ohm' in text_lower:
            return 'electrical'
        else:
            return 'first_principles'

    def determine_source(self, filepath: Path) -> str:
        """Determine source"""
        filepath_str = str(filepath).lower()
        if 'gemini' in filepath_str:
            return 'gemini_validation'
        elif 'kimi' in filepath_str:
            return 'kimi_validation'
        elif 'grok' in filepath_str:
            return 'grok_chats'
        elif 'claude' in filepath_str:
            return 'claude_chats'
        elif 'chatgpt' in filepath_str or 'gpt' in filepath_str:
            return 'chatgpt_chats'
        elif 'philosophy' in filepath_str:
            return 'philosophy_generated'
        else:
            return 'first_principles_generated'

    def process_file(self, filepath: Path):
        """Process a single file with all extraction methods"""
        print(f"Processing: {filepath.name}")

        content = filepath.read_text(encoding='utf-8', errors='ignore')
        source = self.determine_source(filepath)
        extracted = []

        # Extract pre-formatted conversations
        pre_formatted = self.extract_pre_formatted_conversations(content)
        extracted.extend(pre_formatted)
        if pre_formatted:
            print(f"  → {len(pre_formatted)} pre-formatted conversations")

        # Extract dialogues
        dialogues = self.extract_dialogue_sections(content)
        extracted.extend(dialogues)
        if dialogues:
            print(f"  → {len(dialogues)} dialogue sections")

        # Extract code reviews
        code_reviews = self.extract_code_reviews(content)
        extracted.extend(code_reviews)
        if code_reviews:
            print(f"  → {len(code_reviews)} code review examples")

        # Extract numbered principles
        principles = self.extract_numbered_principles(content, filepath.stem)
        extracted.extend([p for p in principles if p])
        if principles:
            print(f"  → {len([p for p in principles if p])} principle mappings")

        # Create examples
        for text in extracted:
            self.examples.append({
                "text": text,
                "source": source,
                "category": self.determine_category(text, filepath),
                "quality_score": self.calculate_quality_score(text)
            })

    def process_all_files(self):
        """Process all files"""
        print("="*60)
        print("COMPREHENSIVE DATASET PARSER")
        print("="*60 + "\n")

        # Engineering files
        eng_dir = self.base_dir / "First-Principles-Failures-Engineering-&-Deugging"
        if eng_dir.exists():
            print("📁 Engineering/First Principles Files:\n")
            for md_file in sorted(eng_dir.glob("*.md")):
                if md_file.name == 'Weighting-Value-Table.md':
                    continue
                self.process_file(md_file)
            print()

        # Philosophy files
        phil_dir = self.base_dir / "Corys-claude-convos-peronality-datasets"
        if phil_dir.exists():
            print("📁 Philosophy/Personality Files:\n")
            for md_file in sorted(phil_dir.glob("*.md")):
                if any(skip in md_file.name for skip in ['README', 'EXECUTIVE', 'QUICK_START']):
                    continue
                self.process_file(md_file)
            print()

        print(f"✅ TOTAL EXAMPLES EXTRACTED: {len(self.examples)}\n")

    def write_jsonl(self, output_path: Path, examples: list):
        """Write JSONL file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                json_line = json.dumps(example, ensure_ascii=False)
                f.write(json_line + '\n')

    def generate_outputs(self):
        """Generate output files"""
        output_dir = self.base_dir / "minimax-m2-aetherpro-training" / "output"
        output_dir.mkdir(exist_ok=True)

        # Filter by quality
        high_quality = [ex for ex in self.examples if ex['quality_score'] >= 7]
        medium_quality = [ex for ex in self.examples if ex['quality_score'] >= 6]

        print("="*60)
        print("QUALITY FILTERING")
        print("="*60)
        print(f"High quality (score >= 7):    {len(high_quality):4d} examples")
        print(f"Medium+ quality (score >= 6): {len(medium_quality):4d} examples")
        print()

        working_set = medium_quality

        # Write main dataset
        self.write_jsonl(output_dir / "training_dataset.jsonl", working_set)

        # Write category files
        categories = {
            'philosophy': ['philosophy'],
            'code_review': ['code_review'],
            'failure_analysis': ['failure_analysis'],
            'technical': ['first_principles', 'electrical']
        }

        for name, cats in categories.items():
            examples = [ex for ex in working_set if ex['category'] in cats]
            if examples:
                self.write_jsonl(output_dir / f"{name}_examples.jsonl", examples)

        # Statistics
        stats = {
            "total_examples": len(self.examples),
            "working_set_examples": len(working_set),
            "category_distribution": {},
            "source_distribution": {},
            "quality_distribution": {}
        }

        for ex in working_set:
            stats['category_distribution'][ex['category']] = \
                stats['category_distribution'].get(ex['category'], 0) + 1
            stats['source_distribution'][ex['source']] = \
                stats['source_distribution'].get(ex['source'], 0) + 1
            stats['quality_distribution'][str(ex['quality_score'])] = \
                stats['quality_distribution'].get(str(ex['quality_score']), 0) + 1

        total = len(working_set)
        if total > 0:
            stats['category_percentages'] = {
                cat: f"{(count/total)*100:.1f}%"
                for cat, count in stats['category_distribution'].items()
            }

        with open(output_dir / "dataset_stats.json", 'w') as f:
            json.dump(stats, f, indent=2)

        print("="*60)
        print("DATASET SUMMARY")
        print("="*60)
        print(f"Total examples: {len(working_set)}\n")
        print("Category Distribution:")
        for cat in sorted(stats['category_distribution'].keys()):
            count = stats['category_distribution'][cat]
            pct = stats['category_percentages'][cat]
            print(f"  {cat:20s}: {count:4d} ({pct})")

        print("\nSource Distribution:")
        for src in sorted(stats['source_distribution'].keys()):
            count = stats['source_distribution'][src]
            print(f"  {src:30s}: {count:4d}")

        print("\nQuality Scores:")
        for score in sorted(stats['quality_distribution'].keys(), reverse=True):
            count = stats['quality_distribution'][score]
            print(f"  Score {score}: {count:4d}")

        print(f"\n📂 Output directory: {output_dir}/")
        print("="*60)

def main():
    parser = ComprehensiveParser("/home/user/Dataset-Curator")
    parser.process_all_files()
    parser.generate_outputs()
    print("\n✅ PARSING COMPLETE!\n")

if __name__ == "__main__":
    main()
