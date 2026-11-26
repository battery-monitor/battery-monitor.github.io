#!/usr/bin/env python3
"""Build BatterVibe's product, support and privacy pages in eight languages."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://battervibe.zpj.io"
STORE_URL = "https://apps.apple.com/cn/app/battervibe/id6833069090?mt=12"
DIRECT_VERSION = "0.10.6"
SITE_REVISION = "20261126-risk"
CAPTURE_PATH = f"/assets/app/{DIRECT_VERSION}"
CAPTURE_SIZES = {"overview": (682, 1299), "details": (682, 1095),
                 "controls": (680, 581), "peak": (1028, 708), "activity": (632, 526)}
LANGUAGES = {"zh-Hans": ("", "简体中文"), "zh-Hant": ("zh-Hant", "繁體中文"),
             "en": ("en", "English"), "ja": ("ja", "日本語"), "ko": ("ko", "한국어"),
             "de": ("de", "Deutsch"), "fr": ("fr", "Français"), "es": ("es", "Español")}
PAGES = ("index.html", "support.html", "privacy.html")
EMAIL = "jiangzp.cs@icloud.com"
CLI_EXAMPLES = "battervibe status --json\nbattervibe menu net"
CLI_HELP = CLI_EXAMPLES + "\nbattervibe --help"
CLI_INSTALL = (
    "alias battervibe='/Applications/battery-mon.app/Contents/MacOS/battery-mon cli'",
    "alias battervibe='/Applications/BatterVibe.app/Contents/MacOS/BatterVibe cli'",
)


def url(language, page):
    folder = LANGUAGES[language][0]
    return "/" + (folder + "/" if folder else "") + ("" if page == "index.html" else page)


def shot(language, name, alt, caption, full_size):
    width, height = CAPTURE_SIZES[name]
    src = f'{CAPTURE_PATH}/{language}/{name}.webp'
    loading = 'fetchpriority="high"' if name == 'overview' else 'loading="lazy"'
    return f'''<figure class="shot shot-{name}"><div class="shot-display">
<img src="{src}" width="{width}" height="{height}" {loading} alt="{escape(alt)}"></div>
<figcaption><span>{escape(caption)}</span><a href="{src}" aria-label="{escape(full_size + ' · ' + caption)}">{escape(full_size)} <span aria-hidden="true">↗</span></a></figcaption></figure>'''


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


def risk_notice(t, extra_class=""):
    risk = t['riskNotice']
    return f'''<section class="risk-notice{extra_class}" id="risk-notice" aria-labelledby="risk-heading">
<h2 id="risk-heading">{escape(risk['title'])}</h2>
<dl class="feature-list"><div><dt>{escape(risk['hdrTitle'])}</dt><dd>{escape(risk['hdr'])}</dd></div>
<div><dt>{escape(risk['lidTitle'])}</dt><dd>{escape(risk['lid'])}</dd></div></dl>
<p>{escape(risk['disclaimer'])}</p></section>'''


def home(language, t):
    h = t['home']
    chip, battery, controls, peak, release = (h[key] for key in ('chip', 'battery', 'controls', 'peak', 'release'))
    cli = t['cli']
    jumps = ''.join(f'<a href="#{anchor}">{escape(label)} <span aria-hidden="true">↓</span></a>'
                    for anchor, label in zip(('activity', 'power', 'daylight', 'peak'), h['jumps']))
    # Keep the original closed-lid deep link on the matching control.
    items = ''.join(f'<div{id_attr}><dt>{escape(title)}</dt><dd>{escape(body)}</dd></div>'
                    for id_attr, (title, body) in zip(('', ' id="flow"', ''), controls['items']))
    return f'''<main id="main">
<section class="hero wrap"><div class="hero-copy"><p class="kicker">{escape(h['kicker'])}</p>
<h1>{escape(h['headline'][0])} <span>{escape(h['headline'][1])}</span></h1>
<p class="hero-intro">{escape(h['intro'])}</p>
<div class="hero-actions"><a class="cta" href="{STORE_URL}">{escape(h['cta'])} <span aria-hidden="true">↗</span></a>
<a class="text-link" href="#availability">{escape(h['releaseLink'])} <span aria-hidden="true">↓</span></a></div>
<p class="compat">{escape(h['compat'])}</p></div>
{shot(language,'overview',h['overviewAlt'],h['overviewCaption'],h['original'])}</section>
<div class="jump-links wrap">{jumps}</div>
<section class="feature wrap" id="activity"><div class="feature-copy">
<h2>{escape(chip['title'])}</h2><p>{escape(chip['body'])}</p><p>{escape(chip['note'])}</p></div>
{shot(language,'activity',chip['alt'],chip['caption'],h['original'])}</section>
<section class="feature wrap" id="power"><div class="feature-copy"><p class="section-label">{escape(h['jumps'][1])}</p>
<h2>{escape(battery['title'])}</h2><p>{escape(battery['body'])}</p><p>{escape(battery['note'])}</p></div>
{shot(language,'details',battery['alt'],battery['caption'],h['original'])}</section>
<section class="controls-band"><div class="feature wrap" id="daylight"><div class="feature-copy"><p class="section-label">{escape(h['jumps'][2])}</p>
<h2>{escape(controls['title'])}</h2><p>{escape(controls['body'])}</p><dl class="feature-list">{items}</dl></div>
{shot(language,'controls',controls['alt'],controls['caption'],h['original'])}</div></section>
<section class="feature feature-peak wrap" id="peak"><div class="feature-copy"><p class="section-label">{escape(h['jumps'][3])}</p>
<h2>{escape(peak['title'])}</h2><p>{escape(peak['body'])}</p><p>{escape(peak['note'])}</p></div>
{shot(language,'peak',peak['alt'],peak['caption'],h['original'])}</section>
<section class="cli-section wrap" id="cli"><div><h2>{escape(cli['title'])}</h2><p>{escape(cli['intro'])}</p>
<a class="text-link" href="{url(language, 'support.html')}#cli">{escape(cli['guide'])} <span aria-hidden="true">→</span></a></div>
<pre class="cli-code"><code>{escape(CLI_EXAMPLES)}</code></pre></section>
<section class="availability wrap" id="availability"><h2>{escape(release['title'])}</h2>
<div class="release-list"><div><h3>{escape(release['direct'])}</h3><p>{escape(release['directBody'])}</p></div>
<div><h3>{escape(release['store'])}</h3><p>{escape(release['storeBody'])}</p><a class="text-link" href="{STORE_URL}">{escape(h['cta'])} <span aria-hidden="true">↗</span></a></div>
<div><h3>{escape(release['update'])}</h3><p>{escape(release['updateBody'])}</p><a class="text-link" href="{url(language, 'support.html')}">{escape(release['support'])} <span aria-hidden="true">→</span></a></div></div></section>
<section class="privacy-band"><div class="wrap"><div><h2>{escape(h['privacyTitle'])}</h2><p>{escape(h['privacyIntro'])}</p></div><a class="text-link" href="{url(language, 'privacy.html')}">{escape(h['privacyLink'])} <span aria-hidden="true">→</span></a></div></section>
{risk_notice(t, ' wrap')}</main>'''


def document(language, page, t):
    d = t['support' if page == 'support.html' else 'privacy']
    updated = '' if page == 'support.html' else f'<p class="updated">{escape(d["effective"])}</p>'
    if page == 'support.html':
        cli = t['cli']
        installs = ''.join(f'<h3>{escape(label)}</h3><pre class="cli-code"><code>{escape(command)}</code></pre>'
                           for label, command in zip(cli['channels'], CLI_INSTALL))
        guide = f'''<section class="cli-guide" id="cli"><h2>{escape(cli['title'])}</h2><p>{escape(cli['setup'])}</p>
{installs}<h3>{escape(cli['exampleTitle'])}</h3><pre class="cli-code"><code>{escape(CLI_HELP)}</code></pre>
<p>{escape(cli['limits'])}</p><p>{escape(cli['results'])}</p></section>'''
        content = '<div class="faq">' + ''.join(f'<details{" open" if i == 0 else ""}><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>'
                    for i, (question, answer) in enumerate(d['faqs'])) + '</div>' + guide + risk_notice(t)
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
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{BASE}{url(code, page)}"><meta property="og:image" content="{BASE}{CAPTURE_PATH}/{code}/share.png"><meta property="og:image:width" content="864"><meta property="og:image:height" content="454"><meta property="og:image:alt" content="{escape(t['home']['chip']['caption'])}"><meta property="og:site_name" content="BatterVibe">
<link rel="icon" href="/assets/app-icon.png"><link rel="stylesheet" href="/site.css?v={SITE_REVISION}"><script src="/site.js" defer></script></head><body>{header(code, page, t)}{main}
<footer class="site-foot"><div class="wrap"><span>BatterVibe · © 2026 Zhiping Jiang</span><div class="foot-links">{footer}</div></div></footer></body></html>
'''
            output = ROOT / LANGUAGES[code][0] / page
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(html)
    print(f'Built {len(LANGUAGES)} languages × {len(PAGES)} pages')


if __name__ == '__main__': build()
