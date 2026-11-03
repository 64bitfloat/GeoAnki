# -*- coding: utf-8 -*-
"""
generate_wards_master.py
全15道県の GeoJSON から政令指定都市の全175行政区を抽出し、
名称、親市名、ふりがな、代表座標（重心/中心）を整理して wards_master.json を生成する
"""

import json
import urllib.request

WARD_KANA = {
    '上京区': 'かみぎょうく', '下京区': 'しもぎょうく', '中京区': 'なかぎょうく', '中区': 'なかく',
    '中原区': 'なかはらく', '中央区': 'ちゅうおうく', '中川区': 'なかがわく', '中村区': 'なかむらく',
    '伏見区': 'ふしみく', '住之江区': 'すみのえく', '住吉区': 'すみよしく', '佐伯区': 'さえきく',
    '保土ケ谷区': 'ほどがやく', '八幡東区': 'やはたひがしく', '八幡西区': 'やはたにしく', '兵庫区': 'ひょうごく',
    '北区': 'きたく', '千種区': 'ちくさく', '南区': 'みなみく', '博多区': 'はかたく',
    '厚別区': 'あつべつく', '右京区': 'うきょうく', '名東区': 'めいとうく', '垂水区': 'たるみく',
    '城南区': 'じょうなんく', '城東区': 'じょうとうく', '堺区': 'さかいく', '多摩区': 'たまく',
    '大宮区': 'おおみやく', '大正区': 'たいしょうく', '天王寺区': 'てんのうじく', '天白区': 'てんぱくく',
    '天竜区': 'てんりゅうく', '太白区': 'たいはくく', '守山区': 'もりやまく', '安佐北区': 'あさきたく',
    '安佐南区': 'あさみなみく', '安芸区': 'あきく', '宮前区': 'みやまえく', '宮城野区': 'みやぎのく',
    '小倉北区': 'こくらきたく', '小倉南区': 'こくらみなみく', '山科区': 'やましなく', '岩槻区': 'いわつきく',
    '川崎区': 'かわさきく', '左京区': 'さきょうく', '平野区': 'ひらのく', '幸区': 'さいわいく',
    '戸塚区': 'とつかく', '戸畑区': 'とばたく', '手稲区': 'ていねく', '早良区': 'さわらく',
    '旭区': 'あさひく', '昭和区': 'しょうわく', '東住吉区': 'ひがしすみよしく', '東区': 'ひがしく',
    '東山区': 'ひがしやまく', '東成区': 'ひがしなりく', '東淀川区': 'ひがしよどがわく', '東灘区': 'ひがしなだく',
    '栄区': 'さかえく', '桜区': 'さくらく', '此花区': 'このはなく', '江南区': 'こうなんく',
    '泉区': 'いずみく', '浜北区': 'はまきたく', '浦和区': 'うらわく', '浪速区': 'なにわく',
    '淀川区': 'よどがわく', '清水区': 'しみずく', '清田区': 'きよたく', '港北区': 'こうほくく',
    '港区': 'みなとく', '港南区': 'こうなんく', '瀬谷区': 'せやく', '灘区': 'なだく',
    '熱田区': 'あつたく', '瑞穂区': 'みずほく', '生野区': 'いくのく', '白石区': 'しろいしく',
    '磯子区': 'いそごく', '神奈川区': 'かながわく', '福島区': 'ふくしまく', '秋葉区': 'あきはく',
    '稲毛区': 'いなげく', '緑区': 'みどりく', '美原区': 'みはらく', '美浜区': 'みはまく',
    '花見川区': 'はなみがわく', '若松区': 'わかまつく', '若林区': 'わかばやしく', '若葉区': 'わかばく',
    '葵区': 'あおいく', '西京区': 'にしきょうく', '西区': 'にしく', '西成区': 'にしなりく',
    '西淀川区': 'にしよどがわく', '西蒲区': 'にしかんく', '見沼区': 'みぬまく', '豊平区': 'とよひらく',
    '都島区': 'みやこじまく', '都筑区': 'つづきく', '金沢区': 'かなざわく', '長田区': 'ながたく',
    '門司区': 'もじく', '阿倍野区': 'あべのく', '青葉区': 'あおばく', '須磨区': 'すまく',
    '駿河区': 'するがく', '高津区': 'たかつく', '鶴見区': 'つるみく', '麻生区': 'あさおく'
}

with open('municipalities.json', 'r', encoding='utf-8') as f:
    muni_data = json.load(f)

with open('ward_to_city.json', 'r', encoding='utf-8') as f:
    ward_to_city = json.load(f)

# 親市の情報辞書 (city_code -> {name, kana, pref_code, pref_name})
city_info = {}
for code, m in muni_data.items():
    if m.get('t') == 'designated':
        city_info[code] = {
            'name': m['n'],
            'kana': m['k'],
            'pref_code': m['p'],
            'pref_name': m['pref'],
            'pop': m.get('pop', 0)
        }

prefs = ['01', '04', '11', '12', '14', '15', '22', '23', '26', '27', '28', '33', '34', '40', '43']

def extract_coords(geom):
    coords = []
    g_type = geom.get('type')
    if g_type == 'Polygon':
        for ring in geom.get('coordinates', []):
            coords.extend(ring)
    elif g_type == 'MultiPolygon':
        for poly in geom.get('coordinates', []):
            for ring in poly:
                coords.extend(ring)
    return coords

wards_master = {}

for p in prefs:
    url = f'https://cdn.jsdelivr.net/gh/smartnews-smri/japan-topography@main/data/municipality/geojson/s0010/N03-21_{p}_210101.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))

    for f in data['features']:
        props = f['properties']
        code = props.get('N03_007')
        city_name = props.get('N03_003')
        ward_name = props.get('N03_004')

        if not (code and city_name and ward_name and city_name.endswith('市') and ward_name.endswith('区')):
            continue

        parent_city_code = ward_to_city.get(code)
        p_info = city_info.get(parent_city_code, {})
        city_kana = p_info.get('kana', '')
        ward_kana = WARD_KANA.get(ward_name, '')
        full_name = f'{city_name}{ward_name}'
        full_kana = f'{city_kana}{ward_kana}'

        # 座標計算
        coords = extract_coords(f.get('geometry', {}))
        if coords:
            lngs = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            center_lng = round(sum(lngs) / len(lngs), 4)
            center_lat = round(sum(lats) / len(lats), 4)
        else:
            center_lat, center_lng = None, None

        if code not in wards_master:
            wards_master[code] = {
                'c': code,
                'p': p,
                'pref': props.get('N03_001'),
                'parent_city_code': parent_city_code,
                'city': city_name,
                'city_kana': city_kana,
                'ward': ward_name,
                'ward_kana': ward_kana,
                'full_name': full_name,
                'full_kana': full_kana,
                'lat': center_lat,
                'lng': center_lng,
                'lvl': 1,
                't': 'ward'
            }

print(f'Total wards in wards_master: {len(wards_master)}')
with open('wards_master.json', 'w', encoding='utf-8') as f:
    json.dump(wards_master, f, ensure_ascii=False, indent=2)

print('Saved wards_master.json!')
