import json

with open('municipalities_with_wards.json', 'r', encoding='utf-8') as f:
    muni_data = json.load(f)

with open('municipality_populations_with_wards.json', 'r', encoding='utf-8') as f:
    pop_data = json.load(f)

# 北海道のエリア判定関数
def get_hokkaido_area(code):
    c = int(code)
    if code == '01100' or (1101 <= c <= 1110): return 'central'
    if code in ('01217', '01224', '01231', '01234', '01235'): return 'central'
    if code in ('01209', '01210', '01215', '01216', '01218', '01222', '01225', '01226', '01227', '01228'): return 'central'
    if code == '01203': return 'central'
    if code in ('01202', '01236'): return 'southern'
    if code in ('01205', '01213', '01230', '01233'): return 'southern'
    if code in ('01204', '01220', '01221', '01229'): return 'northern'
    if code == '01212': return 'northern'
    if code == '01214': return 'northern'
    if code in ('01208', '01211', '01219'): return 'eastern'
    if code == '01207': return 'eastern'
    if code == '01206': return 'eastern'
    if code == '01223': return 'eastern'
    if 1303 <= c <= 1304: return 'central'
    if 1331 <= c <= 1347: return 'southern'
    if 1361 <= c <= 1371: return 'southern'
    if 1391 <= c <= 1409: return 'central'
    if 1423 <= c <= 1438: return 'central'
    if 1452 <= c <= 1472: return 'northern'
    if 1481 <= c <= 1489: return 'northern'
    if 1511 <= c <= 1520: return 'northern'
    if 1543 <= c <= 1564: return 'eastern'
    if 1571 <= c <= 1586: return 'southern'
    if 1601 <= c <= 1610: return 'southern'
    if 1631 <= c <= 1649: return 'eastern'
    if 1661 <= c <= 1668: return 'eastern'
    if 1691 <= c <= 1694: return 'eastern'
    return 'central'

# 各自治体に pop と area を設定
for m in muni_data.values():
    m['pop'] = pop_data.get(m['c'], 0)
    if m['p'] == '01':
        m['area'] = get_hokkaido_area(m['c'])
    else:
        m['area'] = 'ALL'

def rebalance_area_group(munis):
    # 初期分類 (元のlvl準拠)
    majors = [m for m in munis if m['lvl'] == 1]
    cities = [m for m in munis if m['lvl'] == 2]
    towns = [m for m in munis if m['lvl'] == 3]
    villages = [m for m in munis if m['lvl'] == 4]

    majors.sort(key=lambda x: x['pop'], reverse=True)
    cities.sort(key=lambda x: x['pop'], reverse=True)
    towns.sort(key=lambda x: x['pop'], reverse=True)
    villages.sort(key=lambda x: x['pop'], reverse=True)

    # ルール1: 主要都市が5以下の場合、市から人口上位を必要数(最低6)格上げ
    total_cities = len(majors) + len(cities)
    if 0 < len(majors) <= 5:
        if total_cities <= 6:
            majors.extend(cities)
            cities = []
        else:
            needed = 6 - len(majors)
            for _ in range(needed):
                if cities:
                    majors.append(cities.pop(0))
    elif len(majors) == 0 and cities:
        if total_cities <= 6:
            majors = cities
            cities = []
        else:
            majors = cities[:6]
            cities = cities[6:]

    # ルール2: 村が5以下の場合、町に統合
    if 0 < len(villages) <= 5:
        towns.extend(villages)
        towns.sort(key=lambda x: x['pop'], reverse=True)
        villages = []

    groups = []
    if majors:
        lbl = '主要都市' if cities else '市'
        groups.append((lbl, majors))
    if cities:
        groups.append(('市', cities))
    if towns:
        lbl = '町村' if not villages else '町'
        groups.append((lbl, towns))
    if villages:
        groups.append(('村', villages))

    # ルール3: 30を超えるグループを最小分割数（各30問以下）で分割
    final_levels = []
    for label, group_munis in groups:
        n = len(group_munis)
        if n > 30:
            k = (n + 29) // 30  # math.ceil(n / 30)
            # 人口上位から順に k 個のブロックに均等分割
            base_size = n // k
            remainder = n % k
            start = 0
            for i in range(k):
                size = base_size + (1 if i < remainder else 0)
                sub_list = group_munis[start:start+size]
                final_levels.append((f'{label}({i+1})', sub_list))
                start += size
        else:
            final_levels.append((label, group_munis))

    return final_levels

# 全県のレベルマップを作成
# キー: prefCode (北海道の場合は '01_ALL', '01_central', '01_southern', '01_northern', '01_eastern')
all_pref_levels = {}

pref_groups = {}
for m in muni_data.values():
    p = m['p']
    if p not in pref_groups:
        pref_groups[p] = []
    pref_groups[p].append(m)

for p, m_list in pref_groups.items():
    if p == '01':
        # 北海道全体
        all_pref_levels['01_ALL'] = [
            {'level': i+1, 'label': lbl, 'codes': [m['c'] for m in ml]}
            for i, (lbl, ml) in enumerate(rebalance_area_group(m_list))
        ]
        # 各エリア
        for a_id in ('central', 'southern', 'northern', 'eastern'):
            area_munis = [m for m in m_list if m['area'] == a_id]
            all_pref_levels[f'01_{a_id}'] = [
                {'level': i+1, 'label': lbl, 'codes': [m['c'] for m in ml]}
                for i, (lbl, ml) in enumerate(rebalance_area_group(area_munis))
            ]
    else:
        all_pref_levels[p] = [
            {'level': i+1, 'label': lbl, 'codes': [m['c'] for m in ml]}
            for i, (lbl, ml) in enumerate(rebalance_area_group(m_list))
        ]

print('Total level keys generated:', len(all_pref_levels))
# サンプル確認 (埼玉、北海道エリア)
print('Saitama levels:')
for l in all_pref_levels['11']:
    print(f"  Lv.{l['level']} {l['label']}: {len(l['codes'])} munis")

print('Hokkaido central (道央) levels:')
for l in all_pref_levels['01_central']:
    print(f"  Lv.{l['level']} {l['label']}: {len(l['codes'])} munis")

# 保存
with open('pref_levels_master.json', 'w', encoding='utf-8') as f:
    json.dump(all_pref_levels, f, ensure_ascii=False, indent=2)

print('Saved to pref_levels_master.json!')
