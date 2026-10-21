#!/usr/bin/env python3
"""Buscador offline de metadatos/fichas del catálogo científico UNITESIS."""
import argparse, json, pathlib, unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[2]
LIB=ROOT/'docs'/'scientific-evidence'

def norm(s):
    return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().casefold()

def search(data, query='', module='', kind='', language='', limit=20):
    terms=norm(query).split()
    items=[]
    for r in data:
        if module and module not in r.get('modules',[]):continue
        if kind and kind not in r['kind']:continue
        if language and language.casefold()!=r['lang'].casefold():continue
        hay=norm(' '.join([r['title'],r['domain'],r['kind'],r['lang'],' '.join(r.get('keywords',[]))]))
        if not all(t in hay for t in terms):continue
        items.append(r)
    return items[:limit]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--module',default='');p.add_argument('--kind',default='')
    p.add_argument('--query',default='');p.add_argument('--language',default='')
    p.add_argument('--limit',type=int,default=20);p.add_argument('--list-modules',action='store_true')
    args=p.parse_args()
    data=json.loads((LIB/'catalog.json').read_text(encoding='utf-8'))
    if args.list_modules:
        print('\n'.join(sorted({m for r in data for m in r['modules']})));return
    for r in search(data,args.query,args.module,args.kind,args.language,args.limit):
        print(f"{r['id']} | {r['kind']} | {r['lang']} | {r['title']} | {r['file']}")

if __name__=='__main__':main()
