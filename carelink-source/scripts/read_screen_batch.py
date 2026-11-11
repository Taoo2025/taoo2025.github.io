import json,re,sys
from pathlib import Path
C=Path('dios_screen_cache');q=json.loads((C/'queue.json').read_text(encoding='utf8'))
pattern=re.compile(r'Abuja|FCT|Capital|Kwali|Kuje|Bwari|Abaji|Gwagwalada|Gwarinpa|Maitama|Asokoro|hospital|centre|center|died|death|patient|survivor|rape|Ebonyi|Cross River|Obanliku|study|survey',re.I)
for i in range(int(sys.argv[1]),min(int(sys.argv[2]),len(q))):
 a=q[i];d=json.loads((C/(a['id']+'.json')).read_text(encoding='utf8'));paras=d.get('paragraphs',[])
 # html.parser can create nested paragraphs: remove contained suffix duplicates.
 unique=[p for p in paras if not any(len(other)>len(p) and p in other for other in paras)]
 d['cleanParagraphs']=unique;(C/(a['id']+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 print('\n###',i,a['id'],a['title']);print('STATUS',d.get('status'),'DATE',d.get('dates'),d.get('times'),d.get('schemaDates'));print('URL',d.get('finalUrl'))
 # Read body introductions plus all location/clinical/survey paragraphs. For giant
 # nested paragraphs, print contextual windows of all matches plus the beginning.
 for n,p in enumerate(unique):
  if len(p)<=2000:
   if n<2 or pattern.search(p):print(f'P{n}:',p)
  else:
   spans=[(0,min(700,len(p)))]+[(max(0,m.start()-180),min(len(p),m.end()+270)) for m in pattern.finditer(p)]
   merged=[]
   for start,end in sorted(spans):
    if merged and start<=merged[-1][1]:merged[-1]=(merged[-1][0],max(end,merged[-1][1]))
    else:merged.append((start,end))
   print(f'P{n}:',' [...] '.join(p[start:end] for start,end in merged))
