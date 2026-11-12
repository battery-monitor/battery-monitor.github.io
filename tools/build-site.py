#!/usr/bin/env python3
"""Build BatterVibe's product, support and privacy pages in eight languages."""
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


def icon(name):
    paths = {
        'power': '<path d="m13 2-8 12h6l-1 8 9-13h-6l1-7Z"/>',
        'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4m0-14.2-1.4 1.4M6.3 17.7l-1.4 1.4"/>',
        'flow': '<path d="M3 16h18l-1 3H4l-1-3ZM5 13V5h14v8M8 9l3 3 5-5"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def picture(name, alt, hero=False):
    width, height = (1672, 941) if hero else (1536, 1024)
    loading = 'fetchpriority="high"' if hero else 'loading="lazy"'
    sizes = '(max-width: 680px) 100vw, (max-width: 1440px) 90vw, 1280px' if hero else '(max-width: 800px) 90vw, 600px'
    return f'<img src="/assets/scenes/{name}.webp" srcset="/assets/scenes/{name}-800.webp 800w, /assets/scenes/{name}.webp {width}w" sizes="{sizes}" width="{width}" height="{height}" {loading} alt="{escape(alt)}">'


def header(language, page, t):
    links = "".join(f'<a href="{url(language, name)}"' + (' aria-current="page"' if page == name else '')
                    + f'>{escape(title)}</a>' for name, title in zip(PAGES, t["nav"]))
    choices = "".join(f'<li><a href="{url(code, page)}" lang="{code}" hreflang="{code}"'
                      + (' aria-current="true"' if code == language else '')
                      + f'>{escape(label)}</a></li>' for code, (_, label) in LANGUAGES.items())
    return f'''<a class="skip" href="#main">{escape(t['skip'])}</a>
<header class="site-head"><div class="wrap head-row">
<a class="brand" href="{url(language, 'index.html')}"><img src="/assets/app-icon.png" alt="" width="35" height="35">BatterVibe</a>
<nav aria-label="{escape(t['navigation'])}">{links}</nav>
<details class="language language-picker"><summary aria-label="{escape(t['language'] + ': ' + LANGUAGES[language][1])}">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>
<span>{escape(LANGUAGES[language][1])}</span><span aria-hidden="true">⌄</span></summary>
<ul aria-label="{escape(t['language'])}">{choices}</ul></details></div></header>'''


def home(language, t):
    h = t['home']
    tags = ''.join(f'<a href="#{anchor}">{icon(symbol)}<span>{escape(label)}</span><span class="tag-arrow" aria-hidden="true">↓</span></a>'
                   for label, anchor, symbol in zip(h['heroTags'], ('power', 'daylight', 'flow'), ('power', 'sun', 'flow')))
    values = ('60.3', '82.5', '−22.2')
    if language in ('de', 'fr', 'es'): values = tuple(value.replace('.', ',') for value in values)
    terms = ''.join(f'<div><dt>{escape(term)}</dt><dd>{value}<small>W</small></dd></div>'
                    for term, value in zip(h['powerTerms'], values))
    outdoor_features = ''.join(f'<div><dt>{escape(title)}</dt><dd>{escape(body)}</dd></div>' for title, body in h['outdoorFeatures'])
    closed_tags = ''.join(f'<span>{escape(label)}</span>' for label in h['closedTags'])
    control_features = ''.join(f'<div><span class="feature-number" aria-hidden="true">0{i+1}</span><h3>{escape(title)}</h3><p>{escape(body)}</p></div>'
                               for i, (title, body) in enumerate(h['controlFeatures']))
    return f'''<main id="main">
<section class="hero wrap"><div class="hero-copy"><p class="kicker">{escape(h['kicker'])}</p>
<h1>{escape(h['headline'][0])}<span>{escape(h['headline'][1])}</span></h1>
<p class="hero-intro">{escape(h['intro'])}</p>
<div class="hero-actions"><a class="cta" href="#power">{escape(h['cta'])}<span aria-hidden="true">↓</span></a><a class="status-link" href="#availability"><span class="status-dot" aria-hidden="true"></span>{escape(h['releaseLink'])}</a></div>
<p class="compat">{escape(h['compat'])}</p></div>
<figure class="hero-scene">{picture('outdoor-coding', h['heroAlt'], True)}<figcaption>{escape(h['sceneCaption'])}</figcaption></figure>
<div class="scene-links">{tags}</div></section>
<section class="wrap power-section" id="power"><div class="section-copy"><p class="section-label">01 / {escape(h['powerLabel'])}</p><h2>{escape(h['powerTitle'])}</h2><p class="section-intro">{escape(h['powerIntro'])}</p><p class="note">{escape(h['powerFootnote'])}</p></div>
<figure class="power-readout"><div class="readout-head">{icon('power')}<span>{escape(h['exampleLabel'])}</span></div><dl>{terms}</dl><figcaption>{escape(h['powerCaption'].format(input=values[0], use=values[1], net=values[2]))}</figcaption></figure></section>
<section class="scene-section wrap" id="daylight"><figure class="feature-scene">{picture('daylight-screen', h['outdoorAlt'])}<figcaption>{escape(h['sceneCaption'])}</figcaption></figure>
<div class="section-copy"><p class="section-label">02 / {escape(h['outdoorLabel'])}</p><h2>{escape(h['outdoorTitle'])}</h2><p class="section-intro">{escape(h['outdoorIntro'])}</p><dl class="feature-list">{outdoor_features}</dl><p class="note">{escape(h['outdoorNote'])}</p></div></section>
<section class="scene-section flow-section wrap" id="flow"><div class="section-copy"><p class="section-label">03 / {escape(h['closedLabel'])}</p><h2>{escape(h['closedTitle'])}</h2><p class="section-intro">{escape(h['closedIntro'])}</p><div class="task-tags">{closed_tags}</div><p class="note">{escape(h['closedNote'])}</p></div>
<figure class="feature-scene">{picture('closed-lid', h['closedAlt'])}<figcaption>{escape(h['sceneCaption'])}</figcaption></figure></section>
<section class="control-section"><div class="wrap"><div class="control-heading"><p class="section-label">{escape(h['controlLabel'])}</p><h2>{escape(h['controlTitle'])}</h2><p class="section-intro">{escape(h['controlIntro'])}</p></div><div class="control-features">{control_features}</div></div></section>
<section class="availability wrap" id="availability"><div><p class="section-label"><span class="status-dot" aria-hidden="true"></span>{escape(h['releaseLabel'])}</p><h2>{escape(h['releaseTitle'])}</h2><p class="section-intro">{escape(h['releaseIntro'])}</p></div><div class="release-plan"><h3>{escape(h['releasePlanTitle'])}</h3><p>{escape(h['releasePlan'])}</p><a class="text-link" href="{url(language, 'support.html')}">{escape(h['supportCTA'])} <span aria-hidden="true">→</span></a></div></section>
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
            title = t['home']['title'] if page == 'index.html' else t['support' if page == 'support.html' else 'privacy']['title'] + ' · BatterVibe'
            description = t['home']['intro'] if page == 'index.html' else t['support' if page == 'support.html' else 'privacy']['lead']
            alternates = ''.join(f'<link rel="alternate" hreflang="{language}" href="{BASE}{url(language, page)}">' for language in LANGUAGES)
            footer = ''.join(f'<a href="{url(code, name)}">{escape(label)}</a>' for name, label in zip(PAGES[1:], t['nav'][1:]))
            main = home(code, t) if page == 'index.html' else document(code, page, t)
            html = f'''<!doctype html>
<html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f6f8f2">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{BASE}{url(code, page)}">{alternates}
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{BASE}{url(code, page)}"><meta property="og:image" content="{BASE}/assets/scenes/originals/outdoor-coding.png"><meta property="og:site_name" content="BatterVibe">
<link rel="icon" href="/assets/app-icon.png"><link rel="stylesheet" href="/site.css"><script src="/site.js" defer></script></head><body>{header(code, page, t)}{main}
<footer class="site-foot"><div class="wrap"><span>BatterVibe · © 2026 Zhiping Jiang</span><div class="foot-links">{footer}</div></div></footer></body></html>
'''
            output = ROOT / LANGUAGES[code][0] / page
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(html)
    print(f'Built {len(LANGUAGES)} languages × {len(PAGES)} pages')


if __name__ == '__main__': build()
