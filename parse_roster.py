#!/usr/bin/env python3
from bs4 import BeautifulSoup
import csv
import os
import json
import requests

HTML_FILE = 'roster_page.html'
OUT_CSV = 'roster.csv'

def clean(text):
    return text.strip() if text else ''

def main():
    if not os.path.exists(HTML_FILE):
        print(f"Missing {HTML_FILE}; please download the roster page into the workspace.")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    players = soup.find_all('div', class_='sidearm-roster-player-header-details')
    rows = []

    def parse_player_soup(p):
        number_tag = p.find('span', class_='sidearm-roster-player-jersey-number')
        number = clean(number_tag.get_text()) if number_tag else ''

        name_tag = p.find('span', class_='sidearm-roster-player-name')
        first = last = ''
        if name_tag:
            spans = name_tag.find_all('span')
            if len(spans) >= 2:
                first = clean(spans[0].get_text())
                last = clean(spans[1].get_text())
            elif spans:
                first = clean(spans[0].get_text())

        fields = {'position':'','weight':'','height':'','hometown':'','class':'','high_school':''}

        for dl in p.find_all('dl'):
            dt = dl.find('dt')
            dd = dl.find('dd')
            if not dt or not dd:
                continue
            key = clean(dt.get_text()).rstrip(':')
            val = clean(dd.get_text())
            if key == 'Position':
                fields['position'] = val
            elif key == 'Weight':
                fields['weight'] = val
            elif key == 'Height':
                fields['height'] = val
            elif key == 'Hometown':
                fields['hometown'] = val
            elif key == 'Class':
                fields['class'] = val
            elif key == 'High School':
                fields['high_school'] = val

        return {
            'number': number,
            'first_name': first,
            'last_name': last,
            'position': fields['position'],
            'weight': fields['weight'],
            'height': fields['height'],
            'hometown': fields['hometown'],
            'class': fields['class'],
            'high_school': fields['high_school']
        }

    if players:
        for p in players:
            rows.append(parse_player_soup(p))
    else:
        # roster is likely rendered client-side; look for JSON list of player URLs in ld+json
        scripts = soup.find_all('script', type='application/ld+json')
        urls = []
        for s in scripts:
            try:
                data = json.loads(s.string or 'null')
            except Exception:
                continue
            # data may be a dict with 'item' list or a list of persons
            if isinstance(data, dict) and 'item' in data and isinstance(data['item'], list):
                for it in data['item']:
                    if isinstance(it, dict) and 'url' in it:
                        urls.append(it['url'])
            elif isinstance(data, list):
                for it in data:
                    if isinstance(it, dict) and it.get('@type') == 'Person' and 'url' in it:
                        urls.append(it['url'])

        # fetch each player's page and parse
        base = 'https://hurstathletics.com'
        headers = {'User-Agent': 'Mozilla/5.0'}
        for u in urls:
            full = u if u.startswith('http') else base + u
            try:
                resp = requests.get(full, headers=headers, timeout=15)
                if resp.status_code != 200:
                    continue
                psoup = BeautifulSoup(resp.text, 'lxml')
                pdiv = psoup.find('div', class_='sidearm-roster-player-header-details')
                if pdiv:
                    rows.append(parse_player_soup(pdiv))
            except Exception:
                continue

    fieldnames = ['number','first_name','last_name','position','weight','height','hometown','class','high_school']
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote {len(rows)} players to {OUT_CSV}")

if __name__ == '__main__':
    main()
