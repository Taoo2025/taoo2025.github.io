"""Rebuild FCT road distances from organizer-recommended Geofabrik PBF.
Run from workspace; supply --root/--pbf to reproduce elsewhere.
"""
import sys,json,math,hashlib,gzip,argparse,time
from pathlib import Path
from collections import defaultdict,Counter
sys.path.insert(0,str(Path('.route-deps').resolve()))
import osmium
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from shapely.geometry import LineString
from routing_rules import access_allowed,blocked_node,directions,speed_kmh,expand_turns,turn_allowed

p=argparse.ArgumentParser();p.add_argument('--root',default='E:/CASA/hackathon/hanyun-hackathon');p.add_argument('--pbf',default='E:/CASA/hackathon/data/nigeria-routing.osm.pbf');args=p.parse_args()
root=Path(args.root);pbf=Path(args.pbf);out=root/'public/data'
facilities=[f for f in json.loads((out/'nigeria_facilities_clean.json').read_text(encoding='utf-8-sig')) if f['division']=='Fct']
bbox=(6.2,8.0,8.3,10.2);coordinates={};blocked=set();stats=Counter();edges={};rules=defaultdict(list)
speeds={'motorway':80,'trunk':70,'primary':60,'secondary':50,'tertiary':40,'unclassified':30,'residential':25,'living_street':10,'service':15}
def metres(a,b):
    x,y=map(math.radians,a);u,v=map(math.radians,b)
    h=math.sin((v-y)/2)**2+math.cos(y)*math.cos(v)*math.sin((u-x)/2)**2
    return 12742000*math.asin(math.sqrt(min(1,h)))
class Nodes(osmium.SimpleHandler):
    def node(self,n):
        x,y=n.location.lon,n.location.lat
        if bbox[0]<=x<=bbox[2] and bbox[1]<=y<=bbox[3]:
            tags=dict(n.tags)
            if blocked_node(tags):blocked.add(n.id)
            if tags.get('barrier') in ('gate','lift_gate','swing_gate') and access_allowed(tags):stats['gatesWithoutConfirmedOpening']+=1
class Ways(osmium.SimpleHandler):
    def way(self,w):
        tags=dict(w.tags);base=tags.get('highway','').removesuffix('_link')
        if base not in speeds or not access_allowed(tags):return
        forward,backward=directions(tags);ids=[]
        for n in w.nodes:
            ids.append(n.ref)
            if n.location.valid():
                x,y=n.location.lon,n.location.lat
                if bbox[0]<=x<=bbox[2] and bbox[1]<=y<=bbox[3]:coordinates[n.ref]=(x,y)
        for a,b in zip(ids,ids[1:]):
            if a not in coordinates or b not in coordinates:continue
            if a in blocked or b in blocked:stats['blockedSegments']+=1;continue
            length=metres(coordinates[a],coordinates[b])
            if length<=0:continue
            for pair,direction in ([( (a,b),'forward')] if forward else [])+([( (b,a),'backward')] if backward else []):
                speed=speed_kmh(tags.get('maxspeed:'+direction,tags.get('maxspeed','')),speeds[base]);value=(length,length/(speed/3.6),w.id)
                if pair not in edges or value[0]<edges[pair][0]:edges[pair]=value
class Relations(osmium.SimpleHandler):
    def relation(self,r):
        tags=dict(r.tags)
        if tags.get('type')!='restriction':return
        via=[m for m in r.members if m.role=='via'];fr=[m.ref for m in r.members if m.role=='from' and m.type=='w'];to=[m.ref for m in r.members if m.role=='to' and m.type=='w']
        # Only count restrictions with at least one via node in the regional extract,
        # or a referenced way actually represented by the regional graph.
        regional=any(m.type=='n' and m.ref in coordinates for m in via)
        if not regional and not any(x in regional_ways for x in fr+to):return
        stats['regionalRestrictions']+=1
        if any(x in tags.get('except','').split(';') for x in ('motorcar','motor_vehicle')):stats['motorcarExemptRestrictions']+=1;return
        kind=tags.get('restriction:motorcar',tags.get('restriction:motor_vehicle',tags.get('restriction','')))
        if not(kind.startswith('no_') or kind.startswith('only_')) or len(via)!=1 or via[0].type!='n' or len(fr)!=1 or len(to)!=1 or any('conditional' in k for k in tags):
            stats['unsupportedRestrictions']+=1;return
        rules[via[0].ref].append({'from':fr[0],'to':to[0],'kind':kind});stats['supportedRestrictions']+=1

started=time.time()
print('Reading tagged barriers/access nodes (native prefilter)',flush=True)
with osmium.io.Reader(str(pbf),osmium.osm.NODE) as reader:
    osmium.apply(reader,osmium.filter.KeyFilter('barrier','access','motorcar','motor_vehicle','vehicle'),Nodes())
print('Reading drivable ways with native location cache',flush=True)
road_tags=[('highway',road+suffix) for road in speeds for suffix in ('','_link')]
Ways().apply_file(str(pbf),locations=True,idx='flex_mem',filters=[osmium.filter.TagFilter(*road_tags)])
regional_ways={v[2] for v in edges.values()}
print('Reading turn restrictions',flush=True)
with osmium.io.Reader(str(pbf),osmium.osm.RELATION) as reader:osmium.apply(reader,Relations())
print('Building turn-aware graph',dict(stats),flush=True)
expanded=list(expand_turns(edges,rules));nodeids=list({v for a,b,c in expanded for v in (a,b)});index={n:i for i,n in enumerate(nodeids)}
ordinary=[n for n in nodeids if isinstance(n,int) and n not in rules];points=np.array([coordinates[n] for n in ordinary]);scale=np.array([111000*math.cos(math.radians(9)),111000]);tree=cKDTree(points*scale)
snaps={}
for f in facilities:
    _,i=tree.query(np.array(f['coordinates'])*scale);n=ordinary[i];gap=metres(f['coordinates'],points[i]);snaps[f['id']]={'node':index[n],'gap_m':round(gap,1),'valid':gap<=500}
graph=csr_matrix(([v[0] for a,b,v in expanded],([index[b] for a,b,v in expanded],[index[a] for a,b,v in expanded])),shape=(len(nodeids),len(nodeids)))
del expanded,regional_ways
levels={'Primary':1,'Secondary':2,'Tertiary':3};targets=[f for f in facilities if levels.get(f['facilityTypeCode'],0)>1 and snaps[f['id']]['valid']]
output={f['id']:{'snap':snaps[f['id']],'reachableHigher':0,'routes':[]} for f in facilities}
def physical(n):return n[1] if isinstance(n,tuple) else n
for j,target in enumerate(targets):
    end=snaps[target['id']];dist,pred=dijkstra(graph,directed=True,indices=end['node'],return_predecessors=True)
    for origin in facilities:
        snap=snaps[origin['id']]
        if not snap['valid'] or levels[target['facilityTypeCode']]<=levels.get(origin['facilityTypeCode'],3):continue
        length=float(dist[snap['node']])
        if not math.isfinite(length):continue
        record=output[origin['id']];record['reachableHigher']+=1
        if len(record['routes'])==3 and length/1000>max(r['roadKm'] for r in record['routes']):continue
        path=[snap['node']]
        while path[-1]!=end['node']:
            nxt=int(pred[path[-1]])
            if nxt<0 or len(path)>len(nodeids):raise RuntimeError('Invalid predecessor')
            path.append(nxt)
        nodes=[physical(nodeids[n]) for n in path]
        seconds=sum(edges[a,b][1] for a,b in zip(nodes,nodes[1:]));line=[coordinates[n] for n in nodes]
        # Validate actual reconstructed sequence, independent of graph expansion.
        for a,b,c in zip(nodes,nodes[1:],nodes[2:]):
            if b in rules:assert turn_allowed(a,b,c,edges[a,b][2],edges[b,c][2],rules[b])
        boundary=any(min(x-bbox[0],bbox[2]-x,y-bbox[1],bbox[3]-y)<.01 for x,y in line)
        if len(line)>1:line=list(LineString(line).simplify(.00002).coords)
        route={'targetId':target['id'],'roadKm':round(length/1000,3),'estimatedMinutes':round(seconds/60,1),'targetGapM':end['gap_m'],'nearNetworkBoundary':boundary,'geometry':[[round(x,6),round(y,6)] for x,y in line]}
        record['routes']=sorted(record['routes']+[route],key=lambda r:(r['roadKm'],r['targetId']))[:3]
    print('Target',j+1,'/',len(targets),flush=True)
with pbf.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
stats.update({'blockedNodes':len(blocked),'restrictedJunctions':len(rules),'snappedFacilities':sum(s['valid'] for s in snaps.values()),'originsWithRoutes':sum(bool(o['routes']) for o in output.values()),'routes':sum(len(o['routes']) for o in output.values())})
result={'version':2,'source':'https://download.geofabrik.de/africa/nigeria-latest.osm.pbf','sha256':digest,'bbox':bbox,'speedsKmh':speeds,'speedMethod':'road-class assumption capped by parseable directional/general posted maxspeed','snapLimitM':500,'nodes':len(nodeids),'directedEdges':graph.nnz,'audit':dict(stats),'origins':output,'limitations':['Regional extract; paths can be affected by clipping even when not near boundary','Nearest ordinary drivable node within 500m; no verified hospital entrance or connector access; connector distance/time excluded','Unconditional single-via-node motorcar turn restrictions only; unsupported and conditional relations counted in audit','Conditional access/oneway, unknown gate opening, road surface, traffic and clinical acceptance are not modelled','Parallel same-node edges represented by one shortest segment; relation way identity may be incomplete']}
result['region']='Fct';result['facilitySnapshot']=[{k:f[k] for k in ('id','coordinates','facilityTypeCode')} for f in facilities]
payload=json.dumps(result,separators=(',',':')).encode();(out/'fct_routes.json').write_bytes(payload);(out/'fct_routes.json.gz').write_bytes(gzip.compress(payload,mtime=0))
(out/'routing_audit.json').write_text(json.dumps({'version':2,'sha256':digest,'counts':dict(stats),'seconds':round(time.time()-started),'limitations':result['limitations']},indent=2),encoding='utf8')
print(json.dumps(dict(stats)),flush=True)
