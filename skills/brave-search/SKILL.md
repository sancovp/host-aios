---
name: brave-search
description: "Search the web using the Brave Search API, when a search must go through Brave rather than Claude Code's own web search. Needs a Brave Search API key in the environment variable BRAVE_API_KEY."
---

# Brave Search Skill

Use Brave Search to find current information on the web. Claude Code's own web search needs no key; use this skill
when the search must go through Brave.

## The key

The script reads the key from the environment variable `BRAVE_API_KEY` and holds none itself. Without it, the script
says so and exits 1 — never paste a key into this folder: a key belongs in the environment the session runs with, outside
every source and every release.

## Usage

```bash
bash <this skill's folder>/brave_search.sh "your query here"
```

## API
- Endpoint: `https://api.search.brave.com/res/v1/web/search`
- Method: GET
- Header: `X-Subscription-Token: <the key>`
- Param: `q=<query>`

## Response
The script prints one block per result — `TITLE`, `URL`, `DESC` — separated by `---`, or `No results found.`

## Examples

```bash
bash <this skill's folder>/brave_search.sh "Claude Code best practices"
bash <this skill's folder>/brave_search.sh "AI agents market trends" | grep '^URL:'
```
