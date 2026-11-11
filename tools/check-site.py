#!/usr/bin/env python3
"""Check deployed routes and language links without a browser or network."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('site_builder', ROOT / 'tools/build-site.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.language = None; self.picker = False
        self.choices = []; self.assets = []; self.alternates = []; self.canonical = None
    def handle_starttag(self, tag, values):
        attrs = dict(values)
        if tag == 'html': self.language = attrs.get('lang')
        if tag == 'details' and 'language-picker' in attrs.get('class', ''): self.picker = True
        if tag == 'a' and self.picker: self.choices.append(attrs)
        if tag in ('img', 'script') and attrs.get('src'): self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet': self.assets.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'alternate': self.alternates.append(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
    def handle_endtag(self, tag):
        if tag == 'details': self.picker = False


count = 0
for language, (folder, _) in builder.LANGUAGES.items():
    for name in builder.PAGES:
        page = Page(); page.feed((ROOT / folder / name).read_text())
        assert page.language == language
        assert len(page.choices) == len(page.alternates) == 8
        assert {choice['hreflang'] for choice in page.choices} == set(builder.LANGUAGES)
        current = [choice for choice in page.choices if choice.get('aria-current') == 'true']
        assert len(current) == 1 and current[0]['hreflang'] == language
        for choice in page.choices:
            assert choice['href'] == builder.url(choice['hreflang'], name), (language, name, choice)
            path = urlsplit(choice['href']).path
            assert (ROOT / path.lstrip('/') / ('index.html' if path.endswith('/') else '')).is_file()
        assert page.canonical == builder.BASE + builder.url(language, name)
        for asset in page.assets: assert (ROOT / urlsplit(asset).path.lstrip('/')).is_file(), asset
        count += 1
print(f'Checked {count} pages, {count * 8} language routes, assets, current selections and canonical URLs')
