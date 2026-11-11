"""Retrieve only the 41 pending organizer-export URLs for manual AI screening.
Cache is local research material, not a public website asset.
"""
import json,re,hashlib,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
ROOT=Path('E:/CASA/hackathon/hanyun-hackathon')
CACHE=Path('dios_screen_cache');CACHE.mkdir(exist_ok=True)
articles={a['id']:a for a in json.loads((ROOT/'public/data/dios_signals.json').read_text(encoding='utf-8-sig'))}
checks=json.loads((ROOT/'src/data/dios_location_checks.json').read_text(encoding='utf8'))
pending=[articles[k] for k,v in checks.items() if v['sourceVerification']=='原文待核查']
(CACHE/'queue.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2),encoding='utf8')
proxies={'https':'http://127.0.0.1:27890','http':'http://127.0.0.1:27890'}
def fetch(a):
 p=CACHE/(a['id']+'.json')
 if p.exists():return json.loads(p.read_text(encoding='utf8'))
 record={'id':a['id'],'requestedUrl':a['url'],'exportTitle':a['title'],'attemptedAt':'2026-11-11','attempts':[]}
 try:
  response=requests.get(a['url'],timeout=(12,40),proxies=proxies,headers={'User-Agent':'Mozilla/5.0'})
  record['attempts'].append({'url':response.url,'status':response.status_code})
  if response.status_code>=400 and a['url'].startswith('http://'):
   response=requests.get(a['url'].replace('http://','https://',1),timeout=(12,40),proxies=proxies,headers={'User-Agent':'Mozilla/5.0'})
   record['attempts'].append({'url':response.url,'status':response.status_code})
  record.update(status=response.status_code,finalUrl=response.url,contentSha256=hashlib.sha256(response.content).hexdigest())
  soup=BeautifulSoup(response.content,'html.parser')
  record['pageTitle']=soup.title.get_text(' ',strip=True) if soup.title else ''
  record['canonical']=next((x.get('href') for x in soup.select('link[rel="canonical"]')),None)
  record['dates']=[{'name':m.get('property') or m.get('name'),'value':m.get('content')} for m in soup.select('meta') if any(x in ((m.get('property') or m.get('name') or '').lower()) for x in ('published','modified','date'))]
  record['times']=[t.get('datetime') or t.get_text(' ',strip=True) for t in soup.select('time')][:8]
  record['schemaDates']=[]
  for script in soup.select('script[type="application/ld+json"]'):
   for key,value in re.findall(r'"(datePublished|dateModified)"\s*:\s*"([^"]+)"',script.get_text()):record['schemaDates'].append({key:value})
  for n in soup(['script','style','nav','footer','header','aside']):n.decompose()
  body=soup.select_one('.entry-content') or soup.select_one('.td-post-content') or soup.select_one('[itemprop="articleBody"]') or soup.select_one('.post-content') or soup.select_one('article') or soup.select_one('main') or soup
  paragraphs=[x.get_text(' ',strip=True) for x in body.select('p')]
  record['paragraphs']=list(dict.fromkeys(x for x in paragraphs if len(x)>35))
  record['bodyCharacters']=sum(map(len,record['paragraphs']))
 except Exception as e:record['error']=str(e)
 p.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8');return record
with ThreadPoolExecutor(max_workers=6) as pool:
 for result in pool.map(fetch,pending):
  print(json.dumps({k:result.get(k) for k in ('id','status','bodyCharacters','pageTitle','error')},ensure_ascii=False),flush=True)
