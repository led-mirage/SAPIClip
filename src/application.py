# SAPIClip
#
# アプリケーションクラス
#
# Copyright (c) 2025-2026 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os, argparse

from app_logging import get_logger, setup_logging
from settings import Settings

APP_NAME = "SAPIClip"
APP_VERSION = "0.2.0"
COPYRIGHT = "Copyright 2025-2026 led-mirage"

SETTING_FILE = "settings.json"

logger = get_logger("application")

class Application:
    # コンストラクタ
    def __init__(self):
        self.settings: Settings = None
        pass

    # 開始
    def start(self):
        self.set_dpi_awareness()

        parser = argparse.ArgumentParser(description=f"{APP_NAME} {APP_VERSION}")
        parser.add_argument("--setting", type=str, default=SETTING_FILE, help="設定ファイル名")
        args = parser.parse_args()

        self.print_apptitle()

        self.settings = Settings(args.setting)
        self.settings.load()

        from main_window import MainWindow
        main_window = MainWindow(self)
        main_window.show()
        main_window.terminate()

    # 高DPIディスプレイ対応（文字がぼやけないようにする）
    def set_dpi_awareness(self):
        if os.name == "nt":
            try:
                from ctypes import windll
                # Windows 8.1以降のDPI意識設定
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                # 古いOSや環境で失敗してもアプリ自体は起動するように
                pass

    # タイトルを表示する
    def print_apptitle(self):
        print(f"----------------------------------------------------------------------")
        print(f" {APP_NAME} {APP_VERSION}")
        print(f"")
        print(f" {COPYRIGHT}")
        print(f"----------------------------------------------------------------------")
        print(f"")

if __name__ == "__main__":
    log_file_path = setup_logging()

    if log_file_path is not None:
        logger.info("SAPIClip %s started", APP_VERSION)

    try:
        app = Application()
        app.start()
    except Exception as err:
        logger.exception("Application failed")

        message = (
            "An unexpected error occurred while the application was running.\n\n"
            f"{type(err).__name__}: {err}"
        )
        try:
            from ctypes import windll
            windll.user32.MessageBoxW(None, message, APP_NAME, 0x10)
        except Exception:
            pass

        raise SystemExit(1)
    else:
        logger.info("SAPIClip %s stopped normally", APP_VERSION)
