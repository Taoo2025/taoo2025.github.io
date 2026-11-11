import {useEffect,useState} from 'react';
import {useResource} from '../dataRuntime';
const EMPTY={};
const number=value=>Math.round(value||0).toLocaleString('zh-CN');
export default function RegionDashboard({region,onRegion,regions,facilities,population,selected,showPopulation,onShowPopulation,showBoundaries,onShowBoundaries,populationStale}){
 const [seedData]=useResource('locationChecks'),seeds=seedData||EMPTY;
 const [checks,setChecks]=useState(seeds);
 useEffect(()=>{function refresh(){const merged={...seeds};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k?.startsWith('dios-location-')){try{const v=JSON.parse(localStorage.getItem(k));if(v?.articleId)merged[v.articleId]=v}catch{/* keep original seed */}}}setChecks(merged)}refresh();window.addEventListener('dios-review-updated',refresh);window.addEventListener('storage',refresh);return()=>{window.removeEventListener('dios-review-updated',refresh);window.removeEventListener('storage',refresh)}},[seeds]);
 const summary=region==='all'?population?.overall:population?.lgas[region];
 const context=Object.values(checks).filter(c=>c.sourceVerification==='原文已读取'&&c.precision==='州/FCT'&&/FCT|Abuja/i.test(c.eventPlace)&&c.signalKind==='program-context');
 const local=Object.values(checks).filter(c=>c.humanConfirmed===true&&c.localCaseEvidence===true&&c.sourceVerification==='原文已读取'&&c.signalKind==='local-case'&&c.evidence&&c.reviewer&&c.regionCode==='NGA-FCT'&&['LGA','Ward','明确机构'].includes(c.precision)&&(region==='all'||c.verifiedLga===region));
 const unique=new Set(local.map(c=>c.duplicateGroup||c.articleId)).size;
 return <section className="region-dashboard" aria-label="行政区联合分析"><h2>行政区联合分析 · FCT</h2><label>按坐标核实的 LGA <select aria-label="行政区筛选" value={region} onChange={e=>onRegion(e.target.value)}><option value="all">全部 FCT 登记机构</option>{regions.map(r=><option key={r}>{r}</option>)}<option value="outside">落在 FCT 边界外 / 待核查</option></select></label>
 <div className="region-controls"><label><input type="checkbox" checked={showBoundaries} onChange={e=>onShowBoundaries(e.target.checked)}/>行政区边界</label><label><input type="checkbox" checked={showPopulation} disabled={populationStale} onChange={e=>onShowPopulation(e.target.checked)}/>WorldPop 人口格网</label></div>
 <p>当前显示 {facilities.length} 家：{['Primary','Secondary','Tertiary'].map(level=>`${level} ${facilities.filter(f=>f.facilityTypeCode===level).length}`).join(' / ')}。点击医院后，可跨 LGA 查找 FCT 更高层级候选。</p>
 {summary?<><h3>人口空间邻近覆盖</h3><p>2025 年模型人口约 <strong>{number(summary.population)}</strong> 人；{summary.cells} 个有效格网。约 1 km 分辨率。</p><p>距任一登记机构直线 5 km 内：{number(summary.allWithin5km)} 人（{(100*summary.allWithin5km/summary.population).toFixed(1)}%）。</p><p>距二级 / 三级机构直线 5 km 内：{number(summary.higherWithin5km)} 人（{(100*summary.higherWithin5km/summary.population).toFixed(1)}%）；10 km 内 {number(summary.higherWithin10km)} 人。</p><p>同一格网每项统计只计一次。直线邻近不代表行车可达、可接诊或孕产妇人数。</p></>:<p>此范围没有可用人口汇总。</p>}
 {selected&&population&&<p>所选医院最近邻人口分配：约 {number(population.facilityCatchments[selected.id])} 人。每格仅归属一家医院；这是空间分配模型，不是实际就诊量。</p>}
 <h3>DIOS 地点证据</h3><p>FCT 级已读取原文的项目背景报道 {context.length} 篇（AI 辅助核查，待团队复核）；不下分到 LGA。</p><p>当前已确认并去重的区级病例事件：{unique} 个。0 表示没有符合纳入条件的记录，不表示没有事件。</p>{local.map(c=><p key={c.articleId}><button onClick={()=>onRegion(c.verifiedLga)}>{c.verifiedLga}：查看医院与路由</button> <a href={`?view=signals&article=${c.articleId}`}>病例原文审核</a></p>)}<details><summary>查看背景报道与精度</summary>{context.map(c=><p key={c.articleId}><a href={`?view=signals&article=${encodeURIComponent(c.articleId)}`}>{c.eventPlace}</a> · {c.precision}<br/>{c.note}</p>)}</details>
 <p><a href="?view=signals">进入 DIOS 原文审核</a> · <a href={population?.catalog||'https://hub.worldpop.org/'} target="_blank" rel="noreferrer">WorldPop 来源</a></p><small>行政区 © CIESIN / GRID3，CC BY-SA 4.0；人口 © WorldPop，CC BY 4.0。机构位置冲突仍保留原记录，未自动移动坐标。</small></section>
}
