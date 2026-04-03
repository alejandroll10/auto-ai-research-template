"""Test openassetpricing package for Chen-Zimmerman data."""
import openassetpricing as oap

# List available signals
print("=== Available methods ===")
print([m for m in dir(oap) if not m.startswith('_')])

# Try downloading a small sample
print("\n=== Test: Download portfolio returns ===")
try:
    # Try to get long-short returns for a few signals
    df = oap.dl_ret(sample="main", freq="m", nport=10, weighting="vw")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns[:10])}")
    print(df.head(3))
except Exception as e:
    print(f"dl_ret error: {e}")

print("\n=== Test: Download characteristics ===")
try:
    df = oap.dl_char(sample="main")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns[:10])}")
except Exception as e:
    print(f"dl_char error: {e}")

print("\n=== Done ===")
