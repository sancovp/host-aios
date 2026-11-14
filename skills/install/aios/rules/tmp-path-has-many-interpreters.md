# /tmp paths are container-scoped until proven otherwise

TRIGGER:[any `/tmp` path in ecosystem docs · about to declare a path absent/empty/wiped]
DO:[treat a `/tmp` path as container-`/tmp` until proven host · name the interpreter of the path before declaring absence · check inside the relevant container before concluding empty/wiped]
