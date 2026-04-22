"""Test edgar skill — helper functions + raw SEC API + full-text search.

Validates the four paths actually used in research:
  1. edgartools-based Company lookup (10-K filings index)
  2. XBRL facts via helper
  3. Direct SEC companyfacts API (no edgartools dependency)
  4. EDGAR full-text search (EFTS)
"""
import sys

# === Test 1: helper get_company → 10-K filings ===
print("=== Test 1: get_company('AAPL') → 10-K filings index ===")
from utils.edgar_utils import get_company
co = get_company('AAPL')
filings = co.get_filings(form='10-K')
assert len(filings) > 10, f"too few 10-Ks for AAPL: {len(filings)}"
print(f"  AAPL 10-K filings: {len(filings)}, latest filed {filings[0].filing_date}")

# === Test 2: XBRL facts via helper ===
print("\n=== Test 2: get_xbrl_facts('AAPL', 'Revenues') ===")
from utils.edgar_utils import get_xbrl_facts
rev = get_xbrl_facts('AAPL', 'Revenues')
assert len(rev) > 5, f"too few revenue rows: {len(rev)}"
print(f"  Revenues: {len(rev)} rows ({rev['end'].min().date()}..{rev['end'].max().date()}), "
      f"sample units: {rev['unit'].unique()[:3]}")

# === Test 3: direct companyfacts API ===
print("\n=== Test 3: get_company_facts_raw(320193) ===")
from utils.edgar_utils import get_company_facts_raw
facts = get_company_facts_raw(320193)
assert facts['entityName'] == 'Apple Inc.', f"unexpected entity: {facts.get('entityName')}"
n_concepts = len(facts.get('facts', {}).get('us-gaap', {}))
print(f"  Apple us-gaap concepts: {n_concepts}")
assert n_concepts > 100, f"expected >100 concepts, got {n_concepts}"

# === Test 4: full-text search via helper ===
print("\n=== Test 4: search_filings_text('artificial intelligence', '10-K', 2024) ===")
from utils.edgar_utils import search_filings_text
res = search_filings_text('artificial intelligence', form='10-K',
                          start_date='2024-01-01', end_date='2024-12-31')
assert res['total'] > 100, f"expected >100 hits, got {res['total']}"
print(f"  hits: {res['total']:,}, sample first hit cik: {res['filings'][0]['_source'].get('ciks', ['?'])[0]}")

print("\nALL TESTS PASSED")
