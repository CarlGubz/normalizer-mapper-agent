====================================================================
KNOWN WORKBOOK CONTEXT — Macmahon WA Based - Westrac Monthly Caterpillar Equipment.xlsx
(verify against THIS run's real data; column order/content can change between exports,
so treat this as a strong prior, not a substitute for actually checking
`columns`/`samples` below)
====================================================================
Single sheet, **"Export"** — feeds BOTH NEO and LAO from the exact same rows (this
shape has no separate LTP-vs-Measurement-Points split; "Next Occurrence"/NEO and "Last
Occurrence"/LAO are two different date perspectives on the same maintenance-plan row,
matching the "Update Cross Reference → Upload LAO → Upload NEO" steps of Macmahon's own
AMT workflow, not two different source datasets).

Export columns verified: Project, Plant, Op Asset ID, Functional Location, Op
Manufacturer, Op Model, Op Serial Number, Op Asset Status, Ownership, Maintenance
Activity Type, Plan Status, Maintenance Item, Change Rule, Component Code, Position
Code, Maintenance Item Description, Frequency, Maintenance Plan, Task List Key, Current
Meter Reading (Hours), Average Daily Usage, Total Budget, Maintenance Plan Text, Work
Order, Last Done Date, Last Usage Done, Life Remaining Hours, % Life Remaining, Days
Remaining, Predicted Change Date, Next Planned WO Execution Date, Next WO Predicted
Days Variance, Next WO Predicted Life at Exec Date, Next WO Predicted Usage % at Exec
Date.

Fields verified:
  - AssetName: Op Asset ID. ModelCode: Op Model. SerialNumber: Op Serial Number.
  - FunctionalLoc: Functional Location — real hyphenated FLOC strings (e.g.
    "TKHL109-HYSY-CYHY"), shaped as `<equipment>-<component-suffix...>` (only ONE
    leading segment before the component detail — unlike FMG's four-segment
    `<plant>-MP-<area>-<equipment>-<suffix>` prefix; see
    core/cross_reference.py's `_floc_suffix_after_first`).
  - ComponentCode: **Component Code** is a real column here (numeric, Excel-float
    formatted — e.g. `1044.0` — cleaned via the `to_int_str` transform), but it's
    blank on ~5% of rows; macmahon_cross-reference.csv fills the rest.
  - **ModifierCode has no source column on this sheet at all** — entirely supplied by
    macmahon_cross-reference.csv, keyed on (Functional Location suffix, Position Code)
    against the table's own (Functional Location Code, Position Code) columns (see
    core/cross_reference.py's `macmahon_neo`/`macmahon_lao`). Verified: only 24 of 122
    distinct (suffix, position) combinations in the lookup table are genuinely
    ambiguous and are correctly left blank rather than guessed.
  - Position Code takes ~30 distinct values beyond the obvious LH/RH/LHF/RHR (POS.1,
    POS.3-4, P1..P4, CTR, etc.) — all handled generically by the same composite join,
    no special-casing needed.
  - StrategyTaskDescription: Maintenance Item Description. FrequencyValue: Frequency.
    LifeToDateValue: Current Meter Reading (Hours).
  - NewStrategyDate (NEO): Next Planned WO Execution Date. LastStrategyDate (LAO): Last
    Done Date. LastStrategyUsageValue (LAO): Last Usage Done. StrategyDate: Predicted
    Change Date.
  - **No column is documented as "Strategy Usage" specifically** — StrategyUsageValue
    uses **Total Budget** as a best-effort numeric proxy (config/customers/macmahon.json);
    treat this as a simplification pending clarification from Macmahon/Westrac, not a
    verified 1:1 mapping.
  - TaskTypeCode has no clear source column (`Change Rule`'s values — CC/CH/CW — do NOT
    match the reference upload's actual TaskTypeCode values RB/AC) — left as an honest
    enrichment gap rather than a wrong-looking guess.
  - **Branch/Site/Fleet/Customer/RegistrationCounter**: `Ownership` (MEC/MEO/MEF/MEH/MEL),
    `Project` (M350/M215/...), and `Plant` (M11D/M11L/...) are internal Macmahon codes,
    not the legal-entity/branch names this pipeline's output columns need (e.g.
    "MACMAHON CONTRACTORS PTY LTD", "WA - Macmahon") — no supplied file maps one to the
    other, so these stay blank/enrichment, same treatment as Thiess/FMG.
  - The sheet's tail carries a **stray filter-description row** baked into the `Project`
    column ("Applied filters:\nMaintenance Activity Type is Z01\n...") — a genuine
    Excel-export artifact, correctly caught by the normalizer's `banner_row`/
    `missing_identity` reject rules (its Op Asset ID is blank).
  - As with Thiess, the historical "Macmahon NEO/LAO upload" reference CSVs reflect
    additional manual curation (blank/1900-date cleanup, exception review) this
    pipeline's automated rules don't attempt to replicate row-for-row.
