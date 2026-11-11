> 当前提交候选版已加入运行时数据配置、DIOS与医院位置调整、团队JSON共享和旧路由失效保护。详见 [使用说明](docs/提交候选版_使用与数据调整.md)。医院原始点未自动移动。

# CareLink · Nigeria FCT 联合分析

本地源代码位于 CASA/hackathon/hanyun-hackathon。医院入口 `/?view=hospitals`，DIOS 入口 `/?view=signals`；默认同页显示。2026-11-11 更新详见 [实施与方法记录](docs/456实施与方法记录.md)，以及 [队友评价转诊](docs/队友部分_评价转诊.md)、[我的 DIOS 信号](docs/我的部分_DIOS信号.md)。

安装 Node.js 22.12+，仓库目录执行 `npm ci`、`npm run dev`。生产构建执行 `npm run build -- --base=/carelink/`；`npm run preview` 后访问 `/carelink/`。底图需要联网，数据静态随网页提供。GitHub Pages 现有地址保留，本次完成状态以本地文件及验证记录为准，不把本地构建当作已经线上同步。

FCT 支持 6 个 LGA 的坐标核实筛选、上转候选/道路距离、WorldPop 格网及人口空间邻近覆盖、PDP 历史背景和 DIOS 原文审核。其他州当前浏览机构，不提供同等路网覆盖。原始机构全国 46,146 条，FCT 576 条；4 条坐标落在 FCT 外单独核查。

DIOS：550 篇去重文章，Nigeria 字段 262 篇。位置核查队列 50 篇，其中 47 篇已取得可读原文、3 篇原文受限，均待人工复核；已读取的均为 AI 辅助核查，待团队复核。当前没有合格的区级病例事件。审核存个人浏览器，可导出 JSON。项目背景、发布会和医院提及不能直接当作病例发生位置。

人口是 WorldPop 2025 模型人数，按唯一格网计算直线 5/10km 邻近覆盖，不能当作道路时间覆盖、孕产妇或患者人数。道路时间采用明确速度假设；条件转向、真实医院入口、交通和临床接诊能力仍未知。最新可支持道路规则及审计见实施记录。

src 为源代码，public/data 为网页数据，docs 为方法与来源，scripts 为可复现计算/校验。全国 PBF、PDP 5.8GB 原始文件和 WorldPop 全国栅格保存在 CASA/hackathon/data。API 图层按需查询，无需下载全量；不新增 ZIP。来源、许可证及哈希见 DATA_PROVENANCE.md、worldpop_summary.json、routing_audit.json。旧 Nairobi 文件未被活动网页导入。


2026-11-11：此前剩余41篇已完成初筛（39篇可读、2篇受限），详见 [DIOS逐篇人工复核表](docs/DIOS_41篇初筛与人工复核.md)。优先查看14篇高优先级及5组重复候选。


## 从此GitHub仓库恢复开发目录

在carelink-source目录创建public，复制 ../docs/carelink/config.json 到public/config.json，并将 ../docs/carelink/data 整个目录复制到public/data。然后npm ci、npm run dev。源数据以gzip提供，网页运行时解压；离线重算脚本需要普通JSON时，先解压对应文件（尤其nigeria_facilities_clean.json.gz和fct_wards.geojson.gz）。全国PBF和PDP原始大文件仍在CASA，未上传。
