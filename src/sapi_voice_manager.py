# SAPIClip
#
# SAPI音声を管理するクラス
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import win32com.client

from sapi_voice import SAPIVoice

class SAPIVoiceManager:
    """SAPI音声を管理するクラス
    
    Attributes:
        voices (List[SAPIVoice]): 利用可能な音声のリスト
    """

    # 一般的な言語コードに対応する複数のLCID
    LANG_TO_LCIDS = {
        # アフリカーンス語
        "af": ["436"],
        # アラビア語
        "ar": ["401", "801", "c01", "1001", "1401", "1801", "1c01", "2001", "2401", "2801", "2c01", "3001", "3401", "3801", "3c01", "4001"],
        # ブルガリア語
        "bg": ["402"],
        # カタロニア語
        "ca": ["403"],
        # チェコ語
        "cs": ["405"],
        # デンマーク語
        "da": ["406"],
        # ドイツ語
        "de": ["407", "807", "c07", "1007", "1407"],
        # ギリシャ語
        "el": ["408"],
        # 英語
        "en": ["409", "809", "c09", "1009", "1409", "1809", "1c09", "2009", "2409", "2809", "2c09", "3009", "3409"],
        # スペイン語
        "es": ["40a", "80a", "c0a", "100a", "140a", "180a", "1c0a", "200a", "240a", "280a", "2c0a", "300a", "340a", "380a", "3c0a", "400a", "440a", "480a", "4c0a", "500a"],
        # エストニア語
        "et": ["425"],
        # フィンランド語
        "fi": ["40b"],
        # フランス語
        "fr": ["40c", "80c", "c0c", "100c", "140c", "180c"],
        # グジャラート語
        "gu": ["447"],
        # ヘブライ語
        "he": ["40d"],
        # ヒンディー語
        "hi": ["439"],
        # クロアチア語
        "hr": ["41a"],
        # ハンガリー語
        "hu": ["40e"],
        # インドネシア語
        "id": ["421"],
        # イタリア語
        "it": ["410", "810"],
        # 日本語
        "ja": ["411"],
        # カンナダ語
        "kn": ["44b"],
        # 韓国語
        "ko": ["412"],
        # リトアニア語
        "lt": ["427"],
        # ラトビア語
        "lv": ["426"],
        # マケドニア語
        "mk": ["42f"],
        # マラーティー語
        "mr": ["44e"],
        # オランダ語
        "nl": ["413", "813"],
        # ノルウェー語
        "no": ["414", "814"],
        # ポーランド語
        "pl": ["415"],
        # ポルトガル語
        "pt": ["416", "816"],
        # ルーマニア語
        "ro": ["418"],
        # ロシア語
        "ru": ["419"],
        # スロバキア語
        "sk": ["41b"],
        # スロベニア語
        "sl": ["424"],
        # アルバニア語
        "sq": ["41c"],
        # スウェーデン語
        "sv": ["41d", "81d"],
        # スワヒリ語
        "sw": ["441"],
        # タミル語
        "ta": ["449"],
        # テルグ語
        "te": ["44a"],
        # タイ語
        "th": ["41e"],
        # トルコ語
        "tr": ["41f"],
        # ウクライナ語
        "uk": ["422"],
        # ウルドゥ語
        "ur": ["420"],
        # ベトナム語
        "vi": ["42a"],
        # 中国語（簡体字）
        "zh-cn": ["804"],
        # 中国語（繁体字）
        "zh-tw": ["404"]
    }

    def __init__(self):
        """利用可能なすべての音声を初期化"""
        self.voices: list[SAPIVoice] = []
        self.preferred_voices: dict[str, list[str]] = {
            'en': ['Microsoft Zira'],
            'ja': ['Microsoft Sayaka'],
        }
        self._init_voices()

    def _init_voices(self) -> None:
        """レジストリから利用可能な音声を列挙して初期化"""
        registry_paths = [
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices",
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices"
        ]

        for path in registry_paths:
            cat = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
            cat.SetId(path, False)
            for voice in cat.EnumerateTokens():
                self.voices.append(SAPIVoice(voice))

    def get_voice_names(self) -> list[str]:
        """利用可能な音声の名前のリストを返す

        Returns:
            List[str]: 音声の名前のリスト
        """
        return [v.name for v in self.voices]
    
    def get_voice(self, name: str) -> SAPIVoice | None:
        """指定された名前の音声を返す

        Args:
            name (str): 音声の名前

        Returns:
            Optional[SAPIVoice]: 該当する音声。なければNone
        """
        for voice in self.voices:
            if voice.name == name:
                return voice
        return None

    def get_voice_for_language(self, language: str) -> SAPIVoice | None:
        """指定された言語に対応する音声を返す

        Args:
            language (str): 言語コード

        Returns:
            Optional[SAPIVoice]: 該当する音声。なければNone
        """
        def find_voice(lang: str) -> SAPIVoice | None:
            if lang not in self.LANG_TO_LCIDS:
                return None

            lcids = self.LANG_TO_LCIDS[lang]
            available_voices = [
                v for v in self.voices 
                if v.language in lcids
            ]

            if not available_voices:
                return None

            # 優先順位リストがある場合
            if lang in self.preferred_voices:
                for preferred_name in self.preferred_voices[lang]:
                    for voice in available_voices:
                        if voice.name == preferred_name:
                            return voice

            return available_voices[0]

        voice = find_voice(language)
        if voice:
            return voice
        
        return None
