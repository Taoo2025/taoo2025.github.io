"""WorldPop 2025 cell-centre accounting, not a clinical demand model."""
import sys,json,hashlib,argparse
from pathlib import Path
sys.path.insert(0,str(Path('.route-deps').resolve()))
import rasterio
from rasterio.mask import mask
import numpy as np
from shapely.geometry import shape,Point,mapping
from shapely.ops import unary_union
from scipy.spatial import cKDTree
from pyproj import Transformer
p=argparse.ArgumentParser();p.add_argument('--root',default='E:/CASA/hackathon/hanyun-hackathon');p.add_argument('--raster',default='worldpop_nga_2025.tif');a=p.parse_args()
root=Path(a.root);data=root/'public/data';source=Path(a.raster)
features=json.loads((data/'fct_lgas.geojson').read_text(encoding='utf-8'))['features'];regions=sorted([(f['properties']['lga'],shape(f['geometry'])) for f in features]);boundary=unary_union([g for n,g in regions])
allf=json.loads((data/'nigeria_facilities_clean.json').read_text(encoding='utf-8-sig'));checks=json.loads((data/'fct_admin_checks.json').read_text(encoding='utf-8'))['hospitals']
# Restrict institutions to one verified polygon membership; retain disagreement flags.
facilities=[f for f in allf if f['division']=='Fct' and len(checks[f['id']]['matches'])==1]
higher=[f for f in facilities if f['facilityTypeCode'] in ('Secondary','Tertiary')]
transform=Transformer.from_crs(4326,32632,always_xy=True)
def project(coords):return np.array(transform.transform(*np.array(coords).T)).T
trees=[cKDTree(project([f['coordinates'] for f in group])) for group in (facilities,higher)]
with rasterio.open(source) as src:
    array,affine=mask(src,[mapping(boundary)],crop=True,all_touched=False,filled=True)
    values=array[0];nodata=src.nodata
    profile=src.profile.copy();profile.update(height=values.shape[0],width=values.shape[1],transform=affine,compress='lzw')
    with rasterio.open(data/'worldpop_fct_2025.tif','w',**profile) as dst:dst.write(array)
    valid=np.argwhere((values!=nodata)&np.isfinite(values)&(values>=0))
cells=[];ties=0
for row,col in valid:
    x,y=rasterio.transform.xy(affine,int(row),int(col));pt=Point(x,y);matches=[name for name,g in regions if g.covers(pt)]
    if not matches:continue
    if len(matches)>1:ties+=1
    pop=float(values[row,col]);cells.append({'id':f'{row}:{col}','x':round(x,7),'y':round(y,7),'lga':matches[0],'population':round(pop,6)})
xy=project([(c['x'],c['y']) for c in cells])
for tree,group,prefix in zip(trees,(facilities,higher),('all','higher')):
    distances,indices=tree.query(xy)
    for cell,distance,i in zip(cells,distances,indices):cell[prefix+'Km']=round(float(distance)/1000,6);cell[prefix+'FacilityId']=group[int(i)]['id']
def summarize(rows):
    total=sum(c['population'] for c in rows)
    return {'population':round(total,3),'cells':len(rows),**{f'{kind}Within{km}km':round(sum(c['population'] for c in rows if c[kind+'Km']<=km),3) for kind in ('all','higher') for km in (5,10)}}
catchments={}
for cell in cells:
    fid=cell['allFacilityId'];catchments[fid]=catchments.get(fid,0)+cell['population']
summary={'source':'https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/NGA/v1/1km_ua/constrained/nga_pop_2025_CN_1km_R2025A_UA_v1.tif','catalog':'https://hub.worldpop.org/geodata/listing?id=136','year':2025,'release':'WorldPop Global2 R2025A v1, constrained, UN-adjusted','unit':'estimated persons per cell','resolution':'30 arc seconds (~1km at equator)','license':'CC BY 4.0; WorldPop, University of Southampton','rasterSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Cell-centre membership; each valid cell allocated once. Nearest in-FCT mapped facility using EPSG:32632 planar distance. Unique population within 5/10km of any facility and any Secondary/Tertiary facility. Not road travel-time coverage.','eligibleFacilities':len(facilities),'eligibleHigherFacilities':len(higher),'excludedFacilities':576-len(facilities),'boundaryTieCells':ties,'overall':summarize(cells),'lgas':{name:summarize([c for c in cells if c['lga']==name]) for name,g in regions},'facilityCatchments':{k:round(v,3) for k,v in catchments.items()},'limitations':['Total population estimate, not pregnant women, cases or demand','Boundary cell centre assignment, not fractional area weighting','NoData excluded; zero cells retained; floating population retained until display','2025 population, historical facility registry and 2026 operational boundaries differ in vintage','Nearest facility does not establish medical capability, availability, entrance access or driving time','Eligible facilities limited to mapped in-FCT registry; cross-border facilities excluded']}
assert len({c['id'] for c in cells})==len(cells)
assert abs(sum(summary['facilityCatchments'].values())-summary['overall']['population'])<1
assert abs(sum(s['population'] for s in summary['lgas'].values())-summary['overall']['population'])<.1
for s in [summary['overall'],*summary['lgas'].values()]:
    for k in ('all','higher'):assert 0<=s[k+'Within5km']<=s[k+'Within10km']<=s['population']+.01
summary['region']='Fct';summary['facilitySnapshot']=[{k:f[k] for k in ('id','coordinates','facilityTypeCode')} for f in allf if f['division']=='Fct']
(data/'worldpop_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');(data/'worldpop_cells.json').write_text(json.dumps(cells,separators=(',',':')),encoding='utf8')
print(json.dumps({k:summary[k] for k in ('overall','eligibleFacilities','eligibleHigherFacilities','boundaryTieCells')},ensure_ascii=False))
