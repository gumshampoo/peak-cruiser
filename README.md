# Peak Cruiser

登った山の登山道や、山頂から見えた山を、あとから 3D 空間で自由に振り返るための個人ツール。
3Dconnexion の SpaceMouse で 6 軸を連続操作して日本の地形を飛び回れます。

精密さより「山の形が分かること」を優先しています。

## できること

- **SpaceMouse による 6DOF フライト**（WebHID 経由）。視線と移動方向が独立しているので、地形を見下ろしながら水平に飛べます
  - `start.command` で起動すると、使っている間だけ純正ドライバ（3DxWare 10）を止めて SpaceMouse に直接つなぎます。反応が速く、手を離すとすぐ止まります
  - 普通に開いた場合は、ドライバを動かしたままドライバ経由（3DconnexionJS）で自動接続。ドライバが再起動しても自動でつなぎ直します
  - ドライバが無い環境では WebHID で直接接続。一度許可すれば、次回からはページを開くだけ・挿し直すだけで自動接続
  - 新しい 3Dconnexion 製品（SpaceMouse Compact / Wireless / Pro、ユニバーサルレシーバー）にも対応
- **ゲームパッド・キーボードでも操作可能**（SpaceMouse と同時に使えます）
- 速さは地表からの高さに比例（どの高さでも景色の流れる速さが同じ）。強く押すほど速さが大きく伸び（設定で調整可）、同じ方向に押し続けるとさらに加速
- **日本三百名山 301 座＋OpenStreetMap の約 12,600 座**から、ラベルを付ける山の範囲・最大数・間隔を設定で選べます。PeakFinder 風の傾いたラベルが引き出し線で山頂を指します（重なるときは「近くて高い山」を優先。「近い山」「有名な山」にも切り替え可）
- 地球の丸みで隠れる山、手前の尾根に遮られる山は自動で非表示（国土地理院の標高タイルで判定）
- 飛行中はフレームレート優先。地形の細かさを連続的に調整し、止まると少しずつ細かく戻ります。解像度は飛行中は目標FPSに合わせてゆっくり自動調整し（上限・下限は設定可）、止まって1秒たつと最大にしてから休止します
- 画質プリセット（軽量 / 標準 / 高画質）、リアルな空と大気、FXAA
- カメラが止まっている間は再描画しないので、放置中の PC の負荷はほぼゼロ
- 空に 16 方位、右下にミニマップ、「近くの山」一覧
- 地表テクスチャ 7 種（地形図・色別標高図・航空写真・陰影起伏図ほか）、昼夜の切り替え
- タイルは端末にキャッシュされ、一度飛んだ場所は次回すぐ表示されます

## 使い方

**`start.command` をダブルクリック**すると、ローカルサーバーが起動して Chrome で開きます。ビルドもインストールも不要です（macOS 標準の Python 3 を使います）。

止めるときは、開いたターミナルのウィンドウを閉じるか Ctrl+C を押します。

`start.command` を使わずに静的ホスティングや `python3 -m http.server` で開いても動きます。その場合、SpaceMouse はドライバ経由でつながります。

SpaceMouse を使うには:

- **初回だけ**：「SpaceMouse に接続」ボタンを押してデバイスを選びます（WebHID の許可）
- **3DxWare 10 が入っていて `start.command` で起動した場合（おすすめ）**：起動している間は純正ドライバの常駐アプリ（ヘルパー・3DxNLServer・ラジアルメニュー・仮想テンキー・3Dconnexion Home）を**まとめて**止め、SpaceMouse に直接つなぎます。直接の方が反応が速く、特に手を離したときすぐ止まります。ターミナルのウィンドウを閉じる（Ctrl+C）と、ログイン時と同じ方法でまとめて元に戻ります
  - 起動している間、ほかのアプリでは SpaceMouse が使えません
  - 終了後にほかのアプリで反応しない場合は、そのアプリを一度起動し直してください
  - 一部だけ止めると、ほかのアプリで SpaceMouse が使えなくなることが分かっています。手動で止める場合も、必ず全部まとめて止めてください
- **3DxWare 10 が入っていて、それ以外の方法で開いた場合**：ドライバ経由（3DconnexionJS）で自動的につながります（HTTPS か localhost で開くこと）
- **ドライバが無い場合**：WebHID で直接つながります

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
- SpaceMouse（ドライバ経由）: [3DconnexionJS](https://www.npmjs.com/package/@3dconnexion/3dconnexionjs)（3Dconnexion SDK ライセンス。CDN から読み込み、このリポジトリには含めていません）

## 構成

| ファイル | 内容 |
|---|---|
| `index.html` | 本体。これ 1 枚で全機能 |
| `sw.js` | タイルキャッシュ用 Service Worker |
| `server.py` | ローカルサーバー（127.0.0.1:8765）。起動中は純正ドライバをまとめて止め、終了時にまとめて戻す |
| `start.command` | ダブルクリック用の起動ファイル |
| `peaks-jp.json` | OSM から抽出した山のデータ（三百名山と重複するものは除外済み） |

個人用のツールなので、動作の保証やサポートはありません。
