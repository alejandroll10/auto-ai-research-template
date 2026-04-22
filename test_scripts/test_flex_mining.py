"""Test flex-mining skill — verifies the small public artifacts are reachable.

We do NOT download the 500MB Google Drive folder in CI; that would be slow and
the gdown folder API is fragile. We do verify:
  (a) the small public CSV on GitHub (signal theory classification) is reachable
  (b) gdown is importable (so the heavy download path would work)
"""
import sys

# === Test 1: signal-theory CSV from GitHub ===
print("=== Test 1: SignalsTheoryChecked.csv from GitHub ===")
import pandas as pd
url = 'https://raw.githubusercontent.com/chenandrewy/flex-mining/main/DataInput/SignalsTheoryChecked.csv'
df = pd.read_csv(url)
assert len(df) > 50, f"too few rows: {len(df)}"
print(f"  rows: {len(df)}, cols: {list(df.columns)[:8]}")
print(df.head(3).to_string())

# === Test 2: gdown importable (heavy-download dependency) ===
print("\n=== Test 2: gdown importable ===")
try:
    import gdown  # noqa: F401
    print(f"  gdown version: {gdown.__version__ if hasattr(gdown, '__version__') else 'present'}")
except ImportError as e:
    print(f"  FAIL: gdown not installed ({e}); 'pip install gdown' needed")
    sys.exit(1)

# === Test 3: GitHub repo is alive (sanity) ===
print("\n=== Test 3: flex-mining repo reachable ===")
import urllib.request
with urllib.request.urlopen('https://api.github.com/repos/chenandrewy/flex-mining', timeout=10) as r:
    assert r.status == 200
    print(f"  repo OK (HTTP {r.status})")

print("\nALL TESTS PASSED")
