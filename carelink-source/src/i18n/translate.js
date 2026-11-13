// UI-only dictionary. Reports, hospital names and evidence remain in their source language.
const pairs=`医院与转诊|Hospitals & referrals
DIOS信号|DIOS signals
使用与数据调整说明|Data and editing guide
试点州 / FCT|Study state / FCT
搜索医院|Search hospitals
名称、机构ID或LGA|Name, facility ID or LGA
上转候选机构|Higher-level referral candidates
清除选择并重置地图|Clear selection and reset map
从地图或列表选择转出机构。|Select an origin facility on the map or list.
当前为三级机构，已达到本数据的最高层级。|This tertiary facility is at the highest level in this dataset.
正在加载路网计算结果…|Loading road-network results…
医院与路由数据版本不匹配，需重算路由。旧路径不展示。|Facility and route versions differ. Recalculate routes; old paths are hidden.
路网计算当前覆盖 FCT，请切换到 Fct。|Routing currently covers FCT. Select Fct.
区域路网内没有找到连通的更高层级候选。|No connected higher-level candidates were found in this road network.
路网方法与速度假设|Routing method and speed assumptions
Geofabrik 原始数据|Geofabrik source data
Geofabrik / OpenStreetMap。保留机动车通行道路，处理道路单行方向，按最短道路距离选择路径。路段预计时间按道路类别假设速度累加，并受可解析的标注限速约束。已支持单一 via-node 的无条件机动车转向限制和明确禁止机动车的障碍节点。|Geofabrik / OpenStreetMap motor-vehicle roads, with one-way directions and shortest-distance routing. Estimated time sums road-class speed assumptions capped by readable speed limits. Unconditional single via-node turn restrictions and explicit motor-vehicle barriers are supported.
道路数据 © OpenStreetMap contributors，ODbL。|Road data © OpenStreetMap contributors, ODbL.
原始机构信息并非实时数据。专科能力、开放时间、床位与接诊状态未知。|Facility records are not live. Specialist services, hours, beds and acceptance status are unknown.
医院坐标或数据版本发生变化，医院邻近覆盖已暂停，需使用匹配的新数据重算。|Facility coordinates or data versions changed. Proximity coverage is paused until recalculated with matching data.
转诊起点由用户选择登记机构，未从新闻生成患者。|Users select a registered facility as the origin. News reports do not generate patients.
组委会指定机构数据来源|Organizer-designated facility data
FCT提供行政区、人口和路网联合分析；其他州当前浏览机构。|Integrated administrative, population and routing analysis covers FCT. Other states support facility browsing.
选择机构查看原始信息|Select a facility to view its source record
道路距离排序 · 固定速度估算 · 人口邻近覆盖|Road-distance ranking · Assumed-speed estimates · Population proximity
行政区联合分析 · FCT|Regional analysis · FCT
行政区联合分析|Regional analysis
按坐标核实的 LGA|LGA checked against coordinates
行政区筛选|Administrative-area filter
全部 FCT 登记机构|All FCT-registered facilities
落在 FCT 边界外 / 待核查|Outside FCT boundary / review needed
行政区边界|Administrative boundaries
WorldPop 人口格网|WorldPop population grid
人口空间邻近覆盖|Population proximity coverage
同一格网每项统计只计一次。直线邻近不代表行车可达、可接诊或孕产妇人数。|Each grid cell is counted once per measure. Straight-line proximity does not establish driving access, acceptance or maternal population.
此范围没有可用人口汇总。|No population summary is available for this area.
所选医院暂无可用的人口分配值；不将资料缺漏当作0人口。|No population allocation is available for this facility. Missing data is not treated as zero.
DIOS 地点证据|DIOS location evidence
查看背景报道与精度|View context reports and location precision
进入 DIOS 原文审核|Review DIOS source articles
病例原文审核|Review case source
WorldPop 来源|WorldPop source
行政区 © CIESIN / GRID3，CC BY-SA 4.0；人口 © WorldPop，CC BY 4.0。机构位置冲突仍保留原记录，未自动移动坐标。|Boundaries © CIESIN / GRID3, CC BY-SA 4.0; population © WorldPop, CC BY 4.0. Conflicting facility locations retain their original coordinates.
坐标所在行政区核查|Coordinate-based administrative check
HDX 原始 LGA：|Original HDX LGA: 
核查结果：|Check result: 
周边边界结果：|Nearby boundary results: 
GeoPortal 待确认匹配：|GeoPortal matches pending confirmation: 
2026 GRID3 工作边界，尚待政府全面验证。位置冲突需结合原始资料核查。|2026 GRID3 working boundaries await full government validation. Resolve conflicts using source evidence.
边界来源 · CC BY-SA 4.0|Boundary source · CC BY-SA 4.0
LGA 一致|LGA matches
未知|Unknown
待核查|Pending review
国家|Country
州/FCT|State/FCT
明确机构|Specific facility
FCT 孕产健康背景 · PDP|FCT maternal-health context · PDP
以下为调查历史统计，覆盖范围和时间窗口见每项说明。|Historical survey statistics. See each indicator for geographic coverage and reference period.
组委会提供的 PDP 数据|Organizer-provided PDP data
数据调整与团队复核 · DIOS / 医院位置|Data editing and team review · DIOS / facility locations
位置与DIOS数据可调整，不需要改程序。修改保存本浏览器；导出JSON后，队友可在这里导入。GitHub静态页面不会自动写回共享数据库。|Edit location and DIOS data without changing code. Changes stay in this browser; export JSON for teammates to import here. GitHub Pages does not write to a shared database.
导入修正/审核/DIOS JSON|Import edits / reviews / DIOS JSON
导入数据调整|Import data edits
导出团队修改|Export team edits
恢复发布DIOS数据|Restore published DIOS data
导出当前DIOS数据模板|Export current DIOS template
使用发布版本的道路与覆盖结果。|Using published routing and coverage results.
位置或层级已改变，旧路由和医院邻近覆盖暂停；重算后更新配置中的数据文件。|Location or level changed. Old routing and proximity coverage are paused; recalculate and update the configured files.
医院位置调整|Edit facility location
查看原始与对比数据|View original and comparison data
保存该机构修正|Save facility correction
恢复该机构发布值|Restore published facility values
先在医院地图或列表选择机构，再回来修改经纬度、行政区或层级。原始HDX数据不会被覆盖。|Select a facility on the map or list, then edit coordinates, administrative area or level here. Original HDX data is preserved.
数据源配置（维护人员）|Data-source settings (maintainers)
数据文件地址放在配置中；可替换医院、DIOS、边界、路由及人口数据。路由与覆盖需使用同版本医院坐标重算。公开文件不得包含患者身份信息。|Configure URLs for facility, DIOS, boundary, routing and population data. Recalculate routes and coverage using matching facility coordinates. Public files must not contain patient identities.
载入当前配置|Load current settings
恢复发布配置|Restore published settings
应用数据源配置|Apply data-source settings
数据源配置JSON|Data-source settings JSON
经度|Longitude
纬度|Latitude
机构名称|Facility name
登记州|Registered state
登记LGA|Registered LGA
来源URL/证据|Source URL / evidence
审核人|Reviewer
调整原因|Reason for correction
机构层级|Facility level
转诊方案记录 ·|Referral plans ·
保存机构间备选方案与依据，可关联新闻证据；不记录患者身份、不推断紧急程度，也不代表医院已接收。记录仅在本浏览器，支持团队JSON导入导出。|Save facility-to-facility options with rationale and optional news evidence. No patient identities, urgency assessment or acceptance confirmation. Records stay in this browser and support team JSON exchange.
先在医院页选择转出机构，再点击一条更高层级道路候选。|Select an origin on the hospital page, then choose a higher-level road candidate.
记录人|Recorded by
选择依据|Selection rationale
方案记录人|Plan author
方案选择依据|Plan rationale
为何选择该候选、尚需核实什么；不要填写患者身份|Explain the choice and remaining checks. Do not enter patient identities.
关联DIOS报道（可选）|Link a DIOS article (optional)
方案关联报道|Linked article
无关联报道|No linked article
新闻关联仅记录来源，不会把报道地点当作患者或转诊起点。|Article links record evidence only. Reported locations do not become patients or referral origins.
保存当前转诊方案|Save current referral plan
导出转诊方案|Export referral plans
方案状态|Plan status
方案审核人|Plan reviewer
方案审核依据|Plan review rationale
保存方案状态|Save plan status
审核历史与待核实事项|Review history and outstanding checks
待团队复核|Pending team review
已复核方案|Plan reviewed
作废|Voided
医院与路网版本仍匹配|Facility and road-network versions still match
历史方案：数据版本已变化或尚未载入，需重新评估；保留原始快照。|Historical plan: data changed or is not loaded. Reassessment required; original snapshot retained.
方案已保存，尚未联系或确认医院接收。|Plan saved. Hospital contact and acceptance are not confirmed.
方案状态与审核历史已保存；不代表临床转诊已完成。|Plan status and history saved. This does not establish a completed clinical transfer.
方案缺少有效起终点、道路结果、来源、记录人或选择依据|A valid origin, destination, route, source, author and rationale are required.
更新状态需填写审核人、依据并选择状态|Provide a reviewer, rationale and status to update the plan.
DIOS 真实信号与人工验证|DIOS source signals and human review
返回行政区与转诊工作台|Back to regional and referral workspace
复核范围|Review scope
全部 Nigeria|All Nigeria articles
已发布初筛批次|Published screening batch
已发布高优先级|Published high-priority batch
全部候选中原文受限|Candidates with inaccessible sources
复核状态筛选|Review-status filter
全部状态|All statuses
主题|Topic
全部|All
孕产妇死亡|Maternal mortality
产科瘘|Obstetric fistula
搜索 DIOS|Search DIOS
搜索标题或摘要|Search title or summary
选择真实文章查看来源与位置线索。|Select an article to inspect its source and location clues.
关联转诊方案：前往医院页另选起点与候选|Link a referral plan: choose an origin and candidate on the hospital page
查看原文|Read source article
模型：|Model: 
情绪解释：|Sentiment explanation: 
原始位置线索（尚未核实）|Original location clues (unverified)
审核依据|Review evidence
证据、地点修正及原因|Evidence, location correction and rationale
保存审核|Save review
导出审核记录|Export reviews
审核保存在本浏览器，未同步到 DIOS；没有从报道推断患者个体或医院能力。|Reviews stay in this browser and are not synced to DIOS. Reports do not establish individual patients or facility capabilities.
地点角色与精度核查|Location roles and precision review
AI初筛结果 · 待人工复核|AI-assisted screening · Human review pending
类别：|Category: 
日期依据：|Date evidence: 
重复组状态：|Duplicate-group status: 
标记：|Flags: 
无额外标记|No additional flags
本机已有审核优先保留；上方AI结果供对照，不会自动替代人工结论。|Existing local reviews take priority. AI results are for comparison and do not replace human conclusions.
原文状态|Source access
原文已读取|Source read
原文不可访问|Source inaccessible
信号用途|Signal use
待分类|Unclassified
项目背景|Program context
历史研究/统计背景|Historical research / statistics
跨区/历史病例或治疗线索|Cross-area / historical case or treatment clues
当地病例报道|Local case report
其他|Other
定位精度|Location precision
发表日期（不是事件发生日；URL日期须另核）|Publication date (not event date; verify URL dates separately)
事件发生地或项目覆盖区|Event location or program coverage
报道提及的医院|Facility mentioned in the report
发布地或出版机构所在地|Publication or publisher location
原文段落依据|Source passage evidence
判断说明|Review rationale
重复事件组（同一事件填写相同名称）|Duplicate event group (same name for the same event)
人工复核状态|Human review status
待人工复核|Human review pending
背景保留|Retain as context
排除|Excluded
需补证据|More evidence needed
病例候选|Case candidate
背景保留、排除、需补证据与病例候选分开记录；修改证据会重置为待人工复核。病例候选还需下方人工确认才能计入事件。|Record context, exclusions, evidence gaps and case candidates separately. Editing evidence resets review status. Candidates require explicit confirmation below before event inclusion.
核实区域|Verified region
核实 LGA|Verified LGA
未确认 / 其他地区|Unconfirmed / other region
未确认到区|LGA unconfirmed
原文包含该地病例证据（项目活动和发布会地点不算）|The source contains local case evidence (not just a program or press-event location)
我已人工复核上述证据，同意纳入区级事件汇总|I reviewed the evidence and approve inclusion in the LGA event summary
保存地点核查|Save location review
精度不足的报道保留原范围，不自动生成坐标。审核仅保存本浏览器，可从本页导出共享。|Reports retain their supported geographic scope. No coordinates are generated. Reviews stay in this browser and can be exported for sharing.
复核状态与证据历史已保存|Review status and evidence history saved
请填写证据、说明与审核人|Provide evidence, rationale and reviewer.
完成复核需要填写人工审核人|A human reviewer is required to complete review.
病例确认需要病例候选状态、原文、区级地点及人工证据|Case confirmation requires candidate status, a readable source, verified LGA and human evidence.
候选终点：|Candidate destination: 
未核实接诊能力与入口通达。|Acceptance capability and entrance access are unverified.
原始登记：|Original registration: 
原始状态：|Original status: 
原始时间戳：|Source timestamp: 
服务能力：未知|Service capability: unknown
来源：|Source: 
格网模型人口：|Modelled grid population: 
距最近二/三级机构直线|Straight-line distance to nearest secondary/tertiary facility
深红：直线超过 10 km；橙色：10 km 内。人口总量不是病例数。|Dark red: over 10 km straight-line; orange: within 10 km. Population is not a case count.
当前路径：|Current route: 
医院：灰绿 Primary / 蓝 Secondary / 紫 Tertiary；橙线为道路路径；灰虚线仅表示接入间隙，未核实可通行。人口点为格网中心；可在左侧开关图层。|Facilities: grey-green Primary / blue Secondary / purple Tertiary. Orange: road route. Grey dashes: unverified access gaps. Population points mark grid centres; toggle layers in the left panel.
2026-11-11 可复核提交版本|2026-11-11 review-ready release
数据配置加载中|Loading data settings
当前候选：|Current candidate: 
关联报道：|Linked article: 
；保存时审核状态：|; review status when saved: 
核查建议：|Assessment: 
当前机构：|Current facility: 
所选医院最近邻人口分配：约|Nearest-facility population allocation: about
2025 年模型人口约|2025 modelled population: about
人；|people;
距任一登记机构直线 5 km 内：|Within 5 km straight-line of any registered facility: 
距二级 / 三级机构直线 5 km 内：|Within 5 km straight-line of secondary/tertiary facilities: 
当前显示|Showing
当前已确认并去重的区级病例事件：|Confirmed, deduplicated LGA case events: 
FCT 级已读取原文的项目背景报道|FCT-wide context reports with readable sources: 
原始导出 1,330 行；按文章 ID 合并为|Original export: 1,330 rows, deduplicated by article ID into
在 FCT 全部更高层级机构中，沿区域有向路网找到|Higher-level candidates reachable on the directed FCT road network: 
起点接入间隙|Origin access gap
固定速度估算|Assumed-speed estimate
医院连接最近道路节点，上限|Facilities snap to the nearest road node within
路网审计：支持转向规则|Road audit — supported turn restrictions:
机构距可行车路网节点|Facility distance to drivable road node:
已保存位置修正|Saved facility corrections:
 · 路径靠近网络边界，需核查| · Route near network boundary; review required
；优先级：|; priority: 
高|High
中|Medium
低|Low
（非实时接诊状态）|(not live acceptance status)
 PDP 记录| PDP record
人。|people.
当前|Current
：查看医院与路由|: view facilities and routes`;
const fragments=`%）；10 km 内|%); within 10 km: 
km / 假设|km / assumed
km；假设行程|km; assumed travel time
· PDP 记录|· PDP record
· 原始行|· source rows
· 相距|· distance
· 道路|· road
。坐标顺序为经度、纬度。|. Coordinates are longitude, latitude.
。点击医院后，可跨 LGA 查找 FCT 更高层级候选。|. Select a facility to find higher-level candidates across FCT LGAs.
个。|.
个。0 表示没有符合纳入条件的记录，不表示没有事件。|. Zero means no qualifying records, not an absence of events.
个候选。按最短道路距离显示前三个。| candidates. The three shortest road distances are shown.
个有效格网。约 1 km 分辨率。|valid grid cells at approximately 1 km resolution.
人|people
人。每格仅归属一家医院；这是空间分配模型，不是实际就诊量。|people. Each cell is assigned once. This is a spatial allocation model, not actual patient volume.
人（|people (
份|plans
分钟 · 终点接入间隙|min · destination access gap
分钟。|min.
家：|facilities: 
条。|records.
条。情绪分类不代表患者紧急程度。|reviews. Sentiment does not represent patient urgency.
条；未支持|; unsupported:
条；阻断障碍节点|; blocked barrier nodes:
篇。国家与行政区仍需逐条核查。原始导出无病例坐标/发表日期；部分报道已由原文补充日期线索，事件发生日仍需区分，不生成患者点位。|articles. Verify country and administrative location individually. The export has no case coordinates or publication dates; some source dates were added during review. Distinguish event dates; no patient points are generated.
篇。国家字段标记 Nigeria 的文章|articles. Articles tagged Nigeria:
篇。结论均待人工复核，导入的新来源可在全部列表查看。|articles. All screening conclusions await human review. Imported sources appear in the full list.
篇（AI 辅助核查，待团队复核）；不下分到 LGA。|articles (AI-assisted, pending team review); no LGA allocation.
篇，受限|readable, inaccessible:
篇；原文可读|articles; readable sources:
篇；审核记录|articles; review records:
米|m
米。灰色虚线为未核实接入段，不计入距离与时间。|m. Grey dashes show unverified access gaps excluded from distance and time.
米。起终点接入间隙单独显示，未计入道路公里数和分钟数。医院入口和接入段可通行性尚未核实。via-way、条件转向规则、未知闸门开放情况、区域截断、道路质量及实时交通仍可能影响结果。|m. Endpoint gaps are shown separately and excluded from road distance and time. Entrances and connecting access are unverified. Via-way and conditional turns, unknown gate access, regional truncation, road quality and live traffic may affect results.
米接入阈值，需要核查位置。|m snap limit; review the location.
米，超过|m, exceeding the
，道路|, road
；原始坐标|; original coordinates
；来源：|; source:
；证据强度：|; evidence strength:
；道路|; road
GRID3 LGA：|GRID3 LGA:
· Ward：|· Ward:
调整经度|Edit longitude
调整纬度|Edit latitude
调整机构名称|Edit facility name
调整登记州|Edit registered state
调整登记LGA|Edit registered LGA
调整来源URL/证据|Edit source URL / evidence
调整审核人|Edit reviewer
调整调整原因|Edit correction rationale
调整机构层级|Edit facility level
未核实|Unverified
请选择文章并填写审核人与依据|Select an article and provide reviewer and evidence.
已保存本机审核|Review saved in this browser
保存失败；请先导出备份|Save failed; export a backup first.
存储失败，请检查浏览器存储设置|Save failed. Check browser storage settings.
先选择有效道路候选；数据变更后需重新计算|Select a valid route. Recalculate after data changes.
关联报道不存在|Linked article does not exist.
经纬度不能为空|Longitude and latitude are required.
已恢复发布版本DIOS数据；已有逐篇审核仍保留|Published DIOS data restored; existing article reviews retained.
已恢复此机构发布版本，其他修改保留|Published facility values restored; other edits retained.
已恢复发布数据源配置|Published data-source settings restored.
配置JSON格式不正确|Invalid settings JSON.
保存失败，请先导出记录或检查浏览器存储空间|Save failed. Export records or check browser storage.
文件超过12MB，请拆分；原始CSV需先按项目脚本整理为JSON|File exceeds 12 MB. Split it; convert raw CSV with the project scripts first.
确认相关|Relevant
拒绝信号|Reject signal
重复事件|Duplicate event
国家或地点冲突|Country or location conflict
保存时审核状态：|Review status when saved:
已发布初筛批次|Published screening batch`;
const dictionary=Object.fromEntries((pairs+'\n'+fragments).split('\n').map(s=>{const [k,v]=s.split('|');return [k.trim(),v]}));
export function chinese(value){const cn={'Facility network':'机构网络','Health facilities':'医疗机构','valid POIs':'个有效机构点','Unverified':'未核实','Type code:':'机构层级：','Agency unknown':'管理机构未知','Location unavailable':'地点缺失','Unknown':'未知','Primary':'一级','Secondary':'二级','Tertiary':'三级','Zoom in':'放大','Zoom out':'缩小'};return typeof value==='string'&&cn[value.trim()]?value.replace(value.trim(),cn[value.trim()]):value}
const templates=[
 ['HDX Nigeria: Health facilities','HDX Nigeria: Health facilities'],
 ['{0} 条已载入记录；当前地区 {1} 条。','{0} records loaded; {1} in the selected state.'],
 ['已应用 {0} 项修改，仅保存本浏览器。请导出交给队友。','Applied {0} edits in this browser. Export to share with teammates.'],
 ['转诊方案记录 · {0} 份','Referral plans · {0}'],
 [' · 审核：{0} · 优先级{1}',' · Review: {0} · Priority: {1}'],
 ];
export function translate(value){
 if(typeof value!=='string')return value;
 const key=value.trim();
 if(Object.hasOwn(dictionary,key))return value.replace(key,dictionary[key]);
 for(const [cn,en] of templates){const pattern=cn.trim().split(/\{\d+\}/).map(s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('(.*?)');const m=key.match(new RegExp('^'+pattern+'$'));if(m)return en.replace(/\{(\d+)\}/g,(_,i)=>translate(m[Number(i)+1]));}
 return value;
}
