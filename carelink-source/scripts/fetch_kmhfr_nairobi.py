import json
import re
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_URL = "https://api.kmhfr.health.go.ke/api/public/facilities/"
PAGE_SIZE = 100

OUTPUT_FILE = Path("public/data/nairobi_maternal_facilities.json")


MATERNAL_KEYWORDS = [
    "matern",
    "obstet",
    "gynaecol",
    "gynecol",
    "antenatal",
    "postnatal",
    "delivery",
    "midwif",
    "birth",
]

CSECTION_KEYWORDS = [
    "caesarean",
    "cesarean",
    "c-section",
    "c section",
]

BLOOD_KEYWORDS = [
    "blood transfusion",
    "blood bank",
]

CEMONC_KEYWORDS = [
    "comprehensive emergency obstetric",
    "comprehensive obstetric",
    "comprehensive maternity",
    "cemoc",
]

BEMONC_KEYWORDS = [
    "basic emergency obstetric",
    "basic obstetric",
    "bemonc",
]

EMERGENCY_KEYWORDS = [
    "emergency",
    "casualty",
    "trauma",
]


def build_session():
    session = requests.Session()

    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "User-Agent": "MaternalReferralHackathonPrototype/1.0",
        "Accept": "application/json",
    })

    return session


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def parse_level(value):
    if not value:
        return None

    match = re.search(r"(\d+)", str(value))

    if match:
        return int(match.group(1))

    return None


def contains_any(text, keywords):
    text = text.lower()

    return any(keyword in text for keyword in keywords)


def normalise_facility(facility):
    services = facility.get("service_names") or []

    if isinstance(services, str):
        services = [services]

    service_text = " ".join(services).lower()

    name = str(facility.get("name") or "").strip()
    facility_type = str(
        facility.get("facility_type_name") or ""
    ).strip()

    combined_text = (
        service_text
        + " "
        + name.lower()
        + " "
        + facility_type.lower()
    )

    lat = safe_float(facility.get("lat"))
    lon = safe_float(facility.get("long"))

    if lat is None or lon is None:
        return None

    if lat == 0 or lon == 0:
        return None

    has_maternity = contains_any(
        combined_text,
        MATERNAL_KEYWORDS,
    )

    if not has_maternity:
        return None

    facility_id = str(
        facility.get("id")
        or facility.get("code")
        or name
    )

    return {
        "id": facility_id,

        "code": str(
            facility.get("code") or ""
        ).strip(),

        "name": name,

        "coordinates": [
            lon,
            lat,
        ],

        "level": parse_level(
            facility.get("keph_level_name")
        ),

        "levelName": str(
            facility.get("keph_level_name") or ""
        ).strip(),

        "facilityType": facility_type,

        "owner": str(
            facility.get("owner_name") or ""
        ).strip(),

        "ownerType": str(
            facility.get("owner_type_name") or ""
        ).strip(),

        "county": str(
            facility.get("county_name") or ""
        ).strip(),

        "subCounty": str(
            facility.get("sub_county_name") or ""
        ).strip(),

        "ward": str(
            facility.get("ward_name") or ""
        ).strip(),

        "beds": safe_int(
            facility.get("beds")
        ),

        "cots": safe_int(
            facility.get("cots")
        ),

        "open24Hours": bool(
            facility.get("open_whole_day")
        ),

        "openWeekends": bool(
            facility.get("open_weekends")
        ),

        "operationalStatus": str(
            facility.get("operation_status_name")
            or ""
        ).strip(),

        "services": services,

        "hasMaternity": True,

        # These four are derived from the published service names.
        # They are not clinical verification.
        "cSection": contains_any(
            service_text,
            CSECTION_KEYWORDS,
        ),

        "bloodTransfusion": contains_any(
            service_text,
            BLOOD_KEYWORDS,
        ),

        "cemonc": contains_any(
            service_text,
            CEMONC_KEYWORDS,
        ),

        "bemonc": contains_any(
            service_text,
            BEMONC_KEYWORDS,
        ),

        "hasEmergency": contains_any(
            service_text,
            EMERGENCY_KEYWORDS,
        ),

        "source": "Kenya Master Health Facility Registry",

        "sourceUrl": (
            "https://kmhfr.health.go.ke/public/facilities/"
            + facility_id
        ),
    }


def main():
    session = build_session()

    page = 1
    total_pages = None

    output = []

    print("Fetching KMHFR facilities...")

    while True:
        params = {
            "format": "json",
            "page_size": PAGE_SIZE,
            "page": page,
        }

        response = session.get(
            API_URL,
            params=params,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        if total_pages is None:
            total_pages = data.get("total_pages", 1)

            print(
                f"API reports {data.get('count')} facilities "
                f"across {total_pages} pages."
            )

        for facility in data.get("results", []):

            county = str(
                facility.get("county_name") or ""
            ).strip().lower()

            # MVP先只做Nairobi
            if county != "nairobi":
                continue

            normalised = normalise_facility(
                facility
            )

            if normalised:
                output.append(normalised)

        print(
            f"Page {page}/{total_pages} | "
            f"Nairobi maternal facilities: {len(output)}"
        )

        if page >= total_pages:
            break

        page += 1

        # 对政府API稍微温柔一点
        time.sleep(0.25)

    output.sort(
        key=lambda x: (
            -(x["level"] or 0),
            x["name"],
        )
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print(
        f"Saved {len(output)} facilities to:"
    )
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()