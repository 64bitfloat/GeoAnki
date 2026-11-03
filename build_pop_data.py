import urllib.request, re, json
from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.cur_table = None
        self.cur_row = None
        self.cur_cell = None
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.cur_table = []
        elif tag == 'tr' and self.cur_table is not None:
            self.cur_row = []
        elif tag in ('td', 'th') and self.cur_row is not None:
            self.cur_cell = []
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            if self.cur_row is not None:
                self.cur_row.append(''.join(self.cur_cell).strip())
        elif tag == 'tr' and self.cur_table is not None:
            if self.cur_row is not None:
                self.cur_table.append(self.cur_row)
            self.cur_row = None
        elif tag == 'table' and self.cur_table is not None:
            self.tables.append(self.cur_table)
            self.cur_table = None

    def handle_data(self, data):
        if self.in_cell and self.cur_cell is not None:
            self.cur_cell.append(data)

def parse_wiki_table(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    parser = TableParser()
    parser.feed(html)
    for t in parser.tables:
        if len(t) > 50 and any('都道府県' in cell for cell in t[0]):
            return t
    return []

# 1. 市
cities_table = parse_wiki_table('https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E5%B8%82%E3%81%AE%E4%BA%BA%E5%8F%A3%E9%A0%86%E4%BD%8D')
# 2. 町
towns_table = parse_wiki_table('https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E7%94%BA%E3%81%AE%E4%BA%BA%E5%8F%A3%E9%A0%86%E4%BD%8D')
# 3. 村
villages_table = parse_wiki_table('https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E6%9D%91%E3%81%AE%E4%BA%BA%E5%8F%A3%E9%A0%86%E4%BD%8D')

print(f'Cities table rows: {len(cities_table)}')
print(f'Towns table rows: {len(towns_table)}')
print(f'Villages table rows: {len(villages_table)}')

pop_dict = {}

def clean_num(s):
    s = s.replace(',', '').replace('人', '').strip()
    m = re.search(r'\d+', s)
    return int(m.group(0)) if m else 0

# 市テーブル解析 (Header: 順位, 都道府県, 市（区）, 法定人口, 推計人口...)
for row in cities_table[1:]:
    if len(row) >= 4:
        pref = row[1]
        name = row[2]
        pop = clean_num(row[3]) or clean_num(row[4])
        if pref and name:
            pop_dict[(pref, name)] = pop

# 町テーブル解析
for row in towns_table[1:]:
    if len(row) >= 4:
        pref = row[1]
        name = row[2]
        pop = clean_num(row[3]) or clean_num(row[4])
        if pref and name:
            pop_dict[(pref, name)] = pop

# 村テーブル解析
for row in villages_table[1:]:
    if len(row) >= 4:
        pref = row[1]
        name = row[2]
        pop = clean_num(row[3]) or clean_num(row[4])
        if pref and name:
            pop_dict[(pref, name)] = pop

print(f'Total parsed populations in dict: {len(pop_dict)}')

with open('municipalities.json', 'r', encoding='utf-8') as f:
    muni_data = json.load(f)

matched = 0
unmatched = []
muni_pop = {}
for m in muni_data.values():
    pref = m['pref']
    name = m['n']
    pop = pop_dict.get((pref, name))
    if pop is None:
        # 表記揺れチェック (例: ヶ / ケ, 龍 / 竜 など)
        alt_name = name.replace('ヶ', 'ケ').replace('ノ', 'の')
        pop = pop_dict.get((pref, alt_name))
        if pop is None:
            alt_name2 = name.replace('ケ', 'ヶ')
            pop = pop_dict.get((pref, alt_name2))
    
    if pop is not None:
        matched += 1
        muni_pop[m['c']] = pop
    else:
        unmatched.append((m['c'], pref, name))

print(f'Matched: {matched} / {len(muni_data)}')
if unmatched:
    print(f'Unmatched sample ({len(unmatched)}): {unmatched[:15]}')

# 保存
with open('municipality_populations.json', 'w', encoding='utf-8') as f:
    json.dump(muni_pop, f, ensure_ascii=False, indent=2)

print('Saved to municipality_populations.json')
