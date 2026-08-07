# SimpleMusicBot

Discord 上で音楽を再生する単体動作型 Bot です。  
再生エンジン・コマンド・UI は [ProjectMOMOKA](https://github.com/coffin299/ProjectMOMOKA) の Music Cog を移植しています。

![Music Playback](https://momoka-project.com/assets/images/playmusic.png)

## 必要要件

- Python 3.10 以上推奨
- FFmpeg（PATH または `music.ffmpeg_path`）
- Discord Bot Token
- （推奨）YouTube 再生安定化用の cookie ファイル / Deno または Node（yt-dlp EJS）

## ファイル構成

```
music-bot-arona/
├── bot.py                      # 起動・設定読込・Cog ロードのみ
├── cogs/music/                 # Momoka 由来 Music Cog
│   ├── music_cog.py
│   ├── guild_state.py
│   ├── music_views.py
│   ├── music_helpers.py
│   ├── error/errors.py
│   └── plugins/
│       ├── ytdlp_wrapper.py
│       ├── audio_mixer.py
│       └── process_log_bridge.py
├── config.default.yaml         # 既定設定（Momoka music_config 準拠）
├── config.yaml                 # 実設定（自分で作成・Git 管理外）
├── requirements.txt
├── start.bat                   # Creates .venv if missing, installs deps, starts bot
├── tests/                      # 単体テスト
└── docs/                       # Markdown ドキュメント
```

## インストール

```bash
pip install -r requirements.txt
copy config.default.yaml config.yaml
```

`config.yaml` の `token` を Discord Bot Token に置き換えてください。

### Discord Developer Portal

Privileged Gateway Intents: 不要

OAuth2 Scopes: `bot`, `applications.commands`  
主要権限: Send Messages / Embed Links / Connect / Speak / Use Voice Activity など

## 起動

```bash
python bot.py
```

または `start.bat`（`.venv` が無ければ自動作成し、依存を入れて起動）

## コマンド一覧

| コマンド | 説明 |
|---------|------|
| `/play <query>` | 曲名検索または URL を再生 / キュー追加 |
| `/seek <time>` | 指定位置へシーク（`1:30` / `90`） |
| `/pause` | 一時停止 |
| `/resume` | 再開 |
| `/skip` | スキップ |
| `/stop` | 停止＆キュークリア |
| `/leave` | VC 切断 |
| `/queue` | キュー表示 |
| `/nowplaying` | 再生中表示 |
| `/shuffle` | キューシャッフル |
| `/clear` | キュークリア |
| `/remove <n>` | キューから削除 |
| `/volume <0-200>` | 音量 |
| `/loop <off/one/all>` | ループ |
| `/join` | VC 接続 |

再生中は Components V2 の操作パネル（Pause / Skip / Stop / Loop / QLoop）も利用できます。

## 設定の要点（Momoka 準拠）

| キー | 既定 | 意味 |
|------|------|------|
| `music.default_volume` | 20 | 初期音量 (%) |
| `music.max_queue_size` | 10000 | キュー上限 |
| `music.max_guilds` | 50 | 同時保持ギルド状態上限 |
| `music.auto_leave_timeout` | 3 | 無人 VC 自動退出（秒） |
| `music.max_playlist_items` | 10000 | プレイリスト展開上限 |
| `music.inactive_timeout_minutes` | 3 | 非アクティブ状態掃除（分） |
| `music.youtube_cookie_file` | `youtube_cookies.txt` | YouTube cookie |

詳細は [docs/configuration.md](docs/configuration.md) を参照してください。

## ライセンス

MIT
