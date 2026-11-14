# THE SUBAGENT MODEL — an agent sent to test, try out, play with, review or look runs on the bound model; a judge is sent only where the session cannot judge

TARGET:[THE SUBAGENT MODEL — what this installation binds for such agents ([[user_info]] THE BINDINGS): the model they run
on, the model a dispatch falls back to when that one refuses, the model a judge falls back to, and any model never
dispatched · an installation that has bound none: this rule does not fire, and the report names the model each agent
inherited]

TRIGGER:[about to dispatch an agent — the Agent tool, a workflow's agent() — to test, try out, play with, probe, review,
grade, judge or look at something · a lead about to start an agent for one of its child projects · a dispatch refused by its model (a safeguard flag, an API error) · about to send a
judge]

DO:[name the bound model in the dispatch (`model: <the binding>`) · when the bound model refuses, dispatch the binding's
fallback — the judge's fallback when the dispatch is a judge — and name in the report the refusal, its request id and the
model that ran instead · send a JUDGE only for what the session cannot easily judge itself: a measure of total integration
or completeness, and tests and code — whether the tests actually test the intended capability, not the thing that was
written · make every other judgment in the session itself · keep every arm of one comparison on the same model · say in
the report which model each agent ran on · as a lead (the `how-to-lead-an-aios` skill), name in each dispatch the model
for that level of orchestration]

NOT:[let such a dispatch inherit the session's model by omission · change the model partway through a comparison · send
a judge for what the session can easily judge itself · dispatch a model the binding names as never dispatched]
