# Deal Memo Quality System - Complete Guide

## Overview

This system creates a complete feedback loop for improving AI-generated VC deal memos through quality analysis, human feedback, and automated prompt improvement.

---

## Components

### 1️⃣ Quality Analyzer (`quality_analyzer.py`)

Analyzes generated deal memos using AI and provides structured quality reports.

**Usage:**
```bash
python3 quality_analyzer.py deal_memo_filename.md
```

**Output:**
- `*_quality.json` - Structured quality data
- `*_quality.txt` - Human-readable report

**Features:**
- Section-by-section scoring (1-10)
- Completeness flags
- Data verification (unsourced claims)
- Red flags with severity levels
- Improvement priorities

---

### 2️⃣ Feedback Interface (`feedback_interface.html`)

Web interface for reviewing memos and providing structured feedback.

**Usage:**
```bash
open feedback_interface.html
```

**Workflow:**
1. Click "Choose Quality Report JSON"
2. Load a `*_quality.json` file
3. Click sections to review them
4. Rate each section: ✅ Good / ⚠️ Needs Work / ❌ Wrong
5. Add corrections and comments
6. Export feedback as JSON

**Features:**
- Visual quality highlighting (green/yellow/red)
- Interactive rating system
- Progress tracking
- Export feedback for analysis

---

### 3️⃣ Improvement Engine (`improvement_engine.py`)

Analyzes feedback patterns and generates improved prompts.

**Usage:**
```bash
python3 improvement_engine.py
```

**Requirements:**
- At least one `feedback_*.json` file in the directory

**Output:**
- `pattern_analysis_*.txt` - Feedback pattern report
- `prompt_improvement_*.md` - Before/after comparison
- `improved_prompt_*.txt` - New prompt ready to use
- `improvement_data_*.json` - Structured improvement data

**Features:**
- Pattern detection across multiple memos
- Identifies consistently problematic sections
- AI-generated prompt improvements
- Before/after comparison
- Specific improvement recommendations

---

### 4️⃣ Dashboard (`dashboard.html`)

Visual analytics dashboard for quality metrics and trends.

**Usage:**
```bash
open dashboard.html
```

**Workflow:**
1. Click "Load Feedback Files"
2. Select multiple `feedback_*.json` files
3. View comprehensive analytics

**Features:**
- Quality score trends over time
- Section performance breakdowns
- Most common issues
- Partner satisfaction trends
- Improvement timeline
- Interactive charts powered by Chart.js

---

## Complete Workflow

### Step 1: Generate Initial Memo
```bash
python3 deal_memo_generator.py
# Enter company URL when prompted
# Output: deal_memo_*.md
```

### Step 2: Analyze Quality
```bash
python3 quality_analyzer.py deal_memo_*.md
# Output: deal_memo_*_quality.json & .txt
```

### Step 3: Provide Feedback
```bash
open feedback_interface.html
# Load the quality JSON
# Review and rate all sections
# Export as feedback_*.json
```

### Step 4: Generate Improvements
```bash
# After collecting feedback on 3-5 memos:
python3 improvement_engine.py
# Output: Improved prompt and analysis reports
```

### Step 5: View Dashboard
```bash
open dashboard.html
# Load all feedback files
# Analyze trends and improvements
```

### Step 6: Apply Improvements
1. Open `deal_memo_generator.py`
2. Replace the `prompt` variable with content from `improved_prompt_*.txt`
3. Generate new memos with improved quality

---

## Files Generated

| File Pattern | Description | Component |
|--------------|-------------|-----------|
| `deal_memo_*.md` | Generated investment memo | Generator |
| `*_quality.json` | Structured quality report | Analyzer |
| `*_quality.txt` | Human-readable quality report | Analyzer |
| `feedback_*.json` | Exported user feedback | Interface |
| `pattern_analysis_*.txt` | Feedback pattern report | Engine |
| `prompt_improvement_*.md` | Before/after comparison | Engine |
| `improved_prompt_*.txt` | Ready-to-use improved prompt | Engine |
| `improvement_data_*.json` | Structured improvement data | Engine |

---

## Key Metrics

### Quality Scores
- **9-10**: Exceptional - Deep insights, specific data
- **7-8**: Strong - Good analysis, mostly complete
- **5-6**: Adequate - Covers basics, lacks depth
- **3-4**: Weak - Superficial, generic, missing info
- **1-2**: Poor - Incomplete, potentially misleading

### Section Ratings
- **✅ Good**: Meets investment decision standards
- **⚠️ Needs Work**: Insufficient detail or specificity
- **❌ Wrong**: Factual errors or critical omissions

---

## Sample Data Included

The system includes sample feedback files for testing:
- `feedback_deal_memo_scale_20251120_111933_sample.json`
- `feedback_sample_memo2.json`

These demonstrate the feedback structure and allow immediate testing of Components 3 & 4.

---

## Environment Setup

**Required:**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

**Dependencies:**
```bash
pip install anthropic requests beautifulsoup4
```

**For Web Components:**
- Modern web browser
- Internet connection (for Chart.js CDN)

---

## Tips for Best Results

1. **Provide detailed feedback**: Specific corrections help the improvement engine generate better prompts

2. **Review multiple memos**: Patterns emerge after 3-5 memos, making improvements more effective

3. **Focus on consistency**: Rate similar issues consistently across memos

4. **Iterate**: Apply improved prompts → Generate new memos → Analyze → Repeat

5. **Track progress**: Use the dashboard to visualize improvements over time

---

## Troubleshooting

**Quality Analyzer fails:**
- Ensure ANTHROPIC_API_KEY is set
- Check memo file exists and is readable

**Improvement Engine finds no feedback:**
- Export feedback from the interface first
- Ensure `feedback_*.json` files are in the directory

**Dashboard shows no data:**
- Load multiple feedback JSON files
- Ensure files have the correct structure

**Charts not rendering:**
- Check internet connection (Chart.js CDN)
- Try a different browser
- Check browser console for errors

---

## Next Steps

1. **Generate more memos** with different companies
2. **Collect diverse feedback** from multiple reviewers
3. **Apply improved prompts** and measure quality gains
4. **Expand the system**: Add more sections, custom scoring, team collaboration features

---

## System Architecture

```
deal_memo_generator.py → memo.md
                            ↓
quality_analyzer.py → quality.json + quality.txt
                            ↓
feedback_interface.html → feedback.json
                            ↓
improvement_engine.py → improved_prompt.txt + reports
                            ↓
dashboard.html → Visual analytics
```

---

## Demo Flow (Using Sample Data)

```bash
# 1. Analyze existing memo
python3 quality_analyzer.py deal_memo_scale_20251120_111933.md

# 2. Open feedback interface
open feedback_interface.html
# Load the quality JSON, review, and export

# 3. Run improvement engine (uses sample feedback)
python3 improvement_engine.py

# 4. View dashboard
open dashboard.html
# Load all feedback files in directory

# 5. Check the improvement report
cat prompt_improvement_*.md
```

---

**Built for Primary VC - PrimaryOS Operations**
*Demonstrating continuous improvement through feedback loops*
