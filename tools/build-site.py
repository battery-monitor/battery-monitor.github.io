#!/usr/bin/env python3
"""Build the three static pages for each explicitly supported language."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://battery-monitor.zpj.io"
LANGUAGES = {"zh-Hans": ("", "简体中文"), "zh-Hant": ("zh-Hant", "繁體中文"),
             "en": ("en", "English"), "ja": ("ja", "日本語"), "ko": ("ko", "한국어"),
             "de": ("de", "Deutsch"), "fr": ("fr", "Français"), "es": ("es", "Español")}
PAGES = ("index.html", "support.html", "privacy.html")
EMAIL = "jiangzp.cs@icloud.com"


def url(language, page):
    folder = LANGUAGES[language][0]
    return "/" + (folder + "/" if folder else "") + ("" if page == "index.html" else page)


def header(language, page, t):
    links = "".join(f'<a href="{url(language, name)}"' + (' aria-current="page"' if page == name else '')
                    + f'>{escape(title)}</a>' for name, title in zip(PAGES, t["nav"]))
    choices = "".join(f'<li><a href="{url(code, page)}" lang="{code}" hreflang="{code}"'
                      + (' aria-current="true"' if code == language else '')
                      + f'>{escape(label)}</a></li>' for code, (_, label) in LANGUAGES.items())
    return f'''<a class="skip" href="#main">{escape(t['skip'])}</a>
<header class="site-head"><div class="wrap head-row">
<a class="brand" href="{url(language, 'index.html')}"><img src="/assets/app-icon.png" alt="" width="35" height="35">Battery Monitor</a>
<nav aria-label="{escape(t['navigation'])}">{links}</nav>
<details class="language language-picker"><summary aria-label="{escape(t['language'] + ': ' + LANGUAGES[language][1])}">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>
<span>{escape(LANGUAGES[language][1])}</span><span aria-hidden="true">⌄</span></summary>
<ul aria-label="{escape(t['language'])}">{choices}</ul></details></div></header>'''


def home(language, t):
    h = t['home']; chinese = language in ('zh-Hans', 'zh-Hant')
    suffix = '' if chinese else '-en'
    values = ('60.3', '82.5', '−22.2') if chinese else ('53.7', '62.1', '−8.4')
    desktop_menu = ''.join(f'<span>{label}</span>' for label in (('文件', '编辑', '显示') if chinese else ('File', 'Edit', 'View')))
    if language in ('de', 'fr', 'es'): values = tuple(value.replace('.', ',') for value in values)
    terms = ''.join(f'<div{chr(32)+"class=net" if i == 2 else ""}><dt>{escape(term)}</dt><dd>{value}<small>W</small></dd></div>'
                    for i, (term, value) in enumerate(zip(h['powerTerms'], values)))
    features = ''.join(f'<div><dt>{escape(title)}</dt><dd>{escape(body)}</dd></div>' for title, body in h['features'])
    return f'''<main id="main"><section class="wrap hero"><div class="hero-copy">
<p class="kicker">{escape(h['kicker'])}</p><h1>{escape(h['headline'][0])} <span>{escape(h['headline'][1])}</span></h1>
<p>{escape(h['intro'])}</p><a class="cta" href="#power">{escape(h['cta'])} <span aria-hidden="true">↓</span></a><p class="compat">{escape(h['compat'])}</p></div>
<figure class="desktop"><img class="wallpaper" src="/assets/coast.webp" alt="" width="1000" height="667">
<div class="menu-strip" aria-hidden="true"><div class="menu-left"><b>Finder</b>{desktop_menu}</div><div class="menu-right"><span class="battery">{'84' if chinese else '83'}</span><span>09:41</span></div></div>
<div class="preview-panel"><img src="/assets/overview{suffix}.jpg?v=20261111" width="732" height="532" alt="{escape(h['overviewAlt'])}"></div><figcaption>{escape(h['overviewCaption'])}</figcaption></figure></section>
<section class="power" id="power"><div class="wrap"><div><p class="section-label">{escape(h['powerLabel'])}</p><h2>{escape(h['powerTitle'])}</h2><p class="section-intro">{escape(h['powerIntro'])}</p></div>
<figure class="equation"><dl>{terms}</dl><figcaption>{escape(h['powerCaption'].format(input=values[0], use=values[1], net=values[2]))}</figcaption></figure></div></section>
<section class="wrap details"><figure class="detail-screen"><img loading="lazy" src="/assets/battery-details{suffix}.jpg?v=20261111" width="732" height="1122" alt="{escape(h['detailAlt'])}"></figure>
<div><p class="section-label">{escape(h['detailLabel'])}</p><h2>{escape(h['detailTitle'])}</h2><dl class="feature-list">{features}</dl><p class="section-intro">{escape(h['missing'])}</p></div></section>
<section class="privacy-band"><div class="wrap"><div><h2>{escape(h['privacyTitle'])}</h2><p>{escape(h['privacyIntro'])}</p></div><a class="text-link" href="{url(language, 'privacy.html')}">{escape(h['privacyLink'])} <span aria-hidden="true">→</span></a></div></section></main>'''


def document(language, page, t):
    d = t['support' if page == 'support.html' else 'privacy']
    updated = '' if page == 'support.html' else f'<p class="updated">{escape(d["effective"])}</p>'
    if page == 'support.html':
        content = '<div class="faq">' + ''.join(f'<details{" open" if i == 0 else ""}><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>'
                    for i, (question, answer) in enumerate(d['faqs'])) + '</div>'
    else:
        content = '<div class="prose">' + ''.join(f'<h2>{escape(title)}</h2><p>{escape(body)}</p>' for title, body in d['sections']) + '</div>'
    return f'''<main id="main" class="wrap doc"><header>{updated}<h1>{escape(d['title'])}</h1><p class="lead">{escape(d['lead'])}</p></header>
<aside class="contact"><h2>{escape(d['contactTitle'])}</h2><p>{escape(d['contactIntro'])}</p><a href="mailto:{EMAIL}">{EMAIL}</a></aside>{content}</main>'''


def build():
    catalogs = {code: json.loads((ROOT / 'locales' / (code + '.json')).read_text()) for code in LANGUAGES}
    def shape(value):
        if isinstance(value, dict): return {key: shape(item) for key, item in value.items()}
        if isinstance(value, list): return [shape(item) for item in value]
        assert isinstance(value, str) and value
        return 'text'
    for code, t in catalogs.items():
        assert shape(t) == shape(catalogs['en']), f'Incomplete catalog: {code}'
        for page in PAGES:
            title = t['home']['title'] if page == 'index.html' else t['support' if page == 'support.html' else 'privacy']['title'] + ' · Battery Monitor'
            description = t['home']['intro'] if page == 'index.html' else t['support' if page == 'support.html' else 'privacy']['lead']
            alternates = ''.join(f'<link rel="alternate" hreflang="{language}" href="{BASE}{url(language, page)}">' for language in LANGUAGES)
            footer = ''.join(f'<a href="{url(code, name)}">{escape(label)}</a>' for name, label in zip(PAGES[1:], t['nav'][1:]))
            main = home(code, t) if page == 'index.html' else document(code, page, t)
            html = f'''<!doctype html>
<html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f7f9f5">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{BASE}{url(code, page)}">{alternates}
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{BASE}{url(code, page)}"><meta property="og:image" content="{BASE}/assets/overview{'-en' if code not in ('zh-Hans', 'zh-Hant') else ''}.jpg?v=20261111">
<link rel="icon" href="/assets/app-icon.png"><link rel="stylesheet" href="/site.css"><script src="/site.js" defer></script></head><body>{header(code, page, t)}{main}
<footer class="site-foot"><div class="wrap"><span>© 2026 Zhiping Jiang</span><div class="foot-links">{footer}</div></div></footer></body></html>
'''
            output = ROOT / LANGUAGES[code][0] / page
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(html)
    print(f'Built {len(LANGUAGES)} languages × {len(PAGES)} pages')


if __name__ == '__main__': build()
