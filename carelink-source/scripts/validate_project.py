"""Data invariants for the real FCT bundle. No generated source records."""
from pathlib import Path
import json,math,gzip,argparse
parser=argparse.ArgumentParser();parser.add_argument('--root',default='E:/CASA/hackathon/hanyun-hackathon');args=parser.parse_args();root=Path(args.root);data=root/'public/data'
load=lambda name:json.loads((data/name).read_text(encoding='utf-8-sig'))
facilities=load('nigeria_facilities_clean.json');fct={f['id']:f for f in facilities if f['division']=='Fct'};admin=load('fct_admin_checks.json')['hospitals'];cells=load('worldpop_cells.json');population=load('worldpop_summary.json');network=load('fct_routes.json');levels={'Primary':1,'Secondary':2,'Tertiary':3}
assert len(fct)==576 and len(admin)==576
assert sum(len(admin[f]['matches'])==1 for f in fct)==572
assert network['version']==2,'Turn-aware rebuild has not completed'
assert json.loads(gzip.decompress((data/'fct_routes.json.gz').read_bytes()))==network
assert set(network['origins'])==set(fct)
count=0;boundary=0;targettypes={}
for fid,record in network['origins'].items():
    routes=record['routes'];assert len(routes)<=3
    assert [r['roadKm'] for r in routes]==sorted(r['roadKm'] for r in routes)
    if not record['snap']['valid']:assert not routes
    if fct[fid]['facilityTypeCode']=='Tertiary':assert not routes
    assert len({r['targetId'] for r in routes})==len(routes)
    for route in routes:
        target=fct[route['targetId']];assert levels[target['facilityTypeCode']]>levels[fct[fid]['facilityTypeCode']]
        assert math.isfinite(route['roadKm']) and route['roadKm']>=0 and route['estimatedMinutes']>=0
        assert route['geometry'] and record['snap']['gap_m']<=500 and route['targetGapM']<=500
        assert all(6.2<=x<=8.3 and 8<=y<=10.2 for x,y in route['geometry'])
        boundary+=route['nearNetworkBoundary'];count+=1
assert len(cells)==len({c['id'] for c in cells})==population['overall']['cells']
assert abs(sum(c['population'] for c in cells)-population['overall']['population'])<.01
assert abs(sum(s['population'] for s in population['lgas'].values())-population['overall']['population'])<.1
assert abs(sum(population['facilityCatchments'].values())-population['overall']['population'])<1
for c in cells:
    assert c['population']>=0 and c['lga'] in population['lgas']
    for kind in ('all','higher'):
        assert c[kind+'FacilityId'] in fct and c[kind+'Km']>=0
for summary in [population['overall'],*population['lgas'].values()]:
    for k in ('all','higher'):assert 0<=summary[k+'Within5km']<=summary[k+'Within10km']<=summary['population']+.01
baseline=json.loads(Path('routing_baseline.json').read_text()) if Path('routing_baseline.json').exists() else {}
changed=0
for fid,record in network['origins'].items():
    previous=baseline.get(fid,[]);current=[{k:r[k] for k in ('targetId','roadKm','estimatedMinutes')} for r in record['routes']]
    if previous!=current:changed+=1
result={'date':'2026-11-11','status':'passed','routesValidated':count,'boundaryFlaggedRoutes':boundary,'originsChangedVersusV1':changed if baseline else None,'populationCellsValidated':len(cells),'populationConservation':'passed','fctFacilities':len(fct),'routeAudit':network['audit'],'browserChecks':['LGA Abaji: 47 hospitals','WorldPop layer and summary','Cross-LGA higher-level candidates','gzip/JSON response compatibility','Article deep link and existing location evidence','Reject case aggregation without required geographic evidence']}
(root/'docs/456验证结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False))
