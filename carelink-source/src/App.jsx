import ReferralPlans from './components/ReferralPlans';
import AdminCheck from './components/AdminCheck';
import PdpContext from './components/PdpContext';
import HigherFacilities from './components/HigherFacilities';
import DiosPanel from './components/DiosPanel';
import RegionDashboard from './components/RegionDashboard';
import DataWorkbench from './components/DataWorkbench';
import {useEffect,useState,useCallback,useMemo} from 'react';
import {useResource,useOverrides,applyFacilityPatch,spatiallyChanged,adjustedAdmin,matchesSnapshot} from './dataRuntime';
import ReferralMap from './components/ReferralMap';
import FacilityPanel from './components/FacilityPanel';
const EMPTY=[];
export default function App(){
 const [baselineData,error]=useResource('facilities'),[config]=useResource('config'),[adminData,adminError]=useResource('admin'),[boundary,boundaryError]=useResource('boundaries'),[populationData,populationError]=useResource('population'),[anomalies]=useResource('hospitalComparison');
 const baseline=baselineData||EMPTY,overrides=useOverrides();
 const all=useMemo(()=>applyFacilityPatch(baseline,overrides),[baseline,overrides]);
 const [facilityQuery,setFacilityQuery]=useState('');
 const [state,setState]=useState('Fct'),[selectedId,setSelectedId]=useState(null),[region,setRegion]=useState('all'),[showPopulation,setShowPopulation]=useState(false),[showBoundaries,setShowBoundaries]=useState(true),[activeRoute,setActiveRoute]=useState(null);
 useEffect(()=>{if(config?.initialState){setState(config.initialState);setSelectedId(null);setRegion('all')}},[config?.initialState]);
 const selected=useMemo(()=>all.find(f=>f.id===selectedId)||null,[all,selectedId]);
 const onSelect=useCallback(f=>setSelectedId(f?.id||null),[]),chooseRoute=useCallback(route=>setActiveRoute(route),[]);
 const spatialStale=useMemo(()=>spatiallyChanged(baseline,overrides),[baseline,overrides]);
 const populationStale=spatialStale||Boolean(populationData&&!matchesSnapshot(all.filter(f=>f.division===populationData.region),populationData.facilitySnapshot));
 const [cellData,cellsError]=useResource(showPopulation&&!populationStale?'cells':null),cells=cellData||EMPTY;
 const admin=useMemo(()=>adjustedAdmin(adminData,boundary,all,overrides),[adminData,boundary,all,overrides]);
 useEffect(()=>{setActiveRoute(null);if(spatialStale)setShowPopulation(false)},[spatialStale,overrides]);
 const stateFacilities=useMemo(()=>all.filter(f=>f.division===state),[all,state]);
 const regionFacilities=useMemo(()=>state!==config?.studyState||region==='all'?stateFacilities:stateFacilities.filter(f=>{const m=admin?.hospitals[f.id]?.matches||[];return region==='outside'?m.length!==1:m.length===1&&m[0].lga===region}),[stateFacilities,state,region,admin,config?.studyState]);
 const facilities=useMemo(()=>regionFacilities.filter(f=>(f.name+' '+f.id+' '+f.district).toLowerCase().includes(facilityQuery.toLowerCase())),[regionFacilities,facilityQuery]);
 const changeRegion=useCallback(value=>{setRegion(value);setFacilityQuery('');setSelectedId(null);setActiveRoute(null)},[]);
 const regions=useMemo(()=>boundary?.features.map(f=>f.properties.lga).sort()||[],[boundary]);
 const visibleCells=useMemo(()=>!showPopulation||populationStale||state!==config?.studyState?[]:cells.filter(c=>region==='all'||c.lga===region),[cells,showPopulation,populationStale,state,region,config?.studyState]);
 const view=new URLSearchParams(location.search).get('view'),dataError=adminError||boundaryError||populationError||cellsError;
 return <div className="app-shell"><header className="topbar"><div><p className="eyebrow">UNFPA Population Intelligence Prototype · Nigeria</p><h1>CareLink · Maternal Referral Intelligence</h1><small>{config?.releaseLabel||'数据配置加载中'} · <a href="?view=hospitals">医院与转诊</a> · <a href="?view=signals">DIOS信号</a> · <a href={config?.docsUrl} target="_blank" rel="noreferrer">使用与数据调整说明</a></small></div><label>试点州 / FCT <select value={state} onChange={e=>{setState(e.target.value);changeRegion('all')}}>{[...new Set(['Fct',...all.map(f=>f.division)])].sort().map(s=><option key={s}>{s}</option>)}</select></label></header><DataWorkbench baseline={baseline} selected={selected} overrides={overrides} stale={spatialStale} anomalies={anomalies}/><ReferralPlans route={spatialStale?null:activeRoute} facilities={all} blocked={spatialStale}/><div className="workspace" style={{display:view==='signals'?'none':undefined}}><aside className="panel signal-panel"><h2>真实机构数据工作台</h2><label>搜索医院<input aria-label="搜索医院" placeholder="名称、机构ID或LGA" value={facilityQuery} onChange={e=>{setFacilityQuery(e.target.value);setSelectedId(null);setActiveRoute(null)}}/></label><p>HDX Nigeria: Health facilities</p><p>{error||`${all.length} 条已载入记录；当前地区 ${stateFacilities.length} 条。`}</p><p>原始机构信息并非实时数据。专科能力、开放时间、床位与接诊状态未知。</p>{dataError&&<p role="alert">{dataError}</p>}{populationStale&&<p role="status">医院坐标或数据版本发生变化，医院邻近覆盖已暂停，需使用匹配的新数据重算。</p>}{state===config?.studyState&&<RegionDashboard region={region} onRegion={changeRegion} regions={regions} facilities={facilities} population={populationStale?null:populationData} selected={selected} showPopulation={showPopulation} onShowPopulation={setShowPopulation} showBoundaries={showBoundaries} onShowBoundaries={setShowBoundaries} populationStale={populationStale}/>}<AdminCheck facility={selected} suppliedData={admin}/><h3>上转候选机构</h3><HigherFacilities origin={selected} facilities={stateFacilities} onRoute={chooseRoute} blockedReason={spatialStale?'医院位置或层级已调整，旧路由已暂停。请重算并更新配置中的路由文件。':''}/>{state===config?.studyState&&<PdpContext/>}<p>转诊起点由用户选择登记机构，未从新闻生成患者。</p><a href="https://data.humdata.org/dataset/nigeria-health-facilities" target="_blank" rel="noreferrer">组委会指定机构数据来源</a><p>FCT提供行政区、人口和路网联合分析；其他州当前浏览机构。</p></aside><ReferralMap facilities={facilities} selectedFacility={selected} route={spatialStale?null:activeRoute} onSelectFacility={onSelect} boundary={state===config?.studyState&&showBoundaries?boundary:null} region={region} onRegion={changeRegion} populationCells={visibleCells}/><FacilityPanel facilities={facilities} selectedFacility={selected} onSelectFacility={onSelect}/></div>{view!=='hospitals'&&<DiosPanel/>}<footer className="route-bar"><strong>{selected?selected.name:'选择机构查看原始信息'}</strong><span>道路距离排序 · 固定速度估算 · 人口邻近覆盖</span></footer></div>
}
