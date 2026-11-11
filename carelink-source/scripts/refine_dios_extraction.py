import json,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
C=Path('dios_screen_cache');queue=json.loads((C/'queue.json').read_text(encoding='utf8'));proxy={'https':'http://127.0.0.1:27890','http':'http://127.0.0.1:27890'}
def refine(a):
 p=C/(a['id']+'.json');d=json.loads(p.read_text(encoding='utf8'))
 if d.get('status')!=200:return
 try:
  res=requests.get(d['finalUrl'],timeout=35,proxies=proxy,headers={'User-Agent':'Mozilla/5.0'})
  if res.status_code!=200:return
  soup=BeautifulSoup(res.content,'html.parser')
  for x in soup(['script','style','nav','footer','header','aside']):x.decompose()
  candidates=[]
  for selector in ('.single-article .post-content','.td-post-content','.entry-content','.post-content','[itemprop="articleBody"]','article.single-article','main','body'):
   for node in soup.select(selector):
    paras=list(dict.fromkeys(x.get_text(' ',strip=True) for x in node.select('p') if len(x.get_text(' ',strip=True))>35))
    chars=sum(map(len,paras))
    if chars>500:candidates.append((selector,paras,chars));break
   if candidates:break
  if candidates:
   selector,paras,chars=candidates[0];d.update(paragraphs=paras,bodyCharacters=chars,extractionSelector=selector)
   p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 except Exception as e:d['refineError']=str(e);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(refine,queue))
for a in queue:
 d=json.loads((C/(a['id']+'.json')).read_text(encoding='utf8'));print(json.dumps({k:d.get(k) for k in ('id','status','bodyCharacters','extractionSelector','error')},ensure_ascii=False))
