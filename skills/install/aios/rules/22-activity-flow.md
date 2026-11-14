# Activity flow diagrams (Mermaid sequence)

<docsys kind="dev-flow" role="law"/>

TRIGGER:[new workflow/sprint · state machine · answering "how does X work?" · any process lifecycle / runtime execution boundary set up]
DO:[give the Activity a Mermaid `sequenceDiagram` (or `stateDiagram-v2`/`flowchart LR` for state machines) the moment it is set up · mark scale boundaries with `Note over` · correspond every element to real function calls / endpoints / state transitions]
NOT:[draw speculative controls]
