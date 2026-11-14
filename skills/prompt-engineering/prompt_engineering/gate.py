"""
gate.py — the REAL grammar gate, on the `rulecatcher` package (an installed dependency, D3).

This is the rule-learner's intent done right: you DON'T hand-write the error rules. You give the template's
EXEMPLAR chains; rulecatcher LEARNS the grammar (transition rules: next_kind = shape, next_token =
vocabulary); then `gate()` lints a candidate and returns:
  - violations  (found vs expected, per slot)
  - fixes       (candidate tokens / suggested action)
  - a verdict   ORTHOGONAL (in the language, wrong slot → STEERABLE) vs SYNTAX_BREAK (foreign → FATAL)

That verdict is the steerable-vs-fatal gate genus (CSGN's CHECK), which the hand-rolled validate_chain
can't produce. Rendering never imports this; the gate is an optional layer. Falls back to the shallow
validate_chain only if `rulecatcher` is somehow unavailable.
"""

_RC_OK = True
try:
    from rulecatcher.db import connect, list_rules
    from rulecatcher.engine import catch_patterns, adopt_rules
    from rulecatcher.models import ArtifactInput
except Exception:  # pragma: no cover
    _RC_OK = False

try:
    from .cognition import validate_chain
except ImportError:
    from cognition import validate_chain


def _learn(conn, exemplars, scope, rule_types):
    content = "\n".join(exemplars) + "\n"
    catch_patterns(conn, [ArtifactInput(label="exemplars", content=content)],
                   scope=scope, min_support=1, min_confidence=1.0)
    pending = list_rules(conn, "pending", scope=scope)
    ids = [int(r["id"]) for r in pending if r["rule_type"] in rule_types]
    if ids:
        adopt_rules(conn, ids, actor="prompt-engineering", reason="ratified grammar from exemplars")
    return len(ids)


def gate(text, exemplars, *, scope="chain", rule_types=("next_kind", "next_token"), vocab=None):
    """Learn the grammar from `exemplars`, then lint `text` against it.

    Returns {ok, engine, verdict, rules, violations:[{found, expected, verdict, candidates, action}]}.
    engine='rulecatcher' (learned grammar + verdict + fixes) | 'fallback' (shallow validate_chain).
    """
    if not _RC_OK:
        ok, errs = validate_chain(text, vocab=vocab)
        return {"ok": ok, "engine": "fallback", "verdict": "clean" if ok else "syntax_break",
                "rules": 0,
                "violations": [{"found": "", "expected": "", "verdict": "syntax_break",
                                "candidates": [], "action": e} for e in errs]}

    from rulecatcher.linting import lint_text
    with connect(":memory:") as conn:
        n_rules = _learn(conn, exemplars, scope, rule_types)
        violations = lint_text(conn, text, scope=scope, record_stats=False)

    vio = [{"found": v.found_token, "expected": v.expected_token, "verdict": v.verdict,
            "candidates": list(v.candidate_tokens), "action": v.suggested_action} for v in violations]
    if not violations:
        verdict = "clean"
    elif any(v.verdict == "syntax_break" for v in violations):
        verdict = "syntax_break"        # foreign token → FATAL
    else:
        verdict = "orthogonal"          # in the language, wrong slot → STEERABLE
    return {"ok": not violations, "engine": "rulecatcher", "verdict": verdict,
            "rules": n_rules, "violations": vio}


__all__ = ["gate"]
