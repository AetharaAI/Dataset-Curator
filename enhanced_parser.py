#!/usr/bin/env python3
"""
Enhanced Dataset Parser for MiniMax-M2-AetherPro Training
Handles multiple content formats and maintains proper distribution
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

class EnhancedParser:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.examples = []
        self.stats = defaultdict(int)

    def parse_technical_mapping(self, content: str, source: str) -> List[Dict]:
        """Parse technical mapping format (equations + failure modes)"""
        examples = []

        # Split by mapping sections (## Mapping N:)
        mapping_pattern = r'##\s+\*?\*?Mapping\s+\d+:?\s+(.*?)\n(.*?)(?=##\s+\*?\*?Mapping\s+\d+:|##\s+\*?\*?Dialogue|$)'
        matches = re.findall(mapping_pattern, content, re.DOTALL)

        for title, section_content in matches:
            title = title.strip().rstrip('*')

            # Extract equation
            eq_match = re.search(r'```\s*(.*?)\s*```', section_content, re.DOTALL)
            equation = eq_match.group(1).strip() if eq_match else ""

            # Extract variable mapping
            var_mapping = re.search(r'\*\*Variable Mapping.*?\*\*\s*\n(.*?)(?=\n\*\*|\n##|$)',
                                   section_content, re.DOTALL)
            variables = var_mapping.group(1).strip() if var_mapping else ""

            # Extract failure mode
            failure_match = re.search(r'\*\*Failure Mode\*?\*?\s*\n(.*?)(?=\n\*\*|\n##|$)',
                                     section_content, re.DOTALL)
            failure = failure_match.group(1).strip() if failure_match else ""

            # Extract constraint
            constraint_match = re.search(r'\*\*Real.*?Constraint\*?\*?\s*\n(.*?)(?=\n\*\*|\n##|$)',
                                        section_content, re.DOTALL)
            constraint = constraint_match.group(1).strip() if constraint_match else ""

            # Skip if too little content
            if not equation and not failure:
                continue

            # Create user question
            user_msg = f"How does {title} apply to distributed systems?"

            # Build thinking trace
            thinking_parts = []
            if equation:
                thinking_parts.append(f"Starting from the fundamental equation:\n{equation}\n")

            if variables:
                var_lines = [line.strip() for line in variables.split('\n') if line.strip().startswith('-')]
                if var_lines:
                    thinking_parts.append("Mapping the variables to distributed systems:")
                    thinking_parts.extend(var_lines[:5])  # Limit to 5 variables

            if failure:
                thinking_parts.append(f"\nFailure mode analysis:\n{failure[:300]}")  # Limit length

            if constraint:
                thinking_parts.append(f"\nReal-world constraint:\n{constraint[:200]}")

            thinking = "\n".join(thinking_parts)

            # Build response
            response_parts = []
            if equation and variables:
                response_parts.append(f"This maps directly through the equation:\n{equation}\n")
                response_parts.append(f"In distributed systems:\n{variables[:300]}")

            if failure:
                response_parts.append(f"\n**Critical failure mode**: {failure[:400]}")

            if constraint:
                response_parts.append(f"\n**Physical constraint**: {constraint[:200]}")

            response = "\n".join(response_parts) if response_parts else section_content[:500]

            # Build conversation
            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"

            # Calculate quality score
            quality_score = 5
            if equation: quality_score += 2
            if failure: quality_score += 1
            if constraint: quality_score += 1
            if len(thinking) > 200: quality_score += 1

            # Determine category
            if 'failure' in failure.lower() or 'error' in failure.lower():
                category = 'failure_analysis'
            else:
                category = 'first_principles'

            examples.append({
                "text": text,
                "source": source,
                "category": category,
                "quality_score": min(quality_score, 10)
            })

        return examples

    def parse_dialogue_section(self, content: str, source: str) -> List[Dict]:
        """Parse multi-turn dialogue sections"""
        examples = []

        # Pattern for Dialogue N: sections
        dialogue_pattern = r'###+\s+Dialogue\s+\d+:.*?\n(.*?)(?=###+ Dialogue|\Z)'
        dialogues = re.findall(dialogue_pattern, content, re.DOTALL)

        for dialogue_content in dialogues:
            # Extract turns
            turn_pattern = r'\*\s+\*\*Turn\s+\d+.*?\*\*User:\*\*\s*["\']?(.*?)["\']?\s*\*\*AI:\*\*\s*["\']?(.*?)["\']?(?=\n\s*\*\s+\*\*Turn|\n\*\*Rating|\Z)'
            turns = re.findall(turn_pattern, dialogue_content, re.DOTALL)

            if not turns:
                continue

            # Build multi-turn conversation
            conversation_parts = []
            all_thinking = []

            for user_text, ai_text in turns:
                user_text = user_text.strip()
                ai_text = ai_text.strip()

                # Extract thinking from AI text if present
                think_match = re.search(r'((?:We should|This is|Starting from|Applying).*?(?:equation|principle|theorem).*?\.)',
                                       ai_text, re.DOTALL)
                thinking = think_match.group(1) if think_match else f"Analyzing: {user_text[:50]}..."

                # Clean AI response (remove thinking if extracted)
                if think_match:
                    ai_response = ai_text.replace(think_match.group(1), '').strip()
                else:
                    ai_response = ai_text

                all_thinking.append(thinking)

                conversation_parts.append(f"<|user|>\n{user_text}\n<|end|>")
                conversation_parts.append(f"<|assistant|>\n<think>\n{thinking}\n</think>\n{ai_response}\n<|end|>")

            text = "\n".join(conversation_parts)

            # Calculate quality score
            quality_score = 7  # Multi-turn gets baseline 7
            if len(turns) >= 3: quality_score += 1
            if any(re.search(r'\$.*?\$', t[1]) for t in turns): quality_score += 1
            if any('failure' in t[1].lower() or 'error' in t[1].lower() for t in turns): quality_score += 1

            # Determine category
            combined_text = " ".join([t[1] for t in turns])
            if 'code' in combined_text.lower() and '```' in combined_text:
                category = 'code_review'
            elif 'failure' in combined_text.lower() or 'debug' in combined_text.lower():
                category = 'failure_analysis'
            elif 'consciousness' in combined_text.lower() or 'epistemology' in combined_text.lower():
                category = 'philosophy'
            else:
                category = 'first_principles'

            examples.append({
                "text": text,
                "source": source,
                "category": category,
                "quality_score": min(quality_score, 10)
            })

        return examples

    def parse_pre_formatted_conversations(self, content: str, source: str, filepath: Path) -> List[Dict]:
        """Parse conversations already in <|user|>/<|assistant|> format"""
        examples = []

        # Pattern for complete conversation blocks
        pattern = r'```\s*\n(<\|user\|>.*?<\|end\|>)\s*```'
        matches = re.findall(pattern, content, re.DOTALL)

        for block in matches:
            # Extract thinking
            thinking_match = re.search(r'<think>(.*?)</think>', block, re.DOTALL)
            thinking = thinking_match.group(1).strip() if thinking_match else ""

            # Calculate quality score
            quality_score = 6
            if re.search(r'\$\$.*?\$\$|\$.*?\$', block): quality_score += 1
            if re.search(r'NEC|IEEE|Shannon|theorem|principle|equation', block, re.IGNORECASE): quality_score += 1
            if len(thinking) > 200: quality_score += 1
            if block.count('<|user|>') >= 3: quality_score += 1

            # Determine category from filepath and content
            filepath_str = str(filepath).lower()
            if 'philosophy' in filepath_str or 'consciousness' in block.lower():
                category = 'philosophy'
            elif 'code' in block.lower() and '```' in block:
                category = 'code_review'
            elif 'failure' in block.lower() or 'error' in block.lower():
                category = 'failure_analysis'
            else:
                category = 'first_principles'

            examples.append({
                "text": block,
                "source": source,
                "category": category,
                "quality_score": min(quality_score, 10)
            })

        return examples

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
        """Process a single file with all applicable parsers"""
        print(f"Processing: {filepath.relative_to(self.base_dir)}")

        content = filepath.read_text(encoding='utf-8', errors='ignore')
        source = self.determine_source(filepath)
        all_examples = []

        # Try pre-formatted conversations first
        pre_formatted = self.parse_pre_formatted_conversations(content, source, filepath)
        all_examples.extend(pre_formatted)

        # Try dialogue sections
        dialogues = self.parse_dialogue_section(content, source)
        all_examples.extend(dialogues)

        # Try technical mappings (only for engineering files)
        if 'First-Principles' in str(filepath) or 'engineering' in str(filepath).lower():
            mappings = self.parse_technical_mapping(content, source)
            all_examples.extend(mappings)

        return all_examples

    def process_all_files(self):
        """Process all files"""

        # Process First Principles / Engineering files (PRIORITY)
        fp_dir = self.base_dir / "First-Principles-Failures-Engineering-&-Deugging"
        if fp_dir.exists():
            for md_file in fp_dir.glob("*.md"):
                if md_file.name == 'Weighting-Value-Table.md':
                    continue
                examples = self.process_file(md_file)
                self.examples.extend(examples)
                self.stats['engineering_files'] += 1

        # Process Philosophy files (PRIORITY)
        phil_dir = self.base_dir / "Corys-claude-convos-peronality-datasets"
        if phil_dir.exists():
            for md_file in phil_dir.glob("*.md"):
                if any(skip in md_file.name for skip in ['README', 'EXECUTIVE', 'QUICK_START', 'Dossier']):
                    continue
                examples = self.process_file(md_file)
                self.examples.extend(examples)
                self.stats['philosophy_files'] += 1

        # Process AetherPro docs (LIMIT TO KEY FILES ONLY)
        aetherpro_dir = self.base_dir / "minimax-m2-aetherpro-training" / "aetherpro_docs"
        if aetherpro_dir.exists():
            # Only process key architecture files, skip infrastructure
            key_files = [
                'architecture/TRIAD-Complete-Build-Spec-Cory-Method.md',
                'architecture/Mastro-Kimi-Powered-Orchestration-Agent.md',
                'architecture/AetherAI-Triad-Intelligence-Dataset-Tips.md',
                'philosophy/Corys-Dossier-Sovereign-AI.md',
            ]
            for key_file in key_files:
                filepath = aetherpro_dir / key_file
                if filepath.exists():
                    examples = self.process_file(filepath)
                    # Limit examples from each doc file
                    self.examples.extend(examples[:5])  # Max 5 per file
                    self.stats['aetherpro_files'] += 1

        print(f"\n✅ Total examples extracted: {len(self.examples)}")

    def write_jsonl(self, output_path: Path, examples: List[Dict]):
        """Write examples to JSONL file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                json_line = json.dumps(example, ensure_ascii=False)
                f.write(json_line + '\n')

    def generate_outputs(self):
        """Generate output files and statistics"""
        output_dir = self.base_dir / "minimax-m2-aetherpro-training" / "output"
        output_dir.mkdir(exist_ok=True)

        # Filter by quality (>= 7 for high quality)
        high_quality = [ex for ex in self.examples if ex['quality_score'] >= 7]
        medium_quality = [ex for ex in self.examples if ex['quality_score'] >= 6]

        print(f"High quality (>= 7): {len(high_quality)}")
        print(f"Medium+ quality (>= 6): {len(medium_quality)}")

        # Use medium quality for more examples
        working_set = medium_quality

        # Write main file
        self.write_jsonl(output_dir / "training_dataset.jsonl", working_set)

        # Category-specific files
        categories = {
            'philosophy': ['philosophy'],
            'code_review': ['code_review'],
            'failure_analysis': ['failure_analysis'],
            'technical': ['first_principles', 'electrical', 'ai_architecture', 'coding', 'agentic_workflows']
        }

        category_counts = {}
        for name, cats in categories.items():
            examples = [ex for ex in working_set if ex['category'] in cats]
            category_counts[name] = len(examples)
            if examples:
                self.write_jsonl(output_dir / f"{name}_examples.jsonl", examples)

        # Generate statistics
        stats = {
            "total_examples": len(self.examples),
            "medium_quality_examples": len(medium_quality),
            "high_quality_examples": len(high_quality),
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

        # Write stats
        with open(output_dir / "dataset_stats.json", 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"\n=== DATASET SUMMARY ===")
        print(f"Total examples: {len(working_set)}")
        print(f"\nCategory distribution:")
        for cat, pct in stats.get('category_percentages', {}).items():
            count = stats['category_distribution'][cat]
            print(f"  {cat}: {count} examples ({pct})")

        print(f"\nSource distribution:")
        for src, count in stats['source_distribution'].items():
            print(f"  {src}: {count}")

        print(f"\nFiles saved to: {output_dir}/")

def main():
    parser = EnhancedParser("/home/user/Dataset-Curator")
    print("=== Enhanced Dataset Parser ===\n")
    parser.process_all_files()
    parser.generate_outputs()
    print("\n✅ Dataset parsing complete!")

if __name__ == "__main__":
    main()
