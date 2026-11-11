import json, re
from pathlib import Path
from shapely.geometry import shape, Point, mapping
from shapely.ops import unary_union

root=Path('E:/CASA/hackathon/hanyun-hackathon')
geo=json.loads(Path('fct_wards.geojson').read_text(encoding='utf-8-sig'))
wards=[(f['properties'],shape(f['geometry'])) for f in geo['features']]
facilities=json.loads((root/'public/data/nigeria_facilities_clean.json').read_text(encoding='utf-8-sig'))
def normalise(s):
    return re.sub('[^a-z0-9]','',s.lower().replace('municipal area council','abuja municipal'))
report={}
for f in facilities:
    if f['division']!='Fct':continue
    p=Point(f['coordinates'])
    matches=[{'lga':w['lga'],'ward':w['ward'],'objectId':w['OBJECTID']} for w,g in wards if g.covers(p)]
    status='outside' if not matches else 'ambiguous' if len(matches)>1 else 'match' if normalise(matches[0]['lga'])==normalise(f['district']) else 'conflict'
    report[f['id']]={'originalLga':f['district'],'matches':matches,'status':status}
result={'source':'https://www.arcgis.com/home/item.html?id=45cd2ef592094d12aca43113a90a6054','version':'GRID3 NGA Operational Wards v3.0, 2026','license':'CC BY-SA 4.0; CIESIN Columbia University','note':'Operational boundaries, pending full government validation','hospitals':report}
(root/'public/data/fct_admin_checks.json').write_text(json.dumps(result,separators=(',',':')),encoding='utf8')
(root/'public/data/fct_wards.geojson').write_text(json.dumps(geo,separators=(',',':')),encoding='utf8')
lgas=[]
for name in sorted({w['lga'] for w,g in wards}):
    lg=unary_union([g for w,g in wards if w['lga']==name])
    lgas.append({'type':'Feature','properties':{'lga':name},'geometry':mapping(lg.simplify(.0001,preserve_topology=True))})
(root/'public/data/fct_lgas.geojson').write_text(json.dumps({'type':'FeatureCollection','features':lgas},separators=(',',':')),encoding='utf8')
from collections import Counter
print(dict(Counter(x['status'] for x in report.values())))
print([ (f['name'],report[f['id']]) for f in facilities if f['id'] in report and report[f['id']]['status']=='conflict'][:2])
