"""Test chen-zimmerman skill — Open Source Asset Pricing data via openassetpricing pkg.

Replaces an older discovery-only script. Verifies the helper API actually works.
"""
import sys

# === Test 1: helper imports and OpenAP instantiates ===
print("=== Test 1: instantiate OpenAP via helper ===")
from utils.chen_zimmerman_utils import _get_ap, list_portfolio_types
ap = _get_ap()
print(f"  OpenAP instance: {type(ap).__name__}")
ports = list_portfolio_types()
print(f"  available portfolio types: {ports}")

# === Test 2: download a single signal (BM = book-to-market) ===
print("\n=== Test 2: get_signals(['BM']) ===")
from utils.chen_zimmerman_utils import get_signals
bm = get_signals(['BM'])
assert 'permno' in bm.columns and 'yyyymm' in bm.columns and 'BM' in bm.columns, f"unexpected cols: {list(bm.columns)}"
assert len(bm) > 100_000, f"BM panel too small: {len(bm)} rows"
print(f"  BM signal: {len(bm):,} rows, {bm['permno'].nunique()} permnos, "
      f"{bm['yyyymm'].min()}-{bm['yyyymm'].max()}")

# === Test 3: portfolios for BM ===
print("\n=== Test 3: get_portfolios(['BM'], port_type='op') ===")
from utils.chen_zimmerman_utils import get_portfolios
bm_p = get_portfolios(['BM'], port_type='op')
assert 'ret' in bm_p.columns, f"missing ret col: {list(bm_p.columns)}"
assert len(bm_p) > 100, f"BM portfolio panel too small: {len(bm_p)}"
print(f"  BM portfolio rows: {len(bm_p):,}; cols: {list(bm_p.columns)}")
print(f"  mean monthly ret across all ports: {bm_p['ret'].mean():.4f}")

# === Test 4: signal documentation ===
print("\n=== Test 4: signal_doc() ===")
from utils.chen_zimmerman_utils import signal_doc
doc = signal_doc()
assert len(doc) > 100, f"signal_doc too small: {len(doc)}"
print(f"  signal docs: {len(doc)} rows; sample cols: {list(doc.columns)[:6]}")

print("\nALL TESTS PASSED")
