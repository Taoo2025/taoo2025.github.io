# CareLink — Maternal Referral Intelligence
**Nigeria FCT · UNFPA Population Intelligence Hackathon prototype**  
Submission documentation updated: 13 November 2026.

[Open hospital and referral workspace](https://taoo2025.github.io/carelink/?view=hospitals) · [Open DIOS signals workspace](https://taoo2025.github.io/carelink/?view=signals)

CareLink helps users inspect registered health facilities, identify higher-level referral candidates, compare road access and review public maternal-health signals. It combines real source records with transparent modelling assumptions and human review. It is a referral-planning and evidence-review prototype: it does not confirm clinical suitability, hospital acceptance or a completed patient transfer.

The interface defaults to **EN** for new visitors, offers **CN / EN**, and remembers the user's choice. Facility names, news content, evidence and user-entered notes retain their source language.

## What the prototype does

### 1. Facility-to-facility referral planning
1. Select a registered origin facility from the map or list.
2. Inspect its source classification and coordinate-based LGA/Ward check. Conflicting locations retain their original coordinates until a documented human correction is supplied.
3. Find higher-level candidates: **Primary → Secondary/Tertiary; Secondary → Tertiary**. Tertiary has no higher level in this dataset. Registered level is not verification of obstetric services.
4. Connect endpoints to the Geofabrik/OpenStreetMap directed road network and rank candidates by shortest road distance. Show the three shortest candidates. Estimated minutes use stated road-class speeds capped by readable speed limits, not live traffic.
5. Select a candidate and save a plan with author, rationale, endpoint and route snapshots, optional DIOS evidence and review history. Plan states are pending team review, reviewed plan and voided. A reviewed plan does not mean a hospital has accepted a referral.

One-way directions, supported unconditional single via-node turn restrictions and explicit motor-vehicle barriers are considered. Endpoint access gaps are shown separately and excluded from road distance and minutes. Real entrances, connector access, some turn restrictions and gate access remain unverified.

### 2. DIOS evidence and human review
Inspect articles and their source links; distinguish **event location, mentioned facility and publication location**. Classify program/research context separately from local case reports, retain the finest supported geographic precision, and check duplicate-event groups.

Review states are pending human review, retain as context, excluded, more evidence needed and case candidate. Only records satisfying the source, local-case evidence, verified LGA and explicit human-confirmation requirements enter the deduplicated LGA event summary. A mention of Abuja or a hospital does not generate a patient point or referral origin. AI-assisted screening remains subject to human review.

### 3. Population and historical context
WorldPop provides population grids, unique-cell straight-line 5/10 km proximity measures and nearest-facility population allocations. PDP supplies historical maternal-health indicators with their reference periods. These are background measures; they do not currently change referral rankings, establish clinical urgency or represent actual patient volumes.

### 4. Editable evidence and team handoff
Users can correct facility locations/classifications with reviewer, source and reason, review DIOS evidence, and exchange team JSON files. Original records and change histories are retained. Changed facility coordinates or levels invalidate old routing/coverage results; maintainers must recalculate matching datasets and update the configured resources.

**Records are browser-local.** GitHub Pages has no shared write-back database or real-time team synchronization. Export team edits before changing computer/browser or clearing storage. A Git clone does not include records held in someone's browser.

## Geographic scope and published data

**Integrated analysis covers FCT and its six LGAs.** Other Nigerian states support facility browsing, not equivalent nationwide routing or population coverage.

| Published resource | Current scope / count | Use |
| --- | --- | --- |
| HDX health facilities | 46,146 Nigerian source records; 576 registered in FCT | Names, coordinates, registered levels, state/LGA and source metadata |
| Geofabrik/OSM derived routes | 566 FCT origins with 1,698 displayed top-three routes | Directed road distance and assumed-speed travel estimates |
| GRID3/CIESIN boundary resources via GeoPortal | FCT LGA/Ward checks | Coordinate membership and administrative filtering |
| WorldPop 2025 | 7,067 valid FCT grid cells | Modelled population and proximity context |
| Organizer-provided PDP export | Selected FCT historical indicators | Maternal-health background |
| Organizer-channel DIOS export | 1,330 rows → 550 articles; 262 tagged Nigeria | Source-linked signals and manual evidence review |

The current AI source-review queue covers all **262 Nigeria-tagged articles**: **183 readable bodies, 3 page mismatches/insufficient bodies and 76 inaccessible sources**. Recommendations: 151 context, 18 exclusions from the FCT case layer, 81 evidence gaps and 12 out-of-area case/referral clues. These dimensions overlap and should not be added. The earlier 50-article queue and 41-article screening batch are historical subsets. There are 21 duplicate-report/event candidate groups; inaccessible candidates may be linked only by title. Full-body independent fact-checking and clinical verification are not claimed. All records remain pending human confirmation; no patient coordinates or confirmed FCT events were generated. See [the complete article review and unresolved evidence](docs/DIOS_全量原文核查.md). Six facility location anomalies retain comparison records without automatic coordinate correction.

## Data sources and provenance

- [HDX — Nigeria health facilities](https://data.humdata.org/dataset/nigeria-health-facilities)
- [Geofabrik — Nigeria OpenStreetMap extract](https://download.geofabrik.de/africa/nigeria.html)
- [WorldPop Data Hub](https://hub.worldpop.org/) — Global2 R2025A v1, constrained UN-adjusted 2025 population, approximately 1 km.
- [Organizer-provided PDP export](https://drive.google.com/file/d/1h7jYKhDB6A4f-hwv6wfTH2VeOJ-KxHei/view)
- [Organizer-provided DIOS dashboard](https://unfpa-looker-web-app-126183358624.us-east1.run.app/dashboard) — exported resources supplied to the project.
- [Africa GeoPortal](https://www.africageoportal.com/) — boundary checks and supplementary facility cross-checking; external matches are evidence to verify, not automatic replacements for HDX.

See [source provenance](DATA_PROVENANCE.md), [API sources](docs/API数据来源.md) and runtime resource metadata for attribution, download details, hashes and licenses. OSM: ODbL; WorldPop: CC BY 4.0; GRID3/CIESIN boundaries: CC BY-SA 4.0; retain the HDX dataset attribution. Some linked documents preserve earlier development-stage deployment notes; the live links and current scope above describe this release.

Operational records are sourced from the organizer's supplied channels. Routes, population measures and spatial checks are derived computations. Missing clinical or acceptance data stays unknown; no synthetic patients, bed availability or referral outcomes are supplied as real data. Legacy Nairobi/mock files are not imported by the active application.

## Limits to present with the submission

- Registered levels and historical functional status do not verify emergency obstetric capability, staffing, beds, opening hours or current acceptance.
- Travel minutes are model estimates. There is no live traffic, ambulance dispatch, verified entrance access or complete nationwide routing.
- Straight-line population proximity is not driving-time coverage, maternal population, demand or actual attendance.
- DIOS provides public-report evidence, not a patient surveillance feed. Geographic ambiguity and duplicate reporting require human judgement.
- No referral-acceptance dataset or expert-reviewed clinical case benchmark was available from the organizer. Clinical effectiveness and acceptance prediction have not been established.
- Human review, version checks and audit trails support traceability; they do not resolve missing source evidence automatically.

## Run locally / teammate handoff

Clone the **whole repository**, not just this source folder. Install Git and Node.js 22.12+ (a compatible current LTS is suitable). From PowerShell:

~~~powershell
git clone https://github.com/Taoo2025/taoo2025.github.io.git
cd taoo2025.github.io\carelink-source
New-Item -ItemType Directory -Force public
Copy-Item ..\docs\carelink\config.json public\config.json
Copy-Item ..\docs\carelink\data public\data -Recurse -Force
npm ci
npm run dev
~~~

Open the local URL printed by Vite, adding `?view=hospitals` or `?view=signals`. Internet access is needed for map tiles and external source links. Import separately exported team JSON to recover browser-held reviews/plans.

~~~powershell
npm run build -- --base=/carelink/
npm run preview -- --base=/carelink/
~~~

Open the preview URL under `/carelink/`. The existing deployment serves built files from `../docs/carelink/`; changing source alone does not update the public interface. Review and commit the resulting build explicitly.

### Repository layout and reproducibility

- `src/`: React UI, runtime data validation and bilingual display dictionary.
- `scripts/`: derivation and validation scripts. Some historical scripts contain CASA-specific paths; configure these for your machine before running.
- `docs/`: methods, screening and location-comparison records.
- `../docs/carelink/config.json`: published resource URLs; copied to `public/config.json` for local development.
- `../docs/carelink/data/`: published runtime data; copied to `public/data/`.

Published runtime data is sufficient to operate the current prototype. Several resources are gzip-compressed and decoded by the app. Offline recalculation scripts expecting plain JSON require those files to be decompressed first.

The full national PBF, large PDP raw export and national population inputs remain in the CASA archive and are **not all in GitHub**. Rebuilding all derived data from raw inputs requires those inputs or a documented source download. API layers are queried as needed. Do not assume a clone includes the full raw-data archive.

The release has passed production builds, data/workflow validation and bilingual display tests. Browser checks covered route preservation across language switching, persisted language preference and canonical review values behind English labels. These checks do not constitute clinical validation.

## Method documents

- [Referral evaluation and routing](docs/队友部分_评价转诊.md)
- [DIOS signal review](docs/我的部分_DIOS信号.md)
- [Joint spatial methods and implementation](docs/456实施与方法记录.md)
- [Facility location anomaly comparisons](docs/医院位置异常_核查说明.md)
- [DIOS screening and human review](docs/DIOS_41篇初筛与人工复核.md)
- [Saved referral plans and review workflow](docs/转诊方案与复核流程.md)
- [Editing and data replacement guide](docs/提交候选版_使用与数据调整.md)
- [Bilingual interface](docs/中英文切换.md)
