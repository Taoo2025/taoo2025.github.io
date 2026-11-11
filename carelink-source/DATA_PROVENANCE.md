# Nigeria source provenance

Organizer-provided channel: https://data.humdata.org/dataset/nigeria-health-facilities
Resource: NigeriaHealthFacilities.json, resource ID 5a3bdd13-3ada-4bf4-ac38-643390bc0562.
Downloaded 2026-11-03. Original metadata, CSV and geographic JSON retained in public/data/sources. HDX metadata licence: Creative Commons Attribution International (CC BY).
46,146 source features; 46,146 coordinate-valid output records. Coordinate screening: Point geometry, longitude 2–15 and latitude 4–14. This broad sanity check is not administrative boundary verification.
No specialist services, live availability, travel times, patients or DIOS signals were invented. Unknown values remain null. Source functional_status is historical registration information, not current referral acceptance. Original timestamps retained.
Default demonstration region: Fct (576 records); other Nigerian states selectable.
Old Nairobi files and mockData.js remain as historical source files but are no longer imported by the active application.


## 2026-11-11 additions

WorldPop original URL: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/NGA/v1/1km_ua/constrained/nga_pop_2025_CN_1km_R2025A_UA_v1.tif

SHA256: 1442628f7b0094c20870776f08d551f2d5ce192932096c45fd9629a711442d66

WorldPop Global2 R2025A v1, constrained, UN-adjusted; estimated persons per cell; CC BY 4.0; WorldPop, University of Southampton. FCT cell-centre clipping; no synthetic records. Statistical method and limitations: docs/456实施与方法记录.md. Road v2 audit carries the source PBF SHA256 and supported/unsupported rule counts. GRID3 boundary license CC BY-SA 4.0 retained. DIOS manual verification does not imply patient-level geolocation.

Routing v2 PBF SHA256: 69a289f103621bfa9ff67861487e1f95279085af203b98d3867dad9c8ccb4ba2

Counts: {"gatesWithoutConfirmedOpening": 905, "blockedSegments": 244, "regionalRestrictions": 17, "supportedRestrictions": 10, "unsupportedRestrictions": 7, "blockedNodes": 227, "restrictedJunctions": 8, "snappedFacilities": 574, "originsWithRoutes": 566, "routes": 1698}

Validation: docs/456验证结果.json. Local production build passed; this update was not uploaded to GitHub.
