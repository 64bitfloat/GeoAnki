# -*- coding: utf-8 -*-
"""
GeoAnki Suite — 地理暗記学習プラットフォーム統合ビルドスクリプト
1. 全国1,741市区町村暗記モジュール
2. 令制国・旧国名暗記モジュール（地域選択撤廃・全国一括・4段階レベル分け）
3. 世界の国名・首都名暗記モジュール（レベル対象外国のホバー/クリック完全無効化）
市区町村暗記のUI/UX品質を全モジュールで完全踏襲
"""

import json
import os

print("=== Building GeoAnki Suite (index.html) with Refined Features ===")

# -------------------------------------------------------------
# 1. 市区町村データ読み込み (Municipalities)
# -------------------------------------------------------------
with open("municipalities.json", "r", encoding="utf-8") as f:
    muni_raw = json.load(f)

with open("ward_to_city.json", "r", encoding="utf-8") as f:
    ward_to_city = json.load(f)

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
with open("provinces_master.json", "r", encoding="utf-8") as f:
    provinces_master = json.load(f)

with open("provinces.geojson", "r", encoding="utf-8") as f:
    provinces_geojson = json.load(f)

# -------------------------------------------------------------
# 3. 世界の国名・首都データ読み込み (World Countries & Capitals)
# -------------------------------------------------------------
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

muni_json = json.dumps(muni_arr, ensure_ascii=False, separators=(',', ':'))
ward_json = json.dumps(ward_to_city, ensure_ascii=False, separators=(',', ':'))
pref_json = json.dumps(PREFECTURES, ensure_ascii=False, separators=(',', ':'))

prov_master_json = json.dumps(provinces_master, ensure_ascii=False, separators=(',', ':'))
prov_geo_json = json.dumps(provinces_geojson, ensure_ascii=False, separators=(',', ':'))

world_master_json = json.dumps(world_master, ensure_ascii=False, separators=(',', ':'))
world_geo_json = json.dumps(world_geojson, ensure_ascii=False, separators=(',', ':'))
world_regions_json = json.dumps(WORLD_REGIONS, ensure_ascii=False, separators=(',', ':'))

# HTML生成
html_content = f'''<!DOCTYPE html>
<html lang="ja" class="h-full bg-slate-900 text-slate-100">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>GeoAnki — 地理暗記学習プラットフォーム</title>

  <!-- 基本メタ情報 & SEO -->
  <meta name="description" content="全国1,741市区町村・令制国旧国名（68国）・世界の国名と首都（196ヶ国）を美麗な白地図ベクターポリゴンで直感暗記！GeoGuessr・地理学習特化アプリ。" />
  <meta name="keywords" content="GeoGuessr, ジオゲッサー, 市区町村, 旧国名, 令制国, 世界の国名, 首都, 地理, 暗記, Anki, 白地図" />
  <meta name="author" content="64bitfloat" />
  <meta name="theme-color" content="#10b981" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

  <!-- Open Graph Protocol -->
  <meta property="og:site_name" content="GeoAnki" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://64bitfloat.github.io/GeoAnki/" />
  <meta property="og:title" content="GeoAnki — 地理暗記学習プラットフォーム" />
  <meta property="og:description" content="全国1,741市区町村・旧国名・世界の国名首都を白地図ベクターポリゴンで直感暗記！場所当て・4択・記入・探索・弱点復習の5大モード搭載。" />
  <meta property="og:image" content="https://opengraph.githubassets.com/1/64bitfloat/GeoAnki" />
  <meta property="og:locale" content="ja_JP" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="GeoAnki — 地理暗記学習プラットフォーム" />
  <meta name="twitter:description" content="市区町村・旧国名・世界の国名首都を白地図ベクターで直感暗記！GeoGuessr・地理特化トレーナー。" />

  <!-- ファビコン -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%2310b981'/><text x='50' y='64' font-size='44' font-weight='900' fill='white' text-anchor='middle' font-family='sans-serif'>🌍</text></svg>" />

  <!-- Tailwind CSS (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#ecfdf5',
              100: '#d1fae5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
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
      position: relative;
      z-index: 0;
    }}
    .leaflet-container {{
      background: #090d16 !important;
    }}
    .leaflet-pane > svg {{
      transform: translate3d(0, 0, 0);
      backface-visibility: hidden;
    }}
    @keyframes pulse-yellow {{
      0%, 100% {{ fill-opacity: 0.95; stroke-width: 3px; }}
      50% {{ fill-opacity: 0.45; stroke-width: 4.5px; stroke: #eab308; }}
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
<body class="h-full flex flex-col overflow-hidden bg-slate-900 select-none text-slate-100">

  <!-- ============================================================== -->
  <!-- 画面 0: Root Hub (統合ポータルランチャー画面) -->
  <!-- ============================================================== -->
  <div id="screen-root-hub" class="flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-800/90 backdrop-blur border-b border-slate-700/80 px-4 py-3 shrink-0 z-10">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 via-sky-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-emerald-500/20 text-lg">
            🌍
          </div>
          <div>
            <h1 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              GeoAnki
              <span class="text-xs font-normal text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">地理暗記ハブ</span>
            </h1>
            <p class="text-xs text-slate-400 hidden sm:block">全国市区町村・令制国・世界の国名首都 視覚ベクター暗記プラットフォーム</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button id="btn-global-sound" class="p-2 rounded-lg bg-slate-700/60 hover:bg-slate-700 text-emerald-400 transition" title="効果音切替">
            <svg id="global-sound-icon-on" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
            <svg id="global-sound-icon-off" class="w-5 h-5 hidden text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/></svg>
          </button>
          <button id="btn-show-data-mgr" class="p-2 rounded-lg bg-slate-700/60 hover:bg-slate-700 text-slate-300 hover:text-white transition" title="データ管理・設定">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </button>
        </div>
      </div>
    </header>

    <!-- メイン選択エリア -->
    <main class="flex-1 overflow-y-auto px-4 py-6 overscroll-contain">
      <div class="max-w-5xl mx-auto space-y-6">
        <div class="text-center space-y-1.5 mb-6">
          <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight">暗記学習モジュールを選択</h2>
          <p class="text-xs sm:text-sm text-slate-400">暗記したい地理領域を選んで特訓を開始してください。学習履歴は自動保存されます。</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- カード 1: 市区町村 -->
          <div class="bg-slate-800/80 border border-slate-700/80 hover:border-emerald-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition-all duration-300 hover:-translate-y-1 group">
            <div class="space-y-3.5">
              <div class="flex items-center justify-between">
                <div class="w-11 h-11 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition">
                  🗾
                </div>
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">JIS完全準拠</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-emerald-400 transition">市区町村暗記</h3>
                <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                  全国1,741自治体（市・町・村・特別区）。政令市行政区統合＆2層境界。GeoGuessrの地域特定力を極限まで高める特訓。
                </p>
              </div>

              <!-- 進捗状況 -->
              <div class="bg-slate-900/80 rounded-xl p-3 border border-slate-700/60 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-400">制覇状況</span>
                  <span class="font-bold text-emerald-400"><span id="root-muni-cleared">0</span> / 1,741 (<span id="root-muni-pct">0.0%</span>)</span>
                </div>
                <div class="w-full bg-slate-700/60 h-2 rounded-full overflow-hidden">
                  <div id="root-muni-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>正答率: <strong id="root-muni-acc" class="text-slate-200">--%</strong></span>
                  <span id="root-muni-weak-badge" class="text-rose-400">弱点: 0</span>
                </div>
              </div>
            </div>

            <button id="btn-enter-muni" class="mt-5 w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg shadow-emerald-600/30 transition flex items-center justify-center gap-2 active:scale-95">
              <span>特訓を始める</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>

          <!-- カード 2: 令制国・旧国名 -->
          <div class="bg-slate-800/80 border border-slate-700/80 hover:border-emerald-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition-all duration-300 hover:-translate-y-1 group">
            <div class="space-y-3.5">
              <div class="flex items-center justify-between">
                <div class="w-11 h-11 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition">
                  📜
                </div>
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">全国68国・4段階</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-emerald-400 transition">令制国・旧国名暗記</h3>
                <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                  武蔵・信濃・尾張・薩摩など日本の旧国名全68国。主要国・中堅国・一般国・小国の4段階レベルで全国一括特訓。
                </p>
              </div>

              <!-- 進捗状況 -->
              <div class="bg-slate-900/80 rounded-xl p-3 border border-slate-700/60 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-400">制覇状況</span>
                  <span class="font-bold text-emerald-400"><span id="root-prov-cleared">0</span> / 68 (<span id="root-prov-pct">0.0%</span>)</span>
                </div>
                <div class="w-full bg-slate-700/60 h-2 rounded-full overflow-hidden">
                  <div id="root-prov-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>正答率: <strong id="root-prov-acc" class="text-slate-200">--%</strong></span>
                  <span id="root-prov-weak-badge" class="text-rose-400">弱点: 0</span>
                </div>
              </div>
            </div>

            <button id="btn-enter-province" class="mt-5 w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg shadow-emerald-600/30 transition flex items-center justify-center gap-2 active:scale-95">
              <span>特訓を始める</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>

          <!-- カード 3: 世界の国名・首都名 -->
          <div class="bg-slate-800/80 border border-slate-700/80 hover:border-emerald-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition-all duration-300 hover:-translate-y-1 group">
            <div class="space-y-3.5">
              <div class="flex items-center justify-between">
                <div class="w-11 h-11 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition">
                  🌍
                </div>
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">双方向・196国</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-emerald-400 transition">世界の国名・首都名暗記</h3>
                <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                  国連加盟国193ヶ国＋主要地域を網羅。国名と首都名の双方向クイズ、難易度・地域別分類、国旗絵文字表示に対応。
                </p>
              </div>

              <!-- 進捗状況 -->
              <div class="bg-slate-900/80 rounded-xl p-3 border border-slate-700/60 space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-400">制覇状況</span>
                  <span class="font-bold text-emerald-400"><span id="root-world-cleared">0</span> / 196 (<span id="root-world-pct">0.0%</span>)</span>
                </div>
                <div class="w-full bg-slate-700/60 h-2 rounded-full overflow-hidden">
                  <div id="root-world-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>正答率: <strong id="root-world-acc" class="text-slate-200">--%</strong></span>
                  <span id="root-world-weak-badge" class="text-rose-400">弱点: 0</span>
                </div>
              </div>
            </div>

            <button id="btn-enter-world" class="mt-5 w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg shadow-emerald-600/30 transition flex items-center justify-center gap-2 active:scale-95">
              <span>特訓を始める</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        </div>

        <!-- 共通インフォメーション -->
        <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 text-xs text-slate-400 space-y-2">
          <div class="font-bold text-slate-300 flex items-center gap-1.5">
            <span>💡</span>
            <span>学習のヒント & 本プラットフォームの特徴</span>
          </div>
          <ul class="list-disc list-inside space-y-1 text-slate-400">
            <li><strong>完全オフライン動作</strong>: 外部商用タイル通信を行わず、超軽量ベクターマップのみで爆速レンダリングします。</li>
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
    <header class="bg-slate-800/90 backdrop-blur border-b border-slate-700/80 px-4 py-3 shrink-0 z-10">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <button class="btn-return-root p-2 rounded-lg bg-slate-700/60 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="ホームに戻る">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="hidden sm:inline">ホーム</span>
          </button>
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <span class="text-white font-black text-sm tracking-wider">JP</span>
          </div>
          <div>
            <h1 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              GeoAnki 1741
              <span class="text-xs font-normal text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">JIS準拠</span>
            </h1>
            <p class="text-xs text-slate-400 hidden sm:block">全国1,741市区町村 視覚ベクター暗記トレーナー</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs text-slate-400">全国制覇数</div>
            <div class="text-sm sm:text-base font-extrabold text-emerald-400">
              <span id="muni-hub-cleared">0</span> <span class="text-xs font-normal text-slate-400">/ 1,741</span>
              <span id="muni-hub-pct" class="text-xs font-semibold text-slate-300 ml-1">(0.0%)</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="w-full bg-slate-800/50 border-b border-slate-700/50 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-700/60 h-2.5 rounded-full overflow-hidden">
          <div id="muni-hub-progress-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-xs font-semibold text-slate-300 shrink-0">
          全47都道府県中 <span id="muni-hub-completed-prefs" class="text-emerald-400 font-bold">0</span> 県コンプリート
        </div>
      </div>
    </div>

    <div class="bg-slate-900/90 border-b border-slate-800 px-4 py-2 shrink-0 overflow-x-auto no-scrollbar">
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

    <main class="flex-1 overflow-y-auto px-4 py-4 overscroll-contain">
      <div class="max-w-6xl mx-auto space-y-6" id="muni-hub-container">
      </div>
    </main>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 1B: 市区町村 Spoke (クイズ画面) -->
  <!-- ============================================================== -->
  <div id="screen-muni-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <header class="bg-slate-800/95 backdrop-blur border-b border-slate-700/80 px-2.5 py-1.5 sm:px-3 sm:py-2 shrink-0 z-[1000] flex items-center justify-between gap-1.5">
      <div class="flex items-center gap-1.5 sm:gap-2 min-w-0">
        <button id="btn-muni-back-hub" class="flex items-center gap-1 px-2 py-1.5 sm:px-2.5 sm:py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-xs sm:text-sm font-semibold text-white transition active:scale-95 shrink-0" title="都道府県選択に戻る">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">一覧</span>
        </button>
        <button class="btn-return-root p-1.5 sm:p-2 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-300 hover:text-white transition" title="ホームに戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        </button>
        <div class="flex items-baseline gap-1.5 truncate">
          <h2 id="muni-spoke-pref-title" class="text-sm sm:text-base font-bold text-white tracking-wide truncate">都道府県名</h2>
          <span id="muni-spoke-pref-count-badge" class="text-[10px] sm:text-xs font-medium text-slate-300 bg-slate-700/70 px-1.5 sm:px-2 py-0.5 rounded-full shrink-0">35自治体</span>
        </div>
      </div>

      <div class="flex items-center gap-2 shrink-0">
        <div class="text-right">
          <div class="text-[10px] text-slate-400 leading-none hidden sm:block mb-0.5">制覇状況</div>
          <div class="text-xs font-bold text-emerald-400">
            <span id="muni-spoke-cleared-count">0</span>/<span id="muni-spoke-total-count">0</span>
            <span id="muni-spoke-cleared-pct" class="text-slate-300 font-normal ml-0.5 text-[10px] sm:text-xs">(0%)</span>
          </div>
        </div>
      </div>
    </header>

    <div class="bg-slate-900 border-b border-slate-800 px-2 sm:px-3 py-1 shrink-0 flex items-center justify-between gap-1.5 z-[1000]">
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar flex-1 min-w-0" id="muni-level-tabs-container">
      </div>

      <div class="flex items-center bg-slate-800 p-0.5 rounded-lg border border-slate-700 shrink-0">
        <button class="muni-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-semibold bg-slate-700 text-emerald-400 shadow" data-mode="locate">
          <span>🎯</span><span class="hidden sm:inline ml-1">場所当て</span>
        </button>
        <button class="muni-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="name">
          <span>🔤</span><span class="hidden sm:inline ml-1">4択</span>
        </button>
        <button class="muni-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="type">
          <span>✍️</span><span class="hidden sm:inline ml-1">記入</span>
        </button>
        <button class="muni-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="explore">
          <span>🔍</span><span class="hidden sm:inline ml-1">探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div class="flex-1 relative overflow-hidden bg-slate-950">
      <div id="muni-map" class="w-full h-full map-container relative z-0"></div>

      <!-- ローディング表示 -->
      <div id="muni-loading-overlay" class="absolute inset-0 bg-slate-900/80 backdrop-blur-sm z-[1050] flex flex-col items-center justify-center gap-3 hidden">
        <div class="w-10 h-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
        <div class="text-sm font-semibold text-slate-200">市区町村ベクター(GeoJSON)を取得中...</div>
      </div>

      <!-- 離島ボタン群 & 全体リセット -->
      <div class="absolute top-2 right-2 sm:top-3 sm:right-3 z-[1000] flex flex-col gap-1 sm:gap-1.5 items-end">
        <div id="muni-island-buttons" class="flex flex-col gap-0.5 sm:gap-1 items-end"></div>
        <button id="btn-muni-reset-bounds" class="p-1.5 sm:p-2 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-600/70 shadow-lg backdrop-blur text-xs transition active:scale-95" title="県全体を表示">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
        </button>
      </div>

      <!-- 下部操作ドック -->
      <div class="absolute bottom-0 left-0 right-0 z-[1000] p-2 sm:p-4 pb-[calc(0.5rem+env(safe-area-inset-bottom))] pointer-events-none">
        <div class="max-w-xl mx-auto pointer-events-auto">

          <!-- モード1: 場所当てドック -->
          <div id="muni-dock-locate" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl">
            <div class="flex items-center justify-between gap-1.5 mb-1 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span id="muni-locate-level-tag" class="text-[10px] sm:text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded-full shrink-0">Level 1 主要都市</span>
                <span id="muni-locate-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="muni-locate-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 10</span>
            </div>

            <div class="flex items-center justify-between gap-2">
              <div class="flex-1 min-w-0">
                <div class="text-[10px] sm:text-xs text-slate-400 flex items-center gap-1 truncate">
                  <span>地図上でタップ：</span>
                  <span id="muni-locate-kana" class="text-slate-300 font-medium">（ふりがな）</span>
                </div>
                <div id="muni-locate-question-name" class="text-lg sm:text-2xl font-black text-white truncate tracking-wide leading-tight">
                  〇〇市
                </div>
              </div>
              <button id="btn-muni-locate-skip" class="px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-lg sm:rounded-xl bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">
                スキップ →
              </button>
            </div>

            <div id="muni-locate-feedback-bar" class="mt-2 pt-2 border-t border-slate-700/60 hidden">
              <div id="muni-locate-feedback-content" class="flex items-center justify-between gap-2"></div>
            </div>
          </div>

          <!-- モード2: 4択ドック -->
          <div id="muni-dock-name" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-1.5 mb-1.5 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping shrink-0"></span>
                <span class="text-[11px] sm:text-xs font-bold text-amber-300 truncate">黄色の自治体はどれ？</span>
                <span id="muni-name-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="muni-name-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 10</span>
            </div>
            <div class="grid grid-cols-2 gap-1.5 sm:gap-2" id="muni-choice-buttons-grid"></div>
          </div>

          <!-- モード3: 記入ドック -->
          <div id="muni-dock-type" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-1.5 mb-1.5 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping shrink-0"></span>
                <span class="text-[11px] sm:text-xs font-bold text-amber-300 truncate">黄色の自治体名を入力（市区町村まで）：</span>
                <span id="muni-type-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="muni-type-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 10</span>
            </div>
            <form id="muni-form-type" class="flex items-center gap-1.5 sm:gap-2" onsubmit="event.preventDefault(); return false;">
              <input type="text" id="muni-input-type" placeholder="例: 沼津市、函南町" class="flex-1 bg-slate-900/90 border border-slate-600 text-white placeholder-slate-500 text-sm sm:text-base font-bold px-3 py-1.5 sm:py-2 rounded-lg focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-400" autocomplete="off" />
              <button type="submit" id="btn-muni-type-submit" class="px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs sm:text-sm transition active:scale-95 shrink-0 shadow">回答</button>
              <button type="button" id="btn-muni-type-skip" class="px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-lg bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">スキップ →</button>
            </form>
            <div id="muni-type-feedback-bar" class="mt-2 pt-2 border-t border-slate-700/60 hidden">
              <div id="muni-type-feedback-content" class="flex items-center justify-between gap-2"></div>
            </div>
          </div>

          <!-- モード4: 探索ドック -->
          <div id="muni-dock-explore" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div id="muni-explore-empty" class="text-center py-1 sm:py-2 text-slate-400 text-xs">
              地図上のポリゴンをタップすると自治体情報が表示されます
            </div>
            <div id="muni-explore-detail" class="hidden">
              <div class="flex items-start justify-between gap-2">
                <div>
                  <div class="flex items-center gap-1.5 mb-0.5">
                    <span id="muni-exp-type-badge" class="text-[9px] sm:text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">中核市</span>
                    <span id="muni-exp-kana-text" class="text-[10px] sm:text-xs text-slate-400">ふりがな</span>
                  </div>
                  <h3 id="muni-exp-name-text" class="text-base sm:text-xl font-black text-white">自治体名</h3>
                </div>
                <div class="text-right">
                  <div class="text-[9px] sm:text-[10px] text-slate-400">JISコード</div>
                  <div id="muni-exp-code-text" class="text-xs font-mono font-bold text-slate-200">13101</div>
                </div>
              </div>
              <div class="mt-2 pt-1.5 border-t border-slate-700/60 flex items-center justify-between text-xs">
                <div id="muni-exp-stats-tag" class="text-[11px] sm:text-xs text-slate-400">未挑戦</div>
                <button id="btn-muni-quiz-this" class="text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 text-[11px] sm:text-xs">
                  <span>この自治体をテスト</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 2: 令制国 Spoke (全国一括・クイズ画面) -->
  <!-- ============================================================== -->
  <div id="screen-prov-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <header class="bg-slate-800/95 backdrop-blur border-b border-slate-700/80 px-2.5 py-1.5 sm:px-3 sm:py-2 shrink-0 z-[1000] flex items-center justify-between gap-1.5">
      <div class="flex items-center gap-1.5 sm:gap-2 min-w-0">
        <button class="btn-return-root flex items-center gap-1 px-2 py-1.5 sm:px-2.5 sm:py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-xs sm:text-sm font-semibold text-white transition active:scale-95 shrink-0" title="ホームに戻る">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">ホーム</span>
        </button>
        <div class="flex items-baseline gap-1.5 truncate">
          <h2 class="text-sm sm:text-base font-bold text-white tracking-wide truncate">令制国・旧国名</h2>
          <span class="text-[10px] sm:text-xs font-medium text-slate-300 bg-slate-700/70 px-1.5 sm:px-2 py-0.5 rounded-full shrink-0">全国68国</span>
        </div>
      </div>

      <div class="flex items-center gap-2 shrink-0">
        <div class="text-right">
          <div class="text-[10px] text-slate-400 leading-none hidden sm:block mb-0.5">制覇状況</div>
          <div class="text-xs font-bold text-emerald-400">
            <span id="prov-spoke-cleared-count">0</span>/<span id="prov-spoke-total-count">68</span>
            <span id="prov-spoke-cleared-pct" class="text-slate-300 font-normal ml-0.5 text-[10px] sm:text-xs">(0%)</span>
          </div>
        </div>
      </div>
    </header>

    <div class="bg-slate-900 border-b border-slate-800 px-2 sm:px-3 py-1 shrink-0 flex items-center justify-between gap-1.5 z-[1000]">
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar flex-1 min-w-0" id="prov-level-tabs-container">
      </div>

      <div class="flex items-center bg-slate-800 p-0.5 rounded-lg border border-slate-700 shrink-0">
        <button class="prov-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-semibold bg-slate-700 text-emerald-400 shadow" data-mode="locate">
          <span>🎯</span><span class="hidden sm:inline ml-1">場所当て</span>
        </button>
        <button class="prov-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="name">
          <span>🔤</span><span class="hidden sm:inline ml-1">4択</span>
        </button>
        <button class="prov-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="type">
          <span>✍️</span><span class="hidden sm:inline ml-1">記入</span>
        </button>
        <button class="prov-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="explore">
          <span>🔍</span><span class="hidden sm:inline ml-1">探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div class="flex-1 relative overflow-hidden bg-slate-950">
      <div id="prov-map" class="w-full h-full map-container relative z-0"></div>

      <div class="absolute top-2 right-2 sm:top-3 sm:right-3 z-[1000] flex flex-col gap-1 sm:gap-1.5 items-end">
        <button id="btn-prov-reset-bounds" class="p-1.5 sm:p-2 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-600/70 shadow-lg backdrop-blur text-xs transition active:scale-95" title="全体を表示">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
        </button>
      </div>

      <!-- 下部操作ドック -->
      <div class="absolute bottom-0 left-0 right-0 z-[1000] p-2 sm:p-4 pb-[calc(0.5rem+env(safe-area-inset-bottom))] pointer-events-none">
        <div class="max-w-xl mx-auto pointer-events-auto">

          <!-- モード1: 場所当てドック -->
          <div id="prov-dock-locate" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl">
            <div class="flex items-center justify-between gap-1.5 mb-1 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span id="prov-locate-level-tag" class="text-[10px] sm:text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded-full shrink-0">Lv.1 主要国</span>
                <span id="prov-locate-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="prov-locate-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 15</span>
            </div>

            <div class="flex items-center justify-between gap-2">
              <div class="flex-1 min-w-0">
                <div class="text-[10px] sm:text-xs text-slate-400 flex items-center gap-1 truncate">
                  <span>地図上でタップ：</span>
                  <span id="prov-locate-kana" class="text-slate-300 font-medium">（ふりがな・現代地域）</span>
                </div>
                <div id="prov-locate-question-name" class="text-lg sm:text-2xl font-black text-white truncate tracking-wide leading-tight">
                  武蔵
                </div>
              </div>
              <button id="btn-prov-locate-skip" class="px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-lg sm:rounded-xl bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">
                スキップ →
              </button>
            </div>

            <div id="prov-locate-feedback-bar" class="mt-2 pt-2 border-t border-slate-700/60 hidden">
              <div id="prov-locate-feedback-content" class="flex items-center justify-between gap-2"></div>
            </div>
          </div>

          <!-- モード2: 4択ドック -->
          <div id="prov-dock-name" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-1.5 mb-1.5 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping shrink-0"></span>
                <span class="text-[11px] sm:text-xs font-bold text-amber-300 truncate">黄色の旧国名はどれ？</span>
                <span id="prov-name-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="prov-name-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 15</span>
            </div>
            <div class="grid grid-cols-2 gap-1.5 sm:gap-2" id="prov-choice-buttons-grid"></div>
          </div>

          <!-- モード3: 記入ドック -->
          <div id="prov-dock-type" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-1.5 mb-1.5 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping shrink-0"></span>
                <span class="text-[11px] sm:text-xs font-bold text-amber-300 truncate">黄色の旧国名を入力（漢字またはひらがな）：</span>
                <span id="prov-type-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="prov-type-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 15</span>
            </div>
            <form id="prov-form-type" class="flex items-center gap-1.5 sm:gap-2" onsubmit="event.preventDefault(); return false;">
              <input type="text" id="prov-input-type" placeholder="例: 武蔵、むさし" class="flex-1 bg-slate-900/90 border border-slate-600 text-white placeholder-slate-500 text-sm sm:text-base font-bold px-3 py-1.5 sm:py-2 rounded-lg focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-400" autocomplete="off" />
              <button type="submit" id="btn-prov-type-submit" class="px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs sm:text-sm transition active:scale-95 shrink-0 shadow">回答</button>
              <button type="button" id="btn-prov-type-skip" class="px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-lg bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">スキップ →</button>
            </form>
            <div id="prov-type-feedback-bar" class="mt-2 pt-2 border-t border-slate-700/60 hidden">
              <div id="prov-type-feedback-content" class="flex items-center justify-between gap-2"></div>
            </div>
          </div>

          <!-- モード4: 探索ドック -->
          <div id="prov-dock-explore" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div id="prov-explore-empty" class="text-center py-1 sm:py-2 text-slate-400 text-xs">
              地図上のポリゴンをタップすると旧国情報が表示されます
            </div>
            <div id="prov-explore-detail" class="hidden">
              <div class="flex items-start justify-between gap-2">
                <div>
                  <div class="flex items-center gap-1.5 mb-0.5">
                    <span id="prov-exp-doh-badge" class="text-[9px] sm:text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">東海道</span>
                    <span id="prov-exp-kana-text" class="text-[10px] sm:text-xs text-slate-400">むさし</span>
                  </div>
                  <h3 id="prov-exp-name-text" class="text-base sm:text-xl font-black text-white">武蔵</h3>
                </div>
                <div class="text-right">
                  <div class="text-[9px] sm:text-[10px] text-slate-400">現代の地域</div>
                  <div id="prov-exp-modern-text" class="text-xs font-bold text-slate-200">東京都・埼玉県</div>
                </div>
              </div>
              <div class="mt-2 pt-1.5 border-t border-slate-700/60 flex items-center justify-between text-xs">
                <div id="prov-exp-stats-tag" class="text-[11px] sm:text-xs text-slate-400">未挑戦</div>
                <button id="btn-prov-quiz-this" class="text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 text-[11px] sm:text-xs">
                  <span>この旧国をテスト</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 3A: 世界の国名・首都 Hub (地域選択画面) -->
  <!-- ============================================================== -->
  <div id="screen-world-hub" class="hidden flex-1 flex flex-col h-full overflow-hidden">
    <header class="bg-slate-800/90 backdrop-blur border-b border-slate-700/80 px-4 py-3 shrink-0 z-10">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <button class="btn-return-root p-2 rounded-lg bg-slate-700/60 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center gap-1 text-xs font-bold" title="ホームに戻る">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="hidden sm:inline">ホーム</span>
          </button>
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <span class="text-white font-black text-sm tracking-wider">国</span>
          </div>
          <div>
            <h1 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              GeoAnki World
              <span class="text-xs font-normal text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">196ヶ国</span>
            </h1>
            <p class="text-xs text-slate-400 hidden sm:block">世界の国名・首都名 視覚ベクター暗記トレーナー</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs text-slate-400">全世界制覇数</div>
            <div class="text-sm sm:text-base font-extrabold text-emerald-400">
              <span id="world-hub-cleared">0</span> <span class="text-xs font-normal text-slate-400">/ 196</span>
              <span id="world-hub-pct" class="text-xs font-semibold text-slate-300 ml-1">(0.0%)</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="w-full bg-slate-800/50 border-b border-slate-700/50 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-700/60 h-2.5 rounded-full overflow-hidden">
          <div id="world-hub-progress-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-xs font-semibold text-slate-300 shrink-0">
          制覇地域: <span id="world-hub-completed-regions" class="text-emerald-400 font-bold">0</span> / 6州
        </div>
      </div>
    </div>

    <main class="flex-1 overflow-y-auto px-4 py-4 overscroll-contain">
      <div class="max-w-6xl mx-auto space-y-4">
        <!-- 苦手克服クイックバナー -->
        <div id="world-weak-banner" class="hidden bg-rose-950/40 border border-rose-800/50 rounded-xl p-3 flex items-center justify-between gap-3 shadow-lg">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold text-base shrink-0">
              ⚡
            </div>
            <div>
              <div class="text-xs sm:text-sm font-bold text-white flex items-center gap-1.5">
                <span>世界の苦手克服特訓デッキ</span>
                <span id="world-weak-count-badge" class="px-1.5 py-0.2 rounded-full bg-rose-500/20 text-rose-400 text-[10px] font-semibold">0国</span>
              </div>
              <p class="text-[11px] text-slate-400">直近で間違えた国・首都を集中トレーニング</p>
            </div>
          </div>
          <button id="btn-world-start-weak-all" class="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs transition shrink-0 active:scale-95 shadow">
            復習スタート →
          </button>
        </div>

        <div id="world-cards-container" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-2.5"></div>
      </div>
    </main>
  </div>

  <!-- ============================================================== -->
  <!-- 画面 3B: 世界の国名・首都 Spoke (クイズ画面) -->
  <!-- ============================================================== -->
  <div id="screen-world-spoke" class="hidden flex-1 flex flex-col h-full overflow-hidden relative">
    <header class="bg-slate-800/95 backdrop-blur border-b border-slate-700/80 px-2.5 py-1.5 sm:px-3 sm:py-2 shrink-0 z-[1000] flex items-center justify-between gap-1.5">
      <div class="flex items-center gap-1.5 sm:gap-2 min-w-0">
        <button id="btn-world-back-hub" class="flex items-center gap-1 px-2 py-1.5 sm:px-2.5 sm:py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-xs sm:text-sm font-semibold text-white transition active:scale-95 shrink-0" title="地域一覧に戻る">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span class="hidden sm:inline">一覧</span>
        </button>
        <button class="btn-return-root p-1.5 sm:p-2 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-300 hover:text-white transition" title="ホームに戻る">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        </button>
        <div class="flex items-baseline gap-1.5 truncate">
          <h2 id="world-spoke-title" class="text-sm sm:text-base font-bold text-white tracking-wide truncate">全世界</h2>
          <span id="world-spoke-count-badge" class="text-[10px] sm:text-xs font-medium text-slate-300 bg-slate-700/70 px-1.5 sm:px-2 py-0.5 rounded-full shrink-0">196国</span>
        </div>
      </div>

      <div class="flex items-center gap-2 shrink-0">
        <div class="flex items-center bg-slate-700/70 p-0.5 rounded-lg border border-slate-600/70 text-[11px]" id="world-target-toggle">
          <button id="btn-world-target-country" class="px-2 py-0.5 rounded text-white font-bold bg-emerald-600 transition" title="国名を問う">国名</button>
          <button id="btn-world-target-capital" class="px-2 py-0.5 rounded text-slate-300 hover:text-white transition" title="首都名を問う">首都</button>
        </div>

        <div class="text-right">
          <div class="text-[10px] text-slate-400 leading-none hidden sm:block mb-0.5">制覇状況</div>
          <div class="text-xs font-bold text-emerald-400">
            <span id="world-spoke-cleared-count">0</span>/<span id="world-spoke-total-count">0</span>
            <span id="world-spoke-cleared-pct" class="text-slate-300 font-normal ml-0.5 text-[10px] sm:text-xs">(0%)</span>
          </div>
        </div>
      </div>
    </header>

    <div class="bg-slate-900 border-b border-slate-800 px-2 sm:px-3 py-1 shrink-0 flex items-center justify-between gap-1.5 z-[1000]">
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar flex-1 min-w-0" id="world-level-tabs-container">
      </div>

      <div class="flex items-center bg-slate-800 p-0.5 rounded-lg border border-slate-700 shrink-0">
        <button class="world-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-semibold bg-slate-700 text-emerald-400 shadow" data-mode="locate">
          <span>🎯</span><span class="hidden sm:inline ml-1">場所当て</span>
        </button>
        <button class="world-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="name">
          <span>🔤</span><span class="hidden sm:inline ml-1">4択</span>
        </button>
        <button class="world-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="type">
          <span>✍️</span><span class="hidden sm:inline ml-1">記入</span>
        </button>
        <button class="world-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white" data-mode="explore">
          <span>🔍</span><span class="hidden sm:inline ml-1">探索</span>
        </button>
      </div>
    </div>

    <!-- 地図コンテナ -->
    <div class="flex-1 relative overflow-hidden bg-slate-950">
      <div id="world-map" class="w-full h-full map-container relative z-0"></div>

      <div class="absolute top-2 right-2 sm:top-3 sm:right-3 z-[1000] flex flex-col gap-1 sm:gap-1.5 items-end">
        <button id="btn-world-reset-bounds" class="p-1.5 sm:p-2 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-600/70 shadow-lg backdrop-blur text-xs transition active:scale-95" title="地域全体を表示">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
        </button>
      </div>

      <!-- 下部操作ドック -->
      <div class="absolute bottom-0 left-0 right-0 z-[1000] p-2 sm:p-4 pb-[calc(0.5rem+env(safe-area-inset-bottom))] pointer-events-none">
        <div class="max-w-xl mx-auto pointer-events-auto">

          <!-- モード1: 場所当てドック -->
          <div id="world-dock-locate" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl">
            <div class="flex items-center justify-between gap-1.5 mb-1 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span id="world-locate-level-tag" class="text-[10px] sm:text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded-full shrink-0">Level 1 主要国</span>
                <span id="world-locate-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="world-locate-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 10</span>
            </div>

            <div class="flex items-center justify-between gap-2">
              <div class="flex-1 min-w-0 flex items-center gap-2 sm:gap-3">
                <span id="world-locate-flag" class="text-2xl sm:text-3xl shrink-0">🇫🇷</span>
                <div class="min-w-0">
                  <div class="text-[10px] sm:text-xs text-slate-400 flex items-center gap-1 truncate">
                    <span id="world-locate-prompt-label">地図上でタップ：</span>
                    <span id="world-locate-kana" class="text-slate-300 font-medium">（ふりがな）</span>
                  </div>
                  <div id="world-locate-question-name" class="text-lg sm:text-2xl font-black text-white truncate tracking-wide leading-tight">
                    フランス
                  </div>
                </div>
              </div>
              <button id="btn-world-locate-skip" class="px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-lg sm:rounded-xl bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">
                スキップ →
              </button>
            </div>

            <div id="world-locate-feedback-bar" class="mt-2 pt-2 border-t border-slate-700/60 hidden">
              <div id="world-locate-feedback-content" class="flex items-center justify-between gap-2"></div>
            </div>
          </div>

          <!-- モード2: 4択ドック -->
          <div id="world-dock-name" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-1.5 mb-1.5 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping shrink-0"></span>
                <span id="world-name-prompt-label" class="text-[11px] sm:text-xs font-bold text-amber-300 truncate">黄色の国の名前はどれ？</span>
                <span id="world-name-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="world-name-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 10</span>
            </div>
            <div class="grid grid-cols-2 gap-1.5 sm:gap-2" id="world-choice-buttons-grid"></div>
          </div>

          <!-- モード3: 記入ドック -->
          <div id="world-dock-type" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-1.5 mb-1.5 sm:mb-2">
              <div class="flex items-center gap-1.5 truncate">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping shrink-0"></span>
                <span id="world-type-prompt-label" class="text-[11px] sm:text-xs font-bold text-amber-300 truncate">黄色の国の国名を入力：</span>
                <span id="world-type-accuracy-tag" class="text-[10px] sm:text-xs font-semibold px-1.5 py-0.5 rounded-full border shrink-0 text-slate-400 bg-slate-700/40 border-slate-600/40">正答率: --%</span>
              </div>
              <span id="world-type-progress-tag" class="text-[11px] sm:text-xs font-medium text-slate-400 shrink-0">問題 1 / 10</span>
            </div>
            <form id="world-form-type" class="flex items-center gap-1.5 sm:gap-2" onsubmit="event.preventDefault(); return false;">
              <input type="text" id="world-input-type" placeholder="例: フランス、パリ" class="flex-1 bg-slate-900/90 border border-slate-600 text-white placeholder-slate-500 text-sm sm:text-base font-bold px-3 py-1.5 sm:py-2 rounded-lg focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-400" autocomplete="off" />
              <button type="submit" id="btn-world-type-submit" class="px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs sm:text-sm transition active:scale-95 shrink-0 shadow">回答</button>
              <button type="button" id="btn-world-type-skip" class="px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-lg bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">スキップ →</button>
            </form>
            <div id="world-type-feedback-bar" class="mt-2 pt-2 border-t border-slate-700/60 hidden">
              <div id="world-type-feedback-content" class="flex items-center justify-between gap-2"></div>
            </div>
          </div>

          <!-- モード4: 探索ドック -->
          <div id="world-dock-explore" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 shadow-2xl hidden">
            <div id="world-explore-empty" class="text-center py-1 sm:py-2 text-slate-400 text-xs">
              地図上の国をタップすると国名・首都情報が表示されます
            </div>
            <div id="world-explore-detail" class="hidden">
              <div class="flex items-start justify-between gap-2">
                <div class="flex items-center gap-2 sm:gap-3">
                  <span id="world-exp-flag-text" class="text-2xl sm:text-3xl shrink-0">🇯🇵</span>
                  <div>
                    <div class="flex items-center gap-1.5 mb-0.5">
                      <span id="world-exp-region-badge" class="text-[9px] sm:text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">ヨーロッパ</span>
                      <span id="world-exp-kana-text" class="text-[10px] sm:text-xs text-slate-400">ふらんす</span>
                    </div>
                    <h3 id="world-exp-name-text" class="text-base sm:text-xl font-black text-white">フランス</h3>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-[9px] sm:text-[10px] text-slate-400">首都 (ISO)</div>
                  <div id="world-exp-capital-text" class="text-xs font-bold text-slate-200">パリ (FRA)</div>
                </div>
              </div>
              <div class="mt-2 pt-1.5 border-t border-slate-700/60 flex items-center justify-between text-xs">
                <div id="world-exp-stats-tag" class="text-[11px] sm:text-xs text-slate-400">未挑戦</div>
                <button id="btn-world-quiz-this" class="text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 text-[11px] sm:text-xs">
                  <span>この国をテスト</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 共通モーダル: データ管理 & 設定 -->
  <!-- ============================================================== -->
  <div id="modal-data-mgr" class="fixed inset-0 z-[1100] bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 hidden">
    <div class="bg-slate-800 border border-slate-700 rounded-2xl max-w-md w-full p-5 space-y-4 shadow-2xl">
      <div class="flex items-center justify-between border-b border-slate-700 pb-3">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <span>⚙️</span>
          <span>データ管理 & 設定</span>
        </h3>
        <button id="btn-close-data-mgr" class="text-slate-400 hover:text-white p-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-700/60 space-y-2">
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

        <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-700/60 space-y-2">
          <div class="font-bold text-slate-300">データのエクスポート / インポート</div>
          <p class="text-slate-400 text-[11px]">学習履歴（正誤回数、制覇記録）をJSON形式でバックアップ・移行できます。</p>
          <div class="flex gap-2">
            <button id="btn-export-all-data" class="flex-1 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition text-[11px]">
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

    const WORLD_MASTER = {world_master_json};
    const WORLD_GEOJSON = {world_geo_json};
    const WORLD_REGIONS = {world_regions_json};
  </script>

  <!-- ============================================================== -->
  <!-- メインスクリプト -->
  <!-- ============================================================== -->
  <script>
    function getFlagEmoji(alpha2) {{
      if (!alpha2 || alpha2.length !== 2) return '🌐';
      const codePoints = [...alpha2.toUpperCase()].map(c => 127397 + c.charCodeAt(0));
      return String.fromCodePoint(...codePoints);
    }}

    // --- Web Audio API サウンドシステム ---
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
        this.playTone(587.33, 'sine', 0.18, 0, 0.2);
        this.playTone(880.00, 'sine', 0.25, 0.08, 0.22);
      }}
      wrong() {{
        this.playTone(220, 'sawtooth', 0.22, 0, 0.15);
        this.playTone(174.61, 'sawtooth', 0.25, 0.08, 0.15);
      }}
      fanfare() {{
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((f, i) => this.playTone(f, 'sine', 0.35, i * 0.1, 0.25));
      }}
    }}
    const sound = new SoundEngine();

    // --- Storage ---
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

    const KEYS = {{
      MUNI: 'geoanki_muni_v1',
      PROV: 'geoanki_province_v1',
      WORLD: 'geoanki_world_v1'
    }};

    // --- Router ---
    const AppRouter = {{
      currentScreen: 'screen-root-hub',
      screens: [
        'screen-root-hub',
        'screen-muni-hub',
        'screen-muni-spoke',
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

    // --- Root Hub ---
    const RootHub = {{
      init() {{
        document.getElementById('btn-enter-muni').onclick = () => {{
          sound.init();
          AppRouter.navigate('screen-muni-hub');
          MuniApp.renderHub();
        }};
        document.getElementById('btn-enter-province').onclick = () => {{
          sound.init();
          AppRouter.navigate('screen-prov-spoke');
          ProvApp.openSpoke();
        }};
        document.getElementById('btn-enter-world').onclick = () => {{
          sound.init();
          AppRouter.navigate('screen-world-hub');
          WorldApp.renderHub();
        }};

        document.querySelectorAll('.btn-return-root').forEach(btn => {{
          btn.onclick = () => AppRouter.navigate('screen-root-hub');
        }});

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

        const modal = document.getElementById('modal-data-mgr');
        document.getElementById('btn-show-data-mgr').onclick = () => modal.classList.remove('hidden');
        document.getElementById('btn-close-data-mgr').onclick = () => modal.classList.add('hidden');

        document.getElementById('btn-reset-muni-data').onclick = () => {{
          if (confirm('市区町村の全学習データをリセットしますか？')) {{
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
      currentLevel: 'ALL',
      currentMode: 'locate',
      questionPool: [],
      currentIndex: 0,
      currentQuestion: null,
      isAnswered: false,
      answeredResult: null,
      activeRegionFilter: 'ALL',
      geoJsonCache: {{}},

      init() {{
        this.data = STORAGE.get(KEYS.MUNI, {{ records: {{}} }});
        if (!this.data.records) this.data.records = {{}};

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

        document.getElementById('btn-muni-back-hub').onclick = () => {{
          AppRouter.navigate('screen-muni-hub');
          this.renderHub();
        }};
        document.getElementById('btn-muni-reset-bounds').onclick = () => {{
          if (this.map && this.geoJsonLayer) {{
            if (this.currentPref.defaultView) this.map.fitBounds(this.currentPref.defaultView, {{ padding: [20, 20] }});
            else this.map.fitBounds(this.geoJsonLayer.getBounds(), {{ padding: [20, 20] }});
          }}
        }};

        document.querySelectorAll('.muni-mode-tab-btn').forEach(btn => {{
          btn.onclick = () => this.setMode(btn.dataset.mode);
        }});

        document.getElementById('btn-muni-locate-skip').onclick = () => this.skipQuestion();
        document.getElementById('btn-muni-type-skip').onclick = () => this.skipQuestion();

        document.getElementById('btn-muni-quiz-this').onclick = () => {{
          if (this.selectedMuni) {{
            this.setMode('locate');
            this.startSingleQuestion(this.selectedMuni);
          }}
        }};

        const typeForm = document.getElementById('muni-form-type');
        const typeInput = document.getElementById('muni-input-type');
        typeForm.onsubmit = (e) => {{
          if (e) e.preventDefault();
          if (this.isAnswered) {{
            this.currentIndex++;
            this.nextQuestion();
            return false;
          }}
          const val = typeInput.value.trim();
          const q = this.currentQuestion;
          const isCorrect = (val === q[3] || val === q[4]);
          this.handleAnswer(isCorrect, typeInput);
          return false;
        }};

        window.addEventListener('keydown', (e) => {{
          if (AppRouter.currentScreen !== 'screen-muni-spoke') return;
          if (e.target.tagName === 'INPUT' && e.key !== 'Enter') return;
          this.handleKey(e);
        }});
      }},

      renderHub() {{
        const container = document.getElementById('muni-hub-container');
        container.innerHTML = '';

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
                : 'bg-slate-800/80 border-slate-700/80 hover:border-slate-600'
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
                <div class="w-full bg-slate-700/60 h-1.5 rounded-full overflow-hidden">
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

        if (!this.map) {{
          this.map = L.map('muni-map', {{
            attributionControl: false,
            zoomControl: false,
            renderer: L.svg({{ padding: 1.5 }})
          }});
          L.control.zoom({{ position: 'bottomright' }}).addTo(this.map);
        }}

        const islandContainer = document.getElementById('muni-island-buttons');
        islandContainer.innerHTML = '';
        if (pref.islands && pref.islands.length > 0) {{
          pref.islands.forEach(isl => {{
            const btn = document.createElement('button');
            btn.className = 'px-2 py-1 rounded bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-600/70 text-[10px] font-bold shadow-lg';
            btn.textContent = `📍 ${{isl.label}}`;
            btn.onclick = () => this.map.fitBounds(isl.bounds, {{ padding: [20, 20], animate: true }});
            islandContainer.appendChild(btn);
          }});
        }}

        await this.loadGeoJson(pref.code);
        this.renderLevelTabs();
        this.startLevel('ALL');
      }},

      async loadGeoJson(prefCode) {{
        if (this.geoJsonCache[prefCode]) {{
          this.currentGeoJson = this.geoJsonCache[prefCode];
          return;
        }}

        const loading = document.getElementById('muni-loading-overlay');
        loading.classList.remove('hidden');

        // 正式な全国自治体ベクターGeoJSONのURL（smartnews-smri / 国土数値情報N03-21準拠）
        const primaryUrl = `https://cdn.jsdelivr.net/gh/smartnews-smri/japan-topography@main/data/municipality/geojson/s0010/N03-21_${{prefCode}}_210101.json`;
        const fallbackUrl = `https://raw.githubusercontent.com/smartnews-smri/japan-topography/main/data/municipality/geojson/s0010/N03-21_${{prefCode}}_210101.json`;

        try {{
          let resp = await fetch(primaryUrl);
          if (!resp.ok) resp = await fetch(fallbackUrl);
          if (resp.ok) {{
            const data = await resp.json();
            this.geoJsonCache[prefCode] = data;
            this.currentGeoJson = data;
          }} else {{
            throw new Error(`HTTP ${{resp.status}}`);
          }}
        }} catch(e) {{
          console.error("GeoJSON load failed:", e);
          alert('地図データの読み込みに失敗しました。ネットワーク接続を確認してください。');
        }} finally {{
          loading.classList.add('hidden');
        }}
      }},

      renderLevelTabs() {{
        const container = document.getElementById('muni-level-tabs-container');
        container.innerHTML = '';

        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code);
        const counts = {{
          1: prefMunis.filter(m => m[6] === 1).length,
          2: prefMunis.filter(m => m[6] === 2).length,
          3: prefMunis.filter(m => m[6] === 3).length,
          4: prefMunis.filter(m => m[6] === 4).length,
          ALL: prefMunis.length,
          WEAK: prefMunis.filter(m => this.data.records[m[0]] && this.data.records[m[0]].last === 'wrong').length
        }};

        const tabs = [
          {{ id: 1, label: 'Lv.1 主要都市', count: counts[1] }},
          {{ id: 2, label: 'Lv.2 市', count: counts[2] }},
          {{ id: 3, label: 'Lv.3 町', count: counts[3] }},
          {{ id: 4, label: 'Lv.4 村', count: counts[4] }},
          {{ id: 'ALL', label: '全自治体', count: counts.ALL }},
          {{ id: 'WEAK', label: '⚠️ 弱点復習', count: counts.WEAK }}
        ];

        tabs.forEach(t => {{
          if (t.count === 0 && t.id !== 'ALL' && t.id !== 'WEAK') return;
          const btn = document.createElement('button');
          btn.className = `level-tab-btn px-2 sm:px-2.5 py-0.5 sm:py-1 rounded text-[11px] sm:text-xs font-semibold whitespace-nowrap shrink-0 transition ${{
            this.currentLevel === t.id
              ? 'bg-emerald-500 text-white'
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
          }}`;
          btn.innerHTML = `<span>${{t.label}}</span> <span class="font-normal opacity-80">(${{t.count}})</span>`;
          btn.onclick = () => this.startLevel(t.id);
          container.appendChild(btn);
        }});
      }},

      startLevel(levelId) {{
        this.currentLevel = levelId;
        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code);

        if (levelId === 'ALL') {{
          this.questionPool = [...prefMunis];
        }} else if (levelId === 'WEAK') {{
          this.questionPool = prefMunis.filter(m => this.data.records[m[0]] && this.data.records[m[0]].last === 'wrong');
          if (this.questionPool.length === 0) {{
            alert('弱点の自治体はありません！');
            this.startLevel('ALL');
            return;
          }}
        }} else {{
          this.questionPool = prefMunis.filter(m => m[6] === levelId);
        }}

        this.questionPool.sort(() => Math.random() - 0.5);
        this.currentIndex = 0;
        this.renderLevelTabs();
        this.renderMapLayers();
        this.nextQuestion();
      }},

      renderMapLayers() {{
        if (!this.map || !this.currentGeoJson) return;
        if (this.geoJsonLayer) this.map.removeLayer(this.geoJsonLayer);

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
            let code = String(feature.properties.N03_007 || feature.properties.code || '');
            const isTarget = targetCodes.has(code) || (WARD_TO_CITY[code] && targetCodes.has(WARD_TO_CITY[code]));

            layer.on({{
              mouseover: (e) => {{
                if (this.isAnswered) return;
                // 対象外の国・自治体はホバー変化させない
                if (!isTarget && this.currentMode !== 'explore') return;
                e.target.setStyle({{ fillColor: '#e2e8f0', fillOpacity: 1 }});
              }},
              mouseout: (e) => {{
                this.resetPolygonStyles();
              }},
              click: () => {{
                // 対象外の国・自治体はクリック選択不可
                if (!isTarget && this.currentMode !== 'explore') return;
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
        document.querySelectorAll('.muni-mode-tab-btn').forEach(btn => {{
          if (btn.dataset.mode === mode) {{
            btn.className = 'muni-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-semibold bg-slate-700 text-emerald-400 shadow';
          }} else {{
            btn.className = 'muni-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white';
          }}
        }});

        ['locate', 'name', 'type', 'explore'].forEach(m => {{
          const dock = document.getElementById(`muni-dock-${{m}}`);
          if (dock) {{
            if (m === mode) dock.classList.remove('hidden');
            else dock.classList.add('hidden');
          }}
        }});

        this.nextQuestion();
      }},

      nextQuestion() {{
        this.isAnswered = false;
        this.answeredResult = null;
        document.getElementById('muni-locate-feedback-bar').classList.add('hidden');
        document.getElementById('muni-type-feedback-bar').classList.add('hidden');

        if (this.currentMode === 'explore') return;

        if (this.currentIndex >= this.questionPool.length) {{
          sound.fanfare();
          alert('このレベルの全問題を完了しました！');
          this.startLevel(this.currentLevel);
          return;
        }}

        this.currentQuestion = this.questionPool[this.currentIndex];
        this.updateHeaderProgress();

        const q = this.currentQuestion;
        const rec = this.data.records[q[0]] || {{ correct: 0, wrong: 0 }};
        const total = rec.correct + rec.wrong;
        const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
        const progStr = `問題 ${{this.currentIndex + 1}} / ${{this.questionPool.length}}`;

        if (this.currentMode === 'locate') {{
          document.getElementById('muni-locate-level-tag').textContent = `Lv.${{q[6]}} ${{q[5]}}`;
          document.getElementById('muni-locate-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('muni-locate-progress-tag').textContent = progStr;
          document.getElementById('muni-locate-kana').textContent = `（${{q[4]}}）`;
          document.getElementById('muni-locate-question-name').textContent = q[3];
          this.resetPolygonStyles();
        }} else if (this.currentMode === 'name') {{
          document.getElementById('muni-name-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('muni-name-progress-tag').textContent = progStr;
          this.highlightQuestionPolygon();
          this.renderNameChoices();
        }} else if (this.currentMode === 'type') {{
          document.getElementById('muni-type-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('muni-type-progress-tag').textContent = progStr;
          const input = document.getElementById('muni-input-type');
          input.value = '';
          input.focus();
          this.highlightQuestionPolygon();
        }}
      }},

      resetPolygonStyles() {{
        if (!this.geoJsonLayer) return;
        const targetCodes = new Set(this.questionPool.map(m => m[0]));
        const isHighlightMode = (this.currentMode === 'name' || this.currentMode === 'type');
        const currentCode = (this.currentQuestion && isHighlightMode) ? this.currentQuestion[0] : null;

        this.geoJsonLayer.eachLayer(layer => {{
          if (!layer.feature || !layer.feature.properties) return;
          if (layer._path) layer._path.classList.remove('polygon-pulse');

          const featProps = layer.feature.properties;
          let code = String(featProps.N03_007 || featProps.code || '');
          const cityCode = WARD_TO_CITY[code] || code;
          const isTarget = targetCodes.has(code) || targetCodes.has(cityCode);

          // 回答後のハイライト判定
          if (this.isAnswered && this.answeredResult) {{
            const res = this.answeredResult;
            if (res.isCorrect) {{
              if (code === res.code || cityCode === res.code) {{
                layer.setStyle({{ fillColor: '#34d399', fillOpacity: 0.95, weight: 3.5, color: '#059669' }});
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
            }} else {{
              // 不正解時: 正解場所は黄色点滅
              if (code === res.correctCode || cityCode === res.correctCode) {{
                layer.setStyle({{ fillColor: '#fbbf24', fillOpacity: 0.95, weight: 3.5, color: '#eab308' }});
                if (layer._path) layer._path.classList.add('polygon-pulse');
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
              // 誤ってタップした場所は赤色
              if (res.wrongCode && (code === res.wrongCode || cityCode === res.wrongCode)) {{
                layer.setStyle({{ fillColor: '#f87171', fillOpacity: 0.95, weight: 3.5, color: '#dc2626' }});
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
            }}
          }}

          // 通常出題中（4択または記入）のハイライト
          const isCurrentHighlight = !this.isAnswered && currentCode && (code === currentCode || cityCode === currentCode);
          if (isCurrentHighlight) {{
            layer.setStyle({{
              fillColor: '#fbbf24',
              fillOpacity: 0.95,
              weight: 3.5,
              color: '#f59e0b'
            }});
            if (layer.bringToFront) layer.bringToFront();
          }} else {{
            layer.setStyle({{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.65,
              color: '#090d16',
              weight: 1.2
            }});
          }}
        }});
      }},

      highlightQuestionPolygon() {{
        if (!this.geoJsonLayer || !this.currentQuestion) return;
        this.resetPolygonStyles();

        const code = this.currentQuestion[0];
        let targetBounds = null;

        this.geoJsonLayer.eachLayer(layer => {{
          if (!layer.feature || !layer.feature.properties) return;
          const featProps = layer.feature.properties;
          const featCode = String(featProps.N03_007 || featProps.code || '');
          if (featCode === code || WARD_TO_CITY[featCode] === code) {{
            if (layer.getBounds && layer.getBounds().isValid()) {{
              targetBounds = targetBounds ? targetBounds.extend(layer.getBounds()) : layer.getBounds();
            }}
          }}
        }});

        if (targetBounds && (this.currentMode === 'name' || this.isAnswered)) {{
          this.map.flyToBounds(targetBounds, {{ maxZoom: 10.5, duration: 0.5 }});
        }}
      }},

      renderNameChoices() {{
        const grid = document.getElementById('muni-choice-buttons-grid');
        grid.innerHTML = '';
        const q = this.currentQuestion;

        const prefMunis = MUNI_RAW_DATA.filter(m => m[1] === this.currentPref.code && m[0] !== q[0]);
        prefMunis.sort(() => Math.random() - 0.5);
        const choices = [q, ...prefMunis.slice(0, 3)].sort(() => Math.random() - 0.5);

        choices.forEach((c, idx) => {{
          const btn = document.createElement('button');
          btn.className = 'muni-choice-btn py-2 px-3 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition flex items-center gap-2 active:scale-95';
          btn.dataset.code = c[0];
          btn.innerHTML = `
            <span class="w-5 h-5 rounded bg-slate-900 text-slate-400 flex items-center justify-center text-[10px] font-mono">${{idx + 1}}</span>
            <span class="truncate">${{c[3]}}</span>
          `;
          btn.onclick = () => this.handleAnswer(c[0] === q[0], btn);
          grid.appendChild(btn);
        }});
      }},

      skipQuestion() {{
        if (this.isAnswered) return;
        this.currentIndex++;
        this.nextQuestion();
      }},

      onPolygonClick(feature, layer) {{
        let code = String(feature.properties.N03_007 || feature.properties.code || '');
        if (WARD_TO_CITY[code]) code = WARD_TO_CITY[code];

        const targetMuni = MUNI_RAW_DATA.find(m => m[0] === code);
        if (!targetMuni) return;

        if (this.currentMode === 'locate') {{
          if (this.isAnswered) return;
          const isCorrect = (code === this.currentQuestion[0]);
          this.handleAnswer(isCorrect, layer, code);
        }} else if (this.currentMode === 'explore') {{
          this.selectedMuni = targetMuni;
          document.getElementById('muni-explore-empty').classList.add('hidden');
          document.getElementById('muni-explore-detail').classList.remove('hidden');

          document.getElementById('muni-exp-type-badge').textContent = targetMuni[5];
          document.getElementById('muni-exp-kana-text').textContent = targetMuni[4];
          document.getElementById('muni-exp-name-text').textContent = targetMuni[3];
          document.getElementById('muni-exp-code-text').textContent = targetMuni[0];

          const rec = this.data.records[targetMuni[0]] || {{ correct: 0, wrong: 0 }};
          const total = rec.correct + rec.wrong;
          const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
          document.getElementById('muni-exp-stats-tag').textContent = `正解 ${{rec.correct}} / 不正解 ${{rec.wrong}} (正答率: ${{pct}})`;
        }}
      }},

      handleAnswer(isCorrect, targetEl, clickedCode = null) {{
        if (this.isAnswered) return;
        this.isAnswered = true;

        const q = this.currentQuestion;
        if (!this.data.records[q[0]]) this.data.records[q[0]] = {{ correct: 0, wrong: 0 }};
        const rec = this.data.records[q[0]];

        if (isCorrect) {{
          this.answeredResult = {{ isCorrect: true, code: q[0] }};
          sound.correct();
          rec.correct++;
          rec.last = 'correct';
          rec.updated = Date.now();
          STORAGE.set(KEYS.MUNI, this.data);

          if (this.currentMode === 'locate') {{
            const bar = document.getElementById('muni-locate-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `<div class="text-xs font-bold text-emerald-400">⭕ 正解！素晴らしい！</div>`;
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-emerald-600', '!border-emerald-400');
          }} else if (this.currentMode === 'type') {{
            const bar = document.getElementById('muni-type-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `<div class="text-xs font-bold text-emerald-400">⭕ 正解！素晴らしい！</div>`;
          }}

          this.resetPolygonStyles();

          setTimeout(() => {{
            this.currentIndex++;
            this.nextQuestion();
          }}, 900);
        }} else {{
          this.answeredResult = {{ isCorrect: false, correctCode: q[0], wrongCode: clickedCode }};
          sound.wrong();
          rec.wrong++;
          rec.last = 'wrong';
          rec.updated = Date.now();
          STORAGE.set(KEYS.MUNI, this.data);

          if (this.currentMode === 'locate') {{
            this.resetPolygonStyles();
            const bar = document.getElementById('muni-locate-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-rose-400">❌ 惜しい！正解は黄色点滅の場所です</span>
                <button type="button" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white" onclick="MuniApp.currentIndex++; MuniApp.nextQuestion();">次へ (Enter ↵)</button>
              </div>
            `;
          }} else if (this.currentMode === 'name') {{
            this.resetPolygonStyles();
            if (targetEl) targetEl.classList.add('!bg-rose-700');
            const correctBtn = document.querySelector(`.muni-choice-btn[data-code="${{q[0]}}"]`);
            if (correctBtn) correctBtn.classList.add('!border-emerald-400', '!border-2');
          }} else if (this.currentMode === 'type') {{
            this.resetPolygonStyles();
            const bar = document.getElementById('muni-type-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-rose-400">❌ 正解: ${{q[3]}}</span>
                <button type="button" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white" onclick="MuniApp.currentIndex++; MuniApp.nextQuestion();">次へ (Enter ↵)</button>
              </div>
            `;
          }}
        }}
      }},

      startSingleQuestion(muni) {{
        this.questionPool = [muni];
        this.currentIndex = 0;
        this.renderMapLayers();
        this.nextQuestion();
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
        let cleared = 0;
        prefMunis.forEach(m => {{
          const r = this.data.records[m[0]];
          if (r && r.correct > 0) cleared++;
        }});
        document.getElementById('muni-spoke-cleared-count').textContent = cleared;
        document.getElementById('muni-spoke-total-count').textContent = prefMunis.length;
        const pct = prefMunis.length > 0 ? Math.round((cleared / prefMunis.length) * 100) : 0;
        document.getElementById('muni-spoke-cleared-pct').textContent = `(${{pct}}%)`;
      }}
    }};

    // ==============================================================
    // モジュール 2: 令制国・旧国名暗記 (ProvApp - 全国一括 & 4段階レベル)
    // ==============================================================
    const ProvApp = {{
      data: null,
      map: null,
      geoJsonLayer: null,
      currentLevel: 'ALL',
      currentMode: 'locate',
      questionPool: [],
      currentIndex: 0,
      currentQuestion: null,
      isAnswered: false,
      answeredResult: null,

      init() {{
        this.data = STORAGE.get(KEYS.PROV, {{ records: {{}} }});
        if (!this.data.records) this.data.records = {{}};

        document.getElementById('btn-prov-reset-bounds').onclick = () => {{
          if (this.map && this.geoJsonLayer) {{
            this.map.fitBounds(this.geoJsonLayer.getBounds(), {{ padding: [20, 20] }});
          }}
        }};

        document.querySelectorAll('.prov-mode-tab-btn').forEach(btn => {{
          btn.onclick = () => this.setMode(btn.dataset.mode);
        }});

        document.getElementById('btn-prov-locate-skip').onclick = () => this.skipQuestion();
        document.getElementById('btn-prov-type-skip').onclick = () => this.skipQuestion();

        document.getElementById('btn-prov-quiz-this').onclick = () => {{
          if (this.selectedProv) {{
            this.setMode('locate');
            this.startSingleQuestion(this.selectedProv);
          }}
        }};

        const typeForm = document.getElementById('prov-form-type');
        const typeInput = document.getElementById('prov-input-type');
        typeForm.onsubmit = (e) => {{
          if (e) e.preventDefault();
          if (this.isAnswered) {{
            this.currentIndex++;
            this.nextQuestion();
            return false;
          }}
          const val = typeInput.value.trim();
          const q = this.currentQuestion;
          const isCorrect = (val === q.name || val === q.kana || (q.aliases && q.aliases.includes(val)));
          this.handleAnswer(isCorrect, typeInput);
          return false;
        }};

        window.addEventListener('keydown', (e) => {{
          if (AppRouter.currentScreen !== 'screen-prov-spoke') return;
          if (e.target.tagName === 'INPUT' && e.key !== 'Enter') return;
          this.handleKey(e);
        }});
      }},

      openSpoke(initialLevel = 'ALL') {{
        this.updateHeaderProgress();

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
        const container = document.getElementById('prov-level-tabs-container');
        container.innerHTML = '';

        const allProvs = Object.values(PROVINCES_MASTER);

        const counts = {{
          1: allProvs.filter(p => p.lvl === 1).length,
          2: allProvs.filter(p => p.lvl === 2).length,
          3: allProvs.filter(p => p.lvl === 3).length,
          4: allProvs.filter(p => p.lvl === 4).length,
          ALL: allProvs.length,
          WEAK: allProvs.filter(p => this.data.records[p.code] && this.data.records[p.code].last === 'wrong').length
        }};

        const tabs = [
          {{ id: 1, label: 'Lv.1 主要国', count: counts[1] }},
          {{ id: 2, label: 'Lv.2 中堅国', count: counts[2] }},
          {{ id: 3, label: 'Lv.3 一般国', count: counts[3] }},
          {{ id: 4, label: 'Lv.4 小国・難関', count: counts[4] }},
          {{ id: 'ALL', label: '全68国', count: counts.ALL }},
          {{ id: 'WEAK', label: '⚠️ 弱点復習', count: counts.WEAK }}
        ];

        tabs.forEach(t => {{
          if (t.count === 0 && t.id !== 'ALL' && t.id !== 'WEAK') return;
          const btn = document.createElement('button');
          btn.className = `level-tab-btn px-2 sm:px-2.5 py-0.5 sm:py-1 rounded text-[11px] sm:text-xs font-semibold whitespace-nowrap shrink-0 transition ${{
            this.currentLevel === t.id
              ? 'bg-emerald-500 text-white'
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
          }}`;
          btn.innerHTML = `<span>${{t.label}}</span> <span class="font-normal opacity-80">(${{t.count}})</span>`;
          btn.onclick = () => this.startLevel(t.id);
          container.appendChild(btn);
        }});
      }},

      startLevel(levelId) {{
        this.currentLevel = levelId;
        const allProvs = Object.values(PROVINCES_MASTER);

        if (levelId === 'ALL') {{
          this.questionPool = [...allProvs];
        }} else if (levelId === 'WEAK') {{
          this.questionPool = allProvs.filter(p => this.data.records[p.code] && this.data.records[p.code].last === 'wrong');
          if (this.questionPool.length === 0) {{
            alert('弱点の旧国はありません！');
            this.startLevel('ALL');
            return;
          }}
        }} else {{
          this.questionPool = allProvs.filter(p => p.lvl === levelId);
        }}

        this.questionPool.sort(() => Math.random() - 0.5);
        this.currentIndex = 0;
        this.renderLevelTabs();
        this.renderMapLayers();
        this.nextQuestion();
      }},

      renderMapLayers() {{
        if (!this.map || !PROVINCES_GEOJSON) return;
        if (this.geoJsonLayer) this.map.removeLayer(this.geoJsonLayer);

        const targetCodes = new Set(this.questionPool.map(p => p.code));

        this.geoJsonLayer = L.geoJSON(PROVINCES_GEOJSON, {{
          style: (feature) => {{
            const code = feature.properties.code;
            const isTarget = targetCodes.has(code);
            return {{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.65,
              color: '#090d16',
              weight: 1.2,
              opacity: 1
            }};
          }},
          onEachFeature: (feature, layer) => {{
            const code = feature.properties.code;
            const isTarget = targetCodes.has(code);

            layer.on({{
              mouseover: (e) => {{
                // レベル対象外はホバー変化しない
                if (!isTarget && this.currentMode !== 'explore') return;
                e.target.setStyle({{ fillColor: '#e2e8f0', fillOpacity: 1 }});
              }},
              mouseout: (e) => {{
                this.resetPolygonStyles();
              }},
              click: () => {{
                // レベル対象外は選択不可
                if (!isTarget && this.currentMode !== 'explore') return;
                this.onPolygonClick(feature, layer);
              }}
            }});
          }}
        }}).addTo(this.map);

        this.map.fitBounds(this.geoJsonLayer.getBounds(), {{ padding: [20, 20] }});
      }},

      setMode(mode) {{
        this.currentMode = mode;
        document.querySelectorAll('.prov-mode-tab-btn').forEach(btn => {{
          if (btn.dataset.mode === mode) {{
            btn.className = 'prov-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-semibold bg-slate-700 text-emerald-400 shadow';
          }} else {{
            btn.className = 'prov-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white';
          }}
        }});

        ['locate', 'name', 'type', 'explore'].forEach(m => {{
          const dock = document.getElementById(`prov-dock-${{m}}`);
          if (dock) {{
            if (m === mode) dock.classList.remove('hidden');
            else dock.classList.add('hidden');
          }}
        }});

        this.nextQuestion();
      }},

      nextQuestion() {{
        this.isAnswered = false;
        this.answeredResult = null;
        document.getElementById('prov-locate-feedback-bar').classList.add('hidden');
        document.getElementById('prov-type-feedback-bar').classList.add('hidden');

        if (this.currentMode === 'explore') return;

        if (this.currentIndex >= this.questionPool.length) {{
          sound.fanfare();
          alert('このレベルの全問題を完了しました！');
          this.startLevel(this.currentLevel);
          return;
        }}

        this.currentQuestion = this.questionPool[this.currentIndex];
        this.updateHeaderProgress();

        const q = this.currentQuestion;
        const rec = this.data.records[q.code] || {{ correct: 0, wrong: 0 }};
        const total = rec.correct + rec.wrong;
        const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
        const progStr = `問題 ${{this.currentIndex + 1}} / ${{this.questionPool.length}}`;

        const lvlNames = {{ 1: '主要国', 2: '中堅国', 3: '一般国', 4: '小国・難関' }};

        if (this.currentMode === 'locate') {{
          document.getElementById('prov-locate-level-tag').textContent = `Lv.${{q.lvl}} ${{lvlNames[q.lvl] || ''}}`;
          document.getElementById('prov-locate-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('prov-locate-progress-tag').textContent = progStr;
          document.getElementById('prov-locate-kana').textContent = `（${{q.kana}}・${{q.pref || q.modern || ''}}）`;
          document.getElementById('prov-locate-question-name').textContent = q.name;
          this.resetPolygonStyles();
        }} else if (this.currentMode === 'name') {{
          document.getElementById('prov-name-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('prov-name-progress-tag').textContent = progStr;
          this.highlightQuestionPolygon();
          this.renderNameChoices();
        }} else if (this.currentMode === 'type') {{
          document.getElementById('prov-type-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('prov-type-progress-tag').textContent = progStr;
          const input = document.getElementById('prov-input-type');
          input.value = '';
          input.focus();
          this.highlightQuestionPolygon();
        }}
      }},

      resetPolygonStyles() {{
        if (!this.geoJsonLayer) return;
        const targetCodes = new Set(this.questionPool.map(p => p.code));
        const isHighlightMode = (this.currentMode === 'name' || this.currentMode === 'type');
        const currentCode = (this.currentQuestion && isHighlightMode) ? this.currentQuestion.code : null;

        this.geoJsonLayer.eachLayer(layer => {{
          if (!layer.feature || !layer.feature.properties) return;
          if (layer._path) layer._path.classList.remove('polygon-pulse');

          const code = layer.feature.properties.code;
          const isTarget = targetCodes.has(code);

          // 回答後のハイライト判定
          if (this.isAnswered && this.answeredResult) {{
            const res = this.answeredResult;
            if (res.isCorrect) {{
              if (code === res.code) {{
                layer.setStyle({{ fillColor: '#34d399', fillOpacity: 0.95, weight: 3.5, color: '#059669' }});
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
            }} else {{
              // 不正解時: 正解場所は黄色点滅
              if (code === res.correctCode) {{
                layer.setStyle({{ fillColor: '#fbbf24', fillOpacity: 0.95, weight: 3.5, color: '#eab308' }});
                if (layer._path) layer._path.classList.add('polygon-pulse');
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
              // 誤ってタップした場所は赤色
              if (res.wrongCode && code === res.wrongCode) {{
                layer.setStyle({{ fillColor: '#f87171', fillOpacity: 0.95, weight: 3.5, color: '#dc2626' }});
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
            }}
          }}

          // 通常出題中（4択または記入）のハイライト
          const isCurrentHighlight = !this.isAnswered && currentCode && (code === currentCode);
          if (isCurrentHighlight) {{
            layer.setStyle({{
              fillColor: '#fbbf24',
              fillOpacity: 0.95,
              weight: 3.5,
              color: '#f59e0b'
            }});
            if (layer.bringToFront) layer.bringToFront();
          }} else {{
            layer.setStyle({{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.65,
              color: '#090d16',
              weight: 1.2
            }});
          }}
        }});
      }},

      highlightQuestionPolygon() {{
        if (!this.geoJsonLayer || !this.currentQuestion) return;
        this.resetPolygonStyles();

        const targetCode = this.currentQuestion.code;
        let targetBounds = null;

        this.geoJsonLayer.eachLayer(layer => {{
          if (!layer.feature || !layer.feature.properties) return;
          if (layer.feature.properties.code === targetCode) {{
            if (layer.getBounds && layer.getBounds().isValid()) {{
              targetBounds = targetBounds ? targetBounds.extend(layer.getBounds()) : layer.getBounds();
            }}
          }}
        }});

        if (targetBounds && (this.currentMode === 'name' || this.isAnswered)) {{
          this.map.flyToBounds(targetBounds, {{ maxZoom: 8, duration: 0.5 }});
        }}
      }},

      renderNameChoices() {{
        const grid = document.getElementById('prov-choice-buttons-grid');
        grid.innerHTML = '';
        const q = this.currentQuestion;

        const allProvs = Object.values(PROVINCES_MASTER).filter(p => p.code !== q.code);
        allProvs.sort(() => Math.random() - 0.5);
        const choices = [q, ...allProvs.slice(0, 3)].sort(() => Math.random() - 0.5);

        choices.forEach((c, idx) => {{
          const btn = document.createElement('button');
          btn.className = 'prov-choice-btn py-2 px-3 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition flex items-center gap-2 active:scale-95';
          btn.dataset.code = c.code;
          btn.innerHTML = `
            <span class="w-5 h-5 rounded bg-slate-900 text-slate-400 flex items-center justify-center text-[10px] font-mono">${{idx + 1}}</span>
            <span class="truncate">${{c.name}} (${{c.kana}})</span>
          `;
          btn.onclick = () => this.handleAnswer(c.code === q.code, btn);
          grid.appendChild(btn);
        }});
      }},

      skipQuestion() {{
        if (this.isAnswered) return;
        this.currentIndex++;
        this.nextQuestion();
      }},

      onPolygonClick(feature, layer) {{
        const code = feature.properties.code;
        const targetProv = Object.values(PROVINCES_MASTER).find(p => p.code === code);
        if (!targetProv) return;

        if (this.currentMode === 'locate') {{
          if (this.isAnswered) return;
          const isCorrect = (code === this.currentQuestion.code);
          this.handleAnswer(isCorrect, layer, code);
        }} else if (this.currentMode === 'explore') {{
          this.selectedProv = targetProv;
          document.getElementById('prov-explore-empty').classList.add('hidden');
          document.getElementById('prov-explore-detail').classList.remove('hidden');

          document.getElementById('prov-exp-doh-badge').textContent = targetProv.doh || '五畿七道';
          document.getElementById('prov-exp-kana-text').textContent = targetProv.kana;
          document.getElementById('prov-exp-name-text').textContent = targetProv.name;
          document.getElementById('prov-exp-modern-text').textContent = targetProv.pref || targetProv.modern || '';

          const rec = this.data.records[code] || {{ correct: 0, wrong: 0 }};
          const total = rec.correct + rec.wrong;
          const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
          document.getElementById('prov-exp-stats-tag').textContent = `正解 ${{rec.correct}} / 不正解 ${{rec.wrong}} (正答率: ${{pct}})`;
        }}
      }},

      handleAnswer(isCorrect, targetEl, clickedCode = null) {{
        if (this.isAnswered) return;
        this.isAnswered = true;

        const q = this.currentQuestion;
        if (!this.data.records[q.code]) this.data.records[q.code] = {{ correct: 0, wrong: 0 }};
        const rec = this.data.records[q.code];

        if (isCorrect) {{
          this.answeredResult = {{ isCorrect: true, code: q.code }};
          sound.correct();
          rec.correct++;
          rec.last = 'correct';
          rec.updated = Date.now();
          STORAGE.set(KEYS.PROV, this.data);

          if (this.currentMode === 'locate') {{
            const bar = document.getElementById('prov-locate-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `<div class="text-xs font-bold text-emerald-400">⭕ 正解！素晴らしい！</div>`;
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-emerald-600', '!border-emerald-400');
          }} else if (this.currentMode === 'type') {{
            const bar = document.getElementById('prov-type-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `<div class="text-xs font-bold text-emerald-400">⭕ 正解！素晴らしい！</div>`;
          }}

          this.resetPolygonStyles();

          setTimeout(() => {{
            this.currentIndex++;
            this.nextQuestion();
          }}, 900);
        }} else {{
          this.answeredResult = {{ isCorrect: false, correctCode: q.code, wrongCode: clickedCode }};
          sound.wrong();
          rec.wrong++;
          rec.last = 'wrong';
          rec.updated = Date.now();
          STORAGE.set(KEYS.PROV, this.data);

          if (this.currentMode === 'locate') {{
            this.resetPolygonStyles();
            const bar = document.getElementById('prov-locate-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-rose-400">❌ 惜しい！正解は黄色点滅の場所です</span>
                <button type="button" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white" onclick="ProvApp.currentIndex++; ProvApp.nextQuestion();">次へ (Enter ↵)</button>
              </div>
            `;
          }} else if (this.currentMode === 'name') {{
            this.resetPolygonStyles();
            if (targetEl) targetEl.classList.add('!bg-rose-700');
            const correctBtn = document.querySelector(`.prov-choice-btn[data-code="${{q.code}}"]`);
            if (correctBtn) correctBtn.classList.add('!border-emerald-400', '!border-2');
          }} else if (this.currentMode === 'type') {{
            this.resetPolygonStyles();
            const bar = document.getElementById('prov-type-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-rose-400">❌ 正解: ${{q.name}}</span>
                <button type="button" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white" onclick="ProvApp.currentIndex++; ProvApp.nextQuestion();">次へ (Enter ↵)</button>
              </div>
            `;
          }}
        }}
      }},

      startSingleQuestion(prov) {{
        this.questionPool = [prov];
        this.currentIndex = 0;
        this.renderMapLayers();
        this.nextQuestion();
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
        let cleared = 0;
        allProvs.forEach(p => {{
          const r = this.data.records[p.code];
          if (r && r.correct > 0) cleared++;
        }});
        document.getElementById('prov-spoke-cleared-count').textContent = cleared;
        document.getElementById('prov-spoke-total-count').textContent = allProvs.length;
        const pct = allProvs.length > 0 ? Math.round((cleared / allProvs.length) * 100) : 0;
        document.getElementById('prov-spoke-cleared-pct').textContent = `(${{pct}}%)`;
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
      answeredResult: null,

      init() {{
        this.data = STORAGE.get(KEYS.WORLD, {{ records: {{}} }});
        if (!this.data.records) this.data.records = {{}};

        document.getElementById('btn-world-back-hub').onclick = () => {{
          AppRouter.navigate('screen-world-hub');
          this.renderHub();
        }};
        document.getElementById('btn-world-reset-bounds').onclick = () => {{
          if (this.map && this.currentRegion) {{
            if (this.currentRegion.bounds) this.map.fitBounds(this.currentRegion.bounds, {{ padding: [20, 20] }});
            else if (this.currentRegion.center) this.map.setView(this.currentRegion.center, this.currentRegion.zoom);
          }}
        }};

        const btnCountry = document.getElementById('btn-world-target-country');
        const btnCapital = document.getElementById('btn-world-target-capital');
        btnCountry.onclick = () => {{
          this.targetType = 'country';
          btnCountry.className = 'px-2 py-0.5 rounded text-white font-bold bg-emerald-600 transition';
          btnCapital.className = 'px-2 py-0.5 rounded text-slate-300 hover:text-white transition';
          this.nextQuestion();
        }};
        btnCapital.onclick = () => {{
          this.targetType = 'capital';
          btnCapital.className = 'px-2 py-0.5 rounded text-white font-bold bg-emerald-600 transition';
          btnCountry.className = 'px-2 py-0.5 rounded text-slate-300 hover:text-white transition';
          this.nextQuestion();
        }};

        document.querySelectorAll('.world-mode-tab-btn').forEach(btn => {{
          btn.onclick = () => this.setMode(btn.dataset.mode);
        }});

        document.getElementById('btn-world-locate-skip').onclick = () => this.skipQuestion();
        document.getElementById('btn-world-type-skip').onclick = () => this.skipQuestion();

        document.getElementById('btn-world-quiz-this').onclick = () => {{
          if (this.selectedCountry) {{
            this.setMode('locate');
            this.startSingleQuestion(this.selectedCountry);
          }}
        }};

        document.getElementById('btn-world-start-weak-all').onclick = () => {{
          const allCountries = Object.values(WORLD_MASTER);
          const weak = allCountries.filter(c => this.data.records[c.code] && this.data.records[c.code].last === 'wrong');
          if (weak.length > 0) this.openRegion(WORLD_REGIONS[0], 'WEAK');
        }};

        const typeForm = document.getElementById('world-form-type');
        const typeInput = document.getElementById('world-input-type');
        typeForm.onsubmit = (e) => {{
          if (e) e.preventDefault();
          if (this.isAnswered) {{
            this.currentIndex++;
            this.nextQuestion();
            return false;
          }}
          const val = typeInput.value.trim().toLowerCase();
          const q = this.currentQuestion;
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
          this.handleAnswer(isCorrect, typeInput);
          return false;
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

        const weakBanner = document.getElementById('world-weak-banner');
        if (weakCount > 0) {{
          weakBanner.classList.remove('hidden');
          document.getElementById('world-weak-count-badge').textContent = `${{weakCount}}国`;
        }} else {{
          weakBanner.classList.add('hidden');
        }}

        let completedRegionCount = 0;
        WORLD_REGIONS.forEach(reg => {{
          const countries = (reg.filter === 'ALL') ? allCountries : allCountries.filter(c => c.region === reg.filter);
          let clr = 0;
          countries.forEach(c => {{
            const r = this.data.records[c.code];
            if (r && r.correct > 0) clr++;
          }});
          const isComp = (clr === countries.length && countries.length > 0);
          if (isComp && reg.filter !== 'ALL') completedRegionCount++;
          const pct = countries.length > 0 ? Math.round((clr / countries.length) * 100) : 0;

          const card = document.createElement('div');
          card.className = `p-3 rounded-xl border cursor-pointer transition active:scale-98 ${{
            isComp
              ? 'bg-emerald-950/30 border-emerald-500/40 hover:border-emerald-400'
              : 'bg-slate-800/80 border-slate-700/80 hover:border-slate-600'
          }} flex flex-col justify-between`;

          card.innerHTML = `
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white">${{reg.name}}</span>
              ${{isComp ? '<span class="text-[10px] text-emerald-400 font-bold">制覇!</span>' : ''}}
            </div>
            <div class="mt-2 space-y-1">
              <div class="flex justify-between text-[10px] text-slate-400">
                <span>${{clr}} / ${{countries.length}}</span>
                <span>${{pct}}%</span>
              </div>
              <div class="w-full bg-slate-700/60 h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-full" style="width: ${{pct}}%"></div>
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

        this.updateHeaderProgress();

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
        const container = document.getElementById('world-level-tabs-container');
        container.innerHTML = '';

        const allCountries = Object.values(WORLD_MASTER);
        const baseCountries = (this.currentRegion.filter === 'ALL') ? allCountries : allCountries.filter(c => c.region === this.currentRegion.filter);

        const counts = {{
          1: baseCountries.filter(c => c.level === 1).length,
          2: baseCountries.filter(c => c.level === 2).length,
          3: baseCountries.filter(c => c.level === 3).length,
          4: baseCountries.filter(c => c.level === 4).length,
          ALL: baseCountries.length,
          WEAK: baseCountries.filter(c => this.data.records[c.code] && this.data.records[c.code].last === 'wrong').length
        }};

        const tabs = [
          {{ id: 1, label: 'Lv.1 主要国', count: counts[1] }},
          {{ id: 2, label: 'Lv.2 一般国', count: counts[2] }},
          {{ id: 3, label: 'Lv.3 中堅国', count: counts[3] }},
          {{ id: 4, label: 'Lv.4 難関国', count: counts[4] }},
          {{ id: 'ALL', label: '全地域', count: counts.ALL }},
          {{ id: 'WEAK', label: '⚠️ 弱点復習', count: counts.WEAK }}
        ];

        tabs.forEach(t => {{
          if (t.count === 0 && t.id !== 'ALL' && t.id !== 'WEAK') return;
          const btn = document.createElement('button');
          btn.className = `level-tab-btn px-2 sm:px-2.5 py-0.5 sm:py-1 rounded text-[11px] sm:text-xs font-semibold whitespace-nowrap shrink-0 transition ${{
            this.currentLevel === t.id
              ? 'bg-emerald-500 text-white'
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
          }}`;
          btn.innerHTML = `<span>${{t.label}}</span> <span class="font-normal opacity-80">(${{t.count}})</span>`;
          btn.onclick = () => this.startLevel(t.id);
          container.appendChild(btn);
        }});
      }},

      startLevel(levelId) {{
        this.currentLevel = levelId;
        const allCountries = Object.values(WORLD_MASTER);
        const baseCountries = (this.currentRegion.filter === 'ALL') ? allCountries : allCountries.filter(c => c.region === this.currentRegion.filter);

        if (levelId === 'ALL') {{
          this.questionPool = [...baseCountries];
        }} else if (levelId === 'WEAK') {{
          this.questionPool = baseCountries.filter(c => this.data.records[c.code] && this.data.records[c.code].last === 'wrong');
          if (this.questionPool.length === 0) {{
            alert('この地域の弱点国はありません！');
            this.startLevel('ALL');
            return;
          }}
        }} else {{
          this.questionPool = baseCountries.filter(c => c.level === levelId);
        }}

        this.questionPool.sort(() => Math.random() - 0.5);
        this.currentIndex = 0;
        this.renderLevelTabs();
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
            const code = feature.properties.code;
            const isTarget = targetCodes.has(code);

            layer.on({{
              mouseover: (e) => {{
                if (this.isAnswered) return;
                // 【重要】対象外の国はホバーしても色を変えない
                if (!isTarget && this.currentMode !== 'explore') return;
                e.target.setStyle({{ fillColor: '#e2e8f0', fillOpacity: 1 }});
              }},
              mouseout: (e) => {{
                this.resetPolygonStyles();
              }},
              click: () => {{
                // 【重要】対象外の国はクリック選択不可
                if (!isTarget && this.currentMode !== 'explore') return;
                this.onPolygonClick(feature, layer);
              }}
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
        document.querySelectorAll('.world-mode-tab-btn').forEach(btn => {{
          if (btn.dataset.mode === mode) {{
            btn.className = 'world-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-semibold bg-slate-700 text-emerald-400 shadow';
          }} else {{
            btn.className = 'world-mode-tab-btn px-2 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-medium text-slate-300 hover:text-white';
          }}
        }});

        ['locate', 'name', 'type', 'explore'].forEach(m => {{
          const dock = document.getElementById(`world-dock-${{m}}`);
          if (dock) {{
            if (m === mode) dock.classList.remove('hidden');
            else dock.classList.add('hidden');
          }}
        }});

        this.nextQuestion();
      }},

      nextQuestion() {{
        this.isAnswered = false;
        this.answeredResult = null;
        document.getElementById('world-locate-feedback-bar').classList.add('hidden');
        document.getElementById('world-type-feedback-bar').classList.add('hidden');

        if (this.currentMode === 'explore') return;

        if (this.currentIndex >= this.questionPool.length) {{
          sound.fanfare();
          alert('この地域の全問題を完了しました！');
          this.startLevel(this.currentLevel);
          return;
        }}

        this.currentQuestion = this.questionPool[this.currentIndex];
        this.updateHeaderProgress();

        const q = this.currentQuestion;
        const rec = this.data.records[q.code] || {{ correct: 0, wrong: 0 }};
        const total = rec.correct + rec.wrong;
        const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
        const progStr = `問題 ${{this.currentIndex + 1}} / ${{this.questionPool.length}}`;

        if (this.currentMode === 'locate') {{
          document.getElementById('world-locate-level-tag').textContent = `Lv.${{q.level}} ${{q.region}}`;
          document.getElementById('world-locate-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('world-locate-progress-tag').textContent = progStr;
          document.getElementById('world-locate-flag').textContent = getFlagEmoji(q.code2);

          if (this.targetType === 'capital') {{
            document.getElementById('world-locate-prompt-label').textContent = '地図上でタップ（首都から国を探す）：';
            document.getElementById('world-locate-kana').textContent = `（${{q.furigana_cap}}）`;
            document.getElementById('world-locate-question-name').textContent = `${{q.capital}}（首都）`;
          }} else {{
            document.getElementById('world-locate-prompt-label').textContent = '地図上でタップ：';
            document.getElementById('world-locate-kana').textContent = `（${{q.furigana_name}}）`;
            document.getElementById('world-locate-question-name').textContent = q.name;
          }}
          this.resetPolygonStyles();
        }} else if (this.currentMode === 'name') {{
          document.getElementById('world-name-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('world-name-progress-tag').textContent = progStr;
          document.getElementById('world-name-prompt-label').textContent = (this.targetType === 'capital')
            ? '黄色の国の【首都名】はどれ？'
            : '黄色の国の【国名】はどれ？';
          this.highlightQuestionPolygon();
          this.renderNameChoices();
        }} else if (this.currentMode === 'type') {{
          document.getElementById('world-type-accuracy-tag').textContent = `正答率: ${{pct}}`;
          document.getElementById('world-type-progress-tag').textContent = progStr;
          document.getElementById('world-type-prompt-label').textContent = (this.targetType === 'capital')
            ? `黄色の国（${{q.name}}）の【首都名】を入力：`
            : '黄色の国の【国名】を入力：';
          const input = document.getElementById('world-input-type');
          input.value = '';
          input.placeholder = (this.targetType === 'capital') ? `例: ${{q.capital}}` : `例: ${{q.name}}`;
          input.focus();
          this.highlightQuestionPolygon();
        }}
      }},

      resetPolygonStyles() {{
        if (!this.geoJsonLayer) return;
        const targetCodes = new Set(this.questionPool.map(c => c.code));
        const isHighlightMode = (this.currentMode === 'name' || this.currentMode === 'type');
        const currentCode = (this.currentQuestion && isHighlightMode) ? this.currentQuestion.code : null;

        this.geoJsonLayer.eachLayer(layer => {{
          if (!layer.feature || !layer.feature.properties) return;
          if (layer._path) layer._path.classList.remove('polygon-pulse');

          const code = layer.feature.properties.code;
          const isTarget = targetCodes.has(code);

          // 回答後のハイライト判定
          if (this.isAnswered && this.answeredResult) {{
            const res = this.answeredResult;
            if (res.isCorrect) {{
              if (code === res.code) {{
                layer.setStyle({{ fillColor: '#34d399', fillOpacity: 0.95, weight: 3.5, color: '#059669' }});
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
            }} else {{
              // 不正解時: 正解場所は黄色点滅
              if (code === res.correctCode) {{
                layer.setStyle({{ fillColor: '#fbbf24', fillOpacity: 0.95, weight: 3.5, color: '#eab308' }});
                if (layer._path) layer._path.classList.add('polygon-pulse');
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
              // 誤ってタップした場所は赤色
              if (res.wrongCode && code === res.wrongCode) {{
                layer.setStyle({{ fillColor: '#f87171', fillOpacity: 0.95, weight: 3.5, color: '#dc2626' }});
                if (layer.bringToFront) layer.bringToFront();
                return;
              }}
            }}
          }}

          // 通常出題中（4択または記入）のハイライト
          const isCurrentHighlight = !this.isAnswered && currentCode && (code === currentCode);
          if (isCurrentHighlight) {{
            layer.setStyle({{
              fillColor: '#fbbf24',
              fillOpacity: 0.95,
              weight: 3.5,
              color: '#f59e0b'
            }});
            if (layer.bringToFront) layer.bringToFront();
          }} else {{
            layer.setStyle({{
              fillColor: isTarget ? '#f8fafc' : '#334155',
              fillOpacity: isTarget ? 0.95 : 0.60,
              color: '#090d16',
              weight: 0.8
            }});
          }}
        }});
      }},

      highlightQuestionPolygon() {{
        if (!this.geoJsonLayer || !this.currentQuestion) return;
        this.resetPolygonStyles();

        const targetCode = this.currentQuestion.code;
        let targetBounds = null;

        this.geoJsonLayer.eachLayer(layer => {{
          if (!layer.feature || !layer.feature.properties) return;
          if (layer.feature.properties.code === targetCode) {{
            if (layer.getBounds && layer.getBounds().isValid()) {{
              targetBounds = targetBounds ? targetBounds.extend(layer.getBounds()) : layer.getBounds();
            }}
          }}
        }});

        if (targetBounds && (this.currentMode === 'name' || this.isAnswered)) {{
          this.map.flyToBounds(targetBounds, {{ maxZoom: 5.5, duration: 0.5 }});
        }}
      }},

      renderNameChoices() {{
        const grid = document.getElementById('world-choice-buttons-grid');
        grid.innerHTML = '';
        const q = this.currentQuestion;

        const allCountries = Object.values(WORLD_MASTER).filter(c => c.code !== q.code);
        allCountries.sort(() => Math.random() - 0.5);
        const choices = [q, ...allCountries.slice(0, 3)].sort(() => Math.random() - 0.5);

        choices.forEach((c, idx) => {{
          const flag = getFlagEmoji(c.code2);
          const label = (this.targetType === 'capital')
            ? `${{c.capital}}`
            : `${{flag}} ${{c.name}}`;
          const sub = (this.targetType === 'capital')
            ? `${{flag}} ${{c.name}}`
            : `${{c.capital}}`;

          const btn = document.createElement('button');
          btn.className = 'world-choice-btn py-2 px-3 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm border border-slate-700 transition flex items-center justify-between gap-2 active:scale-95';
          btn.dataset.code = c.code;
          btn.innerHTML = `
            <div class="flex items-center gap-2 truncate">
              <span class="w-5 h-5 rounded bg-slate-900 text-slate-400 flex items-center justify-center text-[10px] font-mono">${{idx + 1}}</span>
              <span class="truncate">${{label}}</span>
            </div>
            <span class="text-[10px] text-slate-400 shrink-0 font-normal">${{sub}}</span>
          `;
          btn.onclick = () => this.handleAnswer(c.code === q.code, btn);
          grid.appendChild(btn);
        }});
      }},

      skipQuestion() {{
        if (this.isAnswered) return;
        this.currentIndex++;
        this.nextQuestion();
      }},

      onPolygonClick(feature, layer) {{
        const code = feature.properties.code;
        const targetCountry = WORLD_MASTER[code];
        if (!targetCountry) return;

        if (this.currentMode === 'locate') {{
          if (this.isAnswered) return;
          const isCorrect = (code === this.currentQuestion.code);
          this.handleAnswer(isCorrect, layer, code);
        }} else if (this.currentMode === 'explore') {{
          this.selectedCountry = targetCountry;
          document.getElementById('world-explore-empty').classList.add('hidden');
          document.getElementById('world-explore-detail').classList.remove('hidden');

          document.getElementById('world-exp-flag-text').textContent = getFlagEmoji(targetCountry.code2);
          document.getElementById('world-exp-region-badge').textContent = targetCountry.region;
          document.getElementById('world-exp-kana-text').textContent = targetCountry.furigana_name;
          document.getElementById('world-exp-name-text').textContent = targetCountry.name;
          document.getElementById('world-exp-capital-text').textContent = `${{targetCountry.capital}} (${{targetCountry.code}})`;

          const rec = this.data.records[code] || {{ correct: 0, wrong: 0 }};
          const total = rec.correct + rec.wrong;
          const pct = total > 0 ? Math.round((rec.correct / total) * 100) + '%' : '--%';
          document.getElementById('world-exp-stats-tag').textContent = `正解 ${{rec.correct}} / 不正解 ${{rec.wrong}} (正答率: ${{pct}})`;
        }}
      }},

      handleAnswer(isCorrect, targetEl, clickedCode = null) {{
        if (this.isAnswered) return;
        this.isAnswered = true;

        const q = this.currentQuestion;
        if (!this.data.records[q.code]) this.data.records[q.code] = {{ correct: 0, wrong: 0 }};
        const rec = this.data.records[q.code];

        if (isCorrect) {{
          this.answeredResult = {{ isCorrect: true, code: q.code }};
          sound.correct();
          rec.correct++;
          rec.last = 'correct';
          rec.updated = Date.now();
          STORAGE.set(KEYS.WORLD, this.data);

          if (this.currentMode === 'locate') {{
            const bar = document.getElementById('world-locate-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `<div class="text-xs font-bold text-emerald-400">⭕ 正解！素晴らしい！</div>`;
          }} else if (this.currentMode === 'name') {{
            if (targetEl) targetEl.classList.add('!bg-emerald-600', '!border-emerald-400');
          }} else if (this.currentMode === 'type') {{
            const bar = document.getElementById('world-type-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `<div class="text-xs font-bold text-emerald-400">⭕ 正解！素晴らしい！</div>`;
          }}

          this.resetPolygonStyles();

          setTimeout(() => {{
            this.currentIndex++;
            this.nextQuestion();
          }}, 900);
        }} else {{
          this.answeredResult = {{ isCorrect: false, correctCode: q.code, wrongCode: clickedCode }};
          sound.wrong();
          rec.wrong++;
          rec.last = 'wrong';
          rec.updated = Date.now();
          STORAGE.set(KEYS.WORLD, this.data);

          const answerText = (this.targetType === 'capital') ? `${{q.name}}の首都は「${{q.capital}}」` : `正解は「${{q.name}}」`;

          if (this.currentMode === 'locate') {{
            this.resetPolygonStyles();
            const bar = document.getElementById('world-locate-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-rose-400">❌ 惜しい！${{answerText}}（黄色点滅の場所）です</span>
                <button type="button" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white" onclick="WorldApp.currentIndex++; WorldApp.nextQuestion();">次へ (Enter ↵)</button>
              </div>
            `;
          }} else if (this.currentMode === 'name') {{
            this.resetPolygonStyles();
            if (targetEl) targetEl.classList.add('!bg-rose-700');
            const correctBtn = document.querySelector(`.world-choice-btn[data-code="${{q.code}}"]`);
            if (correctBtn) correctBtn.classList.add('!border-emerald-400', '!border-2');
          }} else if (this.currentMode === 'type') {{
            this.resetPolygonStyles();
            const bar = document.getElementById('world-type-feedback-bar');
            bar.classList.remove('hidden');
            bar.innerHTML = `
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-rose-400">❌ ${{answerText}}</span>
                <button type="button" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white" onclick="WorldApp.currentIndex++; WorldApp.nextQuestion();">次へ (Enter ↵)</button>
              </div>
            `;
          }}
        }}
      }},

      startSingleQuestion(country) {{
        this.questionPool = [country];
        this.currentIndex = 0;
        this.renderMapLayers();
        this.nextQuestion();
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
        let cleared = 0;
        countries.forEach(c => {{
          const r = this.data.records[c.code];
          if (r && r.correct > 0) cleared++;
        }});
        document.getElementById('world-spoke-cleared-count').textContent = cleared;
        document.getElementById('world-spoke-total-count').textContent = countries.length;
        const pct = countries.length > 0 ? Math.round((cleared / countries.length) * 100) : 0;
        document.getElementById('world-spoke-cleared-pct').textContent = `(${{pct}}%)`;
      }}
    }};

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

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Build complete! Output file size: {os.path.getsize('index.html') // 1024} KB")
