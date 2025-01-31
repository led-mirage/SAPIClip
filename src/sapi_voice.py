# SAPIClip
#
# SAPI音声クラス
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import win32com.client

class SAPIVoice:
    """Windows SAPI5音声合成エンジンを扱うクラス

    Attributes:
        name (str): 音声の名前
        language (str): 音声の言語
        speed (int): 読み上げ速度 (-10から10)
        volume (int): 音量 (0から100)
    """

    def __init__(self, voice: object):
        """SAPIVoiceオブジェクトを初期化する

        Args:
            voice: SAPI5音声オブジェクト
        """
        self.engine = win32com.client.Dispatch("SAPI.SpVoice")
        self.engine.Voice = voice
        self._name = voice.GetAttribute("Name")
        self._language = voice.GetAttribute("Language").lower().lstrip("0")
        self._speed = 0
        self._volume = 100

    @property
    def name(self) -> str:
        """音声の名前を取得"""
        return self._name

    @property
    def language(self) -> str:
        """音声の言語を取得"""
        return self._language

    @property
    def speed(self) -> int:
        """読み上げ速度を取得"""
        return self._speed

    @speed.setter
    def speed(self, value: int) -> None:
        """読み上げ速度を設定

        Args:
            value: 速度 (-10から10)

        Raises:
            ValueError: 値が範囲外の場合
        """        
        if -10 <= value <= 10:
            self._speed = value
            self.engine.Rate = value
        else:
            raise ValueError("Speed must be between -10 and 10")

    @property
    def volume(self) -> int:
        """音量を取得"""
        return self._volume

    @volume.setter
    def volume(self, value: int) -> None:
        """音量を設定

        Args:
            value: 音量 (0から100)

        Raises:
            ValueError: 値が範囲外の場合
        """
        if 0 <= value <= 100:
            self._volume = value
            self.engine.Volume = value
        else:
            raise ValueError("Volume must be between 0 and 100")

    def speak(self, text: str) -> None:
        """指定されたテキストを読み上げる

        Args:
            text: 読み上げるテキスト
        """
        self.engine.Speak(text)
