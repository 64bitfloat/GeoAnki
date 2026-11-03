# -*- coding: utf-8 -*-
"""
integrate_wards.py
municipalities.json と municipality_populations.json から政令指定都市20市を展開し、
全175行政区を置き換えた最新データセットを作成する
"""

import json

with open('municipalities.json', 'r', encoding='utf-8') as f:
    muni_raw = json.load(f)

with open('municipality_populations.json', 'r', encoding='utf-8') as f:
    pop_raw = json.load(f)

with open('wards_master.json', 'r', encoding='utf-8') as f:
    wards_master = json.load(f)

with open('ward_to_city.json', 'r', encoding='utf-8') as f:
    ward_to_city = json.load(f)

# 政令指定都市のコードセット
designated_city_codes = set(ward_to_city.values())
print(f'Designated city codes to expand: {len(designated_city_codes)}')

# 新しい自治体辞書
new_muni = {}
new_pop = {}

# 1. 政令指定都市以外の既存自治体をコピー
for code, m in muni_raw.items():
    if code not in designated_city_codes:
        new_muni[code] = m
        if code in pop_raw:
            new_pop[code] = pop_raw[code]

print(f'Non-designated munis kept: {len(new_muni)}')

# 2. 行政区（175区）を追加
for w_code, w in wards_master.items():
    new_muni[w_code] = {
        'c': w_code,
        'p': w['p'],
        'pref': w['pref'],
        'n': w['full_name'],        # 例: "静岡市葵区"
        'k': w['full_kana'],        # 例: "しずおかしあおいく"
        't': 'ward',
        'm_type': 'ward',
        'lvl': 1,                   # 主要都市レベル
        'lat': w['lat'],
        'lng': w['lng'],
        'city': w['city'],          # "静岡市"
        'ward': w['ward']           # "葵区"
    }
    new_pop[w_code] = w.get('pop', 100000)

print(f'Total new munis (including wards): {len(new_muni)}')
print(f'Total new populations: {len(new_pop)}')

# 保存
with open('municipalities_with_wards.json', 'w', encoding='utf-8') as f:
    json.dump(new_muni, f, ensure_ascii=False, indent=2)

with open('municipality_populations_with_wards.json', 'w', encoding='utf-8') as f:
    json.dump(new_pop, f, ensure_ascii=False, indent=2)

print('Saved municipalities_with_wards.json and municipality_populations_with_wards.json!')
