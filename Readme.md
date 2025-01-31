# <img src="image/application.ico" width="48"> SAPIClip

Copyright (c) 2025 led-mirage

[English](Readme_en.md)

## 概要

`SAPIClip（サピクリップ）`は、Windows用のユーティリティプログラムで、クリップボードにコピーされたテキストを自動的に読み上げます。SAPI5を利用した多言語対応の音声合成を特徴とし、言語の自動検出も行います。仕事や勉強の効率化に最適なツールです。

## 姉妹アプリケーション

| アプリ | 音声合成エンジン | エンジン備考 |
|-|-|-|
| [VoivoClip](https://github.com/led-mirage/VoivoClip) | [VOICEVOX](https://voicevox.hiroshiba.jp/) | 別途インストールが必要（無料） |
| [CoeiroClip](https://github.com/led-mirage/CoeiroClip) | [COEIROINK](https://coeiroink.com/) | 別途インストールが必要（無料） |
| [AivoClip](https://github.com/led-mirage/AivoClip) | [A.I.Voice](https://aivoice.jp/) | 別途インストールが必要（有料） |
| [SAPIClip](https://github.com/led-mirage/SAPIClip) | SAPI5 | Windows標準（無料） |

## デモ

## 機能

- **自動クリップボード監視:** クリップボードに新しいテキストがコピーされると、自動で検出し読み上げを開始します。
- **多言語対応の音声合成:** SAPI5を使用し、さまざまな言語を自動で読み上げることができます。
- **音声の切り替え:** 利用可能な音声（話者）間で簡単に切り替えができ、好みの声を選択できます。
- **言語の自動検出:** 話者を`Auto`にすることで言語の自動検出も行い、対応する音声での合成を実現します。
- **話速設定:** 話速を調節できるので、自分の好みに合わせて音声の速さを変更可能です。
- **シンプルなインターフェース:** GUIは直感的に操作でき、コンパクトなため邪魔になりなりません。
- **繰り返し再生:** 最後に読み上げた内容を簡単に再生し直すことができます。

## 動作確認環境

- Windows 11 Pro 24H2
- Python 3.12.0

※アプリケーションは Windows 10でも、Homeエディションでも動作すると思いますが、その環境でのテストは行っていません。

## 実行方法

### 🛩️ 実行ファイル（EXE）を使う場合

#### 1. プロジェクト用のフォルダの作成

任意の場所にプロジェクト用のフォルダを作成してください。

#### 2. アプリのダウンロード

以下のリンクから SAPIClip.ZIP をダウンロードして、作成したフォルダに解凍してください。

https://github.com/led-mirage/SAPIClip/releases/tag/v0.1.0

#### 3. 実行

SAPIClip.exe をダブルクリックすればアプリが起動します。

### 🛩️ Pythonで実行する場合

#### 1. プロジェクト用のフォルダの作成

任意の場所にプロジェクト用のフォルダを作成してください。

#### 2. ターミナルの起動

ターミナルかコマンドプロンプトを起動して、作成したプロジェクトフォルダに移動します。

#### 3. ソースファイルのダウンロード

ZIPファイルをダウンロードして作成したフォルダに展開してください。  
または、Gitが使える方は以下のコマンドを実行してクローンしてもOKです。

```bash
git clone https://github.com/led-mirage/SAPIClip.git
```

#### 4. ライブラリのインストール

以下のコマンドを実行して必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

#### 5. 実行

以下のコマンドを実行するとアプリが起動します。  

```bash
python src\application.py
```

## 設定

### ⚙️ アプリケーション設定ファイル

`settings.json`ファイルにはこのアプリの設定情報が記載されています。

※プログラム引数で設定ファイル名を渡すことで、使用する設定ファイルを切り替えることができます。  
例）SAPIClip --setting my_settings.json

#### ✨ voice（既定値 Auto）

使用する音声名を記載します。`Auto`を指定すると、読み上げるテキストにあった音声を自動選択し読み上げます。

#### ✨ speed（既定値 1.2）

読み上げの速さの設定です。アプリのGUIで設定できます。

#### ✨ replacements（既定値 []）

読み上げるテキストの置換設定です。置換対象（pattern）を正規表現で、置換後の文字列（replacement）を通常の文字列で指定します。

例えば括弧内のテキストと、URLを除去して読み上げたい場合は、以下のように設定します。置換パターンは複数個記載でき、上から順に処理されます。

```json
    "replacements": [
        {
            "pattern": "\\(.*?\\)|（.*?）",
            "replacement": ""
        },
        {
            "pattern": "https?:\\/\\/(?:[\\w\\-\\.]+)+(?:[\\w\\.\\/\\?%&=]*)?",
            "replacement": ""
        }
    ]
```

#### ✨ preferred_voices（既定値 下記参照）

音声が`Auto`の際に優先される音声名を言語ごと指定できます。下記既定値では、テキストが英語の場合には`Microsoft Zira`が使われ、日本語の場合では`Microsoft Haruka`が使用されます。

テキストから推論された言語の音声がインストールされていない場合は、ここで指定した最初の言語の音声が使用されます。例えば、テキストがフランス語でフランス語の音声がインストールされていない場合、`Microsoft Zira`で読み上げようと試みます。

```json
    "preferred_voices": {
        "en": [
            "Microsoft Zira Desktop"
        ],
        "ja": [
            "Microsoft Haruka"
        ]
    }
```

## 音声の追加

Windows 11で音声を追加する方法を説明します。

1. Windowsの設定を開き、`時刻と言語` - `音声認識`と進みます。
2. 音声の管理の`音声を追加`ボタンを押して、インストールしたい言語を追加します。

**注意事項:** 追加ボタンを押してもすぐには反映されません。インストールの経過も表示されないので不安になりますが、しばらく待つとインストールされます。ちょっと不親切なインターフェイスです。

## 注意事項

### ⚡ ウィルス対策ソフトの誤認問題

このプログラムの実行ファイル（SAPIClip.exe）は PyInstaller というライブラリを使って作成していますが、ウィルス対策ソフトにマルウェアと誤認されることがあります。

もちろん、このアプリに悪意のあるプログラムは入っていませんが、気になる人は上記の「Pythonで実行する方法」で実行してください。

誤認問題が解決できるのが一番いいのですが、いい方法が見つかっていないので申し訳ありませんがご了承ください。

VirusTotalでの[チェック結果](https://www.virustotal.com/gui/file/9d0b58b696ce4ffe7153cd253d15fced6110a4953a365eb3971755c387df10b1)は以下の通りです（2025/01/31 v0.1.0）  
SAPIClip.exe … 72個中6個のアンチウィルスエンジンで検出

<img src="doc/virustotal_0.1.0.png" width="600">

## 使用しているライブラリ

### 🔖 requests 2.32.3

ホームページ： https://requests.readthedocs.io/en/latest/  
ライセンス：[Apache License 2.0](https://github.com/psf/requests/blob/main/LICENSE) 

### 🔖 pyperclip 1.9.0 

ホームページ： https://github.com/asweigart/pyperclip/tree/master  
ライセンス：[BSD 3-Clause "New" or "Revised" License](https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt)

### 🔖 Pillow 11.1.0

ホームページ： https://github.com/python-pillow/Pillow  
ライセンス：[MIT-CMUライセンス](https://github.com/python-pillow/Pillow/blob/main/LICENSE)

### 🔖 langdetect 1.0.9

ホームページ： https://github.com/Mimino666/langdetect  
ライセンス：[Apache License 2.0](https://github.com/Mimino666/langdetect/blob/master/LICENSE)

### 🔖 pywin32 308

ホームページ： https://github.com/mhammond/pywin32  
ライセンス：[PSF-2.0 license](https://spdx.org/licenses/PSF-2.0.html)

## ライセンス

© 2025 led-mirage

本アプリケーションは [MITライセンス](https://opensource.org/licenses/MIT) の下で公開されています。詳細については、プロジェクトに含まれる LICENSE ファイルを参照してください。

## バージョン履歴

### 0.1.0 (2025/02/01)

- ファーストリリース
