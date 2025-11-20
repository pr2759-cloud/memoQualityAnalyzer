"""
Improvement Engine
Analyzes feedback patterns and generates improved prompts for better deal memos
"""

import os
import json
import anthropic
from datetime import datetime
from collections import defaultdict
import glob

def load_feedback_files(feedback_dir="."):
    """Load all feedback JSON files from directory"""
    feedback_files = glob.glob(f"{feedback_dir}/feedback_*.json")

    if not feedback_files:
        print("⚠️  No feedback files found. Run feedback interface first.")
        return []

    feedback_data = []
    for filepath in feedback_files:
        with open(filepath, 'r') as f:
            data = json.load(f)
            feedback_data.append({
                'filepath': filepath,
                'data': data
            })

    return feedback_data

def analyze_feedback_patterns(feedback_data):
    """Analyze patterns across multiple feedback sessions"""

    if not feedback_data:
        return None

    analysis = {
        'total_memos_reviewed': len(feedback_data),
        'section_ratings': defaultdict(lambda: {'good': 0, 'needs_work': 0, 'wrong': 0, 'total': 0}),
        'common_issues': defaultdict(int),
        'quality_score_trend': [],
        'problematic_sections': [],
        'frequent_corrections': []
    }

    all_corrections = []

    for feedback_item in feedback_data:
        data = feedback_item['data']

        # Track quality scores
        if 'overall_quality_score' in data:
            analysis['quality_score_trend'].append(data['overall_quality_score'])

        # Analyze section feedback
        section_feedback = data.get('section_feedback', {})
        for section_id, feedback in section_feedback.items():
            rating = feedback.get('rating')
            if rating:
                # Normalize rating name (handle both 'needs-work' and 'needs_work')
                rating = rating.replace('-', '_')
                analysis['section_ratings'][section_id]['total'] += 1
                if rating in ['good', 'needs_work', 'wrong']:
                    analysis['section_ratings'][section_id][rating] += 1

            # Collect corrections
            correction = feedback.get('correction', '').strip()
            if correction:
                all_corrections.append({
                    'section': section_id,
                    'correction': correction,
                    'rating': rating
                })

    # Identify problematic sections (high needs_work or wrong ratings)
    for section_id, ratings in analysis['section_ratings'].items():
        if ratings['total'] > 0:
            problem_rate = (ratings['needs_work'] + ratings['wrong']) / ratings['total']
            if problem_rate > 0.4:  # More than 40% problematic
                analysis['problematic_sections'].append({
                    'section': section_id,
                    'problem_rate': problem_rate,
                    'needs_work': ratings['needs_work'],
                    'wrong': ratings['wrong'],
                    'total': ratings['total']
                })

    # Sort problematic sections by problem rate
    analysis['problematic_sections'].sort(key=lambda x: x['problem_rate'], reverse=True)

    # Store corrections for prompt improvement
    analysis['all_corrections'] = all_corrections

    # Calculate average quality score
    if analysis['quality_score_trend']:
        analysis['avg_quality_score'] = sum(analysis['quality_score_trend']) / len(analysis['quality_score_trend'])

    return analysis

def generate_pattern_report(analysis):
    """Generate human-readable pattern analysis report"""

    report = []
    report.append("=" * 80)
    report.append("FEEDBACK PATTERN ANALYSIS")
    report.append("=" * 80)
    report.append("")

    report.append(f"📊 Total Memos Reviewed: {analysis['total_memos_reviewed']}")
    report.append(f"📈 Average Quality Score: {analysis.get('avg_quality_score', 0):.1f}/10")
    report.append("")

    # Problematic sections
    report.append("-" * 80)
    report.append("🔴 PROBLEMATIC SECTIONS (Most Common Issues)")
    report.append("-" * 80)
    report.append("")

    if analysis['problematic_sections']:
        for i, section in enumerate(analysis['problematic_sections'][:5], 1):
            section_name = section['section'].replace('_', ' ').title()
            problem_pct = section['problem_rate'] * 100
            report.append(f"{i}. {section_name}")
            report.append(f"   Problem Rate: {problem_pct:.1f}% "
                         f"({section['needs_work']} needs work, {section['wrong']} wrong "
                         f"out of {section['total']} reviews)")
            report.append("")
    else:
        report.append("✅ No consistently problematic sections identified")
        report.append("")

    # Section ratings breakdown
    report.append("-" * 80)
    report.append("SECTION RATINGS BREAKDOWN")
    report.append("-" * 80)
    report.append("")

    for section_id, ratings in sorted(analysis['section_ratings'].items()):
        if ratings['total'] > 0:
            section_name = section_id.replace('_', ' ').title()
            good_pct = (ratings['good'] / ratings['total']) * 100
            needs_pct = (ratings['needs_work'] / ratings['total']) * 100
            wrong_pct = (ratings['wrong'] / ratings['total']) * 100

            report.append(f"{section_name}:")
            report.append(f"  ✅ Good: {good_pct:.0f}%  |  ⚠️ Needs Work: {needs_pct:.0f}%  |  ❌ Wrong: {wrong_pct:.0f}%")
            report.append("")

    report.append("=" * 80)

    return "\n".join(report)

def generate_improved_prompt(analysis, original_prompt):
    """Use Claude to generate an improved prompt based on feedback patterns"""

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Prepare feedback summary for Claude
    problematic_sections_summary = "\n".join([
        f"- {s['section'].replace('_', ' ').title()}: "
        f"{s['problem_rate']*100:.0f}% problematic ({s['needs_work']} needs work, {s['wrong']} wrong)"
        for s in analysis['problematic_sections'][:5]
    ])

    # Sample corrections
    corrections_by_section = defaultdict(list)
    for corr in analysis['all_corrections']:
        if corr['rating'] in ['needs_work', 'wrong']:
            corrections_by_section[corr['section']].append(corr['correction'])

    corrections_summary = ""
    for section, corrections in list(corrections_by_section.items())[:5]:
        section_name = section.replace('_', ' ').title()
        corrections_summary += f"\n{section_name}:\n"
        for correction in corrections[:3]:  # Max 3 corrections per section
            corrections_summary += f"  - {correction}\n"

    improvement_prompt = f"""You are a prompt engineering expert helping improve an AI system that generates VC investment memos.

CURRENT SITUATION:
We've analyzed feedback from {analysis['total_memos_reviewed']} generated memos with an average quality score of {analysis.get('avg_quality_score', 0):.1f}/10.

ORIGINAL PROMPT:
{original_prompt}

FEEDBACK ANALYSIS:

Most Problematic Sections:
{problematic_sections_summary}

Common User Corrections:
{corrections_summary}

TASK:
Generate an improved version of the prompt that addresses these specific issues:

1. For each problematic section, add specific instructions that would prevent the identified issues
2. Add concrete examples of what good output looks like for weak sections
3. Include explicit requirements for data sourcing and quantitative backing
4. Add instructions to avoid generic language and require specific insights
5. Ensure the prompt guides toward producing actionable investment memos, not just research reports

Requirements for the improved prompt:
- Maintain the same overall structure and sections
- Add 2-3 specific improvement instructions per problematic section
- Include quality checkpoints (e.g., "Ensure you include at least 3 sourced data points")
- Add examples of good vs. bad output for the worst sections
- Make instructions more actionable and measurable

Return your response in this exact format:

IMPROVED PROMPT:
[The complete improved prompt here]

KEY IMPROVEMENTS MADE:
1. [First improvement and why]
2. [Second improvement and why]
3. [Third improvement and why]
[etc.]

EXPECTED IMPACT:
[Brief explanation of how these changes should improve memo quality]"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=6000,
        messages=[
            {"role": "user", "content": improvement_prompt}
        ]
    )

    return message.content[0].text

def save_improvement_report(analysis, improved_prompt_response, original_prompt):
    """Save improvement analysis and new prompt"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save pattern analysis
    pattern_report = generate_pattern_report(analysis)
    pattern_filepath = f"pattern_analysis_{timestamp}.txt"
    with open(pattern_filepath, 'w') as f:
        f.write(pattern_report)

    # Parse improved prompt response
    improved_section = improved_prompt_response.split("IMPROVED PROMPT:")[1].split("KEY IMPROVEMENTS MADE:")[0].strip()
    improvements = improved_prompt_response.split("KEY IMPROVEMENTS MADE:")[1].split("EXPECTED IMPACT:")[0].strip()
    expected_impact = improved_prompt_response.split("EXPECTED IMPACT:")[1].strip()

    # Save comparison report
    comparison_filepath = f"prompt_improvement_{timestamp}.md"
    with open(comparison_filepath, 'w') as f:
        f.write("# Deal Memo Prompt Improvement Report\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n\n")
        f.write("---\n\n")

        f.write("## Analysis Summary\n\n")
        f.write(f"- **Memos Analyzed**: {analysis['total_memos_reviewed']}\n")
        f.write(f"- **Average Quality Score**: {analysis.get('avg_quality_score', 0):.1f}/10\n")
        f.write(f"- **Problematic Sections**: {len(analysis['problematic_sections'])}\n\n")

        f.write("## Most Problematic Sections\n\n")
        for section in analysis['problematic_sections'][:5]:
            section_name = section['section'].replace('_', ' ').title()
            f.write(f"- **{section_name}**: {section['problem_rate']*100:.0f}% problematic\n")
        f.write("\n")

        f.write("## Original Prompt\n\n")
        f.write("```\n")
        f.write(original_prompt)
        f.write("\n```\n\n")

        f.write("## Improved Prompt\n\n")
        f.write("```\n")
        f.write(improved_section)
        f.write("\n```\n\n")

        f.write("## Key Improvements Made\n\n")
        f.write(improvements)
        f.write("\n\n")

        f.write("## Expected Impact\n\n")
        f.write(expected_impact)
        f.write("\n")

    # Save improved prompt separately for easy use
    prompt_filepath = f"improved_prompt_{timestamp}.txt"
    with open(prompt_filepath, 'w') as f:
        f.write(improved_section)

    # Save full data as JSON
    json_filepath = f"improvement_data_{timestamp}.json"
    with open(json_filepath, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'analysis': {
                'total_memos': analysis['total_memos_reviewed'],
                'avg_quality_score': analysis.get('avg_quality_score', 0),
                'problematic_sections': analysis['problematic_sections'],
                'section_ratings': dict(analysis['section_ratings'])
            },
            'original_prompt': original_prompt,
            'improved_prompt': improved_section,
            'improvements_list': improvements,
            'expected_impact': expected_impact
        }, f, indent=2)

    return {
        'pattern_report': pattern_filepath,
        'comparison_report': comparison_filepath,
        'improved_prompt': prompt_filepath,
        'json_data': json_filepath
    }

def main():
    """Main function to run improvement engine"""

    print("=" * 80)
    print("IMPROVEMENT ENGINE")
    print("Analyze feedback patterns and generate improved prompts")
    print("=" * 80)
    print()

    # Load feedback files
    print("📂 Loading feedback files...")
    feedback_data = load_feedback_files()

    if not feedback_data:
        print("\n❌ No feedback files found!")
        print("Please run the feedback interface and export feedback first.")
        return

    print(f"✅ Loaded {len(feedback_data)} feedback file(s)")
    print()

    # Analyze patterns
    print("🔍 Analyzing feedback patterns...")
    analysis = analyze_feedback_patterns(feedback_data)

    # Show pattern report
    pattern_report = generate_pattern_report(analysis)
    print(pattern_report)
    print()

    # Get original prompt from deal_memo_generator.py
    print("📄 Reading original prompt from deal_memo_generator.py...")
    with open('deal_memo_generator.py', 'r') as f:
        content = f.read()
        # Extract prompt from generate_deal_memo function
        prompt_start = content.find('prompt = f"""')
        prompt_end = content.find('"""', prompt_start + 13)
        original_prompt = content[prompt_start + 13:prompt_end].strip()

    print("✅ Original prompt extracted")
    print()

    # Generate improved prompt
    print("🤖 Generating improved prompt with AI...")
    print("   This may take 60-90 seconds...")
    print()

    improved_prompt_response = generate_improved_prompt(analysis, original_prompt)

    # Save reports
    print("💾 Saving improvement reports...")
    saved_files = save_improvement_report(analysis, improved_prompt_response, original_prompt)

    print()
    print("✅ Improvement analysis complete!")
    print()
    print("📊 Generated files:")
    print(f"   - Pattern Analysis: {saved_files['pattern_report']}")
    print(f"   - Comparison Report: {saved_files['comparison_report']}")
    print(f"   - Improved Prompt: {saved_files['improved_prompt']}")
    print(f"   - JSON Data: {saved_files['json_data']}")
    print()
    print("=" * 80)
    print()

    # Show key improvements
    print("🎯 KEY IMPROVEMENTS PREVIEW:")
    print()
    if "KEY IMPROVEMENTS MADE:" in improved_prompt_response:
        improvements = improved_prompt_response.split("KEY IMPROVEMENTS MADE:")[1].split("EXPECTED IMPACT:")[0].strip()
        print(improvements)
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
