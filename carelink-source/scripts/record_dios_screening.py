"""Human-readable AI screening of the fixed 41-record queue; no auto-confirmation."""
import json,re,hashlib
from pathlib import Path
from datetime import datetime,timezone,timedelta
from collections import Counter
R=Path('E:/CASA/hackathon/hanyun-hackathon');C=Path('dios_screen_cache');D=R/'docs'
articles={a['id']:a for a in json.loads((R/'public/data/dios_signals.json').read_text(encoding='utf-8-sig'))};queue=json.loads((C/'queue.json').read_text(encoding='utf8'));checks=json.loads((R/'src/data/dios_location_checks.json').read_text(encoding='utf8'))
pending_ids={a['id'] for a in queue};assert len(pending_ids)==41
findings={}
def add(id,precision,event,facility,publish,category,kind,note,evidence,priority='中',group='',cases=False,flags=(),date='',access='原文已读取'):
 a=articles[id];cache=json.loads((C/(id+'.json')).read_text(encoding='utf8'))
 dates=[m['value'] for m in cache.get('dates',[]) if m.get('name')=='article:published_time']
 timestamp=dates[0] if dates else next((x['datePublished'] for x in cache.get('schemaDates',[]) if 'datePublished' in x),'')
 date_basis=''
 if not date and timestamp:
  try:date=datetime.fromisoformat(timestamp.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=1))).date().isoformat();date_basis='原页 datePublished/article:published_time，转换至 Nigeria UTC+1；不是事件发生日'
  except ValueError:date=''
 if date and not date_basis:date_basis='原页可见日期（网页读取）'
 if not date and access=='原文已读取':
  match=re.search(r'/(20\d\d)/(\d\d)/(\d\d)/',cache.get('finalUrl',''))
  if match:date='-'.join(match.groups());date_basis='仅 URL 日期线索；原页未取得绝对发表日期，待人工核实'
  elif cache.get('times') and re.fullmatch(r'\d{4}-\d{2}-\d{2}',cache['times'][0]):date=cache['times'][0];date_basis='原页文章 time 日期；不是事件发生日'
 findings[id]={'articleId':id,'title':a['title'],'url':a['url'],'verifiedSourceUrl':cache.get('finalUrl') or a['url'],'sourceVerification':access,'sourceAccessMethod':'原站 HTTP 正文' if access=='原文已读取' else '原站访问检查','screeningStatus':'AI初筛完成，待人工复核' if access=='原文已读取' else '访问检查完成，需补原文后复核','reviewedAt':'2026-11-11','reviewer':'AI辅助原文初筛，待团队复核','humanConfirmed':False,'humanReviewStatus':'待人工复核','humanReviewer':'','humanDecision':'','humanNotes':'','precision':precision,'eventPlace':event,'mentionedFacility':facility,'publisherPlace':publish,'date':date,'publicationTimestamp':timestamp,'dateEvidence':date_basis or '未取得可靠发表日期，不从导出时间推断','eventDate':None,'signalKind':kind,'screeningCategory':category,'screeningProposal':note,'note':note,'evidence':evidence,'reviewPriority':priority,'duplicateGroup':group,'duplicateStatus':'AI疑似同稿/同事件，待人工确认' if group else '未识别到明确重复组，不代表无重复','containsCaseNarrative':cases,'localCaseEvidence':False,'regionCode':'','verifiedLga':'','coordinates':None,'flags':list(flags),'originalLocationClues':a['locations'],'sourceAccessAudit':{'httpStatus':cache.get('status'),'attempts':cache.get('attempts',[]),'error':cache.get('error',''),'responseSha256':cache.get('contentSha256','')}}
P='全国政策/项目背景';F='FCT项目/机构线索';S='历史研究/统计背景';O='外地区病例/治疗线索';N='非目标个案/综合评论';U='原文受限'
add('0d4099a913fb1dae','国家','Nigeria；Abuja 为食品援助启动地，另述多州项目','','媒体办公地未核实',P,'program-context','保留全国倡议背景；Abuja 食品活动不能定位孕产妇病例。','正文食品项目启动、各州妇女扶持和助产人员装备段落。')
add('1c196d20de0520c3','国家','Nigeria；物资发放启动仪式在 Abuja','','发布办公地未核实；正文 Abuja 是仪式地点',P,'program-context','全国孕产/新生儿物资计划；不能把全国受益或物资数量分配给 FCT。','正文开头 nationwide、Abuja 启动仪式与 MAMII 说明段落。')
add('250d562525d0d311','国家','Nigeria；eCRVS 发布在 State House, Abuja','','发布办公地未核实',P,'program-context','国家人口登记系统发布；与 The Sun 同一发布活动，孕产妇死亡数字为全国背景。','正文 State House 发布、数字登记系统及孕产妇死亡可报告性的段落。',group='ECRVS-STATE-HOUSE-2023-11-08')
add('2b39a703e1bda28e','州/FCT','FCT 2016–2019 历史研究；其余讨论为 Nigeria 全国','','作者署名 Abuja；不等于病例发生地',S,'research-context','保留历史研究背景；与 THISDAY 的同作者文章高度相似，不能当新病例事件。','正文 Centre for Social Justice、FCT 2016–2019 预算研究及文末作者署名。',group='CSJ-SGBV-SRHR-COMMENTARY-2021',flags=['historical-study','possible-republication'])
add('2c2bc25ad16d03dd','国家','Nigeria；涉及多州及 FCT 培训覆盖','','原文未核实独立出版地点',P,'program-context','全国卫生系统评论；FCT 是培训覆盖之一，未报告 FCT 区级病例。','原页 2025-09-30 标题下正文：全国医疗改革、24州及FCT培训、卫生融资评论。',date='2025-09-30')
add('2eedfe6e3aed576b','国家','Nigeria；Fistula-Free Programme 启动在卫生部 Abuja 会议室','','媒体办公地未核实',P,'program-context','全国瘘治疗保障项目；Abuja 为启动地点，不能视为当地病例发生地。','正文开头 Ministry conference room、项目资金和全国实施机制段落。')
add('32babba56f4ea47e','国家','Nigeria；NHIA 采访在 Abuja','','NAN 采访地点 Abuja；媒体办公地未核实',P,'program-context','全国急救支付政策；与 Quick News 2026-03-13 的 NAN 采访为疑似同稿。','正文 Ohiri 接受 NAN 采访、免预付、报销和近四万受益者说明。',group='NAN-NHIA-OHIRI-2026-03-13')
add('46d329446af0d4d3','州/FCT','FCT 的 SGBV 历史统计；另含多州童婚研究','','媒体办公地未核实',S,'research-context','FCT 105 起为2020年一段时期的性别暴力统计，不是孕产死亡或产科瘘新发病例。','正文 FCT 段明确报告 2020-03-23 至 2020-05-29 的 SGBV 统计；并列多州童婚数据。',priority='高',flags=['historical-statistic','non-target-case-type'])
add('4e527528bcb18718','国家','Nigeria；引文研究在 Lagos/Abuja，开篇情景在 Borno','','原页来源署名 Nigeria Health Watch (Abuja)；不是病例地',S,'research-context','AllAfrica 与 Nigeria Health Watch 同稿；研究抽样地、媒体署名和开篇叙事不能转换为 FCT 孕产病例。','AllAfrica 可读正文与原发布方全文一致：Borno 开篇、Lagos/Abuja 研究、FCT 女医生比例。',group='NHW-WOMENS-HEALTH-2025-05-28',date='2025-05-28',flags=['publication-date-conflict','possible-republication'])
add('509680b01efc2db9','国家','Nigeria 多州及 Abuja 洪灾；暴力地点 Bama/Banki, Borno','','媒体办公地未核实',P,'program-context','保留人道需求背景；总死亡、孕妇估计和服务量均非 FCT 分区病例。','正文第1–4段的洪灾范围、Borno 暴力地点及全国受影响人口。',flags=['aggregate-not-local-cases'])
add('516b336b6aea55ff','州/FCT','Wassa IDP camp, Abuja 为项目地点；Yar’Adua Centre, Abuja 为会议地点','','媒体办公地未核实',F,'program-context','有明确营地与会议地点，可作服务背景；不能根据 Wassa 名称推断 LGA 或病例坐标。','正文 Wassa 营地 WELEAD 项目及 Yar’Adua Centre 会议段落。',flags=['lga-not-confirmed','venue-vs-service-area'])
add('51799f62bbf8c21c','国家','Nigeria；项目发布在 Abuja，历史瘘幸存者叙述涉及 Kano','','媒体办公地未核实',O,'case-context','有 Kano 相关历史患者叙述；年龄及病程表述存在不一致，不能当 FCT 病例或当前新发病例。','正文 Abuja rollout 和受访者讲述 Kano 长期瘘病史的段落；全国新病例估计没有区级分配。',priority='高',cases=True,flags=['non-FCT-case-narrative','inconsistent-age-duration','historical-not-new-case'])
add('54d3178c91a28b2e','国家','Nigeria；卫生政策论坛在 Abuja','','媒体办公地未核实',P,'program-context','仅按主文章识别全国卫生政策。页面后续 Lagos 培训等为推荐文章，须排除。','主标题对应正文第1段介绍 Abuja 论坛及五份政策文件；后续内容跨越其他文章标题。',flags=['related-content-excluded'])
add('56e80782a77392ec','州/FCT','FCT 五个 Area Council 的项目范围；点名 Kwali、Abaji','','媒体办公地未核实',F,'program-context','可保留 Kwali/Abaji 项目线索与传统接生员培训背景；没有对应孕产死亡/瘘病例数或地址。','正文 MATAI 项目57社区、Kwali/Abaji儿童权利委员会和57名传统接生员培训段落。',flags=['program-area-not-case-area'])
add('5a7d6774104dcef8','国家','Nigeria 访问行程；Abuja 医疗机构访问，另涉及 Benin','UN Severe Acute Respiratory Isolation and Treatment Centre, Abuja','媒体办公地未核实',P,'program-context','属于访问安排及倡议；Nairobi 是既往峰会背景，SARI 机构提及不验证产科能力。','正文访问行程、Abuja SARI 机构、Benin 活动和2019 Nairobi峰会回顾。',flags=['facility-mention-not-capability'])
add('5b283035469d4eee','国家','Nigeria；2025 Safe Motherhood Day 媒体活动在 Abuja','','媒体办公地未核实',P,'program-context','4000名受益者是全国项目累计，不能定位至 Abuja 或拆成病例事件。','正文全国免费剖宫产累计、Abuja媒体会议与瘘项目扩展段落。',flags=['national-cumulative-service-count'])
add('5f41501a6ab60070','国家','Nigeria；融资圆桌会在 Abuja','','媒体办公地未核实',P,'program-context','保留国家融资与转诊障碍背景；文中多个死亡率/年度估计口径不同，不用作当地病例数。','正文 Abuja roundtable、融资缺口及全国PHC/孕产服务统计。',flags=['national-finance-context','mixed-statistical-definitions'])
add('6ed97f2d63a92f81','州/FCT','Ebonyi；治疗/培训在 Abakaliki，患者发病居住地未知','National Obstetric Fistula Centre, Abakaliki；Evangel VVF Centre 为受访者任职机构','受访卫生部人员来自 Abuja；不是治疗发生地',O,'case-context','这是 Ebonyi 治疗及培训线索。20余例为计划修复，不是已完成数量；FCT 只在项目覆盖/卫生部人员来源中出现。','正文开头计划修复、Abakaliki培训场所，以及末段五州项目覆盖但培训试点在Ebonyi/Bauchi。',priority='高',cases=True,flags=['non-FCT-treatment-location','planned-not-completed','onset-location-unknown'])
add('717342a436f1213e','国家','多州：Kwara、Niger/Minna、Gombe；Abuja 为机构服务覆盖之一','National Obstetric Fistula Centre（此文未明确具体院区）','媒体办公地未核实',O,'case-context','多地治疗成果与幸存者叙事。Kwara71人、Minna累计手术、Gombe50人等不同口径不能合成FCT病例。','正文各州治疗/康复段、BFFWH在Kaduna/Abuja/Zamfara服务覆盖段。',priority='高',cases=True,flags=['multistate-treatment-statistics','not-new-incidence'])
add('7236a87f36233675','国家','Nigeria 北部19州及FCT相关机构；开篇分娩叙述在 Yobe','University of Abuja Teaching Hospital, Gwagwalada；FMC Jabi；VVF Center, Gwarinpa Hospital（报道提及）','作者署名 Damaturu, Yobe；不是所有病例发生地',F,'program-context','可记录报道中提及的机构及项目类型，不能据评论更新医院实时服务/接诊能力；FCT没有独立病例统计。','正文受益医院清单、Gwarinpa VVF清单、Yobe分娩开篇和作者署名。',priority='高',cases=True,flags=['facility-capability-unverified','commentary','non-FCT-anecdote'])
add('77f2a4d6614581a1','国家','Nigeria；Lagos/Abuja 是慢病研究样本地，Borno 是开篇情景','','媒体独立办公地未核实',S,'research-context','保留全国妇女健康及研究背景；与 AllAfrica 同稿，不能把研究样本或情景化开篇当FCT产科病例。','原发布方正文研究参与者地域、全国健康指标和开篇Borno情景；AllAfrica明确链接该原稿。',group='NHW-WOMENS-HEALTH-2025-05-28',flags=['possible-republication','study-not-obstetric-case'])
add('7f2f5294cf94526b','国家','Nigeria多地法律服务；文中孕妇枪击事件在 Ajah, Lagos','TAMAR Sexual Assault Referral Centre（未在此文确认院址）','媒体办公地未核实；Abuja也出现在机构办公室清单中',N,'other','孕妇死亡叙述涉及 Lagos 暴力事件，不属于此转诊模型的产科并发症事件；FCT为办公室/司法辖区等角色。','正文WACOL办公室清单、法律诊所统计、Ajah警方枪击孕妇的问题段落。',priority='高',cases=True,flags=['non-FCT-death-narrative','non-obstetric-cause','office-not-case-location'])
add('84d1a308e4508bcc','州/FCT','全国SRH背景；叙事仅称学校位于 Abuja 郊区，袭击地点不明确','Marie Stopes Nigeria 为受访机构；未定位治疗医院','媒体办公地未核实',N,'other','未成年人受害及妊娠叙事需谨慎：学校在FCT不证明袭击/病例发生在FCT；无LGA或目标瘘/孕产死亡事件。','原页开头奖学金学校地点与随后受害妊娠叙述分开；后续为全国SRH政策访谈。',priority='高',cases=True,flags=['school-not-case-location','minor-no-identifying-location','target-case-not-established'],date='2021-12-23')
add('8687d85b1fc44ff5','国家','Nigeria；Abuja 是海外招聘活动地点之一','','媒体办公地未核实',P,'program-context','全国医护外流评论；Abuja招聘活动不能作当地病例或医院人手实测。','正文医护流出、Lagos/Abuja招聘及全国设施/人力评论。',flags=['commentary-not-live-capacity'])
add('8894d52db951bf21','国家','Nigeria；NAN采访在 Abuja','','NAN新闻电头Abuja；媒体办公地未核实',P,'program-context','与 Premium Times 同一 NHIA 采访及政策内容；按同稿候选处理，不能重复计服务人数。','正文电头2026-03-13、Ohiri/NAN采访、免预付与报销政策段落。',group='NAN-NHIA-OHIRI-2026-03-13')
add('8df5b01cab2a5db4','国家','Nigeria 12州及FCT调查覆盖；发布声明在 Abuja','','声明发布地Abuja；媒体办公地未核实',S,'research-context','文章宣布调查启动，不是调查结果，更不含FCT区级瘘病例数。正文45天与起止日期并不一致，需复核。','正文列12州及FCT、调查目的，写明2021-08-11至09-14并称45天。',priority='高',flags=['survey-announcement-not-results','duration-date-inconsistency'])
add('8f1da50b6c8a8c9d','国家','Nigeria；FCT为多地SGBV概述之一，Abuja为大学任职/声明地点','University of Abuja为受访者任职机构，非转诊医院','卫生部声明署名Abuja；媒体办公地未核实',P,'program-context','职业培训倡议与全国风险概述；不能把大学地址、声明地和未分区SGBV描述转成产科病例。','正文University of Abuja受访者、UNICEF列举多州/FCT及声明来源段落。',flags=['affiliation-not-case-location'])
add('8f76427ad3a1fe7f','国家','Nigeria；Lagos/FCT/Ogun为封控/救助范围，另述西北四州研究','','媒体办公地未核实',N,'other','保留社会保障背景，非产科病例报道；FCT是封控和救助政策范围。','正文封控地区救助、养老金覆盖和残疾人社会保障研究段落。')
add('a344e6e48b338021','待核查','','','未取得原文，不能核实',U,'pending','原站403，网页读取亦失败；不依据DIOS摘要确认活动地点、日期或病例。','2026-11-11原始链接访问403；只取得访问拒绝页，无可读正文。',priority='高',access='原文不可访问',flags=['needs-original-text'])
add('ab6c2e3fa9db8510','国家','Nigeria；女性医疗领导力结业活动在 Abuja','','媒体办公地未核实',P,'program-context','29名是领导力项目学员，不是患者；Abuja是活动地点，孕产死亡率只是国家背景。','正文2025 Leadership Journey结业、Abuja Lift-Off活动和国家健康背景段落。')
add('c0b527c864b8f147','国家','Nigeria；NHSRII联合走访方案采访在 Abuja','','NAN新闻电头Abuja；媒体办公地未核实',P,'program-context','可作转诊协同背景；没有具体FCT病例起点、目的医院或接收记录。','正文2026-03-26 NAN采访、joint missions与referral facilities协调方案。')
add('c3fcdcb521acc0ae','国家','Nigeria；Lagos/Abuja等为医生分布城市，另述多州短缺','','媒体办公地未核实',P,'program-context','全国专业人员短缺报道，不能把Abuja医生集中等同FCT各医院实时能力；不同历史统计口径需核对。','正文医生数量、Lagos/Abuja集中及各州人力对比；不是逐院人员清单。',flags=['distribution-not-cases','statistics-not-validated'])
add('c42df9f3481ed4d6','国家','Nigeria；报告发布在 State House, Abuja','','媒体办公地未核实',P,'program-context','与既有20,000标题记录为同发布活动候选；2000脱离童婚与20000留校是不同指标，不能互换。','正文开头20000留校、State House发布及后续不同项目指标；与既有同日THISDAY记录对照。',priority='高',group='UNFPA-LANDSCAPE-LAUNCH-2022-09-08',flags=['headline-number-different-measures'])
add('caa433cb2a394304','州/FCT','Nigeria全国改革；FCT Karmo PHC 为服务体验举例','Karmo Primary Healthcare Centre, FCT','NAN采访在Abuja；媒体办公地未核实',F,'program-context','可作为Karmo机构报道线索，但新闻中满意度/产检增长不能验证临床能力或接诊状态；病例发生地址未知。','正文第17–18段Karmo PHC与孕产服务体验举例，前文为全国改革采访。',priority='高',flags=['facility-identity-not-crossmatched','not-live-capability'])
add('d5b76079c207ee58','国家','Nigeria及全球；Lagos/Abuja/Port Harcourt为城市增长例子','','媒体办公地未核实',N,'other','人口与青年赋权评论；Abuja仅为城市基础设施例子，无产科病例位置。','正文World Population Day、国家人口趋势及城市基础设施讨论。')
add('d80a2643f2d33cf9','国家','Nigeria；急救政策媒体活动在 Abuja','','媒体办公地未核实',P,'program-context','当前主文章未找到DIOS摘要所说孕妇/婴儿因道路问题死亡的依据；标记摘要不一致，不生成病例。','主文从国家急救系统发布至Health-in-Media Charter结尾均为政策说明；之后页面已进入其他新闻。',priority='高',flags=['export-summary-not-supported-by-readable-body','related-content-excluded'])
add('da1da5c65c192fd4','国家','Nigeria；FCT出现在儿童权利法适用范围中','','媒体办公地未核实',N,'other','选举与童婚法律评论；国际/全国风险陈述不代表FCT当地病例。','正文议会提案、25州及FCT法律范围和全球青少年妊娠风险段落。')
add('e44474110ea91955','LGA','Cross River / Obanliku 为历史社会背景；孕产死亡个案具体发生地未知','Kubwa医院仅见于文末另一非产科追思段落，未命名','Abuja为研讨活动/机构办公地等；不等于母亲死亡地',O,'case-context','有历史产时死亡转述，但发生时间及具体地点不明；Obanliku是习俗报道范围，不自动给个案定位。Kubwa是另一人就医故事。','正文Becheve/Obanliku背景、债务用于母亲产时死亡后费用的历史转述，以及文末Kubwa追思段落。',priority='高',cases=True,flags=['historical-case-no-date','case-location-not-established','multiple-unrelated-sections'])
add('f1b072a29a0f5158','州/FCT','FCT 2016–2019 历史研究；其余为Nigeria全国','','作者署名Centre for Social Justice, Abuja；非病例地址',S,'research-context','与Punch同作者同研究/论述疑似转载，保留为历史研究背景，不作新事件重复统计。','正文FCT 2016–2019预算研究与文末作者/机构署名；与Punch篇逐项对照。',group='CSJ-SGBV-SRHR-COMMENTARY-2021',flags=['historical-study','possible-republication'])
add('f1e4ca13adbd4364','国家','Nigeria；eCRVS启动在 State House, Abuja','','记者新闻电头Abuja；媒体办公地未核实',P,'program-context','与THISDAY人口登记系统报道为同一发布活动；全国孕产妇死亡统计不能归到State House或FCT。','正文首段State House eCRVS发布、人口登记系统和全国死亡可报告性说明。',group='ECRVS-STATE-HOUSE-2023-11-08')
add('fe1c90a10ecd3808','待核查','','','原站TLS失败/机器人验证页，未取得正文',U,'pending','原文仍不可读；不能以World Population Day摘要确认日期、地点或风险事件。','原链接TLS访问失败；同站规范域名路径仅显示机器人验证，未尝试绕过。',priority='高',access='原文不可访问',flags=['needs-original-text'])

assert set(findings)==pending_ids
# Document successful primary-page reads through the web tool, even if HTTP scraping failed.
for id in ('2c2bc25ad16d03dd','4e527528bcb18718','84d1a308e4508bcc'):
 findings[id]['sourceAccessMethod']='原站网页读取（HTTP脚本受限，网页工具取得正文）'
findings['4e527528bcb18718']['dateEvidence']='原页可见日期28 May 2025；HTTP元数据29 May不一致，保留人工核对标记'
findings['e44474110ea91955']['precision']='国家'
findings['e44474110ea91955']['spatialEvidence']=[{'role':'习俗/社会背景范围','place':'Obanliku, Cross River','precision':'LGA'},{'role':'历史孕产死亡发生地','place':'未确认','precision':'待核查'},{'role':'另一非产科就医叙述','place':'Kubwa','precision':'州/FCT'}]
findings['516b336b6aea55ff']['spatialEvidence']=[{'role':'项目服务地点','place':'Wassa IDP camp, Abuja','precision':'州/FCT'},{'role':'会议地点','place':'Yar’Adua Centre, Abuja','precision':'州/FCT'}]
for k,v in findings.items():checks[k]=v
# Same-event relation links back to a previously reviewed record without changing its evidence.
checks['3dc9fa268bed6cf5']['duplicateGroup']='UNFPA-LANDSCAPE-LAUNCH-2022-09-08'
checks['3dc9fa268bed6cf5']['duplicateStatus']='AI疑似同发布活动，待人工确认；2000脱离童婚/20000留校为不同指标'
for v in checks.values():
 v.setdefault('humanConfirmed',False);v.setdefault('humanReviewStatus','待人工复核')
assert len(checks)==50 and not any(v.get('humanConfirmed') for v in checks.values())
(R/'src/data/dios_location_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
screen_status=Counter(v['sourceVerification'] for v in findings.values());all_status=Counter(v['sourceVerification'] for v in checks.values());cats=Counter(v['screeningCategory'] for v in findings.values())
groups={g:[k for k,v in checks.items() if v.get('duplicateGroup')==g] for g in sorted({v['duplicateGroup'] for v in findings.values() if v['duplicateGroup']})}
summary={'updatedAt':'2026-11-11','newBatchSize':41,'newBatchStatusCounts':dict(screen_status),'allCandidateCount':50,'allStatusCounts':dict(all_status),'newBatchCategoryCounts':dict(cats),'newBatchHighPriority':sum(v['reviewPriority']=='高' for v in findings.values()),'duplicateCandidateGroups':groups,'humanConfirmedLocalCases':0,'humanReviewRequired':True,'scope':'FCT位置核查候选50篇；不是全部Nigeria 262篇，也不是DIOS550篇全量筛查','unresolvedArticleIds':[k for k,v in findings.items() if v['sourceVerification']!='原文已读取']}
(D/'DIOS_41篇初筛结果.json').write_text(json.dumps({'summary':summary,'articles':list(findings.values())},ensure_ascii=False,indent=2),encoding='utf8')
(D/'地点核查进度.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')

header='''# DIOS 剩余41篇初筛与人工复核表

更新：2026-11-11。范围仅为现有 FCT 地点候选队列中此前待核查的41篇，不是Nigeria全部262篇或DIOS全部550篇。

本批逐条完成访问及地点角色初筛：**39篇取得可读原文，2篇仍受限**。加上此前8篇已读取和1篇受限，50篇候选当前为47篇已读取、3篇受限。这里“已读取”只说明取得并检查了可访问正文，不表示报道事实或医院能力已被独立证实。

**所有结论均待人工复核，没有自动确认病例，没有添加患者坐标。** 2篇受限记录完成了访问检查，但正文筛查仍需补原文；不能称为全部41篇正文都核实完毕。

## 如何人工复核

先看下方“高”优先级及重复组。点击原文，确认：事件发生地是否真的成立；是否只是发布会/学校/医院/办公室；是否为孕产死亡或产科瘘的病例信息；发表日期和事件日期是否区分；同一事件是否重复报道。每条勾选复核结论并填写审核人、时间及依据。也可在网页逐篇保存后导出JSON。

本次未把新闻治疗机构名单写入HDX临床能力字段，未将累计治疗量当新发病例，未将FCT级范围下分至LGA。原始DIOS摘要和位置字段保留不改。

## 需要先看清的结果

- **外地与历史叙事：** Ebonyi/Abakaliki的培训治疗计划、Kwara/Minna/Gombe的治疗成果、Kano的历史瘘叙述不能当FCT病例。Cross River/Obanliku仅明确到社会背景范围，历史母亲死亡的具体地点和日期仍不明确。
- **学校不是事件地：** The Nation报道只说奖学金学校在Abuja郊区，不能据此定位未成年人遭袭或妊娠发生地。不保存个人可识别病例位置。
- **相关但非目标病例：** FCT历史SGBV统计、Lagos暴力致孕妇死亡与本模型的产科并发症事件不同，不自动纳入。
- **摘要与原文不一致：** The Tide急救系统报道的当前主文中，未找到导出摘要所称“孕妇/婴儿因道路死亡”的依据。推荐新闻、广告、页脚与主文分开。
- **疑似重复：** 同作者SRHR评论、NHIA/NAN采访、eCRVS发布活动、UNFPA报告发布、NHW/AllAfrica转载共5组候选。组内“同稿”和“同一活动”性质不同，仍需人工确认，未按相同主题任意合并。
- **日期：** 优先使用原页发表元数据或可见日期；只有URL日期的记录明确标为日期线索。Nigeria时区按UTC+1展示；修改时间、网页当前日期和导出时间不作发表日期。AllAfrica可见日期与元数据有冲突，已单独标记。

## 逐篇复核
'''
lines=[header]
for number,a in enumerate(queue,1):
 v=findings[a['id']]
 lines += [f"\n### {number:02d}．{v['title']}\n",f"- 文章ID：`{v['articleId']}`；[原文]({v['url']})；优先级：**{v['reviewPriority']}**。",f"- 访问：{v['sourceVerification']}；{v['sourceAccessMethod']}。",f"- 发表日期：{v['date'] or '未知'}。依据：{v['dateEvidence']}。事件日期：未确认，不与发表日混用。",f"- 初筛类别：{v['screeningCategory']}；定位精度：{v['precision']}。",f"- 事件/服务范围：{v['eventPlace'] or '未核实'}。",f"- 医院/机构提及：{v['mentionedFacility'] or '未核实具体机构'}。",f"- 发布地角色：{v['publisherPlace']}。",f"- 原文依据（转述）：{v['evidence']}",f"- 建议：{v['screeningProposal']}",f"- 重复组：{v['duplicateGroup'] or '未识别'}；{v['duplicateStatus']}。",f"- 额外核查标记：{', '.join(v['flags']) or '无额外标记'}。",'- [ ] 已打开原文并核对上述地点/日期/主题。','- [ ] 同意初筛建议；或在下方记录修正。','- 人工审核人 / 时间 / 结论 / 修正依据：________________。']
lines += ['\n## 方法、记录与限制\n','固定读取此前41条队列，未换成更容易访问的其他报道。用requests与BeautifulSoup提取原站正文/发表元数据，去除导航、推荐区等，移除无效HTML嵌套导致的重复段落，再由AI逐篇判断地点角色、主题相关性、时间和重复线索。3个原站页面通过网页读取取得正文，保留HTTP脚本失败状态；不绕过登录、验证码或安全拦截。没有从摘要反推证据。','可机器读取的记录见 DIOS_41篇初筛结果.json；人工填写使用本表各条目下的复核栏，或在网页保存后导出JSON。原页访问状态、重定向与响应哈希保存在JSON。39个可读原文的地点/关键证据已初筛；完整新闻事实、统计来源、患者发病地址与医院能力仍需团队复核。','抓取正文的本地研究缓存保存在 CASA/hackathon/data/dios_review_cache，不放进网页或公开GitHub；共享复核表仅含链接与简短转述。原始DIOS导出不改写。本轮不新增ZIP、不上传GitHub。']
(D/'DIOS_41篇初筛与人工复核.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
