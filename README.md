# RaspRadiru
Raspberry piを使ってNHKラジオ英会話を楽しく学べるシステム

## Docker Usage

リポジトリに詰め込んだモジュールと設定がbuildできる．
オプションでバックグラウンドで毎日録音してくれる．

録音設定等は[crontab](https://github.com/Atsuto0519/RaspRadiru/blob/master/settings/crontab)
に書き込んでおけば自動にcronに反映される．

`image_name, container_name`は適宜変更．

```
docker build -t image_name .
docker run -itd --name container_name image_name
```

## ラジオ英会話問題自動作成
復習のために，ラジオ英会話の一週間の問題を自動作成してくれるツール．

以下の順に実行する．
```
python extract_sentence.py
python make_test.py
```

### [extract_sentence.py](https://github.com/Atsuto0519/RaspRadiru/blob/master/pylibs/extract_sentence.py)

ラジオ英会話の公式ページから例文を自動ダウンロードして```sentence.txt```を作成する．

テキスト形式に例文を加工できる．

### [make_test.py](https://github.com/Atsuto0519/RaspRadiru/blob/master/pylibs/make_test.py)

ラジオ英会話の例文から問題をPowerPoint形式で作成する．


### [Sample](https://www.slideshare.net/AtsutoInage/testpptx-96687066)


# らじる★らじる自動再生
NHKのネットラジオらじる★らじるの番組を自動再生するためのプラクティス

## omxplayerを使う
すごく手軽でオススメな方法．

### R1
```
omxplayer --timeout 60s -o local https://nhkradiobkr1-i.akamaihd.net/hls/live/512291/1-r1/1-r1-01.m3u8
```

### R2
```
omxplayer --timeout 60s -o local https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8
```

# らじる★らじる録音

## ffmpegを使う
変換ソフトを使って好きな音声へ変換できる．

すごくお手軽です．

`-t 900`の部分は，録音を開始してから終了するまでの秒単位時間を示しているので15分にしています．
（ラジオ英会話の放送時間）

リアルタイム録音なので，コマンドを叩いたら終わるまでおとなしく待ちましょう．

### R1
```
ffmpeg -i https://nhkradiobkr1-i.akamaihd.net/hls/live/512291/1-r1/1-r1-01.m3u8 -t 900 -movflags faststart -c copy -bsf:a aac_adtstoasc radio_english_r1.m4a
```

### R2
```
ffmpeg -i https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8 -t 900 -movflags faststart -c copy -bsf:a aac_adtstoasc radio_english_r2.m4a
```

# Slack上にファイルアップロード
[upload_slack.py](https://github.com/Atsuto0519/RaspRadiru/blob/master/pylibs/upload_slack.py)
とCronを使って自動投稿させれば非常に便利．

たとえば，上記のダウンロードファイルで毎日あげるなら，

```
crontab -e
```

でCronを開き，
```
5 7 * * 1-5 ffmpeg -i https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8 -t 900 -movflags faststart -c copy -bsf:a aac_adtstoasc radio_english_r2.m4a
5 7 * * 1-5 python slackupload.py radio_english_r2.m4a
```

とすれば毎週月〜金までアップロードされる

# 参考サイト
[Python を使って Slack に投稿](http://nuxx.noob.jp/python-%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6-slack-%E3%81%AB%E6%8A%95%E7%A8%BF/)
