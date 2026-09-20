const projects = [
  {
    id:'fire', categories:['data','gis'], image:'assets/fire.webp', detailImage:'assets/fire-map.webp',
    imageLabel:{zh:'消防响应三阶段波动图',en:'Response-stage variability'},
    meta:{zh:'硕士论文 · 合作研究 · 2026',en:'Master’s dissertation · Collaboration · 2026'},
    title:{zh:'消防响应时间波动性分析',en:'Variability in fire service response time'},
    summary:{zh:'把“平均响应时间”拆成接警、准备与行驶三段，识别不同地区和事件类型的服务波动。',en:'Beyond the average: separating call handling, turnout and driving to examine how response varies across places and incidents.'},
    metrics:[['405,928',{zh:'条建模观测',en:'model observations'}],['97.25%',{zh:'接警时长差异在地区内部',en:'variation within local areas'}]],
    tags:['Python','OLS / Mixed effects','GeoPandas','Data QA'],
    problem:{zh:'传统平均指标掩盖了响应流程中不同环节的波动。研究比较事件类型、时期与地区差异，为流程定位提供更细的证据。',en:'An average response time hides instability in the individual stages. I compared incident type, period and geography to locate where variability occurs.'},
    method:{zh:'清洗并关联 2009—2024 年消防事件及车辆出动记录，建立 1 km 网格和时间面板；分别拟合 OLS、混合效应及事件类型分层模型，并检查变量及模型假设。',en:'I cleaned and joined 2009–2024 incident and mobilisation data, built a 1 km grid and time panel, then used OLS, mixed-effects and incident-stratified models.'},
    result:{zh:'在 405,928 条观测上，接警时长模型的地区组内方差占 97.25%。这提示仅靠地区平均值不足以解释个体事件差异，也需要关注业务过程。',en:'Across 405,928 observations, 97.25% of modelled call-handling variance was within local areas. Area averages alone cannot explain event-level differences.'},
    caveat:{zh:'图表展示汇总统计，不包含原始消防事件记录；该结果是相关性与方差分解，不代表因果效应。',en:'Figures show aggregated results only, not raw incident records. Variance decomposition is descriptive, not a causal estimate.'},
    figure:{zh:'事件风险类型与时期下的响应波动空间模式（论文汇总图）',en:'Spatial patterns of response variability by incident profile and period'},
    links:[['GitHub','https://github.com/Taoo2025/CASA0010_dissertation']]
  },
  {
    id:'transport', categories:['data','gis','web'], image:'assets/london-accessibility.webp',
    imageLabel:{zh:'伦敦 LSOA 可达性指数',en:'London LSOA accessibility index'},
    meta:{zh:'课程团队项目 · 交互平台 · 2026',en:'Course team project · Interactive platform · 2026'},
    title:{zh:'伦敦交通可达性与线路中断平台',en:'London transport accessibility & disruption'},
    summary:{zh:'整合站点、步行路网与街区数据，模拟线路取消后的可达性损失，并做成可探索的地图。',en:'Combining stops, walking networks and neighbourhood data to explore accessibility losses when routes are cancelled.'},
    metrics:[['4,994',{zh:'个 LSOA',en:'LSOA areas'}],['736,868',{zh:'条步行连接',en:'walking connections'}]],
    tags:['NetworkX','Dijkstra','Mapbox GL JS','Geospatial ETL'],
    problem:{zh:'交通设施覆盖与真实步行可达性并不相同。项目让用户查看不同空间尺度下的交通服务，并模拟线路中断的潜在影响。',en:'Transit coverage is not the same as walking accessibility. The platform compares neighbourhood and fine-grid measures and tests the possible effect of route disruption.'},
    method:{zh:'整合 27,553 个站点、OpenStreetMap 步行路网及 4,994 个 LSOA；以 Dijkstra 算法预计算站点步行连接，在 100 m 网格与 LSOA 两级尺度计算指标，再用分块数据和 Mapbox GL JS 提供交互查询。',en:'I combined 27,553 stops, OpenStreetMap walking routes and 4,994 LSOAs; precomputed connections with Dijkstra, analysed 100 m grids and LSOAs, and served chunked data in Mapbox GL JS.'},
    result:{zh:'生成 736,868 条步行连接，并支持地图筛选与线路取消情景分析。地图采用分块索引与按需加载，使较大的空间数据更适合浏览器使用。',en:'The analysis produced 736,868 walking connections and a live route-cancellation explorer. Chunked indexes and lazy loading make a large geospatial dataset usable in the browser.'},
    caveat:{zh:'该项目为课程团队工作；指标是模型化的可达性估计，不等同于实时客流或实际出行行为。',en:'This was a course team project. Accessibility is modelled, not observed real-time passenger behaviour.'},
    figure:{zh:'按 LSOA 汇总的平均可达性指数；AI 在此指 Accessibility Index',en:'LSOA mean Accessibility Index (AI here means Accessibility Index)'},
    links:[['Live map','https://taoo2025.github.io/CASA0029/'],['GitHub','https://github.com/Taoo2025/CASA0029']]
  },
  {
    id:'network', categories:['data','gis'], image:'assets/network.webp', detailImage:'assets/network-decay.webp',
    imageLabel:{zh:'地铁拓扑网络 · 真实分析图',en:'Underground topology · Project figure'},
    meta:{zh:'课程项目 · 网络与选址 · 2026',en:'Course project · Networks & retail · 2026'},
    title:{zh:'地铁网络韧性与超市选址',en:'Underground resilience & supermarket siting'},
    summary:{zh:'用网络失效模拟和空间交互模型回答两个问题：关键站点在哪里，门店开在哪里。',en:'Combining network failure simulation with a spatial interaction model to locate critical stations and compare retail sites.'},
    metrics:[['401',{zh:'个地铁站',en:'stations'}],['43,400',{zh:'条起讫点记录',en:'origin–destination pairs'}]],
    tags:['NetworkX','Spatial interaction','Scenario analysis','GIS'],
    problem:{zh:'高中心性节点是否会成为系统脆弱点？客流预测与步行覆盖又如何影响门店选址？项目将基础设施和商业选址放在可比较的情景模型里。',en:'Which stations make a network fragile? How do forecast flow and walking catchment change a retail site choice? The project compares both through scenario models.'},
    method:{zh:'根据 401 个车站与 467 条轨道连接构建拓扑网络，比较中心性并模拟节点移除。以 775 个居民区、56 家门店和 43,400 条 OD 记录校准生产约束空间交互模型，测试候选位置、规模与交通成本。',en:'I modelled 401 stations and 467 links, compared centrality and simulated removals. A production-constrained spatial interaction model used 775 origins, 56 stores and 43,400 OD pairs for siting scenarios.'},
    result:{zh:'定向移除 10 个高介数节点后，最大连通分量降至 170。选址中，地点 A 的预测客流更高，而地点 B 的 15 分钟步行覆盖人口多 2,072 人，体现了双目标取舍。',en:'After removing 10 high-betweenness nodes, the largest connected component fell to 170. Site A led on forecast flow, while Site B served 2,072 more people within a 15-minute walk.'},
    caveat:{zh:'网络失效是模型情景，预测客流依赖参数和数据假设，不是实际门店经营结果。',en:'Node failure and forecast flow are modelled scenarios, not observed operating outcomes.'},
    figure:{zh:'不同节点移除策略下，地铁网络最大连通分量的变化',en:'Largest connected component under different station removal strategies'},
    links:[]
  },
  {
    id:'retail', categories:['data','gis','web'], image:'assets/retail.webp',
    imageLabel:{zh:'伦敦贫困指数分布分析',en:'London deprivation analysis'},
    meta:{zh:'定量方法课程 · 数据叙事 · 2026',en:'Quantitative methods · Data story · 2026'},
    title:{zh:'伦敦零售格局与贫困指数',en:'London retail geography & deprivation'},
    summary:{zh:'对比 2015 与 2025 年零售点位，分析超市分布与区域贫困水平之间的空间关系。',en:'Comparing 2015 and 2025 retail points to study the spatial relationship between supermarket mix and deprivation.'},
    metrics:[['2015—25',{zh:'十年对比',en:'decade compared'}],['4,994',{zh:'个 LSOA 空间单元',en:'LSOA areas'}]],
    tags:['pandas','GeoPandas','statsmodels','Data storytelling'],
    problem:{zh:'不同贫困程度的街区，其零售选择是否趋于相似？项目将地图表达与统计检验结合，审视“零售同质化”这一城市现象。',en:'Are retail environments in richer and poorer neighbourhoods becoming more alike? This project joins mapped change with statistical testing.'},
    method:{zh:'整理 Geolytix 2015、2025 年门店点位与贫困指数，进行空间汇总、分布对比、相关分析和回归诊断，并制作面向非技术读者的数据故事。',en:'I cleaned Geolytix retail points for 2015 and 2025, joined deprivation data, compared distributions, checked correlations and regression diagnostics, then wrote a public-facing data story.'},
    result:{zh:'样本门店数由 1,503 增至 1,884。分析显示零售结构在不同贫困分位间出现收敛迹象，具体解释受数据覆盖与门店分类方式影响。',en:'The sample grew from 1,503 to 1,884 stores. Retail composition showed signs of convergence across deprivation groups, subject to data coverage and classification.'},
    caveat:{zh:'贫困水平和零售结构的相关性不表示因果关系；两期点位数据可能存在覆盖口径差异。',en:'Association between deprivation and retail mix does not establish causation; coverage may differ between the two years.'},
    figure:{zh:'2015 年伦敦贫困指数的空间分布（项目图表）',en:'Spatial distribution of London deprivation in 2015 (project figure)'},
    links:[['GitHub','https://github.com/Taoo2025/CASA0007_QM']]
  }
];

const others = [
  {title:{zh:'伦敦弱势道路使用者碰撞严重性',en:'London vulnerable road user collision severity'},summary:{zh:'合并事故、伤亡与车辆记录，分析行人与骑行者风险，并探索旅游活动与空间差异。',en:'Joined collision, casualty and vehicle records to investigate pedestrian and cyclist severity and spatial context.'},tags:['Data cleaning','Feature engineering','Spatial risk'],link:'https://github.com/Taoo2025/CASA0006_DSSS'},
  {title:{zh:'短租与居住迁移多主体模拟',en:'Short-term rentals & displacement simulation'},summary:{zh:'以 NetLogo 构建房东与租户行为规则，比较短租上限等政策情景下的模拟结果。',en:'NetLogo simulation of landlord and tenant behaviour under short-let policy scenarios.'},tags:['NetLogo','Agent-based model','Policy scenarios'],link:'https://github.com/Taoo2025/CASA0011_ABM'},
  {title:{zh:'伦敦 Airbnb 专业化的空间分布',en:'Spatial patterns of Airbnb professionalisation'},summary:{zh:'课程小组研究：利用区域聚合和空间可视化，考察专业房东运营强度的地区差异。',en:'Group study mapping and aggregating the spatial intensity of professional Airbnb hosting.'},tags:['Group project','Spatial analysis','Data visualisation'],link:'https://github.com/Taoo2025/casa0013_fsds_finalwork'}
];

let language = localStorage.getItem('portfolio-language') === 'en' ? 'en' : 'zh';
let filter = 'all';
const t = obj => typeof obj === 'string' ? obj : obj[language];
const safe = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const external = ([label,url]) => `<a href="${safe(url)}" target="_blank" rel="noopener noreferrer">${safe(label)} ↗</a>`;
const tagHtml = tags => `<div class="tags">${tags.map(tag=>`<span class="tag">${safe(tag)}</span>`).join('')}</div>`;

function renderProjects(){
  const visible = projects.filter(p => filter === 'all' || p.categories.includes(filter));
  document.getElementById('project-grid').innerHTML = visible.map((p,i) => `<article class="project-card" id="${p.id}">
    <div class="project-image"><img src="${p.image}" alt="${safe(t(p.imageLabel))}"><span class="project-number">${String(projects.indexOf(p)+1).padStart(2,'0')} / 04</span><span class="image-label">${safe(t(p.imageLabel))}</span></div>
    <div class="project-body"><span class="project-meta">${safe(t(p.meta))}</span><h3>${safe(t(p.title))}</h3><p class="project-summary">${safe(t(p.summary))}</p>
    <div class="metrics">${p.metrics.map(([value,label])=>`<div class="metric"><strong>${safe(value)}</strong><span>${safe(t(label))}</span></div>`).join('')}</div>
    ${tagHtml(p.tags)}<div class="card-links"><button class="case-button" type="button" data-case="${p.id}">${language==='zh'?'查看项目详情':'View case study'} →</button>${p.links.slice(0,1).map(external).join('')}</div></div></article>`).join('');
  document.getElementById('result-count').textContent = language === 'zh' ? `显示 ${visible.length} / ${projects.length} 个精选项目` : `Showing ${visible.length} of ${projects.length} selected projects`;
}

function renderOthers(){document.getElementById('other-projects').innerHTML=others.map((p,i)=>`<article class="other-row"><span class="other-index">0${i+5}</span><div><h3>${safe(t(p.title))}</h3><p>${safe(t(p.summary))}</p>${tagHtml(p.tags)}</div><a href="${p.link}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></article>`).join('')}
function setLanguage(next){language=next;localStorage.setItem('portfolio-language',language);document.documentElement.lang=language==='zh'?'zh-CN':'en';document.querySelectorAll('[data-zh][data-en]').forEach(node=>node.innerHTML=node.dataset[language]);const b=document.getElementById('language');b.textContent=language==='zh'?'EN':'中文';b.setAttribute('aria-label',language==='zh'?'Switch to English':'切换为中文');renderProjects();renderOthers()}
function openCase(id){const p=projects.find(p=>p.id===id);if(!p)return;document.getElementById('case-content').innerHTML=`<span class="eyebrow">${safe(t(p.meta))}</span><h2 id="case-title">${safe(t(p.title))}</h2>${[['problem','01 / '+(language==='zh'?'研究问题':'The question')],['method','02 / '+(language==='zh'?'数据与方法':'Data & method')],['result','03 / '+(language==='zh'?'主要发现':'What emerged')]].map(([key,label])=>`<section class="case-section"><h3>${label}</h3><p>${safe(t(p[key]))}</p></section>`).join('')}<figure class="case-figure"><img src="${p.detailImage||p.image}" alt="${safe(t(p.figure))}"><figcaption>${safe(t(p.figure))}</figcaption></figure><p class="case-caveat">${safe(t(p.caveat))}</p>${tagHtml(p.tags)}<div class="case-external">${p.links.map(external).join('')}</div>`;const d=document.getElementById('case-dialog');d.showModal();document.body.classList.add('modal-open');d.querySelector('.close-dialog').focus()}

document.getElementById('language').addEventListener('click',()=>setLanguage(language==='zh'?'en':'zh'));
document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{filter=button.dataset.filter;document.querySelectorAll('.filter').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',b===button?'true':'false')});renderProjects()}));
document.getElementById('project-grid').addEventListener('click',e=>{const b=e.target.closest('[data-case]');if(b)openCase(b.dataset.case)});
const dialog=document.getElementById('case-dialog');
dialog.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');document.querySelector('[data-case]:focus')?.focus()});
setLanguage(language);
