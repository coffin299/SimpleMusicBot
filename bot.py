"""単体音楽Botの起動入口。設定読込と Music Cog のロードだけを担当する。"""

from __future__ import annotations

import asyncio
import copy
import logging
import sys
from pathlib import Path
from typing import Any, Dict

import discord
import yaml
from discord.ext import commands

# 起動時の基本ログ形式を定義する。
logging.basicConfig(
    # INFO 以上を標準出力へ出す。
    level=logging.INFO,
    # 時刻・ロガー名・レベル・本文を揃える。
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
# このモジュール用ロガーを取得する。
logger = logging.getLogger("arona")

# 既定設定ファイル名（リポジトリ同梱）。
DEFAULT_CONFIG_PATH = Path("config.default.yaml")
# ユーザー編集用の実設定ファイル名。
USER_CONFIG_PATH = Path("config.yaml")
# 起動時に読み込む Music Cog 拡張パス。
MUSIC_EXTENSION = "cogs.music.music_cog"


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """ネストした dict を再帰的にマージする。"""
    # 元を壊さないよう深いコピーから始める。
    merged = copy.deepcopy(base)
    # 上書き側のキーを順に適用する。
    for key, value in override.items():
        # 双方が dict なら再帰マージする。
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            # ネスト階層をマージする。
            merged[key] = deep_merge(merged[key], value)
        else:
            # それ以外は上書きする。
            merged[key] = copy.deepcopy(value)
    # マージ結果を返す。
    return merged


def load_config() -> Dict[str, Any]:
    """既定設定とユーザー設定をマージして返す。"""
    # 既定設定が無い場合は起動不能とする。
    if not DEFAULT_CONFIG_PATH.exists():
        # 明確なエラーを出す。
        raise FileNotFoundError(
            f"{DEFAULT_CONFIG_PATH} が見つかりません。"
            "リポジトリ同梱の既定設定が必要です。"
        )
    # 既定 YAML を読み込む。
    with DEFAULT_CONFIG_PATH.open("r", encoding="utf-8") as fp:
        # YAML を dict 化する（空なら空 dict）。
        default_config = yaml.safe_load(fp) or {}
    # ユーザー設定が無ければ既定のみ返す。
    if not USER_CONFIG_PATH.exists():
        # 初回向けにコピー手順を警告する。
        logger.warning(
            "%s が無いため %s のみを使用します。"
            " token を含む config.yaml を作成してください。",
            USER_CONFIG_PATH,
            DEFAULT_CONFIG_PATH,
        )
        # 既定を返す。
        return default_config
    # ユーザー YAML を読み込む。
    with USER_CONFIG_PATH.open("r", encoding="utf-8") as fp:
        # YAML を dict 化する。
        user_config = yaml.safe_load(fp) or {}
    # 既定の上にユーザー設定を重ねる。
    return deep_merge(default_config, user_config)


class MusicBot(commands.Bot):
    """Music Cog を載せる薄い Bot。"""

    def __init__(self, config: Dict[str, Any]):
        # Cog / コマンドから参照できるよう設定を保持する。
        self.config = config
        # 単体Bot識別子（再起動API互換用）。
        self.bot_id = str(config.get("bot_id", "arona"))
        # プレフィックスコマンド用の接頭辞（hybrid 互換）。
        prefix = config.get("prefix", "!")
        # Voice / スラッシュに必要な Intents を用意する。
        intents = discord.Intents.default()
        # ハイブリッドコマンド用にメッセージ本文を有効化する。
        intents.message_content = True
        # VC 入退室検知用に voice_states を有効化する。
        intents.voice_states = True
        # ギルド情報を受け取る。
        intents.guilds = True
        # メンバー取得が必要な場面向けに members を有効化する。
        intents.members = True
        # Bot 本体を初期化する。
        super().__init__(
            # プレフィックスコマンドの接頭辞。
            command_prefix=prefix,
            # Gateway Intents。
            intents=intents,
            # ヘルプは Cog / Docs 側に寄せる。
            help_command=None,
        )
        # スラッシュ同期を1回に抑えるフラグ。
        self._synced = False

    async def setup_hook(self) -> None:
        """起動直後に Music Cog をロードする。"""
        # Music Cog 拡張を読み込む。
        await self.load_extension(MUSIC_EXTENSION)
        # ロード完了をログする。
        logger.info("Loaded extension: %s", MUSIC_EXTENSION)

    async def on_ready(self) -> None:
        """接続完了後にスラッシュコマンドを同期する。"""
        # ユーザー表示名を安全に取る。
        user_name = self.user.name if self.user else "Unknown"
        # 接続成功をログする。
        logger.info("Logged in as %s (id=%s)", user_name, getattr(self.user, "id", "?"))
        # 未同期なら tree を同期する。
        if not self._synced:
            try:
                # グローバル同期する。
                synced = await self.tree.sync()
                # 同期件数をログする。
                logger.info("Synced %s application command(s)", len(synced))
                # 同期済みにする。
                self._synced = True
            except Exception as exc:
                # 同期失敗でも Bot は生かす。
                logger.error("Failed to sync application commands: %s", exc, exc_info=True)

    async def close(self) -> None:
        """終了時に Music Cog へ再起動通知を試みてから切断する。"""
        # Music Cog があれば取得する。
        music_cog = self.get_cog("music_cog")
        # 通知メソッドがあれば呼ぶ。
        if music_cog is not None and hasattr(music_cog, "notify_admin_restart"):
            try:
                # Now Playing を再起動表示へ切り替える。
                await music_cog.notify_admin_restart()
            except Exception as exc:
                # 終了処理自体は続行する。
                logger.warning("notify_admin_restart failed: %s", exc)
        # discord.py の正規クローズを実行する。
        await super().close()


async def amain() -> None:
    """非同期エントリポイント。"""
    # 設定を読み込む。
    config = load_config()
    # token を取得する。
    token = str(config.get("token") or "").strip()
    # プレースホルダや空なら起動しない。
    if not token or token in {"YOUR_BOT_TOKEN_HERE", "changeme"}:
        # 設定不足を明示する。
        raise RuntimeError(
            "config.yaml の token を Discord Bot Token に設定してください。"
        )
    # Bot インスタンスを作る。
    bot = MusicBot(config)
    # トークンで接続する。
    async with bot:
        # メインループを開始する。
        await bot.start(token)


def main() -> None:
    """同期エントリポイント。"""
    try:
        # 非同期 main を実行する。
        asyncio.run(amain())
    except KeyboardInterrupt:
        # Ctrl+C は正常終了扱いとする。
        logger.info("Interrupted by user")
    except Exception as exc:
        # 起動失敗をログして非ゼロ終了する。
        logger.error("Bot failed to start: %s", exc, exc_info=True)
        # 異常終了コードを返す。
        sys.exit(1)


if __name__ == "__main__":
    # スクリプト直接実行時のみ起動する。
    main()
