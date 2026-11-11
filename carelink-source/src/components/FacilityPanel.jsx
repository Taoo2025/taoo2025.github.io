export default function FacilityPanel({
  facilities,
  selectedFacility,
  onSelectFacility,
}) {
  return (
    <aside className="panel facility-panel">
      <div className="panel-header">
        <p className="eyebrow">Facility network</p>

        <h2>Health facilities</h2>

        <p className="facility-count">
          {facilities.length} valid POIs
        </p>
      </div>

      <div className="facility-list">
        {facilities.map((facility) => (
          <button
            key={facility.id}
            className={`facility-card ${
              selectedFacility?.id === facility.id
                ? "selected"
                : ""
            }`}
            onClick={() => onSelectFacility(facility)}
          >
            <div className="facility-title-row">
              <strong>{facility.name}</strong>

              <span className="match-badge unknown">
                Unverified
              </span>
            </div>

            <p>
              Type code:{" "}
              {facility.facilityTypeCode ?? "Unknown"}
            </p>

            <div className="facility-metrics">
              <span>
                {facility.agency || "Agency unknown"}
              </span>
            </div>

            <div className="capabilities">
              <span>
                {facility.location ||
                  facility.division ||
                  "Location unavailable"}
              </span>
            </div>
          </button>
        ))}
      </div>
    </aside>
  );
}