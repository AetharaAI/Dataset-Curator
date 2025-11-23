#!/usr/bin/env python3
"""
Comprehensive Dataset Parser for MiniMax-M2-AetherPro Training
Parses markdown files and converts them to JSONL format per Parser-Instructions.md
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

class DatasetParser:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.examples = []
        self.stats = defaultdict(int)

        # Target distribution (60/15/15/10)
        self.target_distribution = {
            'technical': 0.60,  # electrical, control theory, thermo, fluids
            'philosophy': 0.15,
            'code_review': 0.15,
            'failure_analysis': 0.10
        }

    def clean_text(self, text: str) -> str:
        """Clean text but don't escape - json.dumps will handle escaping"""
        # Just normalize whitespace and remove any existing escape sequences
        text = text.strip()
        return text

    def calculate_quality_score(self, text: str, thinking: str) -> int:
        """Calculate quality score 1-10 based on content"""
        score = 5  # Base score

        # Check for equations (LaTeX or mathematical expressions)
        if re.search(r'\$\$.*?\$\$|\$.*?\$|\\[a-z]+\{', text) or \
           re.search(r'\$\$.*?\$\$|\$.*?\$|\\[a-z]+\{', thinking):
            score += 1

        # Check for real constraints (NEC, IEEE, physics laws, theorems)
        constraint_keywords = r'NEC|IEEE|Shannon|Nyquist|Ohm|Kirchhoff|Carnot|Reynolds|Bernoulli|constraint|theorem|law|principle'
        if re.search(constraint_keywords, text, re.IGNORECASE) or \
           re.search(constraint_keywords, thinking, re.IGNORECASE):
            score += 1

        # Check for failure modes/edge cases
        failure_keywords = r'failure|fail|edge case|break|violate|cascade|diverge|overflow|deadlock'
        if re.search(failure_keywords, text, re.IGNORECASE):
            score += 1

        # Check for substantial thinking (200+ chars)
        if len(thinking) > 200:
            score += 1

        # Check for multi-turn (multiple user/assistant pairs)
        user_count = text.count('<|user|>')
        if user_count >= 3:
            score += 1

        # Cap at 10
        return min(score, 10)

    def extract_conversation_blocks(self, content: str) -> List[str]:
        """Extract conversation blocks that are already formatted"""
        # Pattern for complete conversation blocks
        pattern = r'```\s*\n(<\|user\|>.*?<\|end\|>)\s*```'
        matches = re.findall(pattern, content, re.DOTALL)

        if matches:
            return matches

        # Alternative pattern without code fences
        pattern2 = r'(<\|user\|>.*?<\|end\|>(?:\s*<\|user\|>.*?<\|end\|>)*)'
        matches2 = re.findall(pattern2, content, re.DOTALL)

        return matches2

    def extract_dialogues_from_structured(self, content: str) -> List[Tuple[str, str, str]]:
        """Extract structured dialogues with thinking traces"""
        examples = []

        # Find dialogue sections
        dialogue_pattern = r'\*\*Turn \d+.*?\*\*User:\*\*\s*"(.*?)".*?\*\*AI:\*\*\s*"(.*?)"'
        matches = re.findall(dialogue_pattern, content, re.DOTALL)

        for user_msg, ai_response in matches:
            # Try to extract thinking from the AI response
            think_match = re.search(r'((?:We should|This is|Starting from).*?(?:equation|principle|analogy).*?\.)',
                                   ai_response, re.DOTALL)
            thinking = think_match.group(1) if think_match else self.generate_thinking_trace(user_msg, ai_response)

            examples.append((user_msg.strip(), thinking, ai_response.strip()))

        return examples

    def generate_thinking_trace(self, user_msg: str, response: str) -> str:
        """Generate a basic thinking trace from user message and response"""
        # Extract key concepts from response
        has_equation = bool(re.search(r'\$.*?\$', response))
        has_principle = bool(re.search(r'principle|law|theorem|equation', response, re.IGNORECASE))

        thinking_parts = []

        if has_equation or has_principle:
            thinking_parts.append("Applying first principles to this problem:")

            # Extract any equations
            equations = re.findall(r'\$\$(.*?)\$\$', response)
            if equations:
                thinking_parts.append(f"1. Governing equation: {equations[0]}")

            # Look for analogies
            analogy_match = re.search(r'(like|similar to|analogous to|maps to)\s+([^.]+)', response, re.IGNORECASE)
            if analogy_match:
                thinking_parts.append(f"2. Physical analogy: {analogy_match.group(2)}")

            # Look for step-by-step reasoning
            steps = re.findall(r'\d+\.\s+([^.]+\.)', response)
            if steps:
                thinking_parts.append("3. Step-by-step breakdown:")
                thinking_parts.extend([f"   - {step}" for step in steps[:3]])
        else:
            # Generate basic thinking for non-equation examples
            thinking_parts.append("Analyzing the problem:")
            thinking_parts.append("1. Identify the core issue")
            thinking_parts.append("2. Map to known patterns or principles")
            thinking_parts.append("3. Apply solution with constraints")

        return "\n".join(thinking_parts) if thinking_parts else "Analyzing the request and applying relevant principles."

    def parse_first_principles_file(self, filepath: Path) -> List[Dict]:
        """Parse first principles engineering files (Gemini, Kimi, Grok examples)"""
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        examples = []

        # First try to extract already-formatted conversation blocks
        conv_blocks = self.extract_conversation_blocks(content)

        for block in conv_blocks:
            # Block is already in correct format
            thinking_match = re.search(r'<think>(.*?)</think>', block, re.DOTALL)
            thinking = thinking_match.group(1).strip() if thinking_match else ""

            quality_score = self.calculate_quality_score(block, thinking)

            # Determine category from content
            category = self.determine_category(block, filepath)
            source = self.determine_source(filepath)

            example = {
                "text": block,
                "source": source,
                "category": category,
                "quality_score": quality_score
            }
            examples.append(example)

        # If no pre-formatted blocks, extract dialogues
        if not conv_blocks:
            dialogues = self.extract_dialogues_from_structured(content)

            for user_msg, thinking, response in dialogues:
                # Build the conversation text
                text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"

                quality_score = self.calculate_quality_score(text, thinking)
                category = self.determine_category(text, filepath)
                source = self.determine_source(filepath)

                example = {
                    "text": text,
                    "source": source,
                    "category": category,
                    "quality_score": quality_score
                }
                examples.append(example)

        return examples

    def parse_philosophy_file(self, filepath: Path) -> List[Dict]:
        """Parse philosophy/consciousness files"""
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        examples = []

        # Extract conversation blocks
        conv_blocks = self.extract_conversation_blocks(content)

        for block in conv_blocks:
            thinking_match = re.search(r'<think>(.*?)</think>', block, re.DOTALL)
            thinking = thinking_match.group(1).strip() if thinking_match else ""

            quality_score = self.calculate_quality_score(block, thinking)

            example = {
                "text": block,
                "source": "philosophy_generated",
                "category": "philosophy",
                "quality_score": quality_score
            }
            examples.append(example)

        return examples

    def parse_aetherpro_docs(self, filepath: Path) -> List[Dict]:
        """Parse AetherPro documentation files"""
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        examples = []

        # For docs, we need to create Q&A pairs from content
        # Look for sections with headers
        sections = re.split(r'\n#{1,3}\s+', content)

        for section in sections[1:]:  # Skip first empty split
            if len(section.strip()) < 100:  # Skip very short sections
                continue

            # Extract title and content
            lines = section.split('\n', 1)
            if len(lines) < 2:
                continue

            title = lines[0].strip()
            section_content = lines[1].strip()

            # Create a Q&A from the section
            user_msg = f"Explain {title}"

            # Generate thinking trace
            thinking = f"Analyzing {title}:\n1. Review the architecture and purpose\n2. Identify key components and their interactions\n3. Explain implementation details and constraints"

            # Use first 500 chars of content as response (summary)
            response = section_content[:500] + "..." if len(section_content) > 500 else section_content

            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"

            # Determine category based on filepath
            if 'architecture' in str(filepath):
                category = 'ai_architecture'
            elif 'philosophy' in str(filepath):
                category = 'philosophy'
            else:
                category = 'ai_architecture'

            quality_score = self.calculate_quality_score(text, thinking)

            example = {
                "text": text,
                "source": "aetherpro_docs",
                "category": category,
                "quality_score": quality_score
            }
            examples.append(example)

        return examples

    def determine_category(self, text: str, filepath: Path) -> str:
        """Determine category based on content and filepath"""
        text_lower = text.lower()
        filepath_str = str(filepath).lower()

        # Check for philosophy
        if 'philosophy' in filepath_str or 'consciousness' in filepath_str:
            return 'philosophy'

        # Check for code review
        if 'code' in text_lower and ('review' in text_lower or '```' in text):
            return 'code_review'

        # Check for failure analysis
        if any(word in text_lower for word in ['failure', 'debug', 'crash', 'error', 'fault']):
            return 'failure_analysis'

        # Check for electrical
        if any(word in text_lower for word in ['electrical', 'voltage', 'current', 'circuit', 'nec', 'ohm']):
            return 'electrical'

        # Check for AI architecture
        if any(word in text_lower for word in ['agent', 'llm', 'model', 'inference', 'deployment', 'orchestration']):
            return 'ai_architecture'

        # Default to first principles for technical content
        if any(word in text_lower for word in ['equation', 'principle', 'theorem', 'control theory', 'thermodynamics']):
            return 'first_principles'

        return 'first_principles'

    def determine_source(self, filepath: Path) -> str:
        """Determine source based on filepath"""
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
        elif 'aetherpro' in filepath_str:
            return 'aetherpro_docs'
        elif 'philosophy' in filepath_str:
            return 'philosophy_generated'
        else:
            return 'first_principles_generated'

    def process_all_files(self):
        """Process all files in the dataset"""

        # Process First Principles / Engineering files
        fp_dir = self.base_dir / "First-Principles-Failures-Engineering-&-Deugging"
        if fp_dir.exists():
            for md_file in fp_dir.glob("*.md"):
                if md_file.name == 'Weighting-Value-Table.md':
                    continue  # Skip metadata file
                print(f"Processing: {md_file.name}")
                examples = self.parse_first_principles_file(md_file)
                self.examples.extend(examples)
                self.stats['first_principles_files'] += 1

        # Process Philosophy/Consciousness files
        phil_dir = self.base_dir / "Corys-claude-convos-peronality-datasets"
        if phil_dir.exists():
            for md_file in phil_dir.glob("*.md"):
                if 'README' in md_file.name or 'EXECUTIVE' in md_file.name:
                    continue  # Skip meta files
                print(f"Processing: {md_file.name}")

                if 'Philosophy' in md_file.name or 'Consciousness' in md_file.name:
                    examples = self.parse_philosophy_file(md_file)
                else:
                    examples = self.parse_first_principles_file(md_file)

                self.examples.extend(examples)
                self.stats['philosophy_files'] += 1

        # Process AetherPro docs
        aetherpro_dir = self.base_dir / "minimax-m2-aetherpro-training" / "aetherpro_docs"
        if aetherpro_dir.exists():
            for md_file in aetherpro_dir.rglob("*.md"):
                print(f"Processing: {md_file.relative_to(self.base_dir)}")
                examples = self.parse_aetherpro_docs(md_file)
                self.examples.extend(examples)
                self.stats['aetherpro_files'] += 1

        print(f"\nTotal examples extracted: {len(self.examples)}")

    def write_jsonl(self, output_path: Path, examples: List[Dict]):
        """Write examples to JSONL file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                # Create the JSON line - NO ESCAPING HERE, json.dumps handles it
                json_line = json.dumps(example, ensure_ascii=False)
                f.write(json_line + '\n')

    def generate_outputs(self):
        """Generate all output files"""
        output_dir = self.base_dir / "minimax-m2-aetherpro-training" / "output"
        output_dir.mkdir(exist_ok=True)

        # Filter by quality (keep quality_score >= 6)
        high_quality = [ex for ex in self.examples if ex['quality_score'] >= 6]

        print(f"\nHigh quality examples (score >= 6): {len(high_quality)}")

        # Write main validation file
        self.write_jsonl(output_dir / "validation_examples.jsonl", high_quality)

        # Write category-specific files
        philosophy_examples = [ex for ex in high_quality if ex['category'] == 'philosophy']
        self.write_jsonl(output_dir / "philosophy_examples.jsonl", philosophy_examples)

        code_review_examples = [ex for ex in high_quality if ex['category'] == 'code_review']
        self.write_jsonl(output_dir / "code_review_examples.jsonl", code_review_examples)

        failure_examples = [ex for ex in high_quality if ex['category'] == 'failure_analysis']
        self.write_jsonl(output_dir / "failure_analysis_examples.jsonl", failure_examples)

        technical_examples = [ex for ex in high_quality if ex['category'] in
                             ['electrical', 'first_principles', 'ai_architecture', 'coding', 'agentic_workflows']]
        self.write_jsonl(output_dir / "technical_examples.jsonl", technical_examples)

        # Generate stats
        stats = {
            "total_examples": len(self.examples),
            "high_quality_examples": len(high_quality),
            "files_processed": {
                "first_principles": self.stats['first_principles_files'],
                "philosophy": self.stats['philosophy_files'],
                "aetherpro": self.stats['aetherpro_files']
            },
            "category_distribution": {},
            "source_distribution": {},
            "quality_distribution": {}
        }

        # Calculate distributions
        for ex in high_quality:
            stats['category_distribution'][ex['category']] = \
                stats['category_distribution'].get(ex['category'], 0) + 1
            stats['source_distribution'][ex['source']] = \
                stats['source_distribution'].get(ex['source'], 0) + 1
            stats['quality_distribution'][str(ex['quality_score'])] = \
                stats['quality_distribution'].get(str(ex['quality_score']), 0) + 1

        # Calculate percentages for categories
        total = len(high_quality)
        stats['category_percentages'] = {
            cat: f"{(count/total)*100:.1f}%"
            for cat, count in stats['category_distribution'].items()
        }

        # Write stats
        with open(output_dir / "stats.json", 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"\n=== OUTPUT SUMMARY ===")
        print(f"Validation examples: {len(high_quality)}")
        print(f"Philosophy examples: {len(philosophy_examples)}")
        print(f"Code review examples: {len(code_review_examples)}")
        print(f"Failure analysis examples: {len(failure_examples)}")
        print(f"Technical examples: {len(technical_examples)}")
        print(f"\nCategory distribution:")
        for cat, pct in stats['category_percentages'].items():
            print(f"  {cat}: {pct}")
        print(f"\nStats saved to: {output_dir / 'stats.json'}")

def main():
    parser = DatasetParser("/home/user/Dataset-Curator")
    print("Starting dataset parsing...")
    parser.process_all_files()
    parser.generate_outputs()
    print("\n✅ Dataset parsing complete!")

if __name__ == "__main__":
    main()
