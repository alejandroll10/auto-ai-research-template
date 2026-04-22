"""Test form-5500 skill — verifies live DOL fetch + Schedule H asset breakdown.

Downloads two small schedules for 2022 (R = 2.5MB, C = 0.8MB) plus Schedule H
(17MB) on first run, then exercises the helper API. Uses the cache on subsequent
runs so re-tests are fast.
"""
import sys

# === Test 1: download Schedule R (smallest) and verify columns ===
print("=== Test 1: download_schedule(2022, 'r') ===")
from utils.form_5500_utils import download_schedule
sr = download_schedule(2022, 'r')
assert len(sr) > 1000, f"Schedule R 2022 should have many rows, got {len(sr)}"
assert 'ACK_ID' in sr.columns, f"missing ACK_ID; cols: {list(sr.columns)[:10]}"
print(f"  rows: {len(sr):,}, cols: {len(sr.columns)}")
print(f"  sample cols: {list(sr.columns)[:8]}")

# === Test 2: download Schedule C ===
print("\n=== Test 2: download_schedule(2022, 'c') ===")
sc = download_schedule(2022, 'c')
assert len(sc) > 100, f"Schedule C 2022 too small: {len(sc)}"
assert 'ACK_ID' in sc.columns
print(f"  rows: {len(sc):,}, cols: {len(sc.columns)}")

# === Test 3: download Schedule H + asset-breakdown columns present ===
print("\n=== Test 3: download_schedule(2022, 'h') + asset columns ===")
sh = download_schedule(2022, 'h')
assert len(sh) > 10000, f"Schedule H 2022 too small: {len(sh)}"
need = {'INT_REG_INVST_CO_EOY_AMT', 'TOT_ASSETS_EOY_AMT', 'EMPLR_CONTRIB_EOY_AMT'}
assert need.issubset(sh.columns), f"missing critical cols: {need - set(sh.columns)}"
mf_total = sh['INT_REG_INVST_CO_EOY_AMT'].fillna(0).sum() / 1e9
tot = sh['TOT_ASSETS_EOY_AMT'].fillna(0).sum() / 1e9
print(f"  rows: {len(sh):,}, cols: {len(sh.columns)}")
print(f"  Aggregate EOY mutual-fund holdings (INT_REG_INVST_CO): ${mf_total:,.0f}B")
print(f"  Aggregate EOY total assets:                            ${tot:,.0f}B")
assert mf_total > 100, f"mutual-fund total absurdly small: ${mf_total}B"
assert tot > 1000, f"total assets absurdly small: ${tot}B"

# === Test 4: link main 5500 to Schedule H by ACK_ID ===
print("\n=== Test 4: link main F_5500 to Schedule H by ACK_ID ===")
from utils.form_5500_utils import download_5500, link_schedule
main = download_5500(2022)
assert len(main) > 50000, f"main 5500 too small: {len(main)}"
assert 'ACK_ID' in main.columns
joined = link_schedule(main, sh)
print(f"  main rows: {len(main):,}, schedule H rows: {len(sh):,}, joined: {len(joined):,}")
assert len(joined) > 10000, f"join produced too few rows: {len(joined)}"

# === Test 5: cache reuse — second download should be near-instant ===
print("\n=== Test 5: cache reuse ===")
import time
t0 = time.time()
_ = download_schedule(2022, 'r')
elapsed = time.time() - t0
print(f"  Schedule R reload: {elapsed*1000:.0f} ms")
assert elapsed < 2.0, f"cache reload too slow: {elapsed}s"

print("\nALL TESTS PASSED")
