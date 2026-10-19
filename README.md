# Peak Cruiser

登った山の登山道や、山頂から見えた山を、あとから 3D 空間で自由に振り返るための個人ツール。
3Dconnexion の SpaceMouse で 6 軸を連続操作して日本の地形を飛び回れます。

精密さより「山の形が分かること」を優先しています。

## できること

- **SpaceMouse による 6DOF フライト**（WebHID 経由）。視線と移動方向が独立しているので、地形を見下ろしながら水平に飛べます
  - 一度許可すれば、次回からはページを開くだけ・挿し直すだけで自動接続
  - 新しい 3Dconnexion 製品（SpaceMouse Compact / Wireless / Pro、ユニバーサルレシーバー）にも対応
- **ゲームパッド・キーボードでも操作可能**（SpaceMouse と同時に使えます）
- **日本三百名山 301 座＋OpenStreetMap の約 12,600 座**から、ラベルを付ける山の範囲・最大数・間隔を設定で選べます。PeakFinder 風の傾いたラベルが引き出し線で山頂を指します（重なるときは有名な山が優先）
- 地球の丸みで隠れる山、手前の尾根に遮られる山は自動で非表示（国土地理院の標高タイルで判定）
- 画質プリセット（軽量 / 標準 / 高画質）、リアルな空と大気、FXAA
- カメラが止まっている間は再描画しないので、放置中の PC の負荷はほぼゼロ
- 空に 16 方位、右下にミニマップ、「近くの山」一覧
- 地表テクスチャ 7 種（地形図・色別標高図・航空写真・陰影起伏図ほか）、昼夜の切り替え
- タイルは端末にキャッシュされ、一度飛んだ場所は次回すぐ表示されます

## 使い方

ブラウザで開くだけです。ビルドもインストールも不要。

SpaceMouse を使うには:

1. **Chrome または Edge** で開く（WebHID 対応ブラウザが必要）
2. 3Dconnexion の純正ドライバを一時的に終了する（デバイスを排他的に掴んでいるため）
3. 「SpaceMouse に接続」ボタンを押してデバイスを選択

SpaceMouse が無くても、キーボードやゲームパッドで飛べます。

| 操作 | キーボード | ゲームパッド | SpaceMouse |
|---|---|---|---|
| 前後・左右 | W / S / A / D | 左スティック | 押す・引く・横にずらす |
| 上昇・下降 | E・Space / Q・C | RT / LT | 持ち上げる / 押し込む |
| 向き・見上げ | ← → / ↑ ↓ | 右スティック | ひねる / 傾ける |
| 速く | Shift | — | — |
| 視線を水平に戻す | H | A | 左ボタン |
| 近くの山 一覧 | — | — | 右ボタン |

## 動作環境

- WebHID 対応ブラウザ（Chrome / Edge）
- HTTPS または localhost（WebHID と Service Worker の要件）

## データの出典

- 地形（標高）: [ArcGIS World Elevation 3D](https://www.arcgis.com/)
- 地図タイル: [OpenTopoMap](https://opentopomap.org/) (CC-BY-SA) / [国土地理院](https://maps.gsi.go.jp/development/ichiran.html) / [OpenStreetMap](https://www.openstreetmap.org/)
- 三百名山の座標・標高: [日本百選と座標値](https://100sen.cyber-ninja.jp/)
- その他の山の名前・座標・標高: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL)
- 尾根の判定に使う標高: [国土地理院 標高タイル](https://maps.gsi.go.jp/development/demtile.html)
- 描画: [CesiumJS](https://cesium.com/platform/cesiumjs/)

## 構成

| ファイル | 内容 |
|---|---|
| `index.html` | 本体。これ 1 枚で全機能 |
| `sw.js` | タイルキャッシュ用 Service Worker |
| `peaks-jp.json` | OSM から抽出した山のデータ（三百名山と重複するものは除外済み） |

個人用のツールなので、動作の保証やサポートはありません。
