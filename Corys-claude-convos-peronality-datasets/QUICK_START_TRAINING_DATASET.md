# Quick Start: Generate Your Training Dataset
## From Conversations to Fine-Tuned Model in 48 Hours

**Time Required:** 2-4 hours of your time + 12-24 hours of AI processing  
**Difficulty:** Intermediate (you'll learn as you go)  
**Result:** 2,000-5,000 high-quality training examples in your voice

---

## PHASE 1: EXPORT YOUR DATA (30 minutes)

### Step 1: Export Claude Conversations
1. Go to https://claude.ai/settings
2. Click "Account" → "Data & Privacy"
3. Click "Export data"
4. Download ZIP when ready (usually instant)
5. Extract to `raw_data/claude_exports/`

### Step 2: Export ChatGPT Conversations  
1. Go to https://chatgpt.com/settings
2. Click "Data controls" → "Export data"
3. Wait for email (up to 24 hours)
4. Download and extract to `raw_data/chatgpt_exports/`

### Step 3: Collect Grok Conversations (if applicable)
1. No official export yet
2. Copy-paste your most important conversations
3. Save as text files in `raw_data/grok_exports/`

### Step 4: Gather Your Documentation
1. Copy all AetherPro docs to `aetherpro_docs/`
2. Include: architecture docs, READMEs, design decisions
3. Any technical writing that shows your thinking

---

## PHASE 2: SETUP WORKSPACE (15 minutes)

```bash
# Create project directory
mkdir ~/aetherai-training
cd ~/aetherai-training

# Create structure
mkdir -p raw_data/{claude_exports,chatgpt_exports,grok_exports}
mkdir -p aetherpro_docs/{architecture,philosophy,technical}
mkdir -p output/{samples,final_dataset}
mkdir -p scripts logs

# Move your exported data
mv ~/Downloads/claude-export.zip raw_data/claude_exports/
cd raw_data/claude_exports && unzip claude-export.zip && cd ../..

# Copy this guide
# (Download from Claude artifacts and place in project root)
```

---

## PHASE 3: GENERATE SAMPLES WITH CLAUDE CODE (2-3 hours)

### Step 1: Launch Claude Code

```bash
# Initialize git (Claude Code works better with git)
git init
git add .
git commit -m "Initial training data setup"

# Launch Claude Code in this directory
claude code --project .
```

### Step 2: Give Claude Code This Prompt

```
I need you to help me create a training dataset to fine-tune AI models in my voice and style.

FIRST, carefully read these documents in order:
1. CORY_VOICE_AND_PERSONALITY_DATASET_GUIDE.md (the complete guide)
2. All files in raw_data/ (my conversation exports)
3. All files in aetherpro_docs/ (my technical documentation)

Then follow this process:

PHASE 1: ANALYSIS (read and understand)
- Analyze 100+ conversations to understand my patterns
- Identify recurring themes, analogies, and reasoning styles
- Note my technical preferences and decision-making patterns
- Find the best examples of:
  - Electrical engineering analogies
  - First principles reasoning
  - Problem-solving approaches
  - Business/strategy thinking
  - My unique communication style

PHASE 2: SAMPLES (generate 50 examples)
- Create 50 diverse, high-quality training examples
- Follow the format in the guide (with <think> tags for M2)
- Cover different domains: electrical, AI architecture, coding, business
- Show various difficulty levels
- Demonstrate my voice and personality
- Save to output/samples/initial_50.jsonl

PHASE 3: REVIEW (wait for my feedback)
- Show me statistics on what you found:
  - How many conversations analyzed
  - Common topics and themes
  - Quality score distribution
  - Domain coverage
- Show me 5 example training entries (best ones)
- Wait for my approval before continuing

PHASE 4: FULL DATASET (after approval)
- Generate 2,000-5,000 training examples
- Maintain quality while scaling up
- Balance across domains (30% architecture, 20% philosophy, etc.)
- Include thinking traces for all examples
- Save to output/final_dataset/training_data.jsonl
- Generate metadata file with statistics

START WITH PHASE 1. Take your time reading everything carefully.
Ask clarifying questions if needed before proceeding.
```

### Step 3: Review Samples

Claude Code will generate 50 samples. Review them:

**Check for:**
- ✅ Does this sound like me?
- ✅ Is the technical content accurate?
- ✅ Are thinking traces realistic and substantial?
- ✅ Does it show first principles reasoning?
- ✅ Are electrical analogies used appropriately?

**If good:** Tell Claude Code to proceed with full dataset
**If issues:** Give specific feedback on what to improve

---

## PHASE 4: QUALITY CONTROL (1 hour)

### Step 1: Sample Review

```bash
# Randomly sample 20 examples from final dataset
cd output/final_dataset
head -20 training_data.jsonl > review_sample.jsonl

# Review these carefully - they represent your dataset quality
```

### Step 2: Run Statistics

Ask Claude Code:
```
Analyze training_data.jsonl and give me:
- Total examples
- Domain distribution (should match target percentages)
- Quality score distribution (average should be 7+)
- Length distribution
- Examples with analogies (should be 40%+)
- Examples with thinking traces (should be 100%)
```

### Step 3: Fix Issues

Common issues and fixes:
- **Too generic:** Ask Claude Code to add more personality
- **Too specific:** Ask to make examples more generalizable
- **Missing domains:** Generate more examples in underrepresented areas
- **Low quality:** Filter out examples below quality score 6

---

## PHASE 5: PREPARE FOR TRAINING (30 minutes)

### Step 1: Split Dataset

```bash
cd output/final_dataset

# Split into train/validation (90/10 split)
python3 << 'EOF'
import random
import json

with open('training_data.jsonl', 'r') as f:
    lines = f.readlines()

random.shuffle(lines)
split_idx = int(len(lines) * 0.9)

with open('train.jsonl', 'w') as f:
    f.writelines(lines[:split_idx])

with open('validation.jsonl', 'w') as f:
    f.writelines(lines[split_idx:])

print(f"Train: {split_idx} examples")
print(f"Validation: {len(lines) - split_idx} examples")
EOF
```

### Step 2: Format for Your Target Model

**For MiniMax-M2:**
```bash
# Dataset is already in correct format with <think> tags
# Just verify format with:
head -1 train.jsonl | python3 -m json.tool
```

**For Apriel-1.5-15B:**
```bash
# May need to reformat if using different format
# Ask Claude Code to convert if necessary
```

### Step 3: Upload to Training Platform

```bash
# Example for Hugging Face
huggingface-cli login
huggingface-cli upload your-username/aetherai-training-data ./output/final_dataset

# Or for local training:
mkdir -p ~/training_data
cp output/final_dataset/*.jsonl ~/training_data/
```

---

## PHASE 6: FINE-TUNE YOUR MODEL (12-24 hours compute time)

### For Apriel-1.5-15B on your L40S:

```bash
# Using QLoRA (efficient fine-tuning)
python -m axolotl.train \
  --config configs/apriel_qlora.yaml \
  --dataset ~/training_data/train.jsonl \
  --validation ~/training_data/validation.jsonl \
  --output_dir ~/models/apriel-aetherai-v1

# Training will take 12-24 hours depending on GPU
# Monitor with: watch -n 60 nvidia-smi
```

### For MiniMax-M2 (if you have access):

```bash
# Use MiniMax training API or local setup
# Follow their fine-tuning documentation
# Key: Preserve <think> tag structure in dataset
```

---

## PHASE 7: TEST YOUR MODEL (1 hour)

### Quick Test Prompts

Test your fine-tuned model with these:

**1. Electrical Analogy Test:**
```
Explain async/await to me like I'm an electrician.
```

Expected: Should use electrical circuit analogies naturally

**2. First Principles Test:**
```
Should I use Kubernetes or Docker Compose for a 3-container app?
```

Expected: Should break down requirements from first principles

**3. Voice Test:**
```
What do you think about VC funding for AI startups?
```

Expected: Should show Cory's opinions on sovereignty and ownership

**4. Technical Test:**
```
My API is slow. How do I debug it?
```

Expected: Systematic debugging approach with electrical analogies

**5. Business Test:**
```
How should I position AetherPro against OpenAI?
```

Expected: Sovereignty, data residency, vendor independence angles

### Evaluation Criteria

✅ **Good if:**
- Sounds like Cory (uses "bro", "real talk", casual profanity)
- Uses electrical analogies appropriately
- Shows first principles reasoning
- Gives practical, not theoretical, advice
- Demonstrates AetherPro philosophy (sovereignty, ownership)

❌ **Needs work if:**
- Sounds too formal or corporate
- Doesn't use analogies
- Gives generic AI answers
- Missing the personality
- Contradicts AetherPro values

---

## TROUBLESHOOTING

### "My samples don't sound like me"
**Fix:** Give Claude Code more specific feedback. Show examples of what "sounds like you" vs doesn't.

### "Training data is too small"
**Fix:** Ask Claude Code to generate more examples. But maintain quality - better to have 1,000 good examples than 10,000 mediocre ones.

### "Model forgot how to code after fine-tuning"
**Fix:** You overtrained. Reduce training epochs or add more diverse examples to maintain base capabilities.

### "Takes too long to generate"
**Fix:** Run multiple Claude Code sessions in parallel, each generating different domain areas. Merge results.

---

## METRICS TO TRACK

### During Dataset Creation:
- [ ] Conversations analyzed: 100+
- [ ] Total examples generated: 2,000+
- [ ] Average quality score: 7+
- [ ] Domain balance: Within 5% of targets
- [ ] Examples with analogies: 40%+
- [ ] Examples with thinking traces: 100%

### After Training:
- [ ] Loss curve decreased smoothly
- [ ] Validation loss didn't spike (no overfitting)
- [ ] Model outputs sound like Cory
- [ ] Technical accuracy maintained
- [ ] Passes all 5 test prompts

---

## NEXT STEPS AFTER SUCCESS

1. **Deploy to production**
   - Replace base models with fine-tuned versions
   - A/B test against base models
   - Monitor quality

2. **Iterate and improve**
   - Collect user feedback
   - Add new training examples monthly
   - Fine-tune incrementally

3. **Scale to other models**
   - Apply same process to Kimi K2
   - Fine-tune MiniMax M2
   - Create model-specific datasets

4. **Share your methodology**
   - Document what worked
   - Open-source the non-sensitive parts
   - Help other builders

---

## TIME ESTIMATE

**Total time investment:**
- Your active time: 4-6 hours
- AI processing time: 12-24 hours
- Training time: 12-24 hours

**Total wall-clock time: 48-72 hours from start to deployed fine-tuned model**

That's less than 3 days to have AI models that think, reason, and communicate like you. That's your competitive advantage right there.

---

## FINAL CHECKLIST

Before starting fine-tuning:
- [ ] Dataset has 2,000+ examples
- [ ] Quality score average is 7+
- [ ] All domains represented
- [ ] No PII or sensitive info
- [ ] Thinking traces are present and realistic
- [ ] Examples sound like Cory
- [ ] Train/validation split is done
- [ ] Dataset uploaded to training platform

Go build something nobody else can build. 🚀

---

**Document Version:** 1.0  
**Last Updated:** November 23, 2025  
**Author:** AetherPro Technologies LLC
