# 在线数据服务与使用口径

## GRID3 Ward v3.0
条目 https://www.arcgis.com/home/item.html?id=45cd2ef592094d12aca43113a90a6054
图层 https://services3.arcgis.com/BU6Aadhn6tbBEdyk/arcgis/rest/services/GRID3_NGA_operational_wards_v3_0/FeatureServer/0
查询在图层地址后加 /query，参数 f=geojson，where=state='FCT, Abuja'，outFields=*，outSR=4326。请求参数应 URL 编码。FCT 返回 62 个多边形。关注 state、lga、ward、OBJECTID、date、source。工作边界不是最终权威行政区。CIESIN/Columbia University 2026，CC BY-SA 4.0。fct_admin_checks.json 为派生结果，同样标注该许可。

## GeoPortal Existing Health Care Facilities
服务 https://services3.arcgis.com/BU6Aadhn6tbBEdyk/arcgis/rest/services/Nigeria_Existing_Health_Care_Facilities/FeatureServer
先查询 ?f=json 获取 layer ID，再查询 /ID/query。使用 f=geojson、where=1=1、geometry=6.5,8.1,8.0,9.6、geometryType=esriGeometryEnvelope、inSR=4326、outSR=4326、outFields=*。此次返回 181 个范围内候选。字段 facility、states、lgas、Wards。数据覆盖可能不完整，名称相似候选不是已确认同一机构。下载再利用前检查服务最新许可信息。

## HDX
组委会入口 https://data.humdata.org/dataset/nigeria-health-facilities 。原始 CSV 不含坐标，使用同来源 NigeriaHealthFacilities.json。来源元数据包含在 public/data/sources/hdx-metadata.json。

## Geofabrik
下载 https://download.geofabrik.de/africa/nigeria-latest.osm.pbf 。原始文件在 E:/CASA/hackathon/data/nigeria-routing.osm.pbf。路由结果含 SHA256。道路数据 © OpenStreetMap contributors，ODbL。网页在 data/fct_routes.json.gz 加载预计算结果，解压后使用。

## PDP
组委会文件 https://drive.google.com/file/d/1h7jYKhDB6A4f-hwv6wfTH2VeOJ-KxHei/view 。PDP 原始 CSV 5,776,304,917 字节，位置 E:/CASA/hackathon/data/pv_all_data_export.csv。18 条 FCT 相关指标已提取，无需随交接包发送原始大表。

## DIOS
入口 https://unfpa-looker-web-app-126183358624.us-east1.run.app/dashboard 。原始导出在 public/data/sources/dios。文章原文使用各记录 url 在线读取。没有本地缓存整篇新闻。


## WorldPop 2025

官方目录：https://hub.worldpop.org/geodata/listing?id=136 。本次使用官方1km、constrained、UN-adjusted、R2025A v1全国GeoTIFF，并裁剪FCT用于静态网页，未调用在线人口分析API。详见456实施与方法记录。
