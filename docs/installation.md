# Music Bot Arona - Discord音楽ボット

ProjectMOMOKA-1 の Music Cog を正として移植した、単体動作の Discord 音楽ボットです。

## 主な機能

- YouTube / ニコニコ動画などの再生（yt-dlp + FFmpeg）
- キュー管理・ループ・シーク・音量
- Components V2 の Now Playing 操作パネル
- 無人 VC の自動退出

## クイックスタート

### 必要環境

- Python 3.10+ 推奨
- FFmpeg
- Discord Bot Token

### インストール

```bash
git clone https://github.com/coffin399/music-bot-arona.git
cd music-bot-arona
pip install -r requirements.txt
copy config.default.yaml config.yaml
```

`config.yaml` の `token` を設定してから起動します。

```bash
python bot.py
```

Windows では `start.bat` でも起動できます（`.venv` が無ければ自動作成し、依存を入れてから `bot.py` を実行します。バッチ内メッセージは英語です）。

## ドキュメント

- [設定](configuration.md)
- [使い方](usage.md)

## コマンド一覧

### 再生コントロール

- `/play <曲名またはURL>`
- `/pause` / `/resume` / `/stop` / `/skip`
- `/seek <時間>`
- `/volume <0-200>`
- `/loop <off/one/all>`

### キュー

- `/queue` / `/nowplaying` / `/shuffle` / `/clear` / `/remove <番号>`

### ボイス

- `/join` / `/leave`

## 設定の例（Momoka 準拠）

```yaml
music:
  default_volume: 20
  max_queue_size: 10000
  max_guilds: 50
  auto_leave_timeout: 3
  max_playlist_items: 10000
  inactive_timeout_minutes: 3
  ffmpeg_path: ffmpeg
  youtube_cookie_file: youtube_cookies.txt
```

## 構成

- `bot.py` … 起動と Cog ロードのみ
- `cogs/music/` … Momoka 由来の Music Cog

## 制約

- TTS / LLM / GUI / 寄付連携は含みません
- 再起動後の VC 再生自動復元は含みません
- Google Drive 連携は含みません
- Spotify 等の DRM 保護 URL は再生できません
