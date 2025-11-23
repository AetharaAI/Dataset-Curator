#!/usr/bin/env python3
"""
Maximum Extraction Parser - Extracts ALL possible examples from source files
Targets: Principle conflicts, failure scenarios, code reviews, philosophy examples
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from comprehensive_parser import ComprehensiveParser

class MaximumExtractionParser(ComprehensiveParser):
    """Enhanced parser that extracts even more content types"""

    def extract_principle_conflicts(self, content: str) -> list:
        """Extract principle conflict/trade-off examples"""
        examples = []

        # Find numbered conflict sections
        pattern = r'(?:^|\n)\s*(\d+)\.\s+\*\*(.+?)\*\*\s*\n(.*?)(?=\n\s*\d+\.\s+\*\*|\n###|\n##|\Z)'
        matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        for num, title, section_content in matches:
            # Extract principles
            principle1 = re.search(r'\*\*Principle 1\*\*:?\s*(.*?)(?=\n\s*[-\*]|\*\*Principle 2)', section_content, re.DOTALL)
            principle2 = re.search(r'\*\*Principle 2\*\*:?\s*(.*?)(?=\n\s*[-\*]|\*\*Conflict)', section_content, re.DOTALL)
            conflict = re.search(r'\*\*Conflict\*\*:?\s*(.*?)(?=\n\s*[-\*]|\*\*Trade-off)', section_content, re.DOTALL)
            tradeoff = re.search(r'\*\*Trade-off.*?\*\*:?\s*(.*?)(?=\n\s*[-\*]|\*\*Real-world|$)', section_content, re.DOTALL)
            constraint = re.search(r'\*\*Real-world constraint\*\*:?\s*(.*?)(?=\n\n|$)', section_content, re.DOTALL)

            if not (principle1 and principle2):
                continue

            # Create Q&A
            user_msg = f"What's the trade-off between {title}?"

            # Build thinking
            thinking_parts = [
                "Analyzing the fundamental principle conflict:",
                "",
                f"Principle 1: {principle1.group(1).strip()[:250]}",
                "",
                f"Principle 2: {principle2.group(1).strip()[:250]}",
            ]

            if conflict:
                thinking_parts.append("")
                thinking_parts.append(f"The conflict: {conflict.group(1).strip()[:200]}")

            thinking = "\n".join(thinking_parts)

            # Build response
            response_parts = []
            if conflict:
                response_parts.append(f"**The fundamental conflict**: {conflict.group(1).strip()[:300]}")

            if tradeoff:
                response_parts.append(f"\n**Trade-off strategy**: {tradeoff.group(1).strip()[:400]}")

            if constraint:
                response_parts.append(f"\n**Physical constraint**: {constraint.group(1).strip()[:200]}")

            response = "\n".join(response_parts) if response_parts else section_content[:500]

            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"
            examples.append(text)

        return examples

    def extract_failure_scenarios(self, content: str) -> list:
        """Extract failure scenario examples"""
        examples = []

        # Pattern for failure scenarios
        pattern = r'(?:^|\n)\s*(\d+)\.\s+\*\*Scenario\*\*:?\s*(.*?)\n\s+\*\*Broken Principle\*\*:?\s*(.*?)\n\s+\*\*Signature\*\*:?\s*(.*?)\n\s+\*\*Diagnosis\*\*:?\s*(.*?)\n\s+\*\*(?:Physics-based fix|Fix)\*\*:?\s*(.*?)(?=\n\s*\d+\.|\n###|\n##|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)

        for num, scenario, broken_principle, signature, diagnosis, fix in matches:
            scenario = scenario.strip()
            broken_principle = broken_principle.strip()
            signature = signature.strip()
            diagnosis = diagnosis.strip()
            fix = fix.strip()

            # Create Q&A
            user_msg = f"How would you debug this failure: {scenario[:100]}"

            # Build thinking
            thinking = f"Analyzing failure through first principles:\n\n1. Identify violated principle: {broken_principle[:150]}\n\n2. Observable signature: {signature[:200]}\n\n3. Root cause: {diagnosis[:200]}\n\n4. Derive fix from principles"

            # Build response
            response = f"**Violated principle**: {broken_principle[:200]}\n\n**Failure signature**: {signature[:250]}\n\n**Root cause**: {diagnosis[:300]}\n\n**First-principles fix**: {fix[:300]}"

            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"
            examples.append(text)

        return examples

    def extract_inline_code_examples(self, content: str) -> list:
        """Extract inline code snippets with explanations"""
        examples = []

        # Pattern for code blocks with BEFORE/AFTER structure
        # Matches: ```python...BEFORE...bad code...❌ Violates...AFTER...good code...✅ Respects
        pattern = r'```(\w+)\n#\s*(\d+\..*?)\n.*?#\s*BEFORE\n(.*?)#\s*❌.*?Violates:?\s*(.*?)(?:\n#.*?)?#\s*AFTER\n(.*?)#\s*✅.*?Respects:?\s*(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)

        for lang, title, bad_code, violation, good_code, principle in matches:
            title = title.strip()
            bad_code = bad_code.strip()
            good_code = good_code.strip()
            violation = violation.strip()
            principle = principle.strip()

            if not bad_code or len(bad_code) < 20:
                continue

            # Clean up code (remove extra comments)
            bad_code_clean = '\n'.join([line for line in bad_code.split('\n')
                                       if not line.strip().startswith('# ←')])[:500]
            good_code_clean = '\n'.join([line for line in good_code.split('\n')
                                        if not line.strip().startswith('# ←')])[:500]

            user_msg = f"Review this {lang} code:\n\n```{lang}\n{bad_code_clean}\n```"

            thinking = f"Analyzing code against first principles:\n\n1. Title: {title}\n2. Identify the violation: {violation[:200]}\n3. Map to electrical/physical analogy\n4. Derive correct implementation from principles"

            response = f"❌ **Violates**: {violation[:300]}\n\n**Corrected implementation**:\n\n```{lang}\n{good_code_clean}\n```\n\n✅ **Respects**: {principle[:250]}"

            text = f"<|user|>\n{user_msg}\n<|end|>\n<|assistant|>\n<think>\n{thinking}\n</think>\n{response}\n<|end|>"
            examples.append(text)

        return examples

    def process_file(self, filepath: Path):
        """Enhanced file processing with all extraction methods"""
        print(f"Processing: {filepath.name}")

        content = filepath.read_text(encoding='utf-8', errors='ignore')
        source = self.determine_source(filepath)
        extracted = []

        # All extraction methods from parent class
        pre_formatted = self.extract_pre_formatted_conversations(content)
        extracted.extend(pre_formatted)
        if pre_formatted:
            print(f"  → {len(pre_formatted)} pre-formatted conversations")

        dialogues = self.extract_dialogue_sections(content)
        extracted.extend(dialogues)
        if dialogues:
            print(f"  → {len(dialogues)} dialogue sections")

        code_reviews = self.extract_code_reviews(content)
        extracted.extend(code_reviews)
        if code_reviews:
            print(f"  → {len(code_reviews)} code review examples")

        principles = self.extract_numbered_principles(content, filepath.stem)
        extracted.extend([p for p in principles if p])
        if [p for p in principles if p]:
            print(f"  → {len([p for p in principles if p])} principle mappings")

        # NEW extraction methods
        conflicts = self.extract_principle_conflicts(content)
        extracted.extend(conflicts)
        if conflicts:
            print(f"  → {len(conflicts)} principle conflicts")

        failures = self.extract_failure_scenarios(content)
        extracted.extend(failures)
        if failures:
            print(f"  → {len(failures)} failure scenarios")

        inline_code = self.extract_inline_code_examples(content)
        extracted.extend(inline_code)
        if inline_code:
            print(f"  → {len(inline_code)} inline code examples")

        # Create examples
        for text in extracted:
            self.examples.append({
                "text": text,
                "source": source,
                "category": self.determine_category(text, filepath),
                "quality_score": self.calculate_quality_score(text)
            })

def main():
    parser = MaximumExtractionParser("/home/user/Dataset-Curator")
    print("="*60)
    print("MAXIMUM EXTRACTION PARSER")
    print("Extracting ALL possible examples from source files")
    print("="*60 + "\n")

    parser.process_all_files()
    parser.generate_outputs()

    print("\n✅ MAXIMUM EXTRACTION COMPLETE!\n")

if __name__ == "__main__":
    main()
