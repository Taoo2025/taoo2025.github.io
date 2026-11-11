export default function SignalPanel({ signal }) {
  return (
    <aside className="panel signal-panel">
      <div className="panel-header">
        <p className="eyebrow">Referral signal</p>
        <h2>{signal.id}</h2>
      </div>

      <div className="signal-card">
        <span className="urgency-badge">
          {signal.urgency} priority
        </span>

        <h3>{signal.condition}</h3>

        <div className="info-block">
          <span className="label">Origin</span>
          <strong>{signal.originFacility}</strong>
        </div>

        <div className="info-block">
          <span className="label">Required capability</span>

          <ul>
            {signal.requiredServices.map((service) => (
              <li key={service}>{service}</li>
            ))}
          </ul>
        </div>

        <button className="primary-button">
          Validate signal
        </button>
      </div>
    </aside>
  );
}