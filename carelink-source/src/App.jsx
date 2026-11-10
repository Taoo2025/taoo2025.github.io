import PdpContext from './components/PdpContext';
import HigherFacilities from './components/HigherFacilities';
import DiosPanel from './components/DiosPanel';
import {useEffect,useState,useCallback} from 'react';
import ReferralMap from './components/ReferralMap';
import FacilityPanel from './components/FacilityPanel';
export default function App(){
 const [all,setAll]=useState([]),[state,setState]=useState('Fct'),[selected,setSelected]=useState(null),[error,setError]=useState('');
 useEffect(()=>{fetch(import.meta.env.BASE_URL+'data/nigeria_facilities_clean.json').then(r=>{if(!r.ok)throw Error('数据加载失败');return r.json()}).then(setAll).catch(e=>setError(e.message))},[]);
 const [activeRoute,setActiveRoute]=useState(null);
 const chooseRoute=useCallback(route=>setActiveRoute(route),[]);
 const facilities=all.filter(f=>f.division===state);
 return <div className="app-shell"><header className="topbar"><div><p className="eyebrow">UNFPA Population Intelligence Prototype · Nigeria</p><h1>Maternal Referral Intelligence</h1></div><label>试点州 / FCT <select value={state} onChange={e=>{setState(e.target.value);setSelected(null)}}>{[...new Set(['Fct',...all.map(f=>f.division)])].sort().map(s=><option key={s}>{s}</option>)}</select></label></header><div className="workspace" style={{display:new URLSearchParams(location.search).get('view')==='signals'?'none':undefined}}><aside className="panel signal-panel"><h2>真实机构数据工作台</h2><p>HDX Nigeria: Health facilities</p><p>{error||`${all.length} 条已载入记录；当前地区 ${facilities.length} 条。`}</p><p>原始机构信息并非实时数据。专科能力、开放时间、床位与接诊状态未知。</p><h3>上转候选机构</h3><HigherFacilities origin={selected} facilities={facilities} onRoute={chooseRoute}/>{state === 'Fct' && <PdpContext/>}<a href="?view=signals">查看 DIOS 信号</a><p>尚无经核实病例或风险信号，不显示虚构患者、紧急程度或转诊起点。</p><a href="https://data.humdata.org/dataset/nigeria-health-facilities" target="_blank" rel="noreferrer">组委会指定数据来源</a><p>FCT 为初始浏览地区，可切换其他州。</p></aside><ReferralMap facilities={facilities} selectedFacility={selected} route={activeRoute} onSelectFacility={setSelected}/><FacilityPanel facilities={facilities} selectedFacility={selected} onSelectFacility={setSelected}/></div>{new URLSearchParams(location.search).get('view')!=='hospitals'&&<DiosPanel/>}<footer className="route-bar"><strong>{selected?selected.name:'选择机构查看原始信息'}</strong><span>Geofabrik 路网距离与固定速度行程估算</span></footer></div>
}





