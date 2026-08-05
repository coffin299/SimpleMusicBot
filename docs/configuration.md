# 設定ファイルの説明

設定の正本は ProjectMOMOKA-1 の `music_config.default.yaml` です。  
本リポジトリではそれを `config.default.yaml` に統合し、単体Bot用に `token` / `prefix` / `bot_id` を追加しています。

## 設定ファイルの場所

1. `config.default.yaml` を `config.yaml` にコピー
2. `token` を Discord Bot Token に変更
3. 必要なら `music` 節だけ上書き

```bash
copy config.default.yaml config.yaml
```

起動時は **既定設定 ← ユーザー設定** の順で深いマージが行われます。

## 基本設定

```yaml
token: "YOUR_BOT_TOKEN_HERE"
prefix: "!"
bot_id: "arona"
```

| キー | 必須 | 説明 |
|------|------|------|
| `token` | はい | Discord Bot Token |
| `prefix` | いいえ | hybrid コマンド用プレフィックス（既定 `!`） |
| `bot_id` | いいえ | 識別子（既定 `arona`） |

## 音楽設定（Momoka 準拠）

```yaml
music:
  default_volume: 20
  max_queue_size: 10000
  max_guilds: 50
  auto_leave_timeout: 3
  max_playlist_items: 10000
  inactive_timeout_minutes: 3
  ffmpeg_path: ffmpeg
  ffmpeg_before_options: -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5
  ffmpeg_options: -vn
  youtube_cookie_file: youtube_cookies.txt
  niconico:
    email: ''
    password: ''
```

| キー | 既定 | 説明 |
|------|------|------|
| `default_volume` | 20 | 初期音量（%） |
| `max_queue_size` | 10000 | キュー上限 |
| `max_guilds` | 50 | 同時保持するギルド状態の上限 |
| `auto_leave_timeout` | 3 | 人間がいない VC から退出するまでの秒数 |
| `max_playlist_items` | 10000 | プレイリスト展開上限 |
| `inactive_timeout_minutes` | 3 | 非アクティブ状態の掃除間隔（分） |
| `ffmpeg_path` | `ffmpeg` | FFmpeg 実行ファイル |
| `youtube_cookie_file` | `youtube_cookies.txt` | YouTube cookie パス |

`niconico.email` / `password` は設定枠として残していますが、現行の抽出経路では cookie ファイル中心です。

## メッセージ設定

`music.messages` 配下のテンプレートでユーザー向け文言を変更できます。  
プレースホルダ例: `{title}` `{duration}` `{requester_display_name}` `{volume}` `{error}`

詳細な既定文言は `config.default.yaml` を参照してください。

## Cookie / キャッシュ

- `./youtube_cookies.txt` または `./youtube_cookie.txt`
- `./nico_cookies.txt`（無ければ起動時に空作成される場合あり）
- `./cache/`（プロジェクトキャッシュ。Cog ロード時に掃除）

## 無効化している Momoka 機能

- 寄付リンク UI
- 再起動時 VC セッションの DB 永続化 / 復元
- TTS / LLM / GUI 連携設定

## セキュリティ

- `config.yaml` は Git 管理対象外にしてください（トークン漏洩防止）
- cookie ファイルもリポジトリにコミットしないでください
