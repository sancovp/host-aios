# Context engineering — session gates

TRIGGER:[session start · a new user term appearing (⇒ record it, never let it float) · a layout change (⇒ update the pointer rules) · session end · about to bypass a validation or testing gate]
START:[scan for `.claude/rules/` (+ `.agent/rules/`) · load user-level (always active) + project-level rules + the project DESIGN.md + bijection doc + state-machine constraints]
DURING:[hold validation/testing gates · add a new user term to the project ontology/skill (never let it float) · update the pointer rules on a layout change]
END:[crystallize proven insights to rules (used 2-3×, general, clear trigger+success) · update DESIGN.md + the vocabulary · treat every action → candidate rule → candidate verification script → hard constraint]
NOT:[bypass validation/testing gates · let a new term float unrecorded]
