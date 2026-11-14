# Scaffold → harness (a gate adds DETECTION, never authority)

<docsys kind="gate" role="law"/>

TRIGGER:[a rule landing with no gate · about to treat an ungated rule as optional or deferrable · a violation caught by hand that a script could catch · a script used 2-3× (⇒ promote it to a skill)]
PRINCIPLE:[every rule binds, gated or not · a gate CATCHES a violation, it does not create the obligation · an ungated rule is UNVERIFIED, never optional · rule says WHAT to enforce, skill says HOW]
DO:[build a verification script for every critical rule that programmatically detects violation = the hard constraint · follow the pattern Detect → Stop → Diagnose → Fix → Resume · rollback on a mid-critical-op violation (not press-on) · promote a repeatedly-used script to a skill]
NOT:[imply an ungated rule may be skipped, deferred, or weighed against convenience · write a rule as a PERMISSION that overlaps another rule's prohibition]
