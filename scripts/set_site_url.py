#!/usr/bin/env python3
"""Set the public origin used in metadata, the sitemap, and social previews."""
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 scripts/set_site_url.py https://your-domain.example')
value = sys.argv[1].strip().rstrip('/')
parsed = urlsplit(value)
if parsed.scheme != 'https' or not parsed.netloc or parsed.path or parsed.query or parsed.fragment or parsed.username:
    raise SystemExit('Use an HTTPS origin with no path, query, or fragment, such as https://example.com')
path = Path(__file__).resolve().parents[1] / 'src/content.json'
data = json.loads(path.read_text())
data['site_url'] = value
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Website origin set to ' + value)
print('Build locally or commit and push to let GitHub Actions rebuild the site.')
