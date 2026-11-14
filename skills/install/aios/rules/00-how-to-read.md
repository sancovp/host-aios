# HOW TO READ

TRIGGER:[any Read() call · any grep call]

NOT:
  wc -l file            (skipped)
  Read(offset=1)
  grep -n keyword file  ─┐
  Read(offset=1970)     ←┤ next offset picked FROM grep hit
  grep -n keyword2 file  │
  Read(offset=3049)     ←┘
  [gaps: 501-1969, 2011-3048 → NEVER READ]

DO:
  wc -l file → total=N
  Read(offset=1,          limit=L1)
  Read(offset=1+L1,       limit=L2)
  Read(offset=1+L1+L2,    limit=L3)
  ...
  Read(offset=O_k, limit=L_k)  while O_k + L_k < N
  [grep: NOT in this chain — used only AFTER, to re-jump to known lines]

RULE:[offset_next := offset_prev + limit_prev · always · no grep between Reads · stop when offset+limit >= N]
RULE:[grep LOCATES, never PROVES · a grep hit ⇒ run the full Read() chain on that file]
RULE:[know context e2e (full file, offset=1..N) before drawing a conclusion from it]
