# A BIG DESIGN.md KEEPS A TABLE OF CONTENTS — as a rule, in its project's own rules dir

<docsys kind="index" role="law"/>

TRIGGER:[a project's `DESIGN.md` passes ~500 lines · about to write, draft or decide anything a big
`DESIGN.md` governs · about to conclude "we never decided that" · any edit to a `DESIGN.md` that
has a TOC rule]
PRINCIPLE:[saved is not findable · a ruling nothing points at is lost the same way an unwritten one
is, and more quietly, because the file exists · only `.claude/rules/` auto-injects, so the index
lives there]
DO:[keep `<project>/.claude/rules/design_toc.md`: a hand-written WHERE THE CURRENT ANSWER IS table
for the questions that recur, plus every `##`/`###` heading with its line number, generated ·
create it with `python3 <the design-toc skill's folder>/design_toc.py <project> --init` · regenerate
with the same command (no flag) in the same commit as any `DESIGN.md` edit · run `--check` before
trusting a line number and before a version leaves, and read its output — it checks the `DESIGN.md`'s READ ORDER
([[26-canonical-design]]) as well as the TOC · add a table row when a question gets asked twice]
NOT:[hand-edit the generated block · answer "did we decide X?" from memory of the conversation ·
treat a TOC as a substitute for rolling the DESIGN.md up (it makes a pile findable; it does not make
it one argument)]
COMPOSES:[[[every-level-describes-and-breadcrumbs-below]] — the pointer belongs where the reader
lands · [[29-state-indexes-design]] — details hang off by pointer · [[26-canonical-design]] — the
one DESIGN.md it indexes]

→ The script: the `design-toc` skill's `design_toc.py`.
