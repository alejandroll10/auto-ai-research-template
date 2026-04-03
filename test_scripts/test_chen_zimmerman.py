"""Test Chen-Zimmerman Open Source Asset Pricing data access."""
import subprocess
import sys

# Check if openassetpricing package exists
try:
    import openassetpricing
    print("openassetpricing package available")
except ImportError:
    print("openassetpricing not available, using direct download")

# Try pandas-datareader approach
try:
    import pandas_datareader.data as web
    # Chen-Zimmerman isn't in pandas-datareader, but let's confirm
    print("pandas-datareader available but Chen-Zimmerman not in it")
except:
    pass

# Try direct download from GitHub
import requests
import io

print("\n=== Checking GitHub README for current download links ===")
readme_url = "https://raw.githubusercontent.com/OpenSourceAP/CrossSection/master/README.md"
r = requests.get(readme_url, timeout=15)
if r.status_code == 200:
    # Find download links
    lines = r.text.split('\n')
    for line in lines:
        if 'drive.google' in line.lower() or 'download' in line.lower() or 'csv' in line.lower() or 'parquet' in line.lower():
            print(f"  {line.strip()}")
    print(f"\nREADME fetched successfully ({len(r.text)} chars)")
else:
    print(f"Failed to fetch README: {r.status_code}")

print("\n=== Test complete ===")
