"""Test EDGAR access — both edgartools and direct SEC API."""
import os

# === Test 1: edgartools ===
print("=== Test 1: edgartools ===")
try:
    from edgar import *
    set_identity("test research@university.edu")

    # Company lookup
    company = Company("AAPL")
    print(f"Company: {company.name} (CIK: {company.cik})")

    # Get recent 10-K
    filings = company.get_filings(form="10-K")
    print(f"10-K filings found: {len(filings)}")
    latest = filings[0]
    print(f"Latest 10-K: {latest.filing_date}")

    # Get financials
    financials = company.get_financials()
    bs = financials.balance_sheet
    print(f"Balance sheet periods: {len(bs.periods) if bs else 'N/A'}")

    # XBRL facts
    facts = company.get_facts()
    revenues = facts.to_pandas("us-gaap:Revenues")
    print(f"Revenue data points: {len(revenues)}")
    print(revenues.tail(3).to_string())

    print("\nedgartools: WORKING")
except Exception as e:
    print(f"edgartools error: {e}")

# === Test 2: Direct SEC EDGAR API ===
print("\n=== Test 2: Direct SEC EDGAR API (data.sec.gov) ===")
import requests

headers = {"User-Agent": "test research@university.edu"}

# Company search
url = "https://efts.sec.gov/LATEST/search-index?q=%22machine%20learning%22&dateRange=custom&startdt=2024-01-01&enddt=2024-12-31&forms=10-K"
# Company facts
url2 = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"
r = requests.get(url2, headers=headers, timeout=15)
if r.status_code == 200:
    data = r.json()
    print(f"XBRL facts for: {data.get('entityName', 'unknown')}")
    facts_keys = list(data.get('facts', {}).get('us-gaap', {}).keys())[:5]
    print(f"Sample facts: {facts_keys}")
    print("Direct API: WORKING")
else:
    print(f"Direct API failed: {r.status_code}")

# Filing search (EFTS)
print("\n=== Test 3: EDGAR Full-Text Search ===")
url3 = "https://efts.sec.gov/LATEST/search-index?q=%22artificial+intelligence%22&forms=10-K&dateRange=custom&startdt=2024-01-01&enddt=2024-12-31"
r3 = requests.get(url3, headers=headers, timeout=15)
print(f"Full-text search status: {r3.status_code}")
if r3.status_code == 200:
    results = r3.json()
    print(f"Hits: {results.get('hits', {}).get('total', {}).get('value', 'unknown')}")
else:
    # Try the other search endpoint
    url3b = "https://efts.sec.gov/LATEST/search-index?q=%22artificial+intelligence%22&forms=10-K"
    r3b = requests.get(url3b, headers=headers, timeout=15)
    print(f"Alt search: {r3b.status_code}")

print("\n=== All tests complete ===")
