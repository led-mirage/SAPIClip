# SAPIClip
#
# アプリケーションクラス
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import argparse

from settings import Settings

APP_NAME = "SAPIClip"
APP_VERSION = "0.1.1"
COPYRIGHT = "Copyright 2025 led-mirage"

SETTING_FILE = "settings.json"

class Application:
    # コンストラクタ
    def __init__(self):
        self.settings: Settings = None
        pass

    # 開始
    def start(self):
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
    
    # タイトルを表示する
    def print_apptitle(self):
        print(f"----------------------------------------------------------------------")
        print(f" {APP_NAME} {APP_VERSION}")
        print(f"")
        print(f" {COPYRIGHT}")
        print(f"----------------------------------------------------------------------")
        print(f"")

if __name__ == "__main__":
    from application import Application
    app = Application()
    app.start()
