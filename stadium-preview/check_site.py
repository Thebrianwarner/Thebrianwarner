#!/usr/bin/env python3
"""Offline Stadium source checks. Run from repository root: python3 stadium-preview/check_site.py"""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PAGES = ["index.html","operation.html","championship-conversation.html","coachs-office.html","film-room.html","defense-investigator.html","saturday-school.html","team-store.html"]
class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.tags=[]; self.titles=[]; self.current_title=False; self.images=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs); self.tags.append(tag)
        if tag=='a' and attrs.get('href'): self.links.append(attrs['href'])
        if tag=='link' and attrs.get('href'): self.links.append(attrs['href'])
        if tag=='img': self.images.append(attrs)
        if tag=='title': self.current_title=True
    def handle_endtag(self,tag):
        if tag=='title': self.current_title=False
    def handle_data(self,data):
        if self.current_title: self.titles.append(data)

errors=[]
for name in PAGES:
    path=ROOT/name
    if not path.is_file(): errors.append(f'{name}: missing file'); continue
    data=path.read_text(encoding='utf-8')
    p=Inspector(); p.feed(data)
    if not p.titles: errors.append(f'{name}: missing title')
    for tag in ('html','head','body','main'):
        if tag not in p.tags: errors.append(f'{name}: missing <{tag}>')
    if 'stadium.css' not in p.links: errors.append(f'{name}: missing shared stylesheet')
    for link in p.links:
        if link.startswith(('http:','https:','mailto:','tel:','#','data:')): continue
        target=link.split('#',1)[0].split('?',1)[0]
        if target and not (ROOT/target).is_file(): errors.append(f'{name}: broken link {link}')
    for img in p.images:
        if 'alt' not in img: errors.append(f'{name}: image missing alt')
    print(f'{name}: {len(p.links)} links checked')
if errors:
    print('FAILED:'); print('\\n'.join(errors)); sys.exit(1)
print('PASS: all expected pages, local links, document landmarks, and image alt attributes')
