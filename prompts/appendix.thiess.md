====================================================================
KNOWN WORKBOOK CONTEXT — New Westrac Thiess (WA) Supplier Plan_*_WORKFILE.xlsx
(verify against THIS run's real data; column order/content can change between exports,
so treat this as a strong prior, not a substitute for actually checking
`columns`/`samples` below)
====================================================================
This ONE workbook covers both the Thiess and MACA WA fleets (plus a handful of related
entities — Fortescue Metals Group, IB Operations, New Caterpillar Machines — that share
the same Westrac dealer relationship), distinguished purely by the resolved `CustomerCode`
value on each row, not by separate sheets or separate config profiles — see
prompts/README.md and config/customers/thiess.json's description.

The workbook has many tabs (Pivot Analysis, Supply Plan, 12M Forecast, Component
History, Fleet Listing, Equipment Admin, SMU, SMU Errors, Cross Ref, Cross Ref New,
AMT). Only two are this pipeline's actual source sheets:

- **Supply Plan** (LTP role → NEO): Thiess, CONCAT3, CONCAT (AMT), Model, State, Site,
  Unit Number, Unit Description, Service Type, Service Type Description, JDE Forecast
  Date, Frequency, Last Completed Date, Last Completed SMU, Approved Start Date,
  Requested Delivery Date, PO Promised Delivery Date, Start Date Change From Last
  Month, WO Number, Ship To Destination, PO Number, PO + Part No., Line #, Qty #, Part
  Number, PN # Description, LTP - Commens, Comments, Status, Estimated Ship Date, Will
  this make Thiess Required by Date?, Time, Component Match, Asset Match.
- **Component History** (MEASUREMENT_POINTS role → LAO): CONCAT, Unit Number, Equipment
  Description, Service Type, Service Type Description, % Due, Frequency SMU, Last
  Completed Hours, Last Completed Date, Hours Run, JDE Forecast Date, Meter to Run SMU,
  Location, Location Description, ST, Actual Location, AMT Description, CONCAT3,
  Component Match, Asset Match.

Gotchas verified against the real workbook:
  - The **'Thiess' column header on Supply Plan/12M Forecast is misleading** — it holds
    a Model+Description concat string (e.g. "Cat D10TTurbo Primary LEFT"), NOT a
    customer/entity selector. Do not map it to CustomerCode.
  - Neither Supply Plan nor Component History has a Component Code, Modifier Code,
    Branch, Site (compound), Fleet, Customer, or full Serial Number column — these are
    genuine gaps for this shape (Component Code/Modifier Code are recovered by
    core/cross_reference.py's `thiess_neo`/`thiess_lao` from
    thiess_cross-reference.csv; the rest have no available source and stay blank,
    labelled `requires_enrichment`, same treatment this project already gives FMG's
    BranchCode/SiteCode/FleetCode/CustomerCode).
  - Supply Plan's own **'Frequency'** column is a real numeric hour interval; don't
    confuse it with 12M Forecast's differently-shaped columns of a similar name — this
    sheet doesn't have that particular decoy, but does carry 'Service Type' (short code,
    e.g. "N4100") alongside 'Service Type Description' (free text, e.g. "Rear Axle") —
    map StrategyTaskDescription to the **Description** column, and reserve the bare
    **Service Type** code exclusively for the cross-reference join key (see
    core/cross_reference.py's `thiess_neo`).
  - Component History's **'Equipment Description'** carries a `"Cat "` prefix (e.g.
    "Cat MD6250") that Supply Plan's own 'Model' column doesn't (e.g. "MD6310") — both
    need to match the cross-reference table's bare model code, so LAO's ModelCode uses
    the `strip_cat_prefix` transform (config/customers/thiess.json) and the LAO
    enricher does the same internally before the join.
  - Component History's **first data row is a literal repeat of its own header names**
    (a stray Excel artifact, not real data) — it currently isn't caught by any reject
    rule (its 'Unit Number' cell literally contains the text "Unit Number", which is
    neither blank nor 1-2-character gibberish) and will surface as a single garbage row
    in LAO/LAO_Exceptions. Known, low-impact (one row), not fixed automatically to avoid
    a workbook-specific special case in general-purpose code.
  - **RegistrationCounter** is NOT a fixed per-customer constant here the way it is for
    the FMG `default` profile (217040 for every row) — it varies per fleet even within
    one CustomerCode (e.g. THIESS PTY LTD - FLEETCO alone spans 50050/50076/50072
    across different rows in the reference upload). No table in the supplied workbook
    assigns this ID, so it's left as a genuine, honestly-labelled enrichment gap.
  - The historical, manually-produced "Thiess & Maca NEO/LAO Upload" reference CSVs
    include several extra curation steps this pipeline doesn't attempt to replicate
    exactly (see the Westrac "CUSTOMER WORKFILE" workflow diagrams: blank/1900-date
    cleanup, human exception review, month-to-month carry-forward) — expect this
    pipeline's own automated exclusion/exception/dedup rules (§9-§13 of the main
    README) to produce different row counts than that historical file, same caveat this
    project already documents for its other customers.
