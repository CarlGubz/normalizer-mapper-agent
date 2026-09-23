====================================================================
KNOWN CONTEXT — MACA (scaffold profile, no source workbook supplied yet)
====================================================================
`test-data/06. MACA/` contains **Maca CrossRef.xlsx** (the AMT component-code lookup,
now bundled as `prompts/cross-references/maca_cross-reference.csv`), the two
already-finalized **Maca NEO/LAO Upload May26.csv** reference files, and a workflow
diagram (`Maca Workflow.png`) — but no raw "Prepare Workfile" customer forecast
source file, which the workflow diagram itself describes as arriving separately each
month from MACA's CSM via email.

Checked and ruled out: the MACA-tagged rows inside the Thiess workbook's own `AMT` tab
(`New Westrac Thiess (WA) Supplier Plan_*_WORKFILE.xlsx`, `Customer` == "MACA MINING PTY
LTD", 2,466 rows) share **zero** assets with the standalone Maca NEO/LAO Upload
reference files (55 distinct assets there, 22 in the Thiess-embedded MACA rows, no
overlap) and cover different sites (Sanjiv Ridge/Miralga Creek/Muchea vs.
Gruyere/DSO/Parked/Karlawinda/...) — these are two genuinely different data feeds, not
the same fleet exported twice. MACA is NOT derivable from the Thiess workbook.

**Maca CrossRef.xlsx structure** (`CONCAT(XREF)`, `MODEL`, `AMT COMPONENT CODE`,
`MACA/Downer`, `CONCAT AMT`): `AMT COMPONENT CODE` is a compound AMT string in the same
family as BHP's ("5207 - CIRCLE DRIVE-00 - (NONE)"), and `MACA/Downer` is a compound
`<component>.<position>.<class>.<counter> <description>` string (e.g.
"14001.FL.CNC.0 Brake") — structurally different from both Thiess's and Macmahon's
lookup tables, so neither `thiess_neo`/`thiess_lao` nor `macmahon_neo`/`macmahon_lao`
apply; MACA needs its own enricher once its real customer_file's column layout is
known. **No enricher has been wired into `core/cross_reference.py`'s `ENRICHERS` dict
yet** — writing one now, without a real workbook to validate the join key against,
would be unverifiable guesswork (unlike Thiess/Macmahon, where a real source sheet was
available to check ambiguity rates against). `config/customers/maca.json`'s
`sheet_config`/field aliases are likewise a best-effort scaffold copied from the
project's generic default profile, not verified against real MACA data.

**Before this profile is run for real:** obtain MACA's actual monthly forecast
workbook (the "Prepare Workfile" input in `Maca Workflow.png`, step 2), re-check its
sheet names/columns against `config/customers/maca.json`'s placeholders, write/verify a
`maca_neo`/`maca_lao` cross-reference enricher the same way `thiess_neo` and
`macmahon_neo` were (ambiguity-checked against the real lookup table), and validate the
resulting NEO/LAO against `Maca NEO/LAO Upload May26.csv`.
