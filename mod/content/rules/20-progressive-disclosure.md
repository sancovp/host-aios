# Progressive disclosure (3-tier context)

<docsys kind="scaffold" role="law"/>

TRIGGER:[about to write code or docs inside any subdir · entering a dir whose local rules have not been read this window · a deep subdir gaining a constraint a parent action could break]
TIERS:[
1. User-level (the AIOS's rules, which `~/.claude` reaches — the release in use where [[user_info]] binds THE AIOS RELEASES, changed only by a new release; else `~/.claude/rules/`) = cross-project mechanics — always loaded
2. Project-level (`<project>/.claude/rules/`) = project canon — point to it from the project CLAUDE.md/README so it loads on entry
3. Module-sandbox (`<project>/<module>/.claude/rules/`) = module-specific — loaded when operating in that subdir
]
DO:[read a subdir's local rules before writing code there · put a one-line POINTER warning in the parent when a deep subdir has a constraint a parent action could break]
NOT:[put the full deep-subdir rule in the parent]
