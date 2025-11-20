"""
VC Deal Memo Generator
A tool to analyze startups and generate structured investment memos
Built for Primary VC - PrimaryOS Operations
"""

import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import anthropic

def fetch_website_content(url):
    """Fetch and parse website content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc else ""
        
        # Get title
        title = soup.title.string if soup.title else ""
        
        return {
            'url': url,
            'title': title,
            'description': description,
            'content': text[:8000]  # Limit content length
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'content': ''
        }

def generate_deal_memo(company_data):
    """Generate a structured VC deal memo using Claude"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are a venture capital analyst at Primary, a seed-stage VC firm focused on transformational businesses. 

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

Be analytical, balanced, and specific. Use bullet points within sections for clarity. If information is not available from the website, note it as "[Information not available from public sources]"."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def save_memo(company_url, memo_content):
    """Save the memo to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_name = company_url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0].replace('.com', '').replace('.', '_')
    
    filename = f"deal_memo_{company_name}_{timestamp}.md"
    # Save in current directory instead of /mnt/user-data/outputs/
    filepath = filename
    
    with open(filepath, 'w') as f:
        f.write(f"# Investment Memo: {company_url}\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n\n")
        f.write("---\n\n")
        f.write(memo_content)
    
    return filepath

def main():
    print("=" * 60)
    print("VC DEAL MEMO GENERATOR")
    print("Built for Primary VC - PrimaryOS Operations")
    print("=" * 60)
    print()
    
    # Get company URL
    company_url = input("Enter company website URL: ").strip()
    
    if not company_url.startswith('http'):
        company_url = 'https://' + company_url
    
    print(f"\n📊 Analyzing {company_url}...")
    print("Step 1/3: Fetching website content...")
    
    # Fetch company data
    company_data = fetch_website_content(company_url)
    
    if 'error' in company_data and company_data['content'] == '':
        print(f"❌ Error fetching website: {company_data['error']}")
        return
    
    print("Step 2/3: Generating investment memo with AI analysis...")
    
    # Generate memo
    memo = generate_deal_memo(company_data)
    
    print("Step 3/3: Saving memo...")
    
    # Save memo
    filepath = save_memo(company_url, memo)
    
    print(f"\n✅ Deal memo generated successfully!")
    print(f"📄 Saved to: {filepath}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()