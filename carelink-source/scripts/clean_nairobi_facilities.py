import json
from pathlib import Path

INPUT = Path("public/data/nairobi_health_facilities.geojson")
OUTPUT = Path("public/data/nairobi_facilities_clean.json")


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def is_valid_nairobi_coordinate(lon, lat):
    if lon is None or lat is None:
        return False

    # 排除明显无效坐标
    if lon == 0 or lat == 0:
        return False

    # Nairobi 周边宽松范围
    return (
        36.5 <= lon <= 37.2
        and -1.6 <= lat <= -0.9
    )


with INPUT.open("r", encoding="utf-8") as f:
    data = json.load(f)


cleaned = []


for feature in data["features"]:
    properties = feature.get("properties") or {}
    geometry = feature.get("geometry")

    lon = None
    lat = None

    # 1. 优先使用 GeoJSON geometry
    if geometry and geometry.get("coordinates"):
        coords = geometry["coordinates"]

        if len(coords) >= 2:
            lon = safe_float(coords[0])
            lat = safe_float(coords[1])

    # 2. geometry 缺失或无效时，尝试 LONG / LAT
    if not is_valid_nairobi_coordinate(lon, lat):
        lon = safe_float(properties.get("LONG"))
        lat = safe_float(properties.get("LAT"))

    # 3. 两种来源都无有效 Nairobi 坐标，才跳过
    if not is_valid_nairobi_coordinate(lon, lat):
        continue

    facility = {
        "id": (
            properties.get("HMIS_")
            or properties.get("OBJECTID")
        ),

        "name": (
            properties.get("F_NAME")
            or "Unknown facility"
        ),

        "coordinates": [
            lon,
            lat,
        ],

        "province": properties.get("PROV"),
        "district": properties.get("DIST"),
        "division": properties.get("DIVISION"),
        "location": properties.get("LOCATION"),
        "subLocation": properties.get("SUB_LOCATI"),

        "facilityTypeCode": properties.get("F_TYPE"),
        "agency": properties.get("AGENCY"),

        "source": "Kenya Health Facilities ArcGIS layer",
    }

    cleaned.append(facility)


cleaned.sort(
    key=lambda x: x["name"].lower()
)


with OUTPUT.open(
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        cleaned,
        f,
        ensure_ascii=False,
        indent=2,
    )


print(f"Input features: {len(data['features'])}")
print(f"Valid Nairobi facilities: {len(cleaned)}")
print(
    "Removed invalid coordinates:",
    len(data["features"]) - len(cleaned),
)
print(f"Saved to: {OUTPUT}")