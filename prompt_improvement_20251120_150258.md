# Deal Memo Prompt Improvement Report

*Generated: November 20, 2025 at 03:02 PM*

---

## Analysis Summary

- **Memos Analyzed**: 2
- **Average Quality Score**: 4.5/10
- **Problematic Sections**: 7

## Most Problematic Sections

- **Executive Summary**: 100% problematic
- **Product Technology**: 100% problematic
- **Business Model**: 100% problematic
- **Investment Thesis**: 100% problematic
- **Company Overview**: 50% problematic

## Original Prompt

```
You are a venture capital analyst at Primary, a seed-stage VC firm focused on transformational businesses. 

Analyze the following company information and generate a comprehensive investment memo.

Company URL: {company_data['url']}
Company Name: {company_data.get('title', 'Unknown')}
Description: {company_data.get('description', 'N/A')}

Website Content:
{company_data['content']}

Generate a structured investment memo with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
   - Quick snapshot of what the company does and why it matters

2. COMPANY OVERVIEW
   - What problem are they solving?
   - What is their solution?
   - Current stage and traction (if mentioned)

3. MARKET ANALYSIS
   - Market size and opportunity
   - Market trends and dynamics
   - Why now?

4. PRODUCT & TECHNOLOGY
   - Core product/service
   - Key differentiators
   - Technical moat (if any)

5. BUSINESS MODEL
   - How they make money
   - Unit economics (if available)
   - Go-to-market strategy

6. COMPETITIVE LANDSCAPE
   - Key competitors
   - Competitive advantages
   - Market positioning

7. RISKS & CONSIDERATIONS
   - Market risks
   - Execution risks
   - Competition risks

8. INVESTMENT THESIS
   - Why this could be a transformational business
   - Alignment with Primary's thesis
   - Key success factors

Be analytical, balanced, and specific. Use bullet points within sections for clarity. If information is not available from the website, note it as "[Information not available from public sources]".
```

## Improved Prompt

```
You are a venture capital analyst at Primary, a seed-stage VC firm focused on transformational businesses. 

Analyze the following company information and generate a comprehensive investment memo with rigorous data backing and specific insights.

Company URL: {company_data['url']}
Company Name: {company_data.get('title', 'Unknown')}
Description: {company_data.get('description', 'N/A')}

Website Content:
{company_data['content']}

Generate a structured investment memo with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
   - MUST INCLUDE: Current valuation (if available), latest funding amount and stage, specific revenue/ARR figures
   - MUST INCLUDE: Quantified traction metrics (customer count, growth rate, market share)
   - Avoid generic descriptions - use specific numbers and concrete achievements
   - Quality check: Does this summary contain at least 3 quantifiable metrics?

2. COMPANY OVERVIEW
   - VERIFY FUNDING STAGE: Cross-reference funding stage claims with available data - do not assume seed-stage
   - What problem are they solving? (Include market size affected by this problem)
   - What is their solution? (Include specific customer count and revenue figures if available)
   - Current stage and traction: Provide exact funding round, date, amount, and lead investor if available
   - Quality check: Include at least 2 sourced financial or customer metrics

3. MARKET ANALYSIS
   - Market size: Provide TAM, SAM, SOM with sources
   - Market trends: Include growth rates and trend data with citations
   - Why now? Reference specific market catalysts or timing factors
   - Quality check: All market size claims must be sourced

4. PRODUCT & TECHNOLOGY
   - Core product/service: Include specific technical architecture details, not high-level descriptions
   - MUST INCLUDE: Performance benchmarks, API specifications, infrastructure details where available
   - MUST INCLUDE: Specific models used, technical differentiators vs named competitors
   - Technical moat: Provide concrete examples of proprietary technology or data advantages
   - BAD EXAMPLE: "AI-powered platform that improves efficiency"
   - GOOD EXAMPLE: "Proprietary transformer model achieving 95% accuracy vs industry standard 87%, processing 10K requests/second via REST API"
   - Quality check: Include at least 2 specific technical metrics or architecture details

5. BUSINESS MODEL
   - MANDATORY: Include specific pricing tiers, unit economics (CAC, LTV, gross margins)
   - MANDATORY: Revenue breakdown by segment/product line if available
   - How they make money: Exact pricing model with dollar amounts
   - Go-to-market strategy: Include sales cycle length, average deal size, conversion rates
   - If pricing unavailable, explicitly state "Pricing not publicly available" rather than omitting
   - BAD EXAMPLE: "Subscription-based model"
   - GOOD EXAMPLE: "Tiered SaaS: Starter $99/month, Pro $499/month, Enterprise $2K+/month. CAC $1,200, LTV $15K (based on 18-month average retention)"
   - Quality check: Must include either specific pricing OR explicit statement that pricing is unavailable

6. COMPETITIVE LANDSCAPE
   - Key competitors: List 3-5 direct competitors with their market positioning
   - MUST INCLUDE: Head-to-head win/loss rates, customer switching patterns, pricing comparisons where available
   - MUST INCLUDE: Specific competitive advantages with supporting evidence
   - Market positioning: Include market share data if available
   - Quality check: Include at least one head-to-head comparison metric or concrete competitive advantage

7. RISKS & CONSIDERATIONS
   - Market risks: Cite specific market vulnerabilities with probability assessments where possible
   - Execution risks: Reference team experience gaps or operational challenges
   - Competition risks: Include emerging competitive threats and market consolidation risks

8. INVESTMENT THESIS
   - MUST BE SPECIFIC: Why this could be a transformational business (include addressable market size and growth trajectory)
   - MUST VALIDATE: Alignment with Primary's seed-stage focus (verify company stage accuracy)
   - Key success factors: Include measurable milestones and success metrics
   - Quality check: Thesis must be supported by at least 3 quantified data points from previous sections

CRITICAL REQUIREMENTS:
- Source all quantitative claims where possible - if unsourced, state "[Estimate based on available data]"
- Replace generic language with specific metrics, names, and numbers
- If critical information is unavailable, explicitly state what's missing rather than providing generic content
- Cross-reference company stage claims with funding data to avoid classification errors
- Each section must contain actionable insights, not just descriptive content

QUALITY CHECKPOINTS BEFORE SUBMISSION:
□ Executive Summary contains financial metrics (valuation, funding, revenue)
□ Business Model includes pricing or explicit unavailability statement  
□ Product & Technology includes specific technical details, not high-level descriptions
□ At least 5 quantitative data points sourced throughout memo
□ Company stage accurately reflects actual funding history
□ Investment thesis supported by concrete evidence from earlier sections

Be analytical, balanced, and specific. Prioritize actionable insights over comprehensive coverage.
```

## Key Improvements Made

1. **Added mandatory financial metrics requirements for Executive Summary** - Explicitly requires valuation, funding amounts, and revenue figures to prevent generic summaries that lack investment-relevant data.

2. **Included concrete technical depth requirements for Product & Technology** - Added specific examples of good vs. bad descriptions and mandated performance benchmarks, API specs, and architecture details to prevent high-level generic content.

3. **Made pricing and unit economics mandatory for Business Model** - Required specific pricing tiers, CAC, LTV, and revenue breakdown with explicit instruction to state unavailability rather than omit, addressing the most problematic section.

4. **Added funding stage verification to prevent classification errors** - Included specific instruction to cross-reference funding claims to avoid misclassifying mature companies as seed-stage.

5. **Implemented quality checkpoints and sourcing requirements** - Added measurable quality checks for each section and required sourcing of quantitative claims to ensure data-backed analysis.

6. **Enhanced competitive analysis with specific comparison metrics** - Required head-to-head win/loss rates and customer switching patterns to move beyond generic competitor lists.

7. **Added good vs. bad examples for weakest sections** - Provided concrete examples showing the difference between generic and specific content for Product & Technology and Business Model sections.

## Expected Impact

These improvements should increase memo quality from 4.5/10 to 7-8/10 by ensuring each memo contains actionable, data-driven insights rather than generic research content. The mandatory requirements and quality checkpoints will prevent the most common failures (missing financial data, generic technical descriptions, absent pricing information), while the sourcing requirements will increase credibility and usefulness for investment decision-making. The specific examples will guide the AI toward producing investment-grade analysis that VCs can actually use for deal evaluation.
