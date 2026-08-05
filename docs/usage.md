# 使用方法ガイド

Music Bot Arona（Momoka Music Cog 移植版）の使い方です。

## 準備

1. Bot をサーバーへ招待（`bot` + `applications.commands`）
2. 再生したいボイスチャンネルへ自分が参加
3. テキストチャンネルでスラッシュコマンドを実行

## 基本の再生

```
/play 曲名
/play https://www.youtube.com/watch?v=...
```

- 再生中に追加するとキューへ入ります
- プレイリスト URL は `max_playlist_items` まで展開されます
- DRM 保護サイト（例: Spotify）は再生できません

## 操作パネル

`/play` 成功後の Now Playing パネルから次を操作できます。

- Pause / Resume
- Skip
- Stop（確認ダイアログあり）
- Loop（1曲） / QLoop（キュー全体）
- キューページング（曲が多いとき）

## コマンド

### 再生

| コマンド | 例 |
|---------|----|
| `/play` | `/play never gonna give you up` |
| `/seek` | `/seek 1:30` |
| `/pause` | `/pause` |
| `/resume` | `/resume` |
| `/skip` | `/skip` |
| `/stop` | `/stop` |
| `/volume` | `/volume 40` |
| `/loop` | `/loop one` |

### キュー

| コマンド | 説明 |
|---------|------|
| `/queue` | キュー一覧 |
| `/nowplaying` | 再生中情報 |
| `/shuffle` | シャッフル |
| `/clear` | クリア |
| `/remove` | 番号指定で削除 |

### VC

| コマンド | 説明 |
|---------|------|
| `/join` | 自分の VC へ接続 |
| `/leave` | 切断 |

## 自動退出

人間がいなくなった VC からは `auto_leave_timeout`（既定 3 秒）後に退出します。

## トラブルシュート

| 症状 | 確認点 |
|------|--------|
| スラッシュが出ない | Intent / 招待スコープ / `tree.sync` 成否 |
| 音が出ない | FFmpeg PATH、Bot の Speak 権限、自分も同じ VC |
| YouTube だけ失敗 | cookie、Deno/Node、年齢制限・地域制限 |
| ニコニコ失敗 | `nico_cookies.txt`、ログイン状態 |

## 含まない機能

- TTS 読み上げとの同時ミキシング操作
- LLM からの音楽コマンド実行
- 再起動後の自動再生復元
