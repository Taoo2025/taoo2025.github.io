import sys, json, math, hashlib
from pathlib import Path
sys.path.insert(0, str(Path('.route-deps').resolve()))
import osmium
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
from shapely.geometry import LineString

ROOT = Path('E:/CASA/hackathon/hanyun-hackathon')
PBF = Path('E:/CASA/hackathon/data/nigeria-routing.osm.pbf')
facilities = [f for f in json.loads((ROOT/'public/data/nigeria_facilities_clean.json').read_text(encoding='utf-8-sig')) if f['division']=='Fct']
# Generous regional boundary permits paths outside FCT. Results remain regional.
bbox = (6.2, 8.0, 8.3, 10.2)
coordinates = {}
class Nodes(osmium.SimpleHandler):
    def node(self, n):
        x,y=n.location.lon,n.location.lat
        if bbox[0]<=x<=bbox[2] and bbox[1]<=y<=bbox[3]: coordinates[n.id]=(x,y)
print('Reading regional nodes', flush=True)
Nodes().apply_file(str(PBF))
speeds={'motorway':80,'trunk':70,'primary':60,'secondary':50,'tertiary':40,'unclassified':30,'residential':25,'living_street':10,'service':15}
edges={}
def metres(a,b):
    x,y=map(math.radians,a);u,v=map(math.radians,b)
    h=math.sin((v-y)/2)**2+math.cos(y)*math.cos(v)*math.sin((u-x)/2)**2
    return 12742000*math.asin(math.sqrt(min(1,h)))
class Ways(osmium.SimpleHandler):
    def way(self,w):
        tags=dict(w.tags); road=tags.get('highway',''); base=road.removesuffix('_link')
        if base not in speeds: return
        access=next((tags[k] for k in ['motorcar','motor_vehicle','vehicle','access'] if k in tags),'yes')
        if access in ['no','private','agricultural','forestry']: return
        direction=tags.get('oneway:motor_vehicle',tags.get('oneway','yes' if tags.get('junction')=='roundabout' or road=='motorway' else 'no'))
        ids=[n.ref for n in w.nodes]
        for a,b in zip(ids,ids[1:]):
            if a not in coordinates or b not in coordinates: continue
            length=metres(coordinates[a],coordinates[b]); seconds=length/(speeds[base]/3.6)
            pairs=[(a,b),(b,a)] if direction not in ['yes','1','true','-1','reverse'] else ([(b,a)] if direction in ['-1','reverse'] else [(a,b)])
            for pair in pairs:
                if pair not in edges or length<edges[pair][0]:edges[pair]=(length,seconds)
print('Reading drivable ways', flush=True)
Ways().apply_file(str(PBF))
ids=sorted({n for pair in edges for n in pair}); index={n:i for i,n in enumerate(ids)}
points=np.array([coordinates[n] for n in ids]); scale=np.array([111000*math.cos(math.radians(9)),111000]); tree=cKDTree(points*scale)
snaps={}
for f in facilities:
    _,i=tree.query(np.array(f['coordinates'])*scale); gap=metres(f['coordinates'],points[i]);snaps[f['id']]={'node':int(i),'gap_m':round(gap,1),'valid':gap<=500}
rows=[index[b] for a,b in edges]; cols=[index[a] for a,b in edges]
graph=csr_matrix(([v[0] for v in edges.values()],(rows,cols)),shape=(len(ids),len(ids)))
levels={'Primary':1,'Secondary':2,'Tertiary':3}; targets=[f for f in facilities if levels.get(f['facilityTypeCode'],0)>1 and snaps[f['id']]['valid']]
dist,pred=dijkstra(graph,directed=True,indices=[snaps[f['id']]['node'] for f in targets],return_predecessors=True)
output={}
for origin in facilities:
    snap=snaps[origin['id']]; options=[]
    if snap['valid']:
        for j,target in enumerate(targets):
            if levels[target['facilityTypeCode']]<=levels.get(origin['facilityTypeCode'],3):continue
            length=float(dist[j,snap['node']]); end=snaps[target['id']]
            if not math.isfinite(length):continue
            options.append((length,j,target,end))
    options.sort(key=lambda x:x[0]); routes=[]
    for length,j,target,end in options[:3]:
        path=[snap['node']]
        while path[-1]!=end['node']:
            nxt=int(pred[j,path[-1]])
            if nxt<0:raise RuntimeError('Invalid predecessor')
            path.append(nxt)
        seconds=sum(edges[(ids[a],ids[b])][1] for a,b in zip(path,path[1:]))
        line=[points[i].tolist() for i in path]
        if len(line)>1:line=list(LineString(line).simplify(0.00002).coords)
        routes.append({'targetId':target['id'],'roadKm':round(length/1000,3),'estimatedMinutes':round(seconds/60,1),'targetGapM':end['gap_m'],'geometry':[[round(x,6),round(y,6)] for x,y in line]})
    output[origin['id']]={'snap':snap,'reachableHigher':len(options),'routes':routes}
result={'source':'https://download.geofabrik.de/africa/nigeria-latest.osm.pbf','sha256':hashlib.sha256(PBF.read_bytes()).hexdigest(),'bbox':bbox,'speedsKmh':speeds,'snapLimitM':500,'nodes':len(ids),'directedEdges':len(edges),'origins':output,'limitations':['Regional network boundary','Node snapping up to 500 m; connectors excluded from road distance and time','Way-level access and oneway only; turn restrictions and barriers not modelled','Fixed road-class speed assumptions; no traffic, maxspeed or surface adjustments']}
(ROOT/'public/data/fct_routes.json').write_text(json.dumps(result,separators=(',',':')),encoding='utf8')
print(json.dumps({'nodes':len(ids),'edges':len(edges),'snapped':sum(s['valid'] for s in snaps.values()),'originsWithRoutes':sum(bool(o['routes']) for o in output.values())}),flush=True)
