"""
Quality Analyzer for Deal Memos
Analyzes generated memos and provides quality scores, completeness flags, and improvement recommendations
"""

import os
import json
import anthropic
from datetime import datetime
import sys

def analyze_memo_quality(memo_content, memo_filepath=None):
    """
    Analyze a deal memo for quality using Claude
    Returns structured quality assessment with scores and flags
    """

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    quality_prompt = f"""You are a senior venture capital analyst reviewing a deal memo for quality.

Analyze the following investment memo and provide a comprehensive quality assessment.

MEMO TO ANALYZE:
{memo_content}

Provide your analysis in the following JSON structure:

{{
  "overall_score": <1-10>,
  "overall_assessment": "<2-3 sentence summary>",
  "section_scores": {{
    "executive_summary": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": ["<specific issue 1>", "<specific issue 2>"],
      "strengths": ["<strength 1>", "<strength 2>"]
    }},
    "company_overview": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }},
    "market_analysis": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }},
    "product_technology": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }},
    "business_model": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }},
    "competitive_landscape": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }},
    "risks_considerations": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }},
    "investment_thesis": {{
      "score": <1-10>,
      "completeness": "<complete/partial/insufficient>",
      "issues": [],
      "strengths": []
    }}
  }},
  "data_verification": {{
    "quantitative_claims": <number of quantitative claims found>,
    "sourced_claims": <number with clear sources>,
    "unsourced_claims": ["<claim 1>", "<claim 2>"],
    "potential_hallucinations": ["<concern 1>", "<concern 2>"]
  }},
  "red_flags": [
    {{
      "severity": "<critical/high/medium/low>",
      "category": "<generic_language/unsupported_claim/insufficient_detail/logical_inconsistency>",
      "description": "<specific red flag>",
      "location": "<section name>"
    }}
  ],
  "improvement_priorities": [
    {{
      "priority": <1-5, where 1 is highest>,
      "section": "<section name>",
      "recommendation": "<specific actionable recommendation>"
    }}
  ]
}}

Scoring Guidelines:
- 9-10: Exceptional - Deep insights, specific data, compelling narrative
- 7-8: Strong - Good analysis, mostly complete, some specifics
- 5-6: Adequate - Covers basics, lacks depth or specificity
- 3-4: Weak - Superficial, generic, missing key information
- 1-2: Poor - Incomplete, unhelpful, potentially misleading

Focus on:
1. Specificity vs. generic statements
2. Data/evidence backing claims
3. Logical consistency
4. Completeness of analysis
5. Actionable insights for investment decision

Return ONLY the JSON object, no additional text."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": quality_prompt}
        ]
    )

    # Parse the JSON response
    response_text = message.content[0].text

    # Extract JSON from response (handle potential markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()

    quality_report = json.loads(response_text)

    # Add metadata
    quality_report["metadata"] = {
        "analyzed_at": datetime.now().isoformat(),
        "memo_file": memo_filepath,
        "analyzer_version": "1.0"
    }

    return quality_report

def generate_quality_report_text(quality_report):
    """Convert JSON quality report to readable text format"""

    report = []
    report.append("=" * 70)
    report.append("DEAL MEMO QUALITY REPORT")
    report.append("=" * 70)
    report.append("")

    # Overall assessment
    report.append(f"OVERALL SCORE: {quality_report['overall_score']}/10")
    report.append(f"{quality_report['overall_assessment']}")
    report.append("")

    # Section scores
    report.append("-" * 70)
    report.append("SECTION-BY-SECTION ANALYSIS")
    report.append("-" * 70)
    report.append("")

    for section_name, section_data in quality_report['section_scores'].items():
        section_title = section_name.replace('_', ' ').title()
        score = section_data['score']
        completeness = section_data['completeness'].upper()

        # Score indicator
        if score >= 8:
            indicator = "✓✓"
        elif score >= 6:
            indicator = "✓"
        elif score >= 4:
            indicator = "⚠"
        else:
            indicator = "✗"

        report.append(f"{indicator} {section_title}: {score}/10 ({completeness})")

        if section_data['strengths']:
            report.append("   Strengths:")
            for strength in section_data['strengths']:
                report.append(f"   + {strength}")

        if section_data['issues']:
            report.append("   Issues:")
            for issue in section_data['issues']:
                report.append(f"   - {issue}")

        report.append("")

    # Data verification
    report.append("-" * 70)
    report.append("DATA VERIFICATION")
    report.append("-" * 70)
    report.append("")

    dv = quality_report['data_verification']
    report.append(f"Quantitative claims found: {dv['quantitative_claims']}")
    report.append(f"Claims with sources: {dv['sourced_claims']}")
    report.append("")

    if dv['unsourced_claims']:
        report.append("Unsourced claims requiring verification:")
        for claim in dv['unsourced_claims']:
            report.append(f"  • {claim}")
        report.append("")

    if dv['potential_hallucinations']:
        report.append("Potential hallucinations or unverifiable statements:")
        for concern in dv['potential_hallucinations']:
            report.append(f"  ⚠ {concern}")
        report.append("")

    # Red flags
    if quality_report['red_flags']:
        report.append("-" * 70)
        report.append("RED FLAGS")
        report.append("-" * 70)
        report.append("")

        for flag in quality_report['red_flags']:
            severity_icon = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(flag['severity'], '⚪')

            report.append(f"{severity_icon} [{flag['severity'].upper()}] {flag['category'].replace('_', ' ').title()}")
            report.append(f"   Location: {flag['location']}")
            report.append(f"   {flag['description']}")
            report.append("")

    # Improvement priorities
    report.append("-" * 70)
    report.append("IMPROVEMENT PRIORITIES")
    report.append("-" * 70)
    report.append("")

    sorted_priorities = sorted(quality_report['improvement_priorities'], key=lambda x: x['priority'])
    for item in sorted_priorities:
        report.append(f"{item['priority']}. [{item['section']}]")
        report.append(f"   {item['recommendation']}")
        report.append("")

    report.append("=" * 70)

    return "\n".join(report)

def save_quality_report(quality_report, memo_filepath):
    """Save quality report as JSON and text files"""

    # Generate base filename from memo filepath
    if memo_filepath:
        base_name = memo_filepath.replace('.md', '')
    else:
        base_name = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Save JSON
    json_filepath = f"{base_name}_quality.json"
    with open(json_filepath, 'w') as f:
        json.dump(quality_report, f, indent=2)

    # Save text report
    txt_filepath = f"{base_name}_quality.txt"
    text_report = generate_quality_report_text(quality_report)
    with open(txt_filepath, 'w') as f:
        f.write(text_report)

    return json_filepath, txt_filepath

def main():
    """Main function to analyze a memo file"""

    print("=" * 70)
    print("DEAL MEMO QUALITY ANALYZER")
    print("=" * 70)
    print()

    if len(sys.argv) > 1:
        memo_filepath = sys.argv[1]
    else:
        memo_filepath = input("Enter path to deal memo file (.md): ").strip()

    if not os.path.exists(memo_filepath):
        print(f"❌ Error: File not found: {memo_filepath}")
        return

    print(f"📄 Reading memo: {memo_filepath}")

    with open(memo_filepath, 'r') as f:
        memo_content = f.read()

    print("🔍 Analyzing memo quality with AI...")
    print("   This may take 30-60 seconds...")
    print()

    quality_report = analyze_memo_quality(memo_content, memo_filepath)

    print("💾 Saving quality report...")
    json_file, txt_file = save_quality_report(quality_report, memo_filepath)

    print()
    print("✅ Quality analysis complete!")
    print(f"📊 JSON report: {json_file}")
    print(f"📋 Text report: {txt_file}")
    print()

    # Display summary
    print(generate_quality_report_text(quality_report))

if __name__ == "__main__":
    main()
