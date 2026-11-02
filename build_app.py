# -*- coding: utf-8 -*-
"""
GeoAnki Suite — 地理暗記学習プラットフォーム統合ビルドスクリプト
1. 全国1,741市区町村暗記モジュール
2. 令制国・旧国名暗記モジュール
3. 世界の国名・首都名暗記モジュール
3モジュール統合型ポータルランチャー (Root Hub) を含む単一SPA index.html を生成
"""

import json
import os

print("=== Building GeoAnki Suite (index.html) ===")

# -------------------------------------------------------------
# 1. 市区町村データ読み込み (Municipalities)
# -------------------------------------------------------------
print("Loading municipalities data...")
with open("municipalities.json", "r", encoding="utf-8") as f:
    muni_raw = json.load(f)

with open("ward_to_city.json", "r", encoding="utf-8") as f:
    ward_to_city = json.load(f)

# Compact array: [code, pref_code, pref_name, name, kana, type, lvl, lat, lng]
muni_arr = []
for m in muni_raw.values():
    muni_arr.append([
        m['c'],
        m['p'],
        m['pref'],
        m['n'],
        m['k'],
        m['t'],
        m['lvl'],
        round(m['lat'], 4) if m.get('lat') else None,
        round(m['lng'], 4) if m.get('lng') else None
    ])

PREFECTURES = [
    {"code": "01", "name": "北海道", "region": "北海道", "islands": [{"label": "全域", "bounds": [[41.3, 139.3], [45.6, 145.9]]}, {"label": "離島エリア", "bounds": [[45.0, 140.9], [45.5, 141.4]]}]},
    {"code": "02", "name": "青森県", "region": "東北"},
    {"code": "03", "name": "岩手県", "region": "東北"},
    {"code": "04", "name": "宮城県", "region": "東北"},
    {"code": "05", "name": "秋田県", "region": "東北"},
    {"code": "06", "name": "山形県", "region": "東北"},
    {"code": "07", "name": "福島県", "region": "東北"},
    {"code": "08", "name": "茨城県", "region": "関東"},
    {"code": "09", "name": "栃木県", "region": "関東"},
    {"code": "10", "name": "群馬県", "region": "関東"},
    {"code": "11", "name": "埼玉県", "region": "関東"},
    {"code": "12", "name": "千葉県", "region": "関東"},
    {"code": "13", "name": "東京都", "region": "関東", "defaultView": [[35.5, 138.9], [35.9, 139.9]], "islands": [{"label": "全域", "bounds": [[24.0, 138.9], [35.9, 142.3]]}, {"label": "本土", "bounds": [[35.5, 138.9], [35.9, 139.9]]}, {"label": "離島エリア1", "bounds": [[32.4, 138.9], [34.8, 140.2]]}, {"label": "離島エリア2", "bounds": [[24.0, 141.9], [27.3, 142.3]]}]},
    {"code": "14", "name": "神奈川県", "region": "関東"},
    {"code": "15", "name": "新潟県", "region": "中部", "defaultView": [[36.7, 137.6], [38.6, 139.9]], "islands": [{"label": "全域", "bounds": [[36.7, 137.6], [38.6, 139.9]]}, {"label": "本土", "bounds": [[36.7, 137.6], [38.6, 139.9]]}, {"label": "離島エリア", "bounds": [[37.7, 138.1], [38.6, 139.3]]}]},
    {"code": "16", "name": "富山県", "region": "中部"},
    {"code": "17", "name": "石川県", "region": "中部"},
    {"code": "18", "name": "福井県", "region": "中部"},
    {"code": "19", "name": "山梨県", "region": "中部"},
    {"code": "20", "name": "長野県", "region": "中部"},
    {"code": "21", "name": "岐阜県", "region": "中部"},
    {"code": "22", "name": "静岡県", "region": "中部"},
    {"code": "23", "name": "愛知県", "region": "中部"},
    {"code": "24", "name": "三重県", "region": "近畿"},
    {"code": "25", "name": "滋賀県", "region": "近畿"},
    {"code": "26", "name": "京都府", "region": "近畿"},
    {"code": "27", "name": "大阪府", "region": "近畿"},
    {"code": "28", "name": "兵庫県", "region": "近畿"},
    {"code": "29", "name": "奈良県", "region": "近畿"},
    {"code": "30", "name": "和歌山県", "region": "近畿"},
    {"code": "31", "name": "鳥取県", "region": "中国"},
    {"code": "32", "name": "島根県", "region": "中国", "defaultView": [[34.3, 131.6], [35.6, 133.4]], "islands": [{"label": "全域", "bounds": [[34.3, 131.6], [36.4, 133.4]]}, {"label": "本土", "bounds": [[34.3, 131.6], [35.6, 133.4]]}, {"label": "離島エリア", "bounds": [[35.9, 132.9], [36.4, 133.4]]}]},
    {"code": "33", "name": "岡山県", "region": "中国"},
    {"code": "34", "name": "広島県", "region": "中国"},
    {"code": "35", "name": "山口県", "region": "中国"},
    {"code": "36", "name": "徳島県", "region": "四国"},
    {"code": "37", "name": "香川県", "region": "四国"},
    {"code": "38", "name": "愛媛県", "region": "四国"},
    {"code": "39", "name": "高知県", "region": "四国"},
    {"code": "40", "name": "福岡県", "region": "九州・沖縄"},
    {"code": "41", "name": "佐賀県", "region": "九州・沖縄"},
    {"code": "42", "name": "長崎県", "region": "九州・沖縄", "defaultView": [[32.5, 129.7], [33.4, 130.4]], "islands": [{"label": "全域", "bounds": [[32.5, 128.5], [34.7, 130.4]]}, {"label": "本土", "bounds": [[32.5, 129.7], [33.4, 130.4]]}, {"label": "離島エリア1", "bounds": [[34.0, 129.1], [34.7, 129.5]]}, {"label": "離島エリア2", "bounds": [[33.7, 129.6], [33.9, 129.8]]}, {"label": "離島エリア3", "bounds": [[32.5, 128.5], [33.1, 129.2]]}]},
    {"code": "43", "name": "熊本県", "region": "九州・沖縄"},
    {"code": "44", "name": "大分県", "region": "九州・沖縄"},
    {"code": "45", "name": "宮崎県", "region": "九州・沖縄"},
    {"code": "46", "name": "鹿児島県", "region": "九州・沖縄", "defaultView": [[30.9, 130.0], [32.3, 131.2]], "islands": [{"label": "全域", "bounds": [[27.0, 128.3], [32.3, 131.2]]}, {"label": "本土", "bounds": [[30.9, 130.0], [32.3, 131.2]]}, {"label": "離島エリア1", "bounds": [[30.1, 130.3], [30.9, 131.1]]}, {"label": "離島エリア2", "bounds": [[27.0, 128.3], [28.6, 130.1]]}]},
    {"code": "47", "name": "沖縄県", "region": "九州・沖縄", "defaultView": [[26.0, 127.5], [26.9, 128.4]], "islands": [{"label": "全域", "bounds": [[24.0, 122.9], [27.1, 128.4]]}, {"label": "本島", "bounds": [[26.0, 127.5], [26.9, 128.4]]}, {"label": "離島エリア", "bounds": [[24.0, 122.9], [25.0, 125.5]]}]}
]

# -------------------------------------------------------------
# 2. 令制国データ読み込み (Provinces)
# -------------------------------------------------------------
print("Loading historic provinces data...")
with open("provinces_master.json", "r", encoding="utf-8") as f:
    provinces_master = json.load(f)

with open("provinces.geojson", "r", encoding="utf-8") as f:
    provinces_geojson = json.load(f)

DOH_LIST = [
    {"id": "ALL", "name": "全国 (68国)", "desc": "五畿七道 68国すべてを網羅"},
    {"id": "kinai", "name": "畿内（五畿）", "filter": "畿内", "desc": "山城・大和・河内・和泉・摂津の5国"},
    {"id": "tokaido", "name": "東海道", "filter": "東海道", "desc": "伊賀から常陸まで太平洋側の15国"},
    {"id": "tosando", "name": "東山道", "filter": "東山道", "desc": "近江・信濃から奥羽（陸奥・出羽）の8国"},
    {"id": "hokurikudo", "name": "北陸道", "filter": "北陸道", "desc": "若狭・越前・加賀から越後・佐渡の7国"},
    {"id": "sanindo", "name": "山陰道", "filter": "山陰道", "desc": "丹波・丹後から出雲・石見・隠岐の8国"},
    {"id": "sanyodo", "name": "山陽道", "filter": "山陽道", "desc": "播磨から安芸・長門まで瀬戸内側の8国"},
    {"id": "nankaido", "name": "南海道", "filter": "南海道", "desc": "紀伊・淡路・四国4国の計6国"},
    {"id": "saikaido", "name": "西海道", "filter": "西海道", "desc": "九州各州および壱岐・対馬の11国"},
]

# -------------------------------------------------------------
# 3. 世界の国名・首都データ読み込み (World Countries & Capitals)
# -------------------------------------------------------------
print("Loading world countries data...")
with open("world_master.json", "r", encoding="utf-8") as f:
    world_master = json.load(f)

with open("world.geojson", "r", encoding="utf-8") as f:
    world_geojson = json.load(f)

WORLD_REGIONS = [
    {"id": "ALL", "name": "全世界 (196ヶ国・地域)", "filter": "ALL", "desc": "国連加盟国および主要地域を網羅", "center": [20.0, 15.0], "zoom": 2},
    {"id": "asia", "name": "アジア (48ヶ国・地域)", "filter": "アジア", "desc": "東アジア、東南アジア、南アジア、中央・西アジア", "bounds": [[-12.0, 25.0], [55.0, 146.0]]},
    {"id": "europe", "name": "ヨーロッパ (44ヶ国・地域)", "filter": "ヨーロッパ", "desc": "西欧、北欧、中欧、東欧、地中海諸国", "bounds": [[34.0, -15.0], [71.0, 42.0]]},
    {"id": "africa", "name": "アフリカ (54ヶ国)", "filter": "アフリカ", "desc": "北アフリカ、西アフリカ、中部・東部・南部アフリカ", "bounds": [[-36.0, -20.0], [38.0, 55.0]]},
    {"id": "north_america", "name": "北アメリカ (23ヶ国)", "filter": "北アメリカ", "desc": "アメリカ・カナダ・中米・カリブ海諸島", "bounds": [[7.0, -125.0], [60.0, -58.0]]},
    {"id": "south_america", "name": "南アメリカ (12ヶ国)", "filter": "南アメリカ", "desc": "ブラジル・アンデス諸国・南部コーン", "bounds": [[-56.0, -82.0], [13.0, -34.0]]},
    {"id": "oceania", "name": "オセアニア (14ヶ国)", "filter": "オセアニア", "desc": "オーストラリア、NZ、ポリネシア・ミクロネシア諸島", "bounds": [[-48.0, 110.0], [10.0, -165.0]]},
]

# JSON strings for embedding
muni_json = json.dumps(muni_arr, ensure_ascii=False, separators=(',', ':'))
ward_json = json.dumps(ward_to_city, ensure_ascii=False, separators=(',', ':'))
pref_json = json.dumps(PREFECTURES, ensure_ascii=False, separators=(',', ':'))

prov_master_json = json.dumps(provinces_master, ensure_ascii=False, separators=(',', ':'))
prov_geo_json = json.dumps(provinces_geojson, ensure_ascii=False, separators=(',', ':'))
doh_json = json.dumps(DOH_LIST, ensure_ascii=False, separators=(',', ':'))

world_master_json = json.dumps(world_master, ensure_ascii=False, separators=(',', ':'))
world_geo_json = json.dumps(world_geojson, ensure_ascii=False, separators=(',', ':'))
world_regions_json = json.dumps(WORLD_REGIONS, ensure_ascii=False, separators=(',', ':'))

print(f"Data prepared: Muni({len(muni_arr)}), Prov({len(provinces_master)}), World({len(world_master)})")

# HTML Template
html_content = f'''<!DOCTYPE html>
<html lang="ja" class="h-full bg-slate-950 text-slate-100">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>GeoAnki Suite — 地理暗記学習プラットフォーム</title>

  <!-- 基本メタ情報 & SEO -->
  <meta name="description" content="市区町村（全1,741自治体）・令制国旧国名（68国）・世界の国名と首都（196ヶ国）を美麗な白地図ベクターポリゴンで直感暗記！GeoGuessr・地理・歴史学習のための統合型SPA学習プラットフォーム。" />
  <meta name="keywords" content="GeoGuessr, ジオゲッサー, 市区町村, 旧国名, 令制国, 世界の国名, 首都, 地理, 暗記, Anki, 白地図" />
  <meta name="author" content="64bitfloat" />
  <meta name="theme-color" content="#0ea5e9" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

  <!-- Open Graph Protocol (OGP / Discord / SNS) -->
  <meta property="og:site_name" content="GeoAnki Suite" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://64bitfloat.github.io/Anki_Geoguessr/" />
  <meta property="og:title" content="GeoAnki Suite — 地理暗記学習プラットフォーム" />
  <meta property="og:description" content="市区町村（全1,741）・旧国名（68国）・世界の国名と首都（196ヶ国）を白地図ベクターポリゴンで直感暗記！場所当て・4択・記入・探索・弱点復習の5大モード搭載。" />
  <meta property="og:image" content="https://opengraph.githubassets.com/1/64bitfloat/Anki_Geoguessr" />
  <meta property="og:locale" content="ja_JP" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="GeoAnki Suite — 地理暗記学習プラットフォーム" />
  <meta name="twitter:description" content="市区町村・旧国名・世界の国名首都を白地図ベクターで直感暗記！GeoGuessr・地理特化トレーナー。" />

  <!-- ファビコン -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230284c7'/><text x='50' y='65' font-size='44' font-weight='900' fill='white' text-anchor='middle' font-family='sans-serif'>🌍</text></svg>" />

  <!-- Tailwind CSS (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0f9ff',
              100: '#e0f2fe',
              400: '#38bdf8',
              500: '#0ea5e9',
              600: '#0284c7',
            }}
          }}
        }}
      }}
    }};
  </script>

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <!-- Turf.js (政令市の外郭ポリゴン自動結合) -->
  <script src="https://cdn.jsdelivr.net/npm/@turf/turf@6/turf.min.js"></script>

  <style>
    html, body {{
      height: 100%;
      height: 100dvh;
      overflow: hidden;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Kaku Gothic ProN", "Yu Gothic UI", Meiryo, sans-serif;
    }}
    .map-container {{
      background: #090d16 !important;
    }}
    .leaflet-container {{
      background: #090d16 !important;
    }}
    .leaflet-pane > svg {{
      transform: translate3d(0, 0, 0);
      backface-visibility: hidden;
    }}
    @keyframes pulse-yellow {{
      0%, 100% {{ fill-opacity: 0.95; stroke-width: 3.5px; fill: #fbbf24; stroke: #f59e0b; }}
      50% {{ fill-opacity: 0.35; stroke-width: 5px; fill: #fef08a; stroke: #fbbf24; }}
    }}
    .polygon-pulse {{
      animation: pulse-yellow 1.2s infinite ease-in-out;
    }}
    .no-scrollbar::-webkit-scrollbar {{
      display: none;
    }}
    .no-scrollbar {{
      -ms-overflow-style: none;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }}
    ::-webkit-scrollbar {{
      width: 5px;
      height: 5px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0f172a;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #475569;
    }}
  </style>
</head>
<body class="h-full flex flex-col overflow-hidden bg-slate-950 select-none text-slate-100">

  <!-- ============================================================== -->
  <!-- 画面 0: Root Hub (統合ポータルランチャー画面) -->
  <!-- ============================================================== -->
  <div id="screen-root-hub" class="flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 py-3 shrink-0 z-10 shadow-lg">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 via-indigo-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-sky-500/20 font-black text-white text-lg">
            🌐
          </div>
          <div>
            <h1 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              GeoAnki Suite
              <span class="text-xs font-normal text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded-full border border-sky-500/20">地理暗記ハブ</span>
            </h1>
            <p class="text-xs text-slate-400 hidden sm:block">市区町村・旧国名・世界の国名と首都 視覚ベクター暗記プラットフォーム</p>
          </div>
        </div>

        <!-- アクションボタン群 -->
        <div class="flex items-center gap-2">
          <button id="btn-global-sound" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 transition" title="効果音オン/オフ">
            <svg id="global-sound-icon-on" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
            <svg id="global-sound-icon-off" class="w-5 h-5 hidden text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/></svg>
          </button>
          <button id="btn-show-data-mgr" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition" title="データ管理・設定">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </button>
        </div>
      </div>
    </header>

    <!-- メイン選択エリア -->
    <main class="flex-1 overflow-y-auto px-4 py-6 overscroll-contain">
      <div class="max-w-5xl mx-auto space-y-6">
        <div class="text-center space-y-2 mb-6">
          <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight">暗記学習モジュールを選択</h2>
          <p class="text-xs sm:text-sm text-slate-400">暗記したい地理領域を選んで特訓を開始してください。学習履歴は自動保存されます。</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- カード 1: 市区町村 -->
          <div class="bg-gradient-to-b from-slate-900 to-slate-900/90 border border-emerald-500/30 hover:border-emerald-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl shadow-emerald-950/20 transition-all duration-300 hover:-translate-y-1 group">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition">
                  🗾
                </div>
                <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">JIS規格完全準拠</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-emerald-400 transition">市区町村暗記</h3>
                <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                  全国1,741自治体（市・町・村・特別区）。政令市行政区統合＆2層境界。GeoGuessrの地域特定力を極限まで高める特訓。
                </p>
              </div>

              <!-- 進捗状況 -->
              <div class="bg-slate-950/60 rounded-xl p-3 border border-slate-800 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-400">制覇状況</span>
                  <span class="font-bold text-emerald-400"><span id="root-muni-cleared">0</span> / 1,741 (<span id="root-muni-pct">0.0%</span>)</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div id="root-muni-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>正答率: <strong id="root-muni-acc" class="text-slate-200">--%</strong></span>
                  <span id="root-muni-weak-badge" class="text-rose-400">弱点: 0</span>
                </div>
              </div>
            </div>

            <button id="btn-enter-muni" class="mt-5 w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg shadow-emerald-600/30 transition flex items-center justify-center gap-2 active:scale-98">
              <span>特訓を始める</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>

          <!-- カード 2: 令制国・旧国名 -->
          <div class="bg-gradient-to-b from-slate-900 to-slate-900/90 border border-sky-500/30 hover:border-sky-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl shadow-sky-950/20 transition-all duration-300 hover:-translate-y-1 group">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="w-12 h-12 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition">
                  📜
                </div>
                <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">五畿七道68国</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-sky-400 transition">令制国・旧国名暗記</h3>
                <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                  武蔵・信濃・尾張・薩摩など日本の旧国名全68国を完全網羅。日本の歴史・古典文学・地域文化の理解を深める。
                </p>
              </div>

              <!-- 進捗状況 -->
              <div class="bg-slate-950/60 rounded-xl p-3 border border-slate-800 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-400">制覇状況</span>
                  <span class="font-bold text-sky-400"><span id="root-prov-cleared">0</span> / 68 (<span id="root-prov-pct">0.0%</span>)</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div id="root-prov-bar" class="bg-gradient-to-r from-sky-500 to-cyan-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>正答率: <strong id="root-prov-acc" class="text-slate-200">--%</strong></span>
                  <span id="root-prov-weak-badge" class="text-rose-400">弱点: 0</span>
                </div>
              </div>
            </div>

            <button id="btn-enter-province" class="mt-5 w-full py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/30 transition flex items-center justify-center gap-2 active:scale-98">
              <span>特訓を始める</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>

          <!-- カード 3: 世界の国名・首都名 -->
          <div class="bg-gradient-to-b from-slate-900 to-slate-900/90 border border-indigo-500/30 hover:border-indigo-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl shadow-indigo-950/20 transition-all duration-300 hover:-translate-y-1 group">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="w-12 h-12 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition">
                  🌍
                </div>
                <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">双方向出題・196国</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition">世界の国名・首都名暗記</h3>
                <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                  国連加盟国193ヶ国＋主要地域を網羅。国名と首都名の双方向クイズ、難易度・地域別分類、国旗絵文字表示に対応。
                </p>
              </div>

              <!-- 進捗状況 -->
              <div class="bg-slate-950/60 rounded-xl p-3 border border-slate-800 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-400">制覇状況</span>
                  <span class="font-bold text-indigo-400"><span id="root-world-cleared">0</span> / 196 (<span id="root-world-pct">0.0%</span>)</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div id="root-world-bar" class="bg-gradient-to-r from-indigo-500 to-purple-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>正答率: <strong id="root-world-acc" class="text-slate-200">--%</strong></span>
                  <span id="root-world-weak-badge" class="text-rose-400">弱点: 0</span>
                </div>
              </div>
            </div>

            <button id="btn-enter-world" class="mt-5 w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 transition flex items-center justify-center gap-2 active:scale-98">
              <span>特訓を始める</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        </div>

        <!-- 共通インフォメーション -->
        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-4 text-xs text-slate-400 space-y-2">
          <div class="font-bold text-slate-300 flex items-center gap-1.5">
            <span>💡</span>
            <span>学習のヒント & 本プラットフォームの特徴</span>
          </div>
          <ul class="list-disc list-inside space-y-1 text-slate-400">
            <li><strong>完全オフライン動作</strong>: 外部地図タイル通信を行わず、軽量ベクターマップのみで爆速レンダリングします。</li>
            <li><strong>消去法を排除した本格暗記</strong>: 正解済みの地域も未正解と同色のダークトーンを維持し、確実な記憶定着を促します。</li>
            <li><strong>キーボード完結対応</strong>: PCでは「4択 [1]-[4]」や「記入モードのEnter連続回答」に対応しています。</li>
          </ul>
        </div>
      </div>
    </main>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 1A: 市区町村 Hub (都道府県選択画面) -->
  <!-- ============================================================== -->
  <div id="screen-muni-hub" class="hidden flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 py-3 shrink-0 z-10">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2 sm:gap-3">
          <button class="btn-return-root p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="ホームに戻る">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="hidden sm:inline">ホーム</span>
          </button>
          <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-black text-sm">
            🗾
          </div>
          <div>
            <h2 class="text-sm sm:text-base font-bold text-white flex items-center gap-1.5">
              市区町村暗記
              <span class="text-[10px] text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">1,741自治体</span>
            </h2>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-[10px] text-slate-400">制覇数</div>
            <div class="text-xs sm:text-sm font-extrabold text-emerald-400">
              <span id="muni-hub-cleared">0</span> <span class="text-[10px] text-slate-400">/ 1,741</span>
              <span id="muni-hub-pct" class="text-[10px] font-semibold text-slate-300 ml-0.5">(0.0%)</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- プログレスバー -->
    <div class="w-full bg-slate-900/60 border-b border-slate-800 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-800 h-2 rounded-full overflow-hidden">
          <div id="muni-hub-progress-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-[11px] text-slate-300 whitespace-nowrap">
          完了県: <span id="muni-hub-completed-prefs" class="text-emerald-400 font-bold">0</span> / 47
        </div>
      </div>
    </div>

    <!-- 地方フィルターピルバー -->
    <div class="bg-slate-900/40 border-b border-slate-800 px-4 py-2 shrink-0 overflow-x-auto no-scrollbar">
      <div class="max-w-6xl mx-auto flex gap-1.5 min-w-max" id="muni-region-filter-bar">
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500 text-white" data-region="ALL">すべて</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="北海道">北海道</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="東北">東北</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="関東">関東</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="中部">中部</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="近畿">近畿</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="中国">中国</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="四国">四国</button>
        <button class="muni-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="九州・沖縄">九州・沖縄</button>
      </div>
    </div>

    <!-- 都道府県カードグリッド -->
    <main class="flex-1 overflow-y-auto px-4 py-4 overscroll-contain">
      <div class="max-w-6xl mx-auto space-y-6" id="muni-hub-container">
      </div>
    </main>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 1B: 市区町村 Spoke (クイズ・学習画面) -->
  <!-- ============================================================== -->
  <div id="screen-muni-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <!-- Spoke ヘッダー -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 px-3 py-2 shrink-0 z-20 flex items-center justify-between gap-2 shadow-md">
      <div class="flex items-center gap-2 min-w-0">
        <button id="btn-muni-back-hub" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="都道府県選択に戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">一覧</span>
        </button>
        <button class="btn-return-root p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition" title="ホームに戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        </button>
        <div class="min-w-0">
          <div class="flex items-center gap-1.5">
            <h2 id="muni-spoke-pref-title" class="text-sm sm:text-base font-extrabold text-white truncate">東京都</h2>
            <span id="muni-spoke-pref-count-badge" class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shrink-0">62自治体</span>
          </div>
          <div class="flex items-center gap-2 text-[11px] text-slate-400 mt-0.5">
            <span>進捗: <strong id="muni-spoke-progress-text" class="text-slate-200">0 / 0</strong></span>
            <span class="text-slate-600">|</span>
            <span id="muni-spoke-accuracy-tag" class="text-slate-400">正答率: --%</span>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-1.5">
        <button id="btn-muni-reset-pref" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-rose-400 transition" title="この県の学習記録をリセット">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
      </div>
    </header>

    <!-- サブコントロールバー (Level & モード切替) -->
    <div class="bg-slate-900/90 border-b border-slate-800 px-3 py-1.5 shrink-0 z-20 flex flex-wrap items-center justify-between gap-2 text-xs">
      <!-- レベルタブ -->
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar" id="muni-level-tabs">
      </div>

      <!-- 操作モードセグメント -->
      <div class="flex items-center bg-slate-950 p-0.5 rounded-lg border border-slate-800 shrink-0" id="muni-mode-segment">
        <button class="muni-mode-btn px-2.5 py-1 rounded-md text-[11px] font-bold transition flex items-center gap-1 bg-emerald-500 text-white" data-mode="locate">
          <span>🎯</span><span>場所当て</span>
        </button>
        <button class="muni-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="name">
          <span>🔤</span><span>4択</span>
        </button>
        <button class="muni-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="type">
          <span>✍️</span><span>記入</span>
        </button>
        <button class="muni-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="explore">
          <span>🔍</span><span>探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div class="flex-1 relative overflow-hidden">
      <div id="muni-map" class="w-full h-full map-container"></div>

      <!-- 離島クイック切り替えボタン群 -->
      <div id="muni-island-buttons" class="absolute top-3 right-3 z-[1000] flex flex-col gap-1.5"></div>

      <!-- 探索ポップオーバー -->
      <div id="muni-explore-card" class="hidden absolute top-3 left-3 z-[1000] bg-slate-900/95 backdrop-blur border border-slate-700/80 rounded-xl p-3 shadow-2xl max-w-xs text-xs space-y-2">
        <div class="flex items-start justify-between gap-2">
          <div>
            <div id="muni-exp-kana" class="text-[10px] text-emerald-400">ふりがな</div>
            <div id="muni-exp-name" class="text-base font-extrabold text-white">自治体名</div>
          </div>
          <button id="btn-muni-close-exp" class="text-slate-400 hover:text-white p-1">✕</button>
        </div>
        <div class="flex items-center gap-2 text-[11px]">
          <span id="muni-exp-type" class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">市町村</span>
          <span id="muni-exp-code" class="text-slate-400 font-mono">13101</span>
        </div>
        <div class="bg-slate-950/70 p-2 rounded-lg border border-slate-800 text-[11px] flex justify-between">
          <span class="text-slate-400">学習履歴</span>
          <span id="muni-exp-stats" class="text-slate-200 font-bold">正解 0 / 不正解 0</span>
        </div>
        <button id="btn-muni-test-single" class="w-full py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition">
          この自治体をテスト 🎯
        </button>
      </div>
    </div>

    <!-- 下部ドックコントロール -->
    <div id="muni-dock" class="bg-slate-900/95 backdrop-blur border-t border-slate-800 px-4 py-3 shrink-0 z-20 shadow-2xl">
      <!-- JSで出題・回答コントロールを動的描画 -->
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 2A: 令制国 Hub (五畿七道選択画面) -->
  <!-- ============================================================== -->
  <div id="screen-prov-hub" class="hidden flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 py-3 shrink-0 z-10 shadow-lg">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2 sm:gap-3">
          <button class="btn-return-root p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="ホームに戻る">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="hidden sm:inline">ホーム</span>
          </button>
          <div class="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center font-black text-sm">
            📜
          </div>
          <div>
            <h2 class="text-sm sm:text-base font-bold text-white flex items-center gap-1.5">
              令制国・旧国名暗記
              <span class="text-[10px] text-sky-400 bg-sky-500/10 px-1.5 py-0.5 rounded border border-sky-500/20">五畿七道</span>
            </h2>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-[10px] text-slate-400">全国制覇数</div>
            <div class="text-xs sm:text-sm font-extrabold text-sky-400">
              <span id="prov-hub-cleared">0</span> <span class="text-[10px] text-slate-400">/ 68</span>
              <span id="prov-hub-pct" class="text-[10px] font-semibold text-slate-300 ml-0.5">(0.0%)</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- プログレスバー -->
    <div class="w-full bg-slate-900/60 border-b border-slate-800 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-800 h-2 rounded-full overflow-hidden">
          <div id="prov-hub-progress-bar" class="bg-gradient-to-r from-sky-500 to-cyan-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-[11px] text-slate-400 whitespace-nowrap">
          制覇地域: <span id="prov-hub-completed-doh" class="text-sky-400 font-bold">0</span> / 8道
        </div>
      </div>
    </div>

    <!-- 五畿七道カードグリッド -->
    <main class="flex-1 overflow-y-auto px-4 py-4 overscroll-contain">
      <div class="max-w-6xl mx-auto space-y-4">
        <!-- 苦手克服クイックバナー -->
        <div id="prov-weak-banner" class="hidden bg-gradient-to-r from-rose-950/40 to-slate-900 border border-rose-500/30 rounded-xl p-3.5 flex items-center justify-between gap-3 shadow-lg">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold text-lg shrink-0">
              ⚡
            </div>
            <div>
              <div class="text-sm font-bold text-white flex items-center gap-2">
                苦手克服特訓デッキ
                <span id="prov-weak-count-badge" class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 text-xs font-semibold">0国</span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">直近で間違えた旧国を集中トレーニング</p>
            </div>
          </div>
          <button id="btn-prov-start-weak-all" class="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm transition shrink-0 active:scale-95 shadow">
            復習スタート →
          </button>
        </div>

        <div id="prov-cards-container" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5"></div>
      </div>
    </main>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 2B: 令制国 Spoke (クイズ・学習画面) -->
  <!-- ============================================================== -->
  <div id="screen-prov-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <!-- Spoke ヘッダー -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 px-3 py-2 shrink-0 z-20 flex items-center justify-between gap-2 shadow-md">
      <div class="flex items-center gap-2 min-w-0">
        <button id="btn-prov-back-hub" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="地域一覧に戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">一覧</span>
        </button>
        <button class="btn-return-root p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition" title="ホームに戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        </button>
        <div class="min-w-0">
          <div class="flex items-center gap-1.5">
            <h2 id="prov-spoke-title" class="text-sm sm:text-base font-extrabold text-white truncate">東海道</h2>
            <span id="prov-spoke-count-badge" class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/30 shrink-0">15国</span>
          </div>
          <div class="flex items-center gap-2 text-[11px] text-slate-400 mt-0.5">
            <span>進捗: <strong id="prov-spoke-progress-text" class="text-slate-200">0 / 0</strong></span>
            <span class="text-slate-600">|</span>
            <span id="prov-spoke-accuracy-tag" class="text-slate-400">正答率: --%</span>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-1.5">
        <button id="btn-prov-fit-all" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition" title="全体を表示">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
        </button>
      </div>
    </header>

    <!-- サブコントロールバー -->
    <div class="bg-slate-900/90 border-b border-slate-800 px-3 py-1.5 shrink-0 z-20 flex flex-wrap items-center justify-between gap-2 text-xs">
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar" id="prov-level-tabs">
      </div>

      <div class="flex items-center bg-slate-950 p-0.5 rounded-lg border border-slate-800 shrink-0" id="prov-mode-segment">
        <button class="prov-mode-btn px-2.5 py-1 rounded-md text-[11px] font-bold transition flex items-center gap-1 bg-sky-500 text-white" data-mode="locate">
          <span>🎯</span><span>場所当て</span>
        </button>
        <button class="prov-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="name">
          <span>🔤</span><span>4択</span>
        </button>
        <button class="prov-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="type">
          <span>✍️</span><span>記入</span>
        </button>
        <button class="prov-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="explore">
          <span>🔍</span><span>探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div class="flex-1 relative overflow-hidden">
      <div id="prov-map" class="w-full h-full map-container"></div>

      <!-- 探索ポップオーバー -->
      <div id="prov-explore-card" class="hidden absolute top-3 left-3 z-[1000] bg-slate-900/95 backdrop-blur border border-slate-700/80 rounded-xl p-3 shadow-2xl max-w-xs text-xs space-y-2">
        <div class="flex items-start justify-between gap-2">
          <div>
            <div id="prov-exp-kana" class="text-[10px] text-sky-400">むさし</div>
            <div id="prov-exp-name" class="text-base font-extrabold text-white">武蔵</div>
          </div>
          <button id="btn-prov-close-exp" class="text-slate-400 hover:text-white p-1">✕</button>
        </div>
        <div class="text-[11px] text-slate-300">
          現代の地域: <span id="prov-exp-modern" class="text-slate-100 font-semibold">東京都・埼玉県・神奈川県東部</span>
        </div>
        <div class="bg-slate-950/70 p-2 rounded-lg border border-slate-800 text-[11px] flex justify-between">
          <span class="text-slate-400">学習成績</span>
          <span id="prov-exp-stats" class="text-slate-200 font-bold">正解 0 / 不正解 0</span>
        </div>
        <button id="btn-prov-test-single" class="w-full py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs transition">
          この旧国をテスト 🎯
        </button>
      </div>
    </div>

    <!-- 下部ドック -->
    <div id="prov-dock" class="bg-slate-900/95 backdrop-blur border-t border-slate-800 px-4 py-3 shrink-0 z-20 shadow-2xl">
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 3A: 世界の国名・首都 Hub (地域選択画面) -->
  <!-- ============================================================== -->
  <div id="screen-world-hub" class="hidden flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 py-3 shrink-0 z-10 shadow-lg">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2 sm:gap-3">
          <button class="btn-return-root p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="ホームに戻る">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="hidden sm:inline">ホーム</span>
          </button>
          <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-black text-sm">
            🌍
          </div>
          <div>
            <h2 class="text-sm sm:text-base font-bold text-white flex items-center gap-1.5">
              世界の国名・首都名暗記
              <span class="text-[10px] text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded border border-indigo-500/20">196ヶ国・地域</span>
            </h2>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-[10px] text-slate-400">全世界制覇数</div>
            <div class="text-xs sm:text-sm font-extrabold text-indigo-400">
              <span id="world-hub-cleared">0</span> <span class="text-[10px] text-slate-400">/ 196</span>
              <span id="world-hub-pct" class="text-[10px] font-semibold text-slate-300 ml-0.5">(0.0%)</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- プログレスバー -->
    <div class="w-full bg-slate-900/60 border-b border-slate-800 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-800 h-2 rounded-full overflow-hidden">
          <div id="world-hub-progress-bar" class="bg-gradient-to-r from-indigo-500 to-purple-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-[11px] text-slate-400 whitespace-nowrap">
          制覇地域: <span id="world-hub-completed-regions" class="text-indigo-400 font-bold">0</span> / 6州
        </div>
      </div>
    </div>

    <!-- 世界地域カードグリッド -->
    <main class="flex-1 overflow-y-auto px-4 py-4 overscroll-contain">
      <div class="max-w-6xl mx-auto space-y-4">
        <!-- 苦手克服クイックバナー -->
        <div id="world-weak-banner" class="hidden bg-gradient-to-r from-rose-950/40 to-slate-900 border border-rose-500/30 rounded-xl p-3.5 flex items-center justify-between gap-3 shadow-lg">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold text-lg shrink-0">
              ⚡
            </div>
            <div>
              <div class="text-sm font-bold text-white flex items-center gap-2">
                世界の苦手克服特訓デッキ
                <span id="world-weak-count-badge" class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 text-xs font-semibold">0国</span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">直近で間違えた国・首都を集中トレーニング</p>
            </div>
          </div>
          <button id="btn-world-start-weak-all" class="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm transition shrink-0 active:scale-95 shadow">
            復習スタート →
          </button>
        </div>

        <div id="world-cards-container" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5"></div>
      </div>
    </main>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 3B: 世界の国名・首都 Spoke (クイズ・学習画面) -->
  <!-- ============================================================== -->
  <div id="screen-world-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <!-- Spoke ヘッダー -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 px-3 py-2 shrink-0 z-20 flex items-center justify-between gap-2 shadow-md">
      <div class="flex items-center gap-2 min-w-0">
        <button id="btn-world-back-hub" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="地域一覧に戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">一覧</span>
        </button>
        <button class="btn-return-root p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition" title="ホームに戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        </button>
        <div class="min-w-0">
          <div class="flex items-center gap-1.5">
            <h2 id="world-spoke-title" class="text-sm sm:text-base font-extrabold text-white truncate">全世界</h2>
            <span id="world-spoke-count-badge" class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 shrink-0">196国</span>
          </div>
          <div class="flex items-center gap-2 text-[11px] text-slate-400 mt-0.5">
            <span>進捗: <strong id="world-spoke-progress-text" class="text-slate-200">0 / 0</strong></span>
            <span class="text-slate-600">|</span>
            <span id="world-spoke-accuracy-tag" class="text-slate-400">正答率: --%</span>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-1.5">
        <!-- 4択/場所当ての出題モードトグル (国名 ↔ 首都名) -->
        <div class="flex items-center bg-slate-950 p-0.5 rounded-lg border border-slate-800 text-[11px]" id="world-quiz-target-toggle">
          <button id="btn-world-target-country" class="px-2 py-1 rounded text-white font-bold bg-indigo-600 transition" title="国名を問う">🗺️ 国名</button>
          <button id="btn-world-target-capital" class="px-2 py-1 rounded text-slate-400 hover:text-white transition" title="首都名を問う">🏛️ 首都</button>
        </div>

        <button id="btn-world-fit-all" class="p-1.5 sm:p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition" title="地域全体を表示">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
        </button>
      </div>
    </header>

    <!-- サブコントロールバー -->
    <div class="bg-slate-900/90 border-b border-slate-800 px-3 py-1.5 shrink-0 z-20 flex flex-wrap items-center justify-between gap-2 text-xs">
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar" id="world-level-tabs">
      </div>

      <div class="flex items-center bg-slate-950 p-0.5 rounded-lg border border-slate-800 shrink-0" id="world-mode-segment">
        <button class="world-mode-btn px-2.5 py-1 rounded-md text-[11px] font-bold transition flex items-center gap-1 bg-indigo-500 text-white" data-mode="locate">
          <span>🎯</span><span>場所当て</span>
        </button>
        <button class="world-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="name">
          <span>🔤</span><span>4択</span>
        </button>
        <button class="world-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="type">
          <span>✍️</span><span>記入</span>
        </button>
        <button class="world-mode-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-slate-400 hover:text-white transition flex items-center gap-1" data-mode="explore">
          <span>🔍</span><span>探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div class="flex-1 relative overflow-hidden">
      <div id="world-map" class="w-full h-full map-container"></div>

      <!-- 探索ポップオーバー -->
      <div id="world-explore-card" class="hidden absolute top-3 left-3 z-[1000] bg-slate-900/95 backdrop-blur border border-slate-700/80 rounded-xl p-3.5 shadow-2xl max-w-xs text-xs space-y-2.5">
        <div class="flex items-start justify-between gap-2">
          <div class="flex items-center gap-2">
            <span id="world-exp-flag" class="text-2xl">🇯🇵</span>
            <div>
              <div id="world-exp-kana" class="text-[10px] text-indigo-400">ふらんす</div>
              <div id="world-exp-name" class="text-base font-extrabold text-white">フランス</div>
            </div>
          </div>
          <button id="btn-world-close-exp" class="text-slate-400 hover:text-white p-1">✕</button>
        </div>
        <div class="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800 space-y-1.5 text-[11px]">
          <div class="flex justify-between">
            <span class="text-slate-400">🏛️ 首都</span>
            <span id="world-exp-capital" class="text-white font-bold">パリ (ぱり)</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-400">🌍 地域 / ISO</span>
            <span id="world-exp-region" class="text-slate-300">ヨーロッパ (FRA)</span>
          </div>
          <div class="flex justify-between pt-1 border-t border-slate-800">
            <span class="text-slate-400">📊 学習成績</span>
            <span id="world-exp-stats" class="text-slate-200 font-bold">正解 0 / 不正解 0</span>
          </div>
        </div>
        <button id="btn-world-test-single" class="w-full py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition">
          この国をテスト 🎯
        </button>
      </div>
    </div>

    <!-- 下部ドック -->
    <div id="world-dock" class="bg-slate-900/95 backdrop-blur border-t border-slate-800 px-4 py-3 shrink-0 z-20 shadow-2xl">
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 共通モーダル: データ管理 & 設定 -->
  <!-- ============================================================== -->
  <div id="modal-data-mgr" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-5 space-y-4 shadow-2xl">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <span>⚙️</span>
          <span>データ管理 & 設定</span>
        </h3>
        <button id="btn-close-data-mgr" class="text-slate-400 hover:text-white p-1">✕</button>
      </div>

      <div class="space-y-3 text-xs">
        <div class="bg-slate-950/70 p-3 rounded-xl border border-slate-800 space-y-2">
          <div class="font-bold text-slate-300">各モジュールの学習データリセット</div>
          <div class="grid grid-cols-3 gap-2">
            <button id="btn-reset-muni-data" class="py-1.5 px-2 rounded bg-slate-800 hover:bg-rose-950 hover:text-rose-400 text-slate-300 transition text-[11px] font-medium border border-slate-700">
              🗾 市区町村
            </button>
            <button id="btn-reset-prov-data" class="py-1.5 px-2 rounded bg-slate-800 hover:bg-rose-950 hover:text-rose-400 text-slate-300 transition text-[11px] font-medium border border-slate-700">
              📜 令制国
            </button>
            <button id="btn-reset-world-data" class="py-1.5 px-2 rounded bg-slate-800 hover:bg-rose-950 hover:text-rose-400 text-slate-300 transition text-[11px] font-medium border border-slate-700">
              🌍 世界の国
            </button>
          </div>
        </div>

        <div class="bg-slate-950/70 p-3 rounded-xl border border-slate-800 space-y-2">
          <div class="font-bold text-slate-300">データのエクスポート / インポート</div>
          <p class="text-slate-400 text-[11px]">学習履歴（正誤回数、制覇記録）をJSON形式でバックアップ・移行できます。</p>
          <div class="flex gap-2">
            <button id="btn-export-all-data" class="flex-1 py-1.5 rounded bg-sky-600 hover:bg-sky-500 text-white font-bold transition text-[11px]">
              📥 バックアップ出力
            </button>
            <button id="btn-import-all-data" class="flex-1 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold transition text-[11px] border border-slate-700">
              📤 バックアップ読込
            </button>
            <input type="file" id="file-import-data" class="hidden" accept=".json" />
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 埋め込みデータセット -->
  <!-- ============================================================== -->
  <script>
    const MUNI_RAW_DATA = {muni_json};
    const WARD_TO_CITY = {ward_json};
    const PREFECTURES = {pref_json};

    const PROVINCES_MASTER = {prov_master_json};
    const PROVINCES_GEOJSON = {prov_geo_json};
    const DOH_LIST = {doh_json};

    const WORLD_MASTER = {world_master_json};
    const WORLD_GEOJSON = {world_geo_json};
    const WORLD_REGIONS = {world_regions_json};
  </script>

  <!-- ============================================================== -->
  <!-- メインスクリプト (統合システム & 各モジュール) -->
  <!-- ============================================================== -->
  <script>
    // --- 共通ユーティリティ: 国旗絵文字生成 ---
    function getFlagEmoji(alpha2) {{
      if (!alpha2 || alpha2.length !== 2) return '🌐';
      const codePoints = [...alpha2.toUpperCase()].map(c => 127397 + c.charCodeAt(0));
      return String.fromCodePoint(...codePoints);
    }}

    // --- 共通サウンドエンジン (Web Audio API 内蔵オシレーター) ---
    class SoundEngine {{
      constructor() {{
        this.ctx = null;
        this.enabled = true;
      }}
      init() {{
        if (!this.ctx) {{
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) this.ctx = new AudioContext();
        }}
        if (this.ctx && this.ctx.state === 'suspended') {{
          this.ctx.resume();
        }}
      }}
      playTone(freq, type, duration, delay = 0, gainLevel = 0.15) {{
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime + delay;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, now);
        gain.gain.setValueAtTime(gainLevel, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + duration);
      }}
      correct() {{
        // 上昇和音アルペジオ (D5 587Hz -> A5 880Hz)
        this.playTone(587.33, 'sine', 0.18, 0, 0.2);
        this.playTone(880.00, 'sine', 0.25, 0.08, 0.22);
      }}
      wrong() {{
        // 下降濁和音 (220Hz -> 174Hz)
        this.playTone(220, 'sawtooth', 0.22, 0, 0.15);
        this.playTone(174.61, 'sawtooth', 0.25, 0.08, 0.15);
      }}
      fanfare() {{
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((f, i) => this.playTone(f, 'sine', 0.35, i * 0.1, 0.25));
      }}
    }}
    const sound = new SoundEngine();

    // --- 共通ストレージ管理 ---
    const STORAGE = {{
      get(key, defaultVal) {{
        try {{
          const item = localStorage.getItem(key);
          return item ? JSON.parse(item) : defaultVal;
        }} catch(e) {{
          return defaultVal;
        }}
      }},
      set(key, val) {{
        try {{
          localStorage.setItem(key, JSON.stringify(val));
        }} catch(e) {{}}
      }}
    }};

    // キー名
    const KEYS = {{
      MUNI: 'geoanki_muni_v1',
      PROV: 'geoanki_province_v1',
      WORLD: 'geoanki_world_v1'
    }};

    // --- ルーティング & 画面切り替え ---
    const AppRouter = {{
      currentScreen: 'screen-root-hub',
      screens: [
        'screen-root-hub',
        'screen-muni-hub',
        'screen-muni-spoke',
        'screen-prov-hub',
        'screen-prov-spoke',
        'screen-world-hub',
        'screen-world-spoke'
      ],
      navigate(targetScreenId) {{
        this.screens.forEach(id => {{
          const el = document.getElementById(id);
          if (el) {{
            if (id === targetScreenId) el.classList.remove('hidden');
            else el.classList.add('hidden');
          }}
        }});
        this.currentScreen = targetScreenId;

        // Leaflet マップのリサイズ再計算
        setTimeout(() => {{
          if (targetScreenId === 'screen-muni-spoke' && MuniApp.map) MuniApp.map.invalidateSize();
          if (targetScreenId === 'screen-prov-spoke' && ProvApp.map) ProvApp.map.invalidateSize();
          if (targetScreenId === 'screen-world-spoke' && WorldApp.map) WorldApp.map.invalidateSize();
        }}, 50);

        if (targetScreenId === 'screen-root-hub') {{
          RootHub.updateSummaries();
        }}
      }}
    }};

    // --- Root Hub (ランチャー画面管理) ---
    const RootHub = {{
      init() {{
        // ボタンイベント
        document.getElementById('btn-enter-muni').onclick = () => {{
          sound.init();
          AppRouter.navigate('screen-muni-hub');
          MuniApp.renderHub();
        }};
        document.getElementById('btn-enter-province').onclick = () => {{
          sound.init();
          AppRouter.navigate('screen-prov-hub');
          ProvApp.renderHub();
        }};
        document.getElementById('btn-enter-world').onclick = () => {{
          sound.init();
          AppRouter.navigate('screen-world-hub');
          WorldApp.renderHub();
        }};

        // 各画面のホームに戻るボタン
        document.querySelectorAll('.btn-return-root').forEach(btn => {{
          btn.onclick = () => AppRouter.navigate('screen-root-hub');
        }});

        // グローバルサウンドトグル
        const btnSound = document.getElementById('btn-global-sound');
        const iconOn = document.getElementById('global-sound-icon-on');
        const iconOff = document.getElementById('global-sound-icon-off');
        const updateSoundUI = () => {{
          if (sound.enabled) {{
            iconOn.classList.remove('hidden');
            iconOff.classList.add('hidden');
          }} else {{
            iconOn.classList.add('hidden');
            iconOff.classList.remove('hidden');
          }}
        }};
        btnSound.onclick = () => {{
          sound.enabled = !sound.enabled;
          STORAGE.set('geoanki_sound_enabled', sound.enabled);
          updateSoundUI();
          if (sound.enabled) sound.correct();
        }};
        sound.enabled = STORAGE.get('geoanki_sound_enabled', true);
        updateSoundUI();

        // データ管理モーダル
        const modal = document.getElementById('modal-data-mgr');
        document.getElementById('btn-show-data-mgr').onclick = () => modal.classList.remove('hidden');
        document.getElementById('btn-close-data-mgr').onclick = () => modal.classList.add('hidden');

        // リセットボタン群
        document.getElementById('btn-reset-muni-data').onclick = () => {{
          if (confirm('市区町村の全学習データをリセットしますか？この操作は取り消せません。')) {{
            localStorage.removeItem(KEYS.MUNI);
            RootHub.updateSummaries();
            MuniApp.data = {{ records: {{}} }};
            alert('市区町村データをリセットしました。');
          }}
        }};
        document.getElementById('btn-reset-prov-data').onclick = () => {{
          if (confirm('令制国（旧国名）の全学習データをリセットしますか？')) {{
            localStorage.removeItem(KEYS.PROV);
            RootHub.updateSummaries();
            ProvApp.data = {{ records: {{}} }};
            alert('令制国データをリセットしました。');
          }}
        }};
        document.getElementById('btn-reset-world-data').onclick = () => {{
          if (confirm('世界の国名・首都の全学習データをリセットしますか？')) {{
            localStorage.removeItem(KEYS.WORLD);
            RootHub.updateSummaries();
            WorldApp.data = {{ records: {{}} }};
            alert('世界の国名・首都データをリセットしました。');
          }}
        }};

        // エクスポート・インポート
        document.getElementById('btn-export-all-data').onclick = () => {{
          const backup = {{
            muni: STORAGE.get(KEYS.MUNI, {{ records: {{}} }}),
            prov: STORAGE.get(KEYS.PROV, {{ records: {{}} }}),
            world: STORAGE.get(KEYS.WORLD, {{ records: {{}} }}),
            timestamp: Date.now()
          }};
          const blob = new Blob([JSON.stringify(backup, null, 2)], {{ type: 'application/json' }});
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `geoanki_suite_backup_${{new Date().toISOString().slice(0, 10)}}.json`;
          a.click();
          URL.revokeObjectURL(url);
        }};

        const fileInput = document.getElementById('file-import-data');
        document.getElementById('btn-import-all-data').onclick = () => fileInput.click();
        fileInput.onchange = (e) => {{
          const file = e.target.files[0];
          if (!file) return;
          const reader = new FileReader();
          reader.onload = (evt) => {{
            try {{
              const d = JSON.parse(evt.target.result);
              if (d.muni) STORAGE.set(KEYS.MUNI, d.muni);
              if (d.prov) STORAGE.set(KEYS.PROV, d.prov);
              if (d.world) STORAGE.set(KEYS.WORLD, d.world);
              alert('バックアップデータを正常に読み込みました。');
              modal.classList.add('hidden');
              RootHub.updateSummaries();
            }} catch(err) {{
              alert('JSONファイルの解析に失敗しました。');
            }}
          }};
          reader.readAsText(file);
        }};

        this.updateSummaries();
      }},

      updateSummaries() {{
        // 1. 市区町村
        const muniStorage = STORAGE.get(KEYS.MUNI, {{ records: {{}} }});
        const muniRecs = muniStorage.records || {{}};
        let muniCleared = 0, muniCorrect = 0, muniWrong = 0, muniWeak = 0;
        Object.values(muniRecs).forEach(r => {{
          if (r.correct > 0) muniCleared++;
          muniCorrect += (r.correct || 0);
          muniWrong += (r.wrong || 0);
          if (r.last === 'wrong') muniWeak++;
        }});
        const muniTotal = MUNI_RAW_DATA.length;
        const muniPct = ((muniCleared / muniTotal) * 100).toFixed(1);
        const muniAcc = (muniCorrect + muniWrong > 0) ? Math.round((muniCorrect / (muniCorrect + muniWrong)) * 100) + '%' : '--%';

        document.getElementById('root-muni-cleared').textContent = muniCleared;
        document.getElementById('root-muni-pct').textContent = muniPct + '%';
        document.getElementById('root-muni-bar').style.width = muniPct + '%';
        document.getElementById('root-muni-acc').textContent = muniAcc;
        document.getElementById('root-muni-weak-badge').textContent = `弱点: ${{muniWeak}}`;

        // 2. 令制国
        const provStorage = STORAGE.get(KEYS.PROV, {{ records: {{}} }});
        const provRecs = provStorage.records || {{}};
        let provCleared = 0, provCorrect = 0, provWrong = 0, provWeak = 0;
        Object.values(provRecs).forEach(r => {{
          if (r.correct > 0) provCleared++;
          provCorrect += (r.correct || 0);
          provWrong += (r.wrong || 0);
          if (r.last === 'wrong') provWeak++;
        }});
        const provTotal = Object.keys(PROVINCES_MASTER).length;
        const provPct = ((provCleared / provTotal) * 100).toFixed(1);
        const provAcc = (provCorrect + provWrong > 0) ? Math.round((provCorrect / (provCorrect + provWrong)) * 100) + '%' : '--%';

        document.getElementById('root-prov-cleared').textContent = provCleared;
        document.getElementById('root-prov-pct').textContent = provPct + '%';
        document.getElementById('root-prov-bar').style.width = provPct + '%';
        document.getElementById('root-prov-acc').textContent = provAcc;
        document.getElementById('root-prov-weak-badge').textContent = `弱点: ${{provWeak}}`;

        // 3. 世界の国
        const worldStorage = STORAGE.get(KEYS.WORLD, {{ records: {{}} }});
        const worldRecs = worldStorage.records || {{}};
        let worldCleared = 0, worldCorrect = 0, worldWrong = 0, worldWeak = 0;
        Object.values(worldRecs).forEach(r => {{
          if (r.correct > 0) worldCleared++;
          worldCorrect += (r.correct || 0);
          worldWrong += (r.wrong || 0);
          if (r.last === 'wrong') worldWeak++;
        }});
        const worldTotal = Object.keys(WORLD_MASTER).length;
        const worldPct = ((worldCleared / worldTotal) * 100).toFixed(1);
        const worldAcc = (worldCorrect + worldWrong > 0) ? Math.round((worldCorrect / (worldCorrect + worldWrong)) * 100) + '%' : '--%';

        document.getElementById('root-world-cleared').textContent = worldCleared;
        document.getElementById('root-world-pct').textContent = worldPct + '%';
        document.getElementById('root-world-bar').style.width = worldPct + '%';
        document.getElementById('root-world-acc').textContent = worldAcc;
        document.getElementById('root-world-weak-badge').textContent = `弱点: ${{worldWeak}}`;
      }}
    }};

    // ==============================================================
    // モジュール 1: 市区町村暗記 (MuniApp)
    // ==============================================================
    const MuniApp = {{
      data: null,
      map: null,
      currentPref: null,
      currentGeoJson: null,
      geoJsonLayer: null,
      wardOuterLayer: null,
      currentLevel: 'ALL',
      currentMode: 'locate',
      questionPool: [],
      currentIndex: 0,
      currentQuestion: null,
      isAnswered: false,
      activeRegionFilter: 'ALL',
      geoJsonCache: {{}},

      init() {{
        this.data = STORAGE.get(KEYS.MUNI, {{ records: {{}} }});
        if (!this.data.records) this.data.records = {{}};

        // フィルターボタン
        document.querySelectorAll('.muni-filter-btn').forEach(btn => {{
          btn.onclick = () => {{
            document.querySelectorAll('.muni-filter-btn').forEach(b => {{
              b.classList.remove('bg-emerald-500', 'text-white');
              b.classList.add('bg-slate-800', 'text-slate-300');
            }});
            btn.classList.add('bg-emerald-500', 'text-white');
            btn.classList.remove('bg-slate-800', 'text-slate-300');
            this.activeRegionFilter = btn.dataset.region;
            this.renderHub();
          }};
        }});

        // Spokeから一覧に戻る
        document.getElementById('btn-muni-back-hub').onclick = () => {{
          AppRouter.navigate('screen-muni-hub');
          this.renderHub();
        }};

        // モードボタン
        document.querySelectorAll('.muni-mode-btn').forEach(btn => {{
          btn.onclick = () => {{
            this.setMode(btn.dataset.mode);
          }};
        }});

        // 探索ポップアップ
        document.getElementById('btn-muni-close-exp').onclick = () => {{
          document.getElementById('muni-explore-card').classList.add('hidden');
        }};
        document.getElementById('btn-muni-test-single').onclick = () => {{
          if (this.selectedMuni) {{
            document.getElementById('muni-explore-card').classList.add('hidden');
            this.setMode('locate');
            this.startSingleQuestion(this.selectedMuni);
          }}
        }};

        // 県データリセット
        document.getElementById('btn-muni-reset-pref').onclick = () => {{
          if (!this.currentPref) return;
          if (confirm(`${{this.currentPref.name}}の学習データをリセットしますか？`)) {{
            const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code);
            prefMunis.forEach(m => delete this.data.records[m[0]]);
            STORAGE.set(KEYS.MUNI, this.data);
            this.updateHeaderProgress();
            this.startLevel(this.currentLevel);
          }}
        }};

        // キーボード操作
        window.addEventListener('keydown', (e) => {{
          if (AppRouter.currentScreen !== 'screen-muni-spoke') return;
          if (e.target.tagName === 'INPUT' && e.key !== 'Enter') return;
          this.handleKey(e);
        }});
      }},

      renderHub() {{
        const container = document.getElementById('muni-hub-container');
        container.innerHTML = '';

        // 進捗集計
        let totalCleared = 0;
        let completedPrefsCount = 0;
        const muniByPref = {{}};
        MUNI_RAW_DATA.forEach(m => {{
          const p = m[1];
          if (!muniByPref[p]) muniByPref[p] = [];
          muniByPref[p].push(m);
        }});

        PREFECTURES.forEach(p => {{
          const list = muniByPref[p.code] || [];
          let cleared = 0;
          list.forEach(m => {{
            if (this.data.records[m[0]] && this.data.records[m[0]].correct > 0) cleared++;
          }});
          if (cleared === list.length && list.length > 0) completedPrefsCount++;
          totalCleared += cleared;
        }});

        const totalMuni = MUNI_RAW_DATA.length;
        const totalPct = ((totalCleared / totalMuni) * 100).toFixed(1);
        document.getElementById('muni-hub-cleared').textContent = totalCleared;
        document.getElementById('muni-hub-pct').textContent = totalPct + '%';
        document.getElementById('muni-hub-progress-bar').style.width = totalPct + '%';
        document.getElementById('muni-hub-completed-prefs').textContent = completedPrefsCount;

        // 地方ごとにグルーピング
        const regions = ['北海道', '東北', '関東', '中部', '近畿', '中国', '四国', '九州・沖縄'];
        regions.forEach(reg => {{
          if (this.activeRegionFilter !== 'ALL' && this.activeRegionFilter !== reg) return;
          const prefs = PREFECTURES.filter(p => p.region === reg);
          if (prefs.length === 0) return;

          const section = document.createElement('div');
          section.className = 'space-y-3';
          section.innerHTML = `
            <div class="flex items-center gap-2 border-b border-slate-800 pb-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h3 class="text-sm font-bold text-slate-200">${{reg}}</h3>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2.5"></div>
          `;
          const grid = section.querySelector('div.grid');

          prefs.forEach(pref => {{
            const list = muniByPref[pref.code] || [];
            let clr = 0;
            list.forEach(m => {{
              if (this.data.records[m[0]] && this.data.records[m[0]].correct > 0) clr++;
            }});
            const isComp = clr === list.length && list.length > 0;
            const pct = list.length > 0 ? Math.round((clr / list.length) * 100) : 0;

            const card = document.createElement('div');
            card.className = `p-3 rounded-xl border cursor-pointer transition active:scale-98 ${{
              isComp
                ? 'bg-emerald-950/30 border-emerald-500/40 hover:border-emerald-400'
                : 'bg-slate-900 border-slate-800 hover:border-slate-700'
            }} flex flex-col justify-between`;

            card.innerHTML = `
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-white">${{pref.name}}</span>
                ${{isComp ? '<span class="text-[10px] text-emerald-400 font-bold">制覇!</span>' : ''}}
              </div>
              <div class="mt-2 space-y-1">
                <div class="flex justify-between text-[10px] text-slate-400">
                  <span>${{clr}} / ${{list.length}}</span>
                  <span>${{pct}}%</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-emerald-500 h-full" style="width: ${{pct}}%"></div>
                </div>
              </div>
            `;

            card.onclick = () => this.openPref(pref);
            grid.appendChild(card);
          }});

          container.appendChild(section);
        }});
      }},

      async openPref(pref) {{
        this.currentPref = pref;
        AppRouter.navigate('screen-muni-spoke');
        document.getElementById('muni-spoke-pref-title').textContent = pref.name;

        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === pref.code);
        document.getElementById('muni-spoke-pref-count-badge').textContent = `${{prefMunis.length}}自治体`;

        this.updateHeaderProgress();

        // 地図初期化
        if (!this.map) {{
          this.map = L.map('muni-map', {{
            attributionControl: false,
            zoomControl: false,
            renderer: L.svg({{ padding: 1.5 }})
          }});
          L.control.zoom({{ position: 'bottomright' }}).addTo(this.map);
        }}

        // 離島ボタンの構築
        const islandContainer = document.getElementById('muni-island-buttons');
        islandContainer.innerHTML = '';
        if (pref.islands && pref.islands.length > 0) {{
          pref.islands.forEach(isl => {{
            const btn = document.createElement('button');
            btn.className = 'px-2 py-1 rounded bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700 text-[10px] font-bold shadow-lg';
            btn.textContent = `📍 ${{isl.label}}`;
            btn.onclick = () => this.map.fitBounds(isl.bounds, {{ padding: [20, 20], animate: true }});
            islandContainer.appendChild(btn);
          }});
        }}

        // GeoJSON のロード (二重化CDN)
        await this.loadGeoJson(pref.code);

        // レベルタブ構築 & 開始
        this.renderLevelTabs();
        this.startLevel('ALL');
      }},

      async loadGeoJson(prefCode) {{
        if (this.geoJsonCache[prefCode]) {{
          this.currentGeoJson = this.geoJsonCache[prefCode];
          return;
        }}

        // ロード中表示
        const cdn1 = `https://cdn.jsdelivr.net/gh/64bitfloat/Japanese_municipalities@main/data/geojson/${{prefCode}}.geojson`;
        const cdn2 = `https://raw.githubusercontent.com/64bitfloat/Japanese_municipalities/main/data/geojson/${{prefCode}}.geojson`;

        try {{
          let resp = await fetch(cdn1);
          if (!resp.ok) resp = await fetch(cdn2);
          if (resp.ok) {{
            const data = await resp.json();
            this.geoJsonCache[prefCode] = data;
            this.currentGeoJson = data;
          }}
        }} catch(e) {{
          console.error("GeoJSON load failed:", e);
        }}
      }},

      renderLevelTabs() {{
        const container = document.getElementById('muni-level-tabs');
        container.innerHTML = '';

        const levels = [
          {{ id: 'ALL', name: '全自治体' }},
          {{ id: 1, name: 'Lv.1 主要都市' }},
          {{ id: 2, name: 'Lv.2 市' }},
          {{ id: 3, name: 'Lv.3 町' }},
          {{ id: 4, name: 'Lv.4 村' }},
          {{ id: 'WEAK', name: '⚠️ 弱点復習' }}
        ];

        levels.forEach(lvl => {{
          const btn = document.createElement('button');
          btn.className = `muni-lvl-btn px-2.5 py-1 rounded-md text-[11px] font-semibold whitespace-nowrap transition ${{
            this.currentLevel === lvl.id
              ? 'bg-emerald-500 text-white'
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
          }}`;
          btn.textContent = lvl.name;
          btn.onclick = () => {{
            this.startLevel(lvl.id);
          }};
          container.appendChild(btn);
        }});
      }},

      startLevel(levelId) {{
        this.currentLevel = levelId;
        document.querySelectorAll('.muni-lvl-btn').forEach(btn => {{
          btn.classList.remove('bg-emerald-500', 'text-white');
          btn.classList.add('bg-slate-800', 'text-slate-300');
        }});
        const activeBtn = [...document.querySelectorAll('.muni-lvl-btn')].find(b => b.textContent.includes(levelId === 'ALL' ? '全' : levelId === 'WEAK' ? '弱点' : `Lv.${{levelId}}`));
        if (activeBtn) {{
          activeBtn.classList.add('bg-emerald-500', 'text-white');
          activeBtn.classList.remove('bg-slate-800', 'text-slate-300');
        }}

        // 問題プール抽出
        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code);
        if (levelId === 'ALL') {{
          this.questionPool = [...prefMunis];
        }} else if (levelId === 'WEAK') {{
          this.questionPool = prefMunis.filter(m => {{
            const rec = this.data.records[m[0]];
            return rec && rec.last === 'wrong';
          }});
          if (this.questionPool.length === 0) {{
            alert('弱点の自治体はありません！素晴らしい！');
            this.startLevel('ALL');
            return;
          }}
        }} else {{
          this.questionPool = prefMunis.filter(m => m[6] === levelId);
          if (this.questionPool.length === 0) {{
            alert('この難易度の自治体はこの県には存在しません。');
            this.startLevel('ALL');
            return;
          }}
        }}

        // シャッフル
        this.questionPool.sort(() => Math.random() - 0.5);
        this.currentIndex = 0;

        // 地図レイヤーの描画
        this.renderMapLayers();
        this.nextQuestion();
      }},

      renderMapLayers() {{
        if (!this.map || !this.currentGeoJson) return;

        if (this.geoJsonLayer) this.map.removeLayer(this.geoJsonLayer);
        if (this.wardOuterLayer) this.map.removeLayer(this.wardOuterLayer);

        const targetCodes = new Set(this.questionPool.map(m => m[0]));

        this.geoJsonLayer = L.geoJSON(this.currentGeoJson, {{
          style: (feature) => {{
            let code = String(feature.properties.N03_007 || feature.properties.code || '');
            const isTarget = targetCodes.has(code) || (WARD_TO_CITY[code] && targetCodes.has(WARD_TO_CITY[code]));
            return {{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.65,
              color: '#090d16',
              weight: 1.2,
              opacity: 1
            }};
          }},
          onEachFeature: (feature, layer) => {{
            layer.on({{
              mouseover: (e) => {{
                if (this.currentMode === 'locate' || this.currentMode === 'explore') {{
                  e.target.setStyle({{ fillColor: '#e2e8f0', fillOpacity: 1 }});
                }}
              }},
              mouseout: (e) => {{
                if (this.geoJsonLayer) this.geoJsonLayer.resetStyle(e.target);
              }},
              click: (e) => {{
                this.onPolygonClick(feature, layer);
              }}
            }});
          }}
        }}).addTo(this.map);

        if (this.currentPref.defaultView) {{
          this.map.fitBounds(this.currentPref.defaultView, {{ padding: [20, 20] }});
        }} else {{
          this.map.fitBounds(this.geoJsonLayer.getBounds(), {{ padding: [20, 20] }});
        }}
      }},

      setMode(mode) {{
        this.currentMode = mode;
        document.querySelectorAll('.muni-mode-btn').forEach(btn => {{
          btn.classList.remove('bg-emerald-500', 'text-white');
          btn.classList.add('text-slate-400');
        }});
        const active = [...document.querySelectorAll('.muni-mode-btn')].find(b => b.dataset.mode === mode);
        if (active) {{
          active.classList.add('bg-emerald-500', 'text-white');
          active.classList.remove('text-slate-400');
        }}
        this.nextQuestion();
      }},

      nextQuestion() {{
        this.isAnswered = false;
        if (this.currentMode === 'explore') {{
          this.renderExploreDock();
          return;
        }}

        if (this.currentIndex >= this.questionPool.length) {{
          sound.fanfare();
          alert('このレベルの全問題を完了しました！');
          this.startLevel(this.currentLevel);
          return;
        }}

        this.currentQuestion = this.questionPool[this.currentIndex];
        this.updateHeaderProgress();

        if (this.currentMode === 'locate') {{
          this.renderLocateDock();
        }} else if (this.currentMode === 'name') {{
          this.highlightQuestionPolygon();
          this.renderNameDock();
        }} else if (this.currentMode === 'type') {{
          this.highlightQuestionPolygon();
          this.renderTypeDock();
        }}
      }},

      highlightQuestionPolygon() {{
        if (!this.geoJsonLayer || !this.currentQuestion) return;
        const code = this.currentQuestion[0];
        this.geoJsonLayer.eachLayer(layer => {{
          const featCode = String(layer.feature.properties.N03_007 || layer.feature.properties.code || '');
          if (featCode === code || WARD_TO_CITY[featCode] === code) {{
            layer.setStyle({{ fillColor: '#fbbf24', fillOpacity: 0.95, weight: 3, color: '#f59e0b' }});
            // 画面中央へ
            if (layer.getBounds) {{
              this.map.flyToBounds(layer.getBounds(), {{ maxZoom: 10.5, duration: 0.5 }});
            }}
          }} else {{
            this.geoJsonLayer.resetStyle(layer);
          }}
        }});
      }},

      renderLocateDock() {{
        const dock = document.getElementById('muni-dock');
        const q = this.currentQuestion;
        const rec = this.data.records[q[0]] || {{ correct: 0, wrong: 0 }};
        const total = rec.correct + rec.wrong;
        const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';

        dock.innerHTML = `
          <div class="max-w-xl mx-auto flex items-center justify-between gap-3">
            <div>
              <div class="text-[11px] text-emerald-400">${{q[4]}}</div>
              <div class="text-lg font-black text-white flex items-center gap-2">
                <span>${{q[3]}}</span>
                <span class="text-xs font-normal text-slate-400">はどこ？</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">過去正答率: ${{pct}}</span>
            </div>
          </div>
        `;
      }},

      renderNameDock() {{
        const dock = document.getElementById('muni-dock');
        const q = this.currentQuestion;

        // ダミー選択肢抽出 (同県、なるべく同Level)
        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code && m[0] !== q[0]);
        prefMunis.sort(() => Math.random() - 0.5);
        const choices = [q, ...prefMunis.slice(0, 3)].sort(() => Math.random() - 0.5);

        let buttonsHtml = '';
        choices.forEach((c, idx) => {{
          buttonsHtml += `
            <button class="muni-choice-btn py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition flex items-center gap-2 active:scale-95" data-code="${{c[0]}}">
              <span class="w-5 h-5 rounded bg-slate-900 text-slate-400 flex items-center justify-center text-[10px] font-mono">${{idx + 1}}</span>
              <span class="truncate">${{c[3]}}</span>
            </button>
          `;
        }});

        dock.innerHTML = `
          <div class="max-w-xl mx-auto space-y-2">
            <div class="text-xs text-slate-400 flex justify-between">
              <span>イエロー点滅の自治体名を選択してください</span>
              <span>[1] - [4] キー対応</span>
            </div>
            <div class="grid grid-cols-2 gap-2" id="muni-choices-grid">
              ${{buttonsHtml}}
            </div>
          </div>
        `;

        dock.querySelectorAll('.muni-choice-btn').forEach(btn => {{
          btn.onclick = () => this.handleAnswer(btn.dataset.code === q[0], btn);
        }});
      }},

      renderTypeDock() {{
        const dock = document.getElementById('muni-dock');
        const q = this.currentQuestion;

        dock.innerHTML = `
          <div class="max-w-xl mx-auto space-y-2">
            <div class="text-xs text-slate-400">点滅している自治体の正式名称（市・町・村まで）を入力</div>
            <form id="muni-type-form" class="flex gap-2">
              <input type="text" id="muni-type-input" class="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500 font-bold" placeholder="例: ${{q[3]}}" autofocus autocomplete="off" />
              <button type="submit" class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow transition">回答</button>
            </form>
          </div>
        `;

        const form = document.getElementById('muni-type-form');
        const input = document.getElementById('muni-type-input');
        input.focus();

        form.onsubmit = (e) => {{
          e.preventDefault();
          if (this.isAnswered) {{
            this.currentIndex++;
            this.nextQuestion();
            return;
          }}
          const val = input.value.trim();
          const isCorrect = (val === q[3] || val === q[4]);
          this.handleAnswer(isCorrect, input);
        }};
      }},

      renderExploreDock() {{
        const dock = document.getElementById('muni-dock');
        dock.innerHTML = `
          <div class="max-w-xl mx-auto text-center text-xs text-slate-400">
            地図上のポリゴンを自由にタップして、自治体の名前や情報を確認できます。
          </div>
        `;
      }},

      onPolygonClick(feature, layer) {{
        let code = String(feature.properties.N03_007 || feature.properties.code || '');
        if (WARD_TO_CITY[code]) code = WARD_TO_CITY[code];

        const targetMuni = MUNI_RAW_DATA.find(m => m[0] === code);
        if (!targetMuni) return;

        if (this.currentMode === 'locate') {{
          if (this.isAnswered) return;
          const isCorrect = (code === this.currentQuestion[0]);
          this.handleAnswer(isCorrect, layer);
        }} else if (this.currentMode === 'explore') {{
          this.selectedMuni = targetMuni;
          const card = document.getElementById('muni-explore-card');
          card.classList.remove('hidden');
          document.getElementById('muni-exp-kana').textContent = targetMuni[4];
          document.getElementById('muni-exp-name').textContent = targetMuni[3];
          document.getElementById('muni-exp-type').textContent = targetMuni[5];
          document.getElementById('muni-exp-code').textContent = targetMuni[0];

          const rec = this.data.records[targetMuni[0]] || {{ correct: 0, wrong: 0 }};
          document.getElementById('muni-exp-stats').textContent = `正解 ${{rec.correct}} / 不正解 ${{rec.wrong}}`;
        }}
      }},

      handleAnswer(isCorrect, targetEl) {{
        if (this.isAnswered) return;
        this.isAnswered = true;

        const q = this.currentQuestion;
        if (!this.data.records[q[0]]) this.data.records[q[0]] = {{ correct: 0, wrong: 0 }};
        const rec = this.data.records[q[0]];

        if (isCorrect) {{
          sound.correct();
          rec.correct++;
          rec.last = 'correct';
          rec.updated = Date.now();
          STORAGE.set(KEYS.MUNI, this.data);

          if (this.currentMode === 'locate') {{
            if (targetEl && targetEl.setStyle) targetEl.setStyle({{ fillColor: '#34d399', fillOpacity: 0.95 }});
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-emerald-600', '!border-emerald-400');
          }}
          setTimeout(() => {{
            this.currentIndex++;
            this.nextQuestion();
          }}, 900);
        }} else {{
          sound.wrong();
          rec.wrong++;
          rec.last = 'wrong';
          rec.updated = Date.now();
          STORAGE.set(KEYS.MUNI, this.data);

          if (this.currentMode === 'locate') {{
            if (targetEl && targetEl.setStyle) targetEl.setStyle({{ fillColor: '#f87171', fillOpacity: 0.95 }});
            // 正解ポリゴンをハイライト
            this.highlightQuestionPolygon();
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-rose-700');
            // 正解ボタンを緑枠に
            const correctBtn = document.querySelector(`.muni-choice-btn[data-code="${{q[0]}}"]`);
            if (correctBtn) correctBtn.classList.add('!border-emerald-400', '!border-2');
          }} else if (this.currentMode === 'type') {{
            targetEl.classList.add('!border-rose-500');
            targetEl.value = `正解: ${{q[3]}} (Enterで次へ)`;
          }}
        }}
      }},

      handleKey(e) {{
        if (this.currentMode === 'name') {{
          const num = parseInt(e.key);
          if (num >= 1 && num <= 4) {{
            const btns = document.querySelectorAll('.muni-choice-btn');
            if (btns[num - 1]) btns[num - 1].click();
          }}
        }}
        if (e.key === 'Enter' && this.isAnswered) {{
          this.currentIndex++;
          this.nextQuestion();
        }}
      }},

      updateHeaderProgress() {{
        if (!this.currentPref) return;
        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code);
        let cleared = 0, correct = 0, wrong = 0;
        prefMunis.forEach(m => {{
          const r = this.data.records[m[0]];
          if (r) {{
            if (r.correct > 0) cleared++;
            correct += r.correct;
            wrong += r.wrong;
          }}
        }});
        document.getElementById('muni-spoke-progress-text').textContent = `${{cleared}} / ${{prefMunis.length}}`;
        const acc = (correct + wrong > 0) ? Math.round((correct / (correct + wrong)) * 100) + '%' : '--%';
        document.getElementById('muni-spoke-accuracy-tag').textContent = `正答率: ${{acc}}`;
      }}
    }};

    // ==============================================================
    // モジュール 2: 令制国・旧国名暗記 (ProvApp)
    // ==============================================================
    const ProvApp = {{
      data: null,
      map: null,
      currentDoh: null,
      geoJsonLayer: null,
      currentLevel: 'ALL',
      currentMode: 'locate',
      questionPool: [],
      currentIndex: 0,
      currentQuestion: null,
      isAnswered: false,

      init() {{
        this.data = STORAGE.get(KEYS.PROV, {{ records: {{}} }});
        if (!this.data.records) this.data.records = {{}};

        document.getElementById('btn-prov-back-hub').onclick = () => {{
          AppRouter.navigate('screen-prov-hub');
          this.renderHub();
        }};
        document.getElementById('btn-prov-fit-all').onclick = () => {{
          if (this.map && this.geoJsonLayer) {{
            this.map.fitBounds(this.geoJsonLayer.getBounds(), {{ padding: [20, 20] }});
          }}
        }};

        document.querySelectorAll('.prov-mode-btn').forEach(btn => {{
          btn.onclick = () => this.setMode(btn.dataset.mode);
        }});

        document.getElementById('btn-prov-close-exp').onclick = () => {{
          document.getElementById('prov-explore-card').classList.add('hidden');
        }};
        document.getElementById('btn-prov-test-single').onclick = () => {{
          if (this.selectedProv) {{
            document.getElementById('prov-explore-card').classList.add('hidden');
            this.setMode('locate');
            this.startSingleQuestion(this.selectedProv);
          }}
        }};

        document.getElementById('btn-prov-start-weak-all').onclick = () => {{
          const allProvs = Object.values(PROVINCES_MASTER);
          const weakProvs = allProvs.filter(p => {{
            const r = this.data.records[p.id];
            return r && r.last === 'wrong';
          }});
          if (weakProvs.length > 0) {{
            this.openDoh(DOH_LIST[0], 'WEAK');
          }}
        }};

        window.addEventListener('keydown', (e) => {{
          if (AppRouter.currentScreen !== 'screen-prov-spoke') return;
          if (e.target.tagName === 'INPUT' && e.key !== 'Enter') return;
          this.handleKey(e);
        }});
      }},

      renderHub() {{
        const container = document.getElementById('prov-cards-container');
        container.innerHTML = '';

        let totalCleared = 0;
        let weakCount = 0;
        const allProvs = Object.values(PROVINCES_MASTER);
        allProvs.forEach(p => {{
          const r = this.data.records[p.id];
          if (r && r.correct > 0) totalCleared++;
          if (r && r.last === 'wrong') weakCount++;
        }});

        const totalPct = ((totalCleared / allProvs.length) * 100).toFixed(1);
        document.getElementById('prov-hub-cleared').textContent = totalCleared;
        document.getElementById('prov-hub-pct').textContent = totalPct + '%';
        document.getElementById('prov-hub-progress-bar').style.width = totalPct + '%';

        // 弱点バナー
        const weakBanner = document.getElementById('prov-weak-banner');
        if (weakCount > 0) {{
          weakBanner.classList.remove('hidden');
          document.getElementById('prov-weak-count-badge').textContent = `${{weakCount}}国`;
        }} else {{
          weakBanner.classList.add('hidden');
        }}

        // 地域カード
        let completedDohCount = 0;
        DOH_LIST.forEach(doh => {{
          const provs = (doh.id === 'ALL')
            ? allProvs
            : allProvs.filter(p => p.doh === doh.filter);

          let clr = 0;
          provs.forEach(p => {{
            const r = this.data.records[p.id];
            if (r && r.correct > 0) clr++;
          }});
          const isComp = (clr === provs.length && provs.length > 0);
          if (isComp && doh.id !== 'ALL') completedDohCount++;
          const pct = provs.length > 0 ? Math.round((clr / provs.length) * 100) : 0;

          const card = document.createElement('div');
          card.className = `p-4 rounded-xl border cursor-pointer transition active:scale-98 ${{
            isComp
              ? 'bg-sky-950/30 border-sky-500/40 hover:border-sky-400'
              : 'bg-slate-900 border-slate-800 hover:border-slate-700'
          }} flex flex-col justify-between`;

          card.innerHTML = `
            <div>
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white">${{doh.name}}</h3>
                <span class="text-[10px] px-2 py-0.5 rounded-full ${{isComp ? 'bg-sky-500/20 text-sky-400 font-bold' : 'bg-slate-800 text-slate-400'}}">${{provs.length}}国</span>
              </div>
              <p class="text-xs text-slate-400 mt-1">${{doh.desc}}</p>
            </div>
            <div class="mt-4 space-y-1.5">
              <div class="flex justify-between text-xs text-slate-400">
                <span>進捗: ${{clr}} / ${{provs.length}}</span>
                <span class="font-bold text-sky-400">${{pct}}%</span>
              </div>
              <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div class="bg-gradient-to-r from-sky-500 to-cyan-400 h-full" style="width: ${{pct}}%"></div>
              </div>
            </div>
          `;

          card.onclick = () => this.openDoh(doh);
          container.appendChild(card);
        }});

        document.getElementById('prov-hub-completed-doh').textContent = completedDohCount;
      }},

      openDoh(doh, initialLevel = 'ALL') {{
        this.currentDoh = doh;
        AppRouter.navigate('screen-prov-spoke');
        document.getElementById('prov-spoke-title').textContent = doh.name;

        const allProvs = Object.values(PROVINCES_MASTER);
        const provs = (doh.id === 'ALL') ? allProvs : allProvs.filter(p => p.doh === doh.filter);
        document.getElementById('prov-spoke-count-badge').textContent = `${{provs.length}}国`;

        if (!this.map) {{
          this.map = L.map('prov-map', {{
            attributionControl: false,
            zoomControl: false,
            renderer: L.svg({{ padding: 1.5 }})
          }});
          L.control.zoom({{ position: 'bottomright' }}).addTo(this.map);
        }}

        this.renderLevelTabs();
        this.startLevel(initialLevel);
      }},

      renderLevelTabs() {{
        const container = document.getElementById('prov-level-tabs');
        container.innerHTML = '';

        const levels = [
          {{ id: 'ALL', name: '全国' }},
          {{ id: 1, name: 'Lv.1 必修' }},
          {{ id: 2, name: 'Lv.2 基本' }},
          {{ id: 3, name: 'Lv.3 中堅' }},
          {{ id: 4, name: 'Lv.4 難関' }},
          {{ id: 'WEAK', name: '⚠️ 弱点' }}
        ];

        levels.forEach(lvl => {{
          const btn = document.createElement('button');
          btn.className = `prov-lvl-btn px-2.5 py-1 rounded-md text-[11px] font-semibold whitespace-nowrap transition ${{
            this.currentLevel === lvl.id
              ? 'bg-sky-500 text-white'
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
          }}`;
          btn.textContent = lvl.name;
          btn.onclick = () => this.startLevel(lvl.id);
          container.appendChild(btn);
        }});
      }},

      startLevel(levelId) {{
        this.currentLevel = levelId;
        document.querySelectorAll('.prov-lvl-btn').forEach(btn => {{
          btn.classList.remove('bg-sky-500', 'text-white');
          btn.classList.add('bg-slate-800', 'text-slate-300');
        }});
        const activeBtn = [...document.querySelectorAll('.prov-lvl-btn')].find(b => b.textContent.includes(levelId === 'ALL' ? '全国' : levelId === 'WEAK' ? '弱点' : `Lv.${{levelId}}`));
        if (activeBtn) {{
          activeBtn.classList.add('bg-sky-500', 'text-white');
          activeBtn.classList.remove('bg-slate-800', 'text-slate-300');
        }}

        const allProvs = Object.values(PROVINCES_MASTER);
        let basePool = (this.currentDoh.id === 'ALL') ? allProvs : allProvs.filter(p => p.doh === this.currentDoh.filter);

        if (levelId === 'ALL') {{
          this.questionPool = [...basePool];
        }} else if (levelId === 'WEAK') {{
          this.questionPool = basePool.filter(p => {{
            const r = this.data.records[p.id];
            return r && r.last === 'wrong';
          }});
          if (this.questionPool.length === 0) {{
            alert('この地域の弱点旧国はありません！');
            this.startLevel('ALL');
            return;
          }}
        }} else {{
          this.questionPool = basePool.filter(p => p.level === levelId);
          if (this.questionPool.length === 0) {{
            alert('この難易度の旧国はこの地域にはありません。');
            this.startLevel('ALL');
            return;
          }}
        }}

        this.questionPool.sort(() => Math.random() - 0.5);
        this.currentIndex = 0;

        this.renderMapLayers();
        this.nextQuestion();
      }},

      renderMapLayers() {{
        if (!this.map || !PROVINCES_GEOJSON) return;
        if (this.geoJsonLayer) this.map.removeLayer(this.geoJsonLayer);

        const targetIds = new Set(this.questionPool.map(p => p.id));

        this.geoJsonLayer = L.geoJSON(PROVINCES_GEOJSON, {{
          style: (feature) => {{
            const id = feature.properties.id;
            const isTarget = targetIds.has(id);
            return {{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.65,
              color: '#080d1a',
              weight: 1.2,
              opacity: 1
            }};
          }},
          onEachFeature: (feature, layer) => {{
            layer.on({{
              mouseover: (e) => {{
                if (this.currentMode === 'locate' || this.currentMode === 'explore') {{
                  e.target.setStyle({{ fillColor: '#e2e8f0', fillOpacity: 1 }});
                }}
              }},
              mouseout: (e) => {{
                if (this.geoJsonLayer) this.geoJsonLayer.resetStyle(e.target);
              }},
              click: () => this.onPolygonClick(feature, layer)
            }});
          }}
        }}).addTo(this.map);

        this.map.fitBounds(this.geoJsonLayer.getBounds(), {{ padding: [20, 20] }});
      }},

      setMode(mode) {{
        this.currentMode = mode;
        document.querySelectorAll('.prov-mode-btn').forEach(btn => {{
          btn.classList.remove('bg-sky-500', 'text-white');
          btn.classList.add('text-slate-400');
        }});
        const active = [...document.querySelectorAll('.prov-mode-btn')].find(b => b.dataset.mode === mode);
        if (active) {{
          active.classList.add('bg-sky-500', 'text-white');
          active.classList.remove('text-slate-400');
        }}
        this.nextQuestion();
      }},

      nextQuestion() {{
        this.isAnswered = false;
        if (this.currentMode === 'explore') {{
          this.renderExploreDock();
          return;
        }}

        if (this.currentIndex >= this.questionPool.length) {{
          sound.fanfare();
          alert('この地域の全問題を完了しました！');
          this.startLevel(this.currentLevel);
          return;
        }}

        this.currentQuestion = this.questionPool[this.currentIndex];
        this.updateHeaderProgress();

        if (this.currentMode === 'locate') {{
          this.renderLocateDock();
        }} else if (this.currentMode === 'name') {{
          this.highlightQuestionPolygon();
          this.renderNameDock();
        }} else if (this.currentMode === 'type') {{
          this.highlightQuestionPolygon();
          this.renderTypeDock();
        }}
      }},

      highlightQuestionPolygon() {{
        if (!this.geoJsonLayer || !this.currentQuestion) return;
        const targetId = this.currentQuestion.id;
        this.geoJsonLayer.eachLayer(layer => {{
          if (layer.feature.properties.id === targetId) {{
            layer.setStyle({{ fillColor: '#fbbf24', fillOpacity: 0.95, weight: 3, color: '#f59e0b' }});
            if (layer.getBounds) {{
              this.map.flyToBounds(layer.getBounds(), {{ maxZoom: 8, duration: 0.5 }});
            }}
          }} else {{
            this.geoJsonLayer.resetStyle(layer);
          }}
        }});
      }},

      renderLocateDock() {{
        const dock = document.getElementById('prov-dock');
        const q = this.currentQuestion;
        const rec = this.data.records[q.id] || {{ correct: 0, wrong: 0 }};
        const total = rec.correct + rec.wrong;
        const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';

        dock.innerHTML = `
          <div class="max-w-xl mx-auto flex items-center justify-between gap-3">
            <div>
              <div class="text-[11px] text-sky-400">${{q.kana}}（${{q.modern}}）</div>
              <div class="text-lg font-black text-white flex items-center gap-2">
                <span>${{q.name}}</span>
                <span class="text-xs font-normal text-slate-400">はどこ？</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">過去正答率: ${{pct}}</span>
            </div>
          </div>
        `;
      }},

      renderNameDock() {{
        const dock = document.getElementById('prov-dock');
        const q = this.currentQuestion;

        const allProvs = Object.values(PROVINCES_MASTER).filter(p => p.id !== q.id);
        allProvs.sort(() => Math.random() - 0.5);
        const choices = [q, ...allProvs.slice(0, 3)].sort(() => Math.random() - 0.5);

        let buttonsHtml = '';
        choices.forEach((c, idx) => {{
          buttonsHtml += `
            <button class="prov-choice-btn py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition flex items-center gap-2 active:scale-95" data-id="${{c.id}}">
              <span class="w-5 h-5 rounded bg-slate-900 text-slate-400 flex items-center justify-center text-[10px] font-mono">${{idx + 1}}</span>
              <span class="truncate">${{c.name}} (${{c.kana}})</span>
            </button>
          `;
        }});

        dock.innerHTML = `
          <div class="max-w-xl mx-auto space-y-2">
            <div class="text-xs text-slate-400 flex justify-between">
              <span>黄色点滅の旧国名を選択してください</span>
              <span>[1] - [4] キー対応</span>
            </div>
            <div class="grid grid-cols-2 gap-2" id="prov-choices-grid">
              ${{buttonsHtml}}
            </div>
          </div>
        `;

        dock.querySelectorAll('.prov-choice-btn').forEach(btn => {{
          btn.onclick = () => this.handleAnswer(btn.dataset.id === q.id, btn);
        }});
      }},

      renderTypeDock() {{
        const dock = document.getElementById('prov-dock');
        const q = this.currentQuestion;

        dock.innerHTML = `
          <div class="max-w-xl mx-auto space-y-2">
            <div class="text-xs text-slate-400">点滅している旧国名を入力（漢字またはひらがな）</div>
            <form id="prov-type-form" class="flex gap-2">
              <input type="text" id="prov-type-input" class="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 font-bold" placeholder="例: ${{q.name}}" autofocus autocomplete="off" />
              <button type="submit" class="px-5 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow transition">回答</button>
            </form>
          </div>
        `;

        const form = document.getElementById('prov-type-form');
        const input = document.getElementById('prov-type-input');
        input.focus();

        form.onsubmit = (e) => {{
          e.preventDefault();
          if (this.isAnswered) {{
            this.currentIndex++;
            this.nextQuestion();
            return;
          }}
          const val = input.value.trim();
          const isCorrect = (val === q.name || val === q.kana || q.aliases.includes(val));
          this.handleAnswer(isCorrect, input);
        }};
      }},

      renderExploreDock() {{
        const dock = document.getElementById('prov-dock');
        dock.innerHTML = `
          <div class="max-w-xl mx-auto text-center text-xs text-slate-400">
            地図上のポリゴンを自由にタップして、旧国名・ふりがな・現代の地域を確認できます。
          </div>
        `;
      }},

      onPolygonClick(feature, layer) {{
        const id = feature.properties.id;
        const targetProv = PROVINCES_MASTER[id];
        if (!targetProv) return;

        if (this.currentMode === 'locate') {{
          if (this.isAnswered) return;
          const isCorrect = (id === this.currentQuestion.id);
          this.handleAnswer(isCorrect, layer);
        }} else if (this.currentMode === 'explore') {{
          this.selectedProv = targetProv;
          const card = document.getElementById('prov-explore-card');
          card.classList.remove('hidden');
          document.getElementById('prov-exp-kana').textContent = targetProv.kana;
          document.getElementById('prov-exp-name').textContent = targetProv.name;
          document.getElementById('prov-exp-modern').textContent = targetProv.modern;

          const rec = this.data.records[id] || {{ correct: 0, wrong: 0 }};
          document.getElementById('prov-exp-stats').textContent = `正解 ${{rec.correct}} / 不正解 ${{rec.wrong}}`;
        }}
      }},

      handleAnswer(isCorrect, targetEl) {{
        if (this.isAnswered) return;
        this.isAnswered = true;

        const q = this.currentQuestion;
        if (!this.data.records[q.id]) this.data.records[q.id] = {{ correct: 0, wrong: 0 }};
        const rec = this.data.records[q.id];

        if (isCorrect) {{
          sound.correct();
          rec.correct++;
          rec.last = 'correct';
          rec.updated = Date.now();
          STORAGE.set(KEYS.PROV, this.data);

          if (this.currentMode === 'locate') {{
            if (targetEl && targetEl.setStyle) targetEl.setStyle({{ fillColor: '#34d399', fillOpacity: 0.95 }});
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-sky-600', '!border-sky-400');
          }}
          setTimeout(() => {{
            this.currentIndex++;
            this.nextQuestion();
          }}, 900);
        }} else {{
          sound.wrong();
          rec.wrong++;
          rec.last = 'wrong';
          rec.updated = Date.now();
          STORAGE.set(KEYS.PROV, this.data);

          if (this.currentMode === 'locate') {{
            if (targetEl && targetEl.setStyle) targetEl.setStyle({{ fillColor: '#f87171', fillOpacity: 0.95 }});
            this.highlightQuestionPolygon();
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-rose-700');
            const correctBtn = document.querySelector(`.prov-choice-btn[data-id="${{q.id}}"]`);
            if (correctBtn) correctBtn.classList.add('!border-emerald-400', '!border-2');
          }} else if (this.currentMode === 'type') {{
            targetEl.classList.add('!border-rose-500');
            targetEl.value = `正解: ${{q.name}} (Enterで次へ)`;
          }}
        }}
      }},

      handleKey(e) {{
        if (this.currentMode === 'name') {{
          const num = parseInt(e.key);
          if (num >= 1 && num <= 4) {{
            const btns = document.querySelectorAll('.prov-choice-btn');
            if (btns[num - 1]) btns[num - 1].click();
          }}
        }}
        if (e.key === 'Enter' && this.isAnswered) {{
          this.currentIndex++;
          this.nextQuestion();
        }}
      }},

      updateHeaderProgress() {{
        const allProvs = Object.values(PROVINCES_MASTER);
        const provs = (this.currentDoh.id === 'ALL') ? allProvs : allProvs.filter(p => p.doh === this.currentDoh.filter);
        let cleared = 0, correct = 0, wrong = 0;
        provs.forEach(p => {{
          const r = this.data.records[p.id];
          if (r) {{
            if (r.correct > 0) cleared++;
            correct += r.correct;
            wrong += r.wrong;
          }}
        }});
        document.getElementById('prov-spoke-progress-text').textContent = `${{cleared}} / ${{provs.length}}`;
        const acc = (correct + wrong > 0) ? Math.round((correct / (correct + wrong)) * 100) + '%' : '--%';
        document.getElementById('prov-spoke-accuracy-tag').textContent = `正答率: ${{acc}}`;
      }}
    }};

    // ==============================================================
    // モジュール 3: 世界の国名・首都名暗記 (WorldApp)
    // ==============================================================
    const WorldApp = {{
      data: null,
      map: null,
      currentRegion: null,
      geoJsonLayer: null,
      currentLevel: 'ALL',
      currentMode: 'locate',
      targetType: 'country', // 'country' | 'capital'
      questionPool: [],
      currentIndex: 0,
      currentQuestion: null,
      isAnswered: false,

      init() {{
        this.data = STORAGE.get(KEYS.WORLD, {{ records: {{}} }});
        if (!this.data.records) this.data.records = {{}};

        document.getElementById('btn-world-back-hub').onclick = () => {{
          AppRouter.navigate('screen-world-hub');
          this.renderHub();
        }};
        document.getElementById('btn-world-fit-all').onclick = () => {{
          if (this.map && this.currentRegion) {{
            if (this.currentRegion.bounds) this.map.fitBounds(this.currentRegion.bounds, {{ padding: [20, 20] }});
            else if (this.currentRegion.center) this.map.setView(this.currentRegion.center, this.currentRegion.zoom);
          }}
        }};

        // 出題対象トグル (国名 ↔ 首都名)
        const btnTargetCountry = document.getElementById('btn-world-target-country');
        const btnTargetCap = document.getElementById('btn-world-target-capital');
        btnTargetCountry.onclick = () => {{
          this.targetType = 'country';
          btnTargetCountry.className = 'px-2 py-1 rounded text-white font-bold bg-indigo-600 transition';
          btnTargetCap.className = 'px-2 py-1 rounded text-slate-400 hover:text-white transition';
          this.nextQuestion();
        }};
        btnTargetCap.onclick = () => {{
          this.targetType = 'capital';
          btnTargetCap.className = 'px-2 py-1 rounded text-white font-bold bg-indigo-600 transition';
          btnTargetCountry.className = 'px-2 py-1 rounded text-slate-400 hover:text-white transition';
          this.nextQuestion();
        }};

        document.querySelectorAll('.world-mode-btn').forEach(btn => {{
          btn.onclick = () => this.setMode(btn.dataset.mode);
        }});

        document.getElementById('btn-world-close-exp').onclick = () => {{
          document.getElementById('world-explore-card').classList.add('hidden');
        }};
        document.getElementById('btn-world-test-single').onclick = () => {{
          if (this.selectedCountry) {{
            document.getElementById('world-explore-card').classList.add('hidden');
            this.setMode('locate');
            this.startSingleQuestion(this.selectedCountry);
          }}
        }};

        document.getElementById('btn-world-start-weak-all').onclick = () => {{
          const allCountries = Object.values(WORLD_MASTER);
          const weak = allCountries.filter(c => {{
            const r = this.data.records[c.code];
            return r && r.last === 'wrong';
          }});
          if (weak.length > 0) {{
            this.openRegion(WORLD_REGIONS[0], 'WEAK');
          }}
        }};

        window.addEventListener('keydown', (e) => {{
          if (AppRouter.currentScreen !== 'screen-world-spoke') return;
          if (e.target.tagName === 'INPUT' && e.key !== 'Enter') return;
          this.handleKey(e);
        }});
      }},

      renderHub() {{
        const container = document.getElementById('world-cards-container');
        container.innerHTML = '';

        let totalCleared = 0;
        let weakCount = 0;
        const allCountries = Object.values(WORLD_MASTER);
        allCountries.forEach(c => {{
          const r = this.data.records[c.code];
          if (r && r.correct > 0) totalCleared++;
          if (r && r.last === 'wrong') weakCount++;
        }});

        const totalPct = ((totalCleared / allCountries.length) * 100).toFixed(1);
        document.getElementById('world-hub-cleared').textContent = totalCleared;
        document.getElementById('world-hub-pct').textContent = totalPct + '%';
        document.getElementById('world-hub-progress-bar').style.width = totalPct + '%';

        // 弱点バナー
        const weakBanner = document.getElementById('world-weak-banner');
        if (weakCount > 0) {{
          weakBanner.classList.remove('hidden');
          document.getElementById('world-weak-count-badge').textContent = `${{weakCount}}国`;
        }} else {{
          weakBanner.classList.add('hidden');
        }}

        // 地域カード
        let completedRegionCount = 0;
        WORLD_REGIONS.forEach(reg => {{
          const countries = (reg.filter === 'ALL')
            ? allCountries
            : allCountries.filter(c => c.region === reg.filter);

          let clr = 0;
          countries.forEach(c => {{
            const r = this.data.records[c.code];
            if (r && r.correct > 0) clr++;
          }});
          const isComp = (clr === countries.length && countries.length > 0);
          if (isComp && reg.filter !== 'ALL') completedRegionCount++;
          const pct = countries.length > 0 ? Math.round((clr / countries.length) * 100) : 0;

          const card = document.createElement('div');
          card.className = `p-4 rounded-xl border cursor-pointer transition active:scale-98 ${{
            isComp
              ? 'bg-indigo-950/30 border-indigo-500/40 hover:border-indigo-400'
              : 'bg-slate-900 border-slate-800 hover:border-slate-700'
          }} flex flex-col justify-between`;

          card.innerHTML = `
            <div>
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white">${{reg.name}}</h3>
                <span class="text-[10px] px-2 py-0.5 rounded-full ${{isComp ? 'bg-indigo-500/20 text-indigo-400 font-bold' : 'bg-slate-800 text-slate-400'}}">${{countries.length}}国</span>
              </div>
              <p class="text-xs text-slate-400 mt-1">${{reg.desc}}</p>
            </div>
            <div class="mt-4 space-y-1.5">
              <div class="flex justify-between text-xs text-slate-400">
                <span>進捗: ${{clr}} / ${{countries.length}}</span>
                <span class="font-bold text-indigo-400">${{pct}}%</span>
              </div>
              <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div class="bg-gradient-to-r from-indigo-500 to-purple-400 h-full" style="width: ${{pct}}%"></div>
              </div>
            </div>
          `;

          card.onclick = () => this.openRegion(reg);
          container.appendChild(card);
        }});

        document.getElementById('world-hub-completed-regions').textContent = completedRegionCount;
      }},

      openRegion(region, initialLevel = 'ALL') {{
        this.currentRegion = region;
        AppRouter.navigate('screen-world-spoke');
        document.getElementById('world-spoke-title').textContent = region.name;

        const allCountries = Object.values(WORLD_MASTER);
        const countries = (region.filter === 'ALL') ? allCountries : allCountries.filter(c => c.region === region.filter);
        document.getElementById('world-spoke-count-badge').textContent = `${{countries.length}}国`;

        if (!this.map) {{
          this.map = L.map('world-map', {{
            attributionControl: false,
            zoomControl: false,
            renderer: L.svg({{ padding: 1.5 }}),
            minZoom: 1.5,
            maxZoom: 9
          }});
          L.control.zoom({{ position: 'bottomright' }}).addTo(this.map);
        }}

        this.renderLevelTabs();
        this.startLevel(initialLevel);
      }},

      renderLevelTabs() {{
        const container = document.getElementById('world-level-tabs');
        container.innerHTML = '';

        const levels = [
          {{ id: 'ALL', name: '全地域' }},
          {{ id: 1, name: 'Lv.1 主要国' }},
          {{ id: 2, name: 'Lv.2 一般国' }},
          {{ id: 3, name: 'Lv.3 中堅国' }},
          {{ id: 4, name: 'Lv.4 難関国' }},
          {{ id: 'WEAK', name: '⚠️ 弱点' }}
        ];

        levels.forEach(lvl => {{
          const btn = document.createElement('button');
          btn.className = `world-lvl-btn px-2.5 py-1 rounded-md text-[11px] font-semibold whitespace-nowrap transition ${{
            this.currentLevel === lvl.id
              ? 'bg-indigo-500 text-white'
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
          }}`;
          btn.textContent = lvl.name;
          btn.onclick = () => this.startLevel(lvl.id);
          container.appendChild(btn);
        }});
      }},

      startLevel(levelId) {{
        this.currentLevel = levelId;
        document.querySelectorAll('.world-lvl-btn').forEach(btn => {{
          btn.classList.remove('bg-indigo-500', 'text-white');
          btn.classList.add('bg-slate-800', 'text-slate-300');
        }});
        const activeBtn = [...document.querySelectorAll('.world-lvl-btn')].find(b => b.textContent.includes(levelId === 'ALL' ? '全地域' : levelId === 'WEAK' ? '弱点' : `Lv.${{levelId}}`));
        if (activeBtn) {{
          activeBtn.classList.add('bg-indigo-500', 'text-white');
          activeBtn.classList.remove('bg-slate-800', 'text-slate-300');
        }}

        const allCountries = Object.values(WORLD_MASTER);
        let basePool = (this.currentRegion.filter === 'ALL') ? allCountries : allCountries.filter(c => c.region === this.currentRegion.filter);

        if (levelId === 'ALL') {{
          this.questionPool = [...basePool];
        }} else if (levelId === 'WEAK') {{
          this.questionPool = basePool.filter(c => {{
            const r = this.data.records[c.code];
            return r && r.last === 'wrong';
          }});
          if (this.questionPool.length === 0) {{
            alert('この地域の弱点国はありません！素晴らしい！');
            this.startLevel('ALL');
            return;
          }}
        }} else {{
          this.questionPool = basePool.filter(c => c.level === levelId);
          if (this.questionPool.length === 0) {{
            alert('この難易度の国はこの地域にはありません。');
            this.startLevel('ALL');
            return;
          }}
        }}

        this.questionPool.sort(() => Math.random() - 0.5);
        this.currentIndex = 0;

        this.renderMapLayers();
        this.nextQuestion();
      }},

      renderMapLayers() {{
        if (!this.map || !WORLD_GEOJSON) return;
        if (this.geoJsonLayer) this.map.removeLayer(this.geoJsonLayer);

        const targetCodes = new Set(this.questionPool.map(c => c.code));

        this.geoJsonLayer = L.geoJSON(WORLD_GEOJSON, {{
          style: (feature) => {{
            const code = feature.properties.code;
            const isTarget = targetCodes.has(code);
            return {{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.60,
              color: '#090d16',
              weight: 0.8,
              opacity: 1
            }};
          }},
          onEachFeature: (feature, layer) => {{
            layer.on({{
              mouseover: (e) => {{
                if (this.currentMode === 'locate' || this.currentMode === 'explore') {{
                  e.target.setStyle({{ fillColor: '#e2e8f0', fillOpacity: 1 }});
                }}
              }},
              mouseout: (e) => {{
                if (this.geoJsonLayer) this.geoJsonLayer.resetStyle(e.target);
              }},
              click: () => this.onPolygonClick(feature, layer)
            }});
          }}
        }}).addTo(this.map);

        if (this.currentRegion.bounds) {{
          this.map.fitBounds(this.currentRegion.bounds, {{ padding: [20, 20] }});
        }} else if (this.currentRegion.center) {{
          this.map.setView(this.currentRegion.center, this.currentRegion.zoom);
        }}
      }},

      setMode(mode) {{
        this.currentMode = mode;
        document.querySelectorAll('.world-mode-btn').forEach(btn => {{
          btn.classList.remove('bg-indigo-500', 'text-white');
          btn.classList.add('text-slate-400');
        }});
        const active = [...document.querySelectorAll('.world-mode-btn')].find(b => b.dataset.mode === mode);
        if (active) {{
          active.classList.add('bg-indigo-500', 'text-white');
          active.classList.remove('text-slate-400');
        }}
        this.nextQuestion();
      }},

      nextQuestion() {{
        this.isAnswered = false;
        if (this.currentMode === 'explore') {{
          this.renderExploreDock();
          return;
        }}

        if (this.currentIndex >= this.questionPool.length) {{
          sound.fanfare();
          alert('この地域の全問題を完了しました！');
          this.startLevel(this.currentLevel);
          return;
        }}

        this.currentQuestion = this.questionPool[this.currentIndex];
        this.updateHeaderProgress();

        if (this.currentMode === 'locate') {{
          this.renderLocateDock();
        }} else if (this.currentMode === 'name') {{
          this.highlightQuestionPolygon();
          this.renderNameDock();
        }} else if (this.currentMode === 'type') {{
          this.highlightQuestionPolygon();
          this.renderTypeDock();
        }}
      }},

      highlightQuestionPolygon() {{
        if (!this.geoJsonLayer || !this.currentQuestion) return;
        const code = this.currentQuestion.code;
        this.geoJsonLayer.eachLayer(layer => {{
          if (layer.feature.properties.code === code) {{
            layer.setStyle({{ fillColor: '#fbbf24', fillOpacity: 0.95, weight: 2.5, color: '#f59e0b' }});
            if (layer.getBounds) {{
              this.map.flyToBounds(layer.getBounds(), {{ maxZoom: 5.5, duration: 0.5 }});
            }}
          }} else {{
            this.geoJsonLayer.resetStyle(layer);
          }}
        }});
      }},

      renderLocateDock() {{
        const dock = document.getElementById('world-dock');
        const q = this.currentQuestion;
        const rec = this.data.records[q.code] || {{ correct: 0, wrong: 0 }};
        const total = rec.correct + rec.wrong;
        const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
        const flag = getFlagEmoji(q.code2);

        const promptText = (this.targetType === 'capital')
          ? `🏛️ 首都: <strong class="text-white">${{q.capital}}</strong> (${{q.furigana_cap}}) の国はどこ？`
          : `🗺️ 国名: <strong class="text-white">${{q.name}}</strong> (${{q.furigana_name}}) はどこ？`;

        dock.innerHTML = `
          <div class="max-w-xl mx-auto flex items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <span class="text-3xl">${{flag}}</span>
              <div>
                <div class="text-[11px] text-indigo-400">${{q.region}}・Lv.${{q.level}}</div>
                <div class="text-sm sm:text-base font-bold text-slate-200">
                  ${{promptText}}
                </div>
              </div>
            </div>
            <div class="text-right shrink-0">
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">正答率: ${{pct}}</span>
            </div>
          </div>
        `;
      }},

      renderNameDock() {{
        const dock = document.getElementById('world-dock');
        const q = this.currentQuestion;

        const allCountries = Object.values(WORLD_MASTER).filter(c => c.code !== q.code);
        allCountries.sort(() => Math.random() - 0.5);
        const choices = [q, ...allCountries.slice(0, 3)].sort(() => Math.random() - 0.5);

        let buttonsHtml = '';
        choices.forEach((c, idx) => {{
          const flag = getFlagEmoji(c.code2);
          const label = (this.targetType === 'capital')
            ? `🏛️ ${{c.capital}}`
            : `${{flag}} ${{c.name}}`;
          const sub = (this.targetType === 'capital')
            ? `${{flag}} ${{c.name}}`
            : `${{c.capital}}`;

          buttonsHtml += `
            <button class="world-choice-btn py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition flex items-center justify-between gap-2 active:scale-95" data-code="${{c.code}}">
              <div class="flex items-center gap-2 truncate">
                <span class="w-5 h-5 rounded bg-slate-900 text-slate-400 flex items-center justify-center text-[10px] font-mono">${{idx + 1}}</span>
                <span class="truncate">${{label}}</span>
              </div>
              <span class="text-[10px] text-slate-400 shrink-0 font-normal">${{sub}}</span>
            </button>
          `;
        }});

        const promptDesc = (this.targetType === 'capital')
          ? '点滅している国の【首都名】を選択してください'
          : '点滅している国の【国名】を選択してください';

        dock.innerHTML = `
          <div class="max-w-xl mx-auto space-y-2">
            <div class="text-xs text-slate-400 flex justify-between">
              <span>${{promptDesc}}</span>
              <span>[1] - [4] キー対応</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2" id="world-choices-grid">
              ${{buttonsHtml}}
            </div>
          </div>
        `;

        dock.querySelectorAll('.world-choice-btn').forEach(btn => {{
          btn.onclick = () => this.handleAnswer(btn.dataset.code === q.code, btn);
        }});
      }},

      renderTypeDock() {{
        const dock = document.getElementById('world-dock');
        const q = this.currentQuestion;
        const flag = getFlagEmoji(q.code2);

        const promptDesc = (this.targetType === 'capital')
          ? `点滅している国（${{flag}} ${{q.name}}）の【首都名】を入力`
          : `点滅している国の【国名】を入力（漢字・カタカナ・ひらがな）`;

        dock.innerHTML = `
          <div class="max-w-xl mx-auto space-y-2">
            <div class="text-xs text-slate-400">${{promptDesc}}</div>
            <form id="world-type-form" class="flex gap-2">
              <input type="text" id="world-type-input" class="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 font-bold" placeholder="${{this.targetType === 'capital' ? '首都名を入力' : '国名を入力'}}" autofocus autocomplete="off" />
              <button type="submit" class="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm shadow transition">回答</button>
            </form>
          </div>
        `;

        const form = document.getElementById('world-type-form');
        const input = document.getElementById('world-type-input');
        input.focus();

        form.onsubmit = (e) => {{
          e.preventDefault();
          if (this.isAnswered) {{
            this.currentIndex++;
            this.nextQuestion();
            return;
          }}
          const val = input.value.trim().toLowerCase();
          let isCorrect = false;

          if (this.targetType === 'capital') {{
            isCorrect = (val === q.capital.toLowerCase() ||
                         val === q.furigana_cap ||
                         q.aliases_cap.some(a => a.toLowerCase() === val));
          }} else {{
            isCorrect = (val === q.name.toLowerCase() ||
                         val === q.furigana_name ||
                         q.aliases_name.some(a => a.toLowerCase() === val));
          }}

          this.handleAnswer(isCorrect, input);
        }};
      }},

      renderExploreDock() {{
        const dock = document.getElementById('world-dock');
        dock.innerHTML = `
          <div class="max-w-xl mx-auto text-center text-xs text-slate-400">
            地図上の国を自由にタップして、国名・首都・国旗・地域・学習履歴を確認できます。
          </div>
        `;
      }},

      onPolygonClick(feature, layer) {{
        const code = feature.properties.code;
        const targetCountry = WORLD_MASTER[code];
        if (!targetCountry) return;

        if (this.currentMode === 'locate') {{
          if (this.isAnswered) return;
          const isCorrect = (code === this.currentQuestion.code);
          this.handleAnswer(isCorrect, layer);
        }} else if (this.currentMode === 'explore') {{
          this.selectedCountry = targetCountry;
          const card = document.getElementById('world-explore-card');
          card.classList.remove('hidden');

          document.getElementById('world-exp-flag').textContent = getFlagEmoji(targetCountry.code2);
          document.getElementById('world-exp-kana').textContent = targetCountry.furigana_name;
          document.getElementById('world-exp-name').textContent = targetCountry.name;
          document.getElementById('world-exp-capital').textContent = `${{targetCountry.capital}} (${{targetCountry.furigana_cap}})`;
          document.getElementById('world-exp-region').textContent = `${{targetCountry.region}} (${{targetCountry.code}})`;

          const rec = this.data.records[code] || {{ correct: 0, wrong: 0 }};
          document.getElementById('world-exp-stats').textContent = `正解 ${{rec.correct}} / 不正解 ${{rec.wrong}}`;
        }}
      }},

      handleAnswer(isCorrect, targetEl) {{
        if (this.isAnswered) return;
        this.isAnswered = true;

        const q = this.currentQuestion;
        if (!this.data.records[q.code]) this.data.records[q.code] = {{ correct: 0, wrong: 0 }};
        const rec = this.data.records[q.code];

        if (isCorrect) {{
          sound.correct();
          rec.correct++;
          rec.last = 'correct';
          rec.updated = Date.now();
          STORAGE.set(KEYS.WORLD, this.data);

          if (this.currentMode === 'locate') {{
            if (targetEl && targetEl.setStyle) targetEl.setStyle({{ fillColor: '#34d399', fillOpacity: 0.95 }});
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-indigo-600', '!border-indigo-400');
          }}
          setTimeout(() => {{
            this.currentIndex++;
            this.nextQuestion();
          }}, 900);
        }} else {{
          sound.wrong();
          rec.wrong++;
          rec.last = 'wrong';
          rec.updated = Date.now();
          STORAGE.set(KEYS.WORLD, this.data);

          if (this.currentMode === 'locate') {{
            if (targetEl && targetEl.setStyle) targetEl.setStyle({{ fillColor: '#f87171', fillOpacity: 0.95 }});
            this.highlightQuestionPolygon();
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-rose-700');
            const correctBtn = document.querySelector(`.world-choice-btn[data-code="${{q.code}}"]`);
            if (correctBtn) correctBtn.classList.add('!border-emerald-400', '!border-2');
          }} else if (this.currentMode === 'type') {{
            targetEl.classList.add('!border-rose-500');
            const answerStr = (this.targetType === 'capital') ? q.capital : q.name;
            targetEl.value = `正解: ${{answerStr}} (Enterで次へ)`;
          }}
        }}
      }},

      handleKey(e) {{
        if (this.currentMode === 'name') {{
          const num = parseInt(e.key);
          if (num >= 1 && num <= 4) {{
            const btns = document.querySelectorAll('.world-choice-btn');
            if (btns[num - 1]) btns[num - 1].click();
          }}
        }}
        if (e.key === 'Enter' && this.isAnswered) {{
          this.currentIndex++;
          this.nextQuestion();
        }}
      }},

      updateHeaderProgress() {{
        const allCountries = Object.values(WORLD_MASTER);
        const countries = (this.currentRegion.filter === 'ALL') ? allCountries : allCountries.filter(c => c.region === this.currentRegion.filter);
        let cleared = 0, correct = 0, wrong = 0;
        countries.forEach(c => {{
          const r = this.data.records[c.code];
          if (r) {{
            if (r.correct > 0) cleared++;
            correct += r.correct;
            wrong += r.wrong;
          }}
        }});
        document.getElementById('world-spoke-progress-text').textContent = `${{cleared}} / ${{countries.length}}`;
        const acc = (correct + wrong > 0) ? Math.round((correct / (correct + wrong)) * 100) + '%' : '--%';
        document.getElementById('world-spoke-accuracy-tag').textContent = `正答率: ${{acc}}`;
      }}
    }};

    // アプリケーション初期化
    window.addEventListener('DOMContentLoaded', () => {{
      RootHub.init();
      MuniApp.init();
      ProvApp.init();
      WorldApp.init();
    }});
  </script>
</body>
</html>
'''

print("Writing index.html...")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Build complete! Output file size: {os.path.getsize('index.html') // 1024} KB")
