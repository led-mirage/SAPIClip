# SAPIClip
#
# アプリケーション設定クラス
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
import os
import threading

class Settings:
    FILE_VER = 1

    def __init__(self, setting_file_path):
        self._setting_file_path = setting_file_path
        self._lock = threading.Lock()
        self._init_member()

    def _init_member(self):
        self._voice = "Auto"
        self._speed = 1.2
        self._replacements = []
        self._preferred_voices = {
            'en': ['Microsoft Zira Desktop'],
            'ja': ['Microsoft Haruka'],
        }

    # 音声
    def get_voice(self):
        with self._lock:
            return self._voice

    def set_voice(self, voice):
        with self._lock:
            self._voice = voice

    # 読み上げスピード
    def get_speed(self):
        with self._lock:
            return self._speed

    def set_speed(self, speed):
        with self._lock:
            self._speed = speed

    # 置換設定
    def get_replacements(self):
        with self._lock:
            return self._replacements
        
    def set_replacements(self, replacements):
        with self._lock:
            self._replacements = replacements

    # Auto時に優先する声の設定
    def get_preferred_voices(self):
        with self._lock:
            return self._preferred_voices

    # 設定ファイルを保存する
    def save(self):
        with self._lock:
            self._save_nolock()

    def _save_nolock(self):
        with open(self._setting_file_path, "w", encoding="utf-8") as file:
            setting = {}
            setting["file_ver"] = Settings.FILE_VER
            setting["voice"] = self._voice
            setting["speed"] = self._speed
            setting["replacements"] = self._replacements
            setting["preferred_voices"] = self._preferred_voices
            json.dump(setting, file, ensure_ascii=False, indent=4)

    # 設定ファイルを読み込む
    def load(self):
        if not os.path.exists(self._setting_file_path):
            self._init_member()
            self._save_nolock()
            return

        with self._lock:
            with open(self._setting_file_path, "r", encoding="utf-8") as file:
                setting = json.load(file)
                file_ver = setting.get("file_ver", 1)
                self._voice = setting.get("voice", self._voice)
                self._speed = setting.get("speed", self._speed)
                self._replacements = setting.get("replacements", self._replacements)
                self._preferred_voices = setting.get("preferred_voices", self._preferred_voices)

        if file_ver < Settings.FILE_VER:
            self._save_nolock()
