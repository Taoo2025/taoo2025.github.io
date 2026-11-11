import {useResource} from '../dataRuntime';
export default function AdminCheck({facility,suppliedData}) {
 const [data,error]=useResource('admin');
 if(!facility)return null;
 const effective=suppliedData||data;
 const record=effective?.hospitals?.[facility.id];
 if(!record)return <p>{error?'行政区核查加载失败':'行政区核查加载中或当前地区未覆盖'}</p>;
 return <details open><summary>坐标所在行政区核查</summary><p>HDX 原始 LGA：{record.originalLga}</p><p>核查结果：{{match:'LGA 一致',conflict:'LGA 冲突，需核查',outside:'边界之外，需核查',ambiguous:'多边界匹配，需核查'}[record.status]}</p>{record.matches.map(m=><p key={m.objectId}>GRID3 LGA：{m.lga} · Ward：{m.ward}</p>)}{record.geoportalCandidates?.map((g,i)=><p key={i}>GeoPortal 待确认匹配：{g.name} · {g.lga} / {g.ward} · 相距 {g.separationM} 米</p>)}{record.surroundingMatches?.map(m=><p key={m.OBJECTID}>周边边界结果：{m.state} / {m.lga} / {m.ward}</p>)}<p>{record.followupNote}</p><p>2026 GRID3 工作边界，尚待政府全面验证。位置冲突需结合原始资料核查。</p><a href={effective.source} target="_blank" rel="noreferrer">边界来源 · CC BY-SA 4.0</a></details>;
}

