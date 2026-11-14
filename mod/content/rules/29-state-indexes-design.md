# State/index tables — every row carries a pointer

<docsys kind="pointers" role="law"/>

TRIGGER:[writing or editing any status/progress/ledger/index table · a row whose pointer is missing (⇒ an unwritten design, a gap to close) · about to inline detail into a table instead of pointing at it]
DO:[give every row of a status/progress/ledger table a path to where that thing's canonical detail (design, spec, the why) lives · keep the table as the one spine with details hanging off by pointer · treat a row whose pointer is missing (`—`) as an unwritten design (a gap to close)]
NOT:[duplicate detail into the table · scatter detail across many docs · leave a row's pointer missing and call the thing finished]
