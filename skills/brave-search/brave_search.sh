#!/bin/bash
# Brave Search via its REST API. The key comes from the environment (BRAVE_API_KEY), never from this file.

ENDPOINT="https://api.search.brave.com/res/v1/web/search"

if [[ -z "${BRAVE_API_KEY:-}" ]]; then
  echo "brave-search: BRAVE_API_KEY is not set — export it in the environment the session runs with" >&2
  exit 1
fi

query="$*"
if [[ -z "$query" ]]; then
  echo "Usage: brave_search.sh \"your query here\""
  exit 1
fi

curl -s -G "$ENDPOINT" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" \
  --data-urlencode "q=$query" \
  -H "Accept: application/json" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
results = data.get('web', {}).get('results', [])
if not results:
    print('No results found.')
    sys.exit(0)
for r in results:
    print(f\"TITLE: {r.get('title','')}\")
    print(f\"URL: {r.get('url','')}\")
    print(f\"DESC: {r.get('description','')}\")
    print('---')
"
