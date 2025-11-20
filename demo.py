"""
Demo script to showcase the Deal Memo Generator
Tests with a sample AI startup
"""

import sys
import os

# Add parent directory to path
sys.path.append('/home/claude')

from deal_memo_generator import fetch_website_content, generate_deal_memo, save_memo

def run_demo():
    print("=" * 60)
    print("DEAL MEMO GENERATOR - DEMO")
    print("Testing with a sample AI company")
    print("=" * 60)
    print()
    
    # Use a well-known AI startup
    test_url = "https://scale.com"
    
    print(f"📊 Analyzing: {test_url}")
    print("This is a real example of what Primary partners would see.")
    print()
    
    print("Step 1/3: Fetching website content...")
    company_data = fetch_website_content(test_url)
    
    if 'error' in company_data and company_data['content'] == '':
        print(f"❌ Error: {company_data['error']}")
        print("\n⚠️  Note: This demo requires internet access.")
        print("The tool works by fetching live company data.")
        return
    
    print(f"✓ Fetched {len(company_data['content'])} characters of content")
    print(f"✓ Company: {company_data.get('title', 'Unknown')}")
    print()
    
    print("Step 2/3: Generating investment memo...")
    print("(This uses Claude to analyze the company through a VC lens)")
    print()
    
    memo = generate_deal_memo(company_data)
    
    print("✓ Memo generated")
    print()
    
    print("Step 3/3: Saving memo...")
    filepath = save_memo(test_url, memo)
    
    print(f"✓ Saved to: {filepath}")
    print()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print("📄 The generated memo includes:")
    print("   • Executive Summary")
    print("   • Company Overview")
    print("   • Market Analysis")
    print("   • Product & Technology")
    print("   • Business Model")
    print("   • Competitive Landscape")
    print("   • Risks & Considerations")
    print("   • Investment Thesis")
    print()
    print("Check the output file to see the full analysis!")
    print()

if __name__ == "__main__":
    run_demo()
