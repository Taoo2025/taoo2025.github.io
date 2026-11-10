import indicators from '../data/pdp-fct-indicators.json';

export default function PdpContext() {
  return (
    <details>
      <summary>FCT 孕产健康背景 · PDP</summary>
      <p>以下为调查历史统计，覆盖范围和时间窗口见每项说明。</p>
      {indicators.map((row) => (
        <article key={row[0]}>
          <strong>{row[5]}</strong>
          <p>{Number(row[18])} {row[17]} · {row[12]} · {row[11]} · {row[9]}</p>
          <small>{row[6]} · PDP 记录 {row[0]}</small>
        </article>
      ))}
      <a href="https://drive.google.com/file/d/1h7jYKhDB6A4f-hwv6wfTH2VeOJ-KxHei/view" target="_blank" rel="noreferrer">组委会提供的 PDP 数据</a>
    </details>
  );
}
