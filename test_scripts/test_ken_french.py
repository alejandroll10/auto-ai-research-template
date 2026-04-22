"""Test ken-french skill — factors download, portfolios, FF3 alpha helper."""
import sys

# === Test 1: FF3 factors via helper ===
print("=== Test 1: get_factors('ff3') ===")
from utils.ken_french_utils import get_factors
ff3 = get_factors('ff3', start='2000-01-01', end='2023-12-31')
assert {'Mkt-RF', 'SMB', 'HML', 'RF'}.issubset(ff3.columns), f"missing cols: {list(ff3.columns)}"
assert len(ff3) > 200, f"FF3 should have >200 monthly obs 2000-2023, got {len(ff3)}"
assert abs(ff3['Mkt-RF'].mean()) < 0.05, f"Mkt-RF mean looks wrong (decimal?): {ff3['Mkt-RF'].mean()}"
print(f"  FF3: {len(ff3)} months, Mkt-RF mean={ff3['Mkt-RF'].mean():.4f} (decimal)")

# === Test 2: FF5 ===
print("\n=== Test 2: get_factors('ff5') ===")
ff5 = get_factors('ff5', start='2000-01-01', end='2023-12-31')
assert {'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF'}.issubset(ff5.columns)
print(f"  FF5: {len(ff5)} months, columns={list(ff5.columns)}")

# === Test 3: 25 size/BM portfolios ===
print("\n=== Test 3: get_portfolios('25_Portfolios_5x5') ===")
from utils.ken_french_utils import get_portfolios
p25 = get_portfolios('25_Portfolios_5x5', start='2000-01-01', end='2023-12-31')
assert p25.shape[1] == 25, f"expected 25 portfolios, got {p25.shape[1]}"
print(f"  25 portfolios: shape={p25.shape}")

# === Test 4: FF3 alpha helper on a synthetic series ===
print("\n=== Test 4: ff3_alpha on Mkt-RF itself (alpha should be ~0, beta ~1) ===")
from utils.ken_french_utils import ff3_alpha
import pandas as pd
mkt_excess = ff3['Mkt-RF'] + ff3['RF']  # back to total market return
result = ff3_alpha(mkt_excess, start='2000-01-01')
assert abs(result['mkt_beta'] - 1.0) < 0.05, f"mkt_beta should be ~1, got {result['mkt_beta']}"
assert abs(result['alpha']) < 0.001, f"alpha should be ~0 for Mkt itself, got {result['alpha']}"
print(f"  alpha={result['alpha']:.5f} (t={result['alpha_t']:.2f}), mkt_beta={result['mkt_beta']:.3f}, R²={result['r_squared']:.3f}")

print("\nALL TESTS PASSED")
