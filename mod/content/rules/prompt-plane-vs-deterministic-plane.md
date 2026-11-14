# Prompt-plane vs deterministic-plane — check the interpreter before flagging "no caller"

PRINCIPLE:[the LLM is a runtime, so an artifact can be "called" with no Python calling it]
TRIGGER:[about to write "dead / no caller / unwired / orphaned / unused"]
PLANES:[
- Plane 1 (deterministic) = a .py fn/route/daemon/component · interpreter = CPU · "no caller yet" IS a real finding
- Plane 2 (prompt-content) = a SKILL.md/persona/system-prompt/rule/CLAUDE.md · interpreter = the LLM reading it · reading IS the call · "dead" = category error
- Plane 3 (skill-exposed library) = .py whose intended driver is an agent reading a skill that points at it · the skill IS the caller-surface · honest status = "not yet skill-exposed"
]
DO:[name the plane first · disambiguate 1 vs 3 by grepping for a SKILL.md/skilltree entry · say "built, not yet auto-driven" for a built-tested-not-yet-auto-driven artifact · expect live agent-driven surface the code never references (correct architecture)]
NOT:[call a built-tested-not-yet-auto-driven artifact a "lie" · call a Plane-2/3 artifact "dead" · "fix" correct architecture by hard-wiring a Python caller]
NOTE:[only heaven + cave-teams are fully-explicit deterministic runtimes]
