# EDM Genre Analyzer

## はじめに
Spotify上のメタデータとBeatport上のジャンルを組にしたものを入力として、ロジスティック回帰モデルでジャンル分類を行うアプリケーションです。

Spotifyの曲へのリンクからジャンル推定を行います。

## セットアップ
曲情報の取得にSpotifyのClient IDとClient Secretが必要になります。ぐぐってください。

以下の内容で``credentials.py``というファイルを、edmga_trainerディレクトリに配置してください。
```.py
credentials = {
    "client_id": '<YOUR CLIENT ID>',
    "client_secret": '<YOUR CLIENT SECRET>'
}
```

## 使い方
``python main.py -t <曲へのリンク>``でジャンル推定を行います。

### 例
```
$ python3 main.py -t https://open.spotify.com/track/73eQLXuOk2cS1ZVoDUM7uW
楽曲を解析します
1: trap-wave 19.56 %
2: house 15.08 %
3: nu-disco-disco 12.29 %
```
