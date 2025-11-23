#!/usr/bin/env python3
"""
Final Robust Parser for MiniMax-M2-AetherPro Training Dataset
Extracts all high-quality examples from markdown files
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

class FinalParser:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.examples = []
        self.stats = defaultdict(int)

    def extract_code_block_conversations(self, content: str) -> list:
        """Extract conversations from code blocks"""
        # Pattern for code blocks containing conversations
        pattern = r'```\s*\n(<\|user\|>.*?<\|end\|>)\s*\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

    def extract_mapping_sections(self, content: str) -> list:
        """Extract technical mapping sections and convert to Q&A"""
        examples = []

        # Split by mapping/dialogue headers
        sections = re.split(r'\n##\s+\*?\*?(?:Mapping|Dialogue)\s+\d+:?\s+', content)

        # Find the headers too
        headers = re.findall(r'\n##\s+\*?\*?(?:Mapping|Dialogue)\s+\d+:?\s+(.*?)\n', content)

        for i, section in enumerate(sections[1:], 0):  # Skip first split (before any mapping)
            if i >= len(headers):
                break

            title = headers[i].strip().rstrip('*')

            # Extract components
            equation_match = re.search(r'```\s*\n(.*?)\n```', section, re.DOTALL)
            equation = equation_match.group(1).strip() if equation_match else ""

            failure_match = re.search(r'\*\*Failure Mode?\*?\*?\s*\n(.*?)(?=\n\*\*|\n##|\Z)', section, re.DOTALL)
            failure = failure_match.group(1).strip() if failure_match else ""

            constraint_match = re.search(r'\*\*(?:Real|Constraint).*?\*\*\s*\n(.*?)(?=\n\*\*|\n##|\Z)', section, re.DOTALL)
            constraint = constraint_match.group(1).strip() if constraint_match else ""

            variables_match = re.search(r'\*\*Variable Mapping.*?\*\*\s*\n(.*?)(?=\n\*\*|\Z)', section, re.DOTALL)
            variables = variables_match.group(1).strip() if variables_match else ""

            # Need at least equation or failure to create example
            if not equation and not failure:
                continue

            # Create Q&A
            user_msg = f"How does {title} apply to distributed systems?"

            # Build thinking
            thinking_parts = []
            if equation:
                thinking_parts.append(f"Starting from the fundamental equation:")
                thinking_parts.append(equation)

            if variables:
                thinking_parts.append("\nMapping variables to distributed systems:")
                var_lines = [line.strip() for line in variables.split('\n') if line.strip().startswith('-')]
                thinking_parts.extend(var_lines[:5])

            if failure:
                thinking_parts.append(f"\nFailure mode analysis:")
                thinking_parts.append(failure[:300])

            thinking = "\n".join(thinking_parts)

            # Build response
            response_parts = []
            if equation:
                response_parts.append(f"This principle is governed by the equation:")
                response_parts.append(equation)

            if failure:
                response_parts.append(f"\n**Critical failure mode**: {failure[:400]}")

            if constraint:
                response_parts.append(f"\n**Physical constraint**: {constraint[:200]}")

            response = "\n".join(response_parts)

            # Build full conversation
            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"

            examples.append(text)

        return examples

    def extract_dialogue_sections(self, content: str) -> list:
        """Extract multi-turn dialogues"""
        examples = []

        # Find dialogue blocks
        dialogue_blocks = re.findall(r'####?\s+Dialogue\s+\d+:.*?\n(.*?)(?=####?\s+Dialogue|\Z)', content, re.DOTALL)

        for dialogue_content in dialogue_blocks:
            # Extract individual turns
            turns = []

            # Pattern for Turn X format
            turn_matches = re.findall(
                r'\*\s+\*\*Turn\s+\d+.*?\*\*User:\*\*\s*["\u201c]?(.*?)["\u201d]?\s*\*\*AI:\*\*\s*["\u201c]?(.*?)["\u201d]?(?=\n\s*\*\s+\*\*Turn|\n\*\*Rating|\Z)',
                dialogue_content,
                re.DOTALL
            )

            if not turn_matches:
                continue

            # Build multi-turn conversation
            conversation_parts = []

            for user_text, ai_text in turn_matches:
                user_text = user_text.strip()
                ai_text = ai_text.strip()

                # Extract or generate thinking
                thinking_match = re.search(r'((?:We should|This is|Starting from|Applying).*?(?:equation|principle).*?\.)', ai_text, re.DOTALL)
                if thinking_match:
                    thinking = thinking_match.group(1)
                    response = ai_text.replace(thinking, '').strip()
                else:
                    # Generate basic thinking
                    thinking = f"Analyzing the problem:\n1. Identify the core principle\n2. Map to the specific scenario\n3. Derive constraints and solution"
                    response = ai_text

                conversation_parts.append(f"<|user|>\n{user_text}\n<|end|>")
                conversation_parts.append(f"<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>")

            if conversation_parts:
                examples.append("\n".join(conversation_parts))

        return examples

    def calculate_quality_score(self, text: str) -> int:
        """Calculate quality score based on content"""
        score = 6  # Base score

        # Has equation
        if re.search(r'\$\$.*?\$\$|\$.*?\$|```', text):
            score += 1

        # Has principle/constraint references
        if re.search(r'NEC|IEEE|Shannon|Nyquist|theorem|principle|constraint', text, re.IGNORECASE):
            score += 1

        # Has failure mode
        if re.search(r'failure|fail|error|fault|cascade|violate', text, re.IGNORECASE):
            score += 1

        # Has substantial thinking
        thinking_match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
        if thinking_match and len(thinking_match.group(1)) > 200:
            score += 1

        # Multi-turn
        if text.count('<|user|>') >= 3:
            score += 1

        return min(score, 10)

    def determine_category(self, text: str, filepath: Path) -> str:
        """Determine category from content and filepath"""
        text_lower = text.lower()
        filepath_str = str(filepath).lower()

        if 'philosophy' in filepath_str or 'consciousness' in text_lower or 'epistemology' in text_lower:
            return 'philosophy'
        elif 'code' in text_lower and '```' in text and 'review' in text_lower:
            return 'code_review'
        elif 'failure' in text_lower or 'debug' in text_lower or 'error' in text_lower:
            return 'failure_analysis'
        elif 'electrical' in text_lower or 'voltage' in text_lower or 'circuit' in text_lower:
            return 'electrical'
        else:
            return 'first_principles'

    def determine_source(self, filepath: Path) -> str:
        """Determine source from filepath"""
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
        """Process a single markdown file"""
        print(f"Processing: {filepath.name}")

        content = filepath.read_text(encoding='utf-8', errors='ignore')
        source = self.determine_source(filepath)

        extracted_texts = []

        # Extract pre-formatted conversations from code blocks
        conv_blocks = self.extract_code_block_conversations(content)
        extracted_texts.extend(conv_blocks)
        if conv_blocks:
            print(f"  Found {len(conv_blocks)} pre-formatted conversations")

        # Extract dialogue sections
        dialogues = self.extract_dialogue_sections(content)
        extracted_texts.extend(dialogues)
        if dialogues:
            print(f"  Found {len(dialogues)} dialogue sections")

        # Extract mapping sections (only for technical files)
        if 'First-Principles' in str(filepath) or 'engineering' in str(filepath).lower():
            mappings = self.extract_mapping_sections(content)
            extracted_texts.extend(mappings)
            if mappings:
                print(f"  Found {len(mappings)} technical mappings")

        # Create examples from extracted texts
        for text in extracted_texts:
            quality_score = self.calculate_quality_score(text)
            category = self.determine_category(text, filepath)

            self.examples.append({
                "text": text,
                "source": source,
                "category": category,
                "quality_score": quality_score
            })

    def process_all_files(self):
        """Process all files in dataset"""
        print("=== Processing Dataset Files ===\n")

        # Process engineering files (first principles)
        eng_dir = self.base_dir / "First-Principles-Failures-Engineering-&-Deugging"
        if eng_dir.exists():
            print("Processing Engineering/First Principles files:")
            for md_file in sorted(eng_dir.glob("*.md")):
                if md_file.name == 'Weighting-Value-Table.md':
                    continue
                self.process_file(md_file)
                self.stats['engineering_files'] += 1
            print()

        # Process philosophy files
        phil_dir = self.base_dir / "Corys-claude-convos-peronality-datasets"
        if phil_dir.exists():
            print("Processing Philosophy/Personality files:")
            for md_file in sorted(phil_dir.glob("*.md")):
                if any(skip in md_file.name for skip in ['README', 'EXECUTIVE', 'QUICK_START']):
                    continue
                self.process_file(md_file)
                self.stats['philosophy_files'] += 1
            print()

        print(f"✅ Total examples extracted: {len(self.examples)}\n")

    def write_jsonl(self, output_path: Path, examples: list):
        """Write examples to JSONL file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                json_line = json.dumps(example, ensure_ascii=False)
                f.write(json_line + '\n')

    def generate_outputs(self):
        """Generate output files and statistics"""
        output_dir = self.base_dir / "minimax-m2-aetherpro-training" / "output"
        output_dir.mkdir(exist_ok=True)

        # Filter by quality
        high_quality = [ex for ex in self.examples if ex['quality_score'] >= 7]
        medium_quality = [ex for ex in self.examples if ex['quality_score'] >= 6]

        print(f"Quality filtering:")
        print(f"  High quality (>= 7): {len(high_quality)}")
        print(f"  Medium+ (>= 6): {len(medium_quality)}")
        print()

        # Use medium quality as working set
        working_set = medium_quality

        # Write main dataset
        self.write_jsonl(output_dir / "training_dataset.jsonl", working_set)
        print(f"✅ Wrote {len(working_set)} examples to training_dataset.jsonl")

        # Write category-specific files
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
                print(f"✅ Wrote {len(examples)} {name} examples")

        # Generate statistics
        stats = {
            "total_examples": len(self.examples),
            "working_set_examples": len(working_set),
            "files_processed": dict(self.stats),
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

        # Calculate percentages
        total = len(working_set)
        if total > 0:
            stats['category_percentages'] = {
                cat: f"{(count/total)*100:.1f}%"
                for cat, count in stats['category_distribution'].items()
            }
            stats['distribution_target'] = {
                "current": stats['category_percentages'],
                "target": {
                    "technical (first_principles + electrical)": "60%",
                    "philosophy": "15%",
                    "code_review": "15%",
                    "failure_analysis": "10%"
                }
            }

        # Write stats
        with open(output_dir / "dataset_stats.json", 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"\n=== DATASET SUMMARY ===")
        print(f"Total examples in dataset: {len(working_set)}")
        print(f"\nCategory distribution:")
        for cat in sorted(stats['category_distribution'].keys()):
            count = stats['category_distribution'][cat]
            pct = stats['category_percentages'][cat]
            print(f"  {cat:20s}: {count:4d} examples ({pct})")

        print(f"\nSource distribution:")
        for src in sorted(stats['source_distribution'].keys()):
            count = stats['source_distribution'][src]
            print(f"  {src:30s}: {count:4d} examples")

        print(f"\nQuality distribution:")
        for score in sorted(stats['quality_distribution'].keys(), reverse=True):
            count = stats['quality_distribution'][score]
            print(f"  Score {score}: {count:4d} examples")

        print(f"\n✅ All files saved to: {output_dir}/")

def main():
    parser = FinalParser("/home/user/Dataset-Curator")
    parser.process_all_files()
    parser.generate_outputs()
    print("\n" + "="*50)
    print("✅ DATASET PARSING COMPLETE!")
    print("="*50)

if __name__ == "__main__":
    main()
