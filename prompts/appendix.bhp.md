====================================================================
KNOWN WORKBOOK CONTEXT — BHP/Westrac Consumption File (COMPONENTS + PARTS sheets)
(verify against THIS run's real data; column order/content can change between exports,
so treat this as a strong prior, not a substitute for actually checking
`columns`/`samples` below)
====================================================================
Verified against test-data/New-BHP-Workfile/260911 Westrac Consumption File.xlsx +
bhp-cross-reference.csv + BHP logic diagram.xlsx + BHP Workfile Sep26.xlsx (BHP's own
working file, whose NEO tab formulas were reverse-engineered to confirm this join —
see core/cross_reference.py's bhp_neo docstring). A second real file of this same shape,
`[01. MAIN - FORECAST] - 251113 Westrac consumption forecast -.xlsx`, was also checked
and matches.

There is **no clean, pre-mapped "Billiton" sheet in this shape** — that was an earlier,
never-verified guess (see prompts/README.md's history). The real source is always two
raw transactional sheets, `COMPONENTS` and `PARTS`, with near-identical columns
(`COMPONENTS` has one extra: `WORK_ORDER_RELEASED`). `config/customers/bhp.json` merges
both into ONE NEO source (`merge_candidates: true` on the LTP-role sheet_config entry) —
this mirrors BHP's own master workfile (`BHP Workfile Sep26.xlsx`), whose NEO tab pulls
the earliest matching `REQUIREMENT_DATE` from EITHER sheet via `XLOOKUP` against both.
**There is no LAO/measurement-points source for this shape at all**: `PARTS` (granular
consumables — filters, hoses, enclosures) is merged into the same NEO source rather than
built into its own LAO target, because `bhp-cross-reference.csv` is a component-level
catalog (engines, transmissions, drives) that `PARTS` material numbers essentially never
match — treating `PARTS` as its own LAO would produce a file that's almost entirely
quarantined to `LAO_Exceptions.csv` (both `ComponentCode`/`ModifierCode` blank) rather
than a useful output.

COMPONENTS/PARTS columns verified: REQUIREMENT_DATE, MONTH_YEAR_LONG, ASSET_SHORT,
PLANT, MATERIAL_NUMBER, MATERIAL_DESCRIPTION, QUANTITY, WORK_ORDER,
[WORK_ORDER_RELEASED — COMPONENTS only], DEMAND_TYPE, LEAD_TIME, SORT_FIELD,
VENDOR_PART_NUMBER_TOP_VENDOR_LAST_3_YEARS, LAST_SMU_READING, COMPONENT_PIECE,
LOCATION_POSITION, FUNCTIONAL_LOCATION_DESCRIPTION, SERIAL_NUMBER.

Fields verified against COMPONENTS/PARTS:
  - AssetName: SORT_FIELD — the bare asset/equipment unit ID (e.g. "DT5167", "GR7111"),
    NOT ASSET_SHORT (that column just holds a site/region code like "WAIO"). This is
    also the asset key `core/cross_reference.py`'s bhp_neo joins on.
  - NewStrategyDate: REQUIREMENT_DATE — explicit customer mapping logic for this shape
    (per the project brief: "RequirementDate values from Customer Input file will serve
    as NewStrategyDate value in the NEO files"). Real Excel datetimes.
  - StrategyTaskDescription: MATERIAL_DESCRIPTION — e.g.
    "ENGINE,SX,C175,HASTDEER 3659319X". Also the text half of the ComponentCode/
    ModifierCode cross-reference join key (see below).
  - PrimaryPartNumberCode: VENDOR_PART_NUMBER_TOP_VENDOR_LAST_3_YEARS (e.g.
    "3659319X") — NOT MATERIAL_NUMBER, which is a numeric SAP-style ID (e.g. 11034966)
    that doesn't match AMT's alphanumeric part-number convention at all.
  - LifeToDateValue: LAST_SMU_READING (a service-meter-hours reading) — best-effort but
    reasonable; no more literal "life to date" column exists.
  - SerialNumber: SERIAL_NUMBER — a real column but genuinely sparse (COMPONENTS: ~1.5%
    of rows; PARTS: ~40%). Map directly when present; a genuine gap otherwise, same as
    every other shape in this project — no cross-reference fallback exists for it here.
  - ModelCode: genuinely absent — neither sheet has a Model/machine-type column
    (ASSET_SHORT/PLANT are site codes, not models). A real, permanent gap for this
    shape — return `source_column: null` rather than guessing.
  - FrequencyValue: genuinely absent — no interval/frequency column anywhere in this
    shape's source data. A real gap.
  - FunctionalLoc: FUNCTIONAL_LOCATION_DESCRIPTION — present, but it's a
    component-plus-asset text string (e.g. "Engine DT5167", "Control System DT5472"),
    not a segmented floc code like FMG's. Used only for row-quarantine/banner checks
    here, not a cross-sheet join key (COMPONENTS and PARTS are independent tables, not
    a role pair that shares a real floc-overlap bonus).
  - ComponentCode / ModifierCode: **no real column on either sheet at all** — always
    return `source_column: null` for these; do not force a match. They're recovered
    entirely by `core/cross_reference.py`'s bhp_neo, which replicates the "Cross Ref
    Key: Serial Prefix & Component Unique Code & Location position" join documented in
    BHP's own "BHP logic diagram.xlsx": AssetName + StrategyTaskDescription +
    LOCATION_POSITION, with Serial Prefix looked up per-asset from
    bhp_cross-reference.csv itself (self-referential — no live AMT feed needed, since
    every asset in the supplied file maps to exactly one Serial Prefix). Coverage is
    real but partial and deliberately asymmetric: bhp_cross-reference.csv is a
    component-level catalog (engines, transmissions, drives, axles), so COMPONENTS
    rows recover ComponentCode/ModifierCode at a meaningful rate (~25-30%) while PARTS
    rows (granular consumables) almost never match — this is why PARTS is merged into
    the same NEO source instead of driving its own target (see above), not a mapping
    bug to fix here.
