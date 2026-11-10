import { useEffect, useState } from 'react';

export default function HigherFacilities({ origin, facilities, onRoute }) {
  const [network, setNetwork] = useState(null);
  const [error, setError] = useState('');
  useEffect(() => {
    fetch(import.meta.env.BASE_URL + 'data/fct_routes.json.gz')
      .then(response => {
        if (!response.ok) throw new Error('路网结果加载失败');
        return new Response(response.body.pipeThrough(new DecompressionStream('gzip'))).json();
      })
      .then(setNetwork)
      .catch(error => setError(error.message));
  }, []);
  useEffect(() => { onRoute(null); }, [origin?.id, onRoute]);
  if (!origin) return <p>从地图或列表选择转出机构。</p>;
  if (origin.facilityTypeCode === 'Tertiary') return <p>当前为三级机构，已达到本数据的最高层级。</p>;
  if (error) return <p role="alert">{error}</p>;
  if (!network) return <p>正在加载路网计算结果…</p>;
  const result = network.origins[origin.id];
  if (!result) return <p>路网计算当前覆盖 FCT，请切换到 Fct。</p>;
  if (!result.snap.valid) return <p>机构距可行车路网节点 {result.snap.gap_m} 米，超过 500 米接入阈值，需要核查位置。</p>;
  return (
    <div>
      <strong>{origin.name} · {origin.facilityTypeCode}</strong>
      <p>在 FCT 全部更高层级机构中，沿区域有向路网找到 {result.reachableHigher} 个候选。按最短道路距离显示前三个。</p>
      <p>起点接入间隙 {result.snap.gap_m} 米。</p>
      {result.routes.map(route => {
        const target = facilities.find(facility => facility.id === route.targetId);
        return <button key={route.targetId} onClick={() => onRoute({ ...route, origin, target })} style={{ display: 'block', width: '100%', marginBottom: 10, textAlign: 'left' }}>
          <strong>{target?.name || route.targetId}</strong><br />
          {target?.facilityTypeCode} · 道路 {route.roadKm.toFixed(2)} km<br />
          固定速度估算 {route.estimatedMinutes} 分钟 · 终点接入间隙 {route.targetGapM} 米
        </button>;
      })}
      {!result.routes.length && <p>区域路网内没有找到连通的更高层级候选。</p>}
      <details><summary>路网方法与速度假设</summary>
        <p>Geofabrik / OpenStreetMap。保留机动车通行道路，处理道路单行方向，按最短道路距离选择路径。路段预计时间按道路类别速度累加。</p>
        <p>{Object.entries(network.speedsKmh).map(([road, speed]) => road + ' ' + speed + ' km/h').join('，')}</p>
        <p>医院连接最近道路节点，上限 500 米。起终点接入间隙单独显示，未计入道路公里数和分钟数。区域边界、转向限制、障碍物、道路质量及实时交通可能影响结果。</p>
        <a href={network.source} target="_blank" rel="noreferrer">Geofabrik 原始数据</a>
        <p>道路数据 © OpenStreetMap contributors，ODbL。</p>
      </details>
    </div>
  );
}

