"""Test FRED skill — verifies API key, helper functions, and bulk-moment recipe.

Run from a deployed project root (PYTHONPATH=code).
Requires FRED_API_KEY in .env.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

if not os.getenv('FRED_API_KEY'):
    print("FAIL: FRED_API_KEY not set in .env")
    sys.exit(1)

# === Test 1: helper get_series for a single series ===
print("=== Test 1: get_series(GDP) via fred_utils ===")
from utils.fred_utils import get_series
gdp = get_series('GDP', start='2000-01-01', end='2023-12-31')
assert len(gdp) > 50, f"GDP should have >50 quarterly obs, got {len(gdp)}"
print(f"  GDP: {len(gdp)} obs, last value = {gdp.iloc[-1]:.1f} ({gdp.index[-1].date()})")

# === Test 2: macro_moments bulk recipe ===
print("\n=== Test 2: macro_moments() ===")
from utils.fred_utils import macro_moments
m = macro_moments(start='2000-01-01', end='2023-12-31')
errors = {k: v for k, v in m.items() if 'error' in v}
ok = {k: v for k, v in m.items() if 'error' not in v}
print(f"  {len(ok)}/{len(m)} series fetched")
for k, v in ok.items():
    print(f"    {k:20s} mean={v['mean']:.3f} std={v['std']:.3f} n={v['n_obs']}")
if errors:
    print(f"  Errors: {errors}")
    sys.exit(1)

# === Test 3: no-key CSV fallback (documented in skill body) ===
print("\n=== Test 3: keyless CSV fallback for VIX ===")
import urllib.request
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS"
with urllib.request.urlopen(url, timeout=15) as r:
    data = r.read().decode()
lines = data.splitlines()
assert len(lines) > 100, f"VIX CSV too short: {len(lines)} lines"
print(f"  VIX CSV: {len(lines)} rows, header = {lines[0]!r}")

print("\nALL TESTS PASSED")
