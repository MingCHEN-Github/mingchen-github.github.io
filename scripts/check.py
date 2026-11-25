#!/usr/bin/env python3
"""Check generated routes, anchor targets, metadata, and resource references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.duplicates=[];self.links=[];self.h1=0;self.title=False;self.description=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):
   if a['id'] in self.ids:self.duplicates.append(a['id'])
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description' and a.get('content'):self.description=True
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag in ('script','img') and a.get('src'):self.links.append(a['src'])
  if tag=='link' and a.get('href'):self.links.append(a['href'])

pages={}
for path in ROOT.rglob('*.html'):
 if path.name.startswith('qa-'):continue
 p=Page();p.feed(path.read_text());pages[path]=p
errors=[];link_count=0
for path,p in pages.items():
 if p.h1!=1:errors.append(f'{path.relative_to(ROOT)}: {p.h1} h1 elements')
 if not p.title or not p.description:errors.append(f'{path.relative_to(ROOT)}: missing metadata')
 if p.duplicates:errors.append(f'{path.relative_to(ROOT)}: duplicate ids {p.duplicates}')
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  link_count+=1
  target=(ROOT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
  if not u.path:target=path
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{path.relative_to(ROOT)}: missing target {href}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{path.relative_to(ROOT)}: missing fragment {href}')
if errors:raise SystemExit('\n'.join(errors))
print(json.dumps({'status':'passed','pages':len(pages),'internal_links_and_assets':link_count,'duplicate_ids':0,'missing_targets':0}))
