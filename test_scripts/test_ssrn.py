"""Test SSRN abstract access patterns."""
import subprocess

# Test a known SSRN paper
urls = [
    "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4000000",
    "https://ssrn.com/abstract=4000000",
    "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3500000",
]

for url in urls:
    print(f"\n=== {url} ===")
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-o", "/dev/null", "-w", "%{http_code} %{url_effective}", url],
            capture_output=True, text=True, timeout=15
        )
        print(f"Status: {result.stdout}")
    except Exception as e:
        print(f"Error: {e}")
