#!/usr/bin/env python3
"""Auditoría básica de artefactos y vínculos relativos, sin afirmar revisión académica."""
import json, pathlib, sys, re
ROOT=pathlib.Path(__file__).resolve().parents[2]
LIB=ROOT/'docs'/'scientific-evidence'

def validate():
    c=json.loads((LIB/'catalog.json').read_text(encoding='utf-8'))
    assert len(c)>=101, f'Se requieren >100 fichas, solo {len(c)}'
    assert len({r['id'] for r in c})==len(c)
    assert len({r['url'].rstrip('/').lower() for r in c})==len(c)
    for r in c:
        p=LIB/r['file']
        assert p.is_file(), p
        body=p.read_text(encoding='utf-8')
        assert body.startswith('---\n') and r['url'] in body
        assert 'full_text_reviewed: false' in body
        assert re.match(r'https?://',r['url'])
        assert r['domain'] in r['modules']
    for p in (LIB/'modules').glob('*.md'):
        for dst in re.findall(r'\]\(\.\./(sources/[^)]+)\)',p.read_text(encoding='utf-8')):
            assert (LIB/dst).is_file(), (p,dst)
    print(f'OK: {len(c)} fichas, {len(list((LIB/"modules").glob("*.md")))} dominios, {sum(r["origin"] == "web_2026-10-17" for r in c)} nuevas con registro web')
if __name__=='__main__':validate()
